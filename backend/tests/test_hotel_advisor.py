"""The model is mocked; these tests never call Gemini or edit the user's database."""

import json
import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.app.database import initialize_database
from backend.app.hotel_advisor import AdvisorError, checked_local_query, gemini_generate, stay_window
from backend.app.main import app

SELECT_TWO_NIGHTS = """SELECT h.hotel_id, h.name, h.address, z.zip_code,
 n.stay_date, n.nightly_rate_cents, n.rooms_available
 FROM saved_hotels AS h
 JOIN saved_hotel_zips AS z ON z.hotel_id = h.hotel_id
 JOIN demo_hotel_nights AS n ON n.hotel_id = h.hotel_id
 WHERE z.zip_code = '16802' AND n.stay_date >= '2026-10-10'
 AND n.stay_date < '2026-10-12' ORDER BY n.stay_date"""


class HotelAdvisorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = Path(self.temp_dir.name) / "advisor-test.db"
        env_patch = patch.dict(os.environ, {"EXPEDIA_LITE_DB_PATH": str(self.db_path)})
        env_patch.start()
        self.addCleanup(env_patch.stop)
        initialize_database()
        self.client = TestClient(app)
        self.addCleanup(self.client.close)
        fixture_path = Path(__file__).parent / "fixtures" / "assignment2_part2_saved_hotel.json"
        self.fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        saved = self.client.post("/api/hotels/saved", json=self.fixture["save_request"])
        self.assertEqual(saved.status_code, 201)
        override = self.fixture["night_override"]
        with closing(sqlite3.connect(self.db_path)) as db:
            db.execute("""UPDATE demo_hotel_nights SET nightly_rate_cents = ?, rooms_available = ?
                       WHERE hotel_id = ? AND stay_date = ?""", (
                override["nightly_rate_cents"], override["rooms_available"],
                self.fixture["save_request"]["hotel"]["place_id"], override["stay_date"],
            ))
            db.commit()

    def test_two_model_calls_wrap_read_only_retrieval_and_exact_stay_math(self):
        question = self.fixture["question"]
        with patch("backend.app.hotel_advisor.gemini_generate", side_effect=[
            '{"sql": ' + json.dumps(SELECT_TWO_NIGHTS) + '}',
            "Fixture Hotel has two simulated nights at $225 total, with at least 7 rooms shown.",
        ]) as model:
            response = self.client.post("/api/hotels/ask", json={"question": question})
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        self.assertEqual(data["status"], "answered")
        self.assertEqual(len(data["retrieved_records"]), 2)
        self.assertEqual(data["checked_stays"][0]["total_cost_cents"], self.fixture["expected"]["total_cost_cents"])
        self.assertEqual(data["checked_stays"][0]["minimum_rooms_available"], self.fixture["expected"]["minimum_rooms_available"])
        self.assertTrue(data["checked_stays"][0]["complete_and_available"])
        self.assertEqual(model.call_count, 2)
        second_prompt = model.call_args_list[1].args[0]
        self.assertIn(question, second_prompt)
        self.assertIn("12500", second_prompt)
        self.assertIn("22500", second_prompt)

    def test_model_sql_cannot_change_or_read_other_tables(self):
        before = self.db_path.read_bytes()
        rejected = [
            "DELETE FROM saved_hotels",
            "SELECT name FROM sqlite_master",
            "SELECT h.hotel_id FROM saved_hotels h; DELETE FROM saved_hotels",
            "SELECT h.hotel_id, h.name, h.address, z.zip_code, n.stay_date, 1 AS nightly_rate_cents, n.rooms_available FROM saved_hotels h JOIN saved_hotel_zips z ON z.hotel_id=h.hotel_id JOIN demo_hotel_nights n ON n.hotel_id=h.hotel_id",
        ]
        for sql in rejected:
            with self.subTest(sql=sql), self.assertRaises(AdvisorError):
                checked_local_query(sql)
        self.assertEqual(before, self.db_path.read_bytes())
        with closing(sqlite3.connect(self.db_path)) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM saved_hotels").fetchone()[0], 1)

    def test_missing_night_never_becomes_available(self):
        with closing(sqlite3.connect(self.db_path)) as db:
            db.execute("DELETE FROM demo_hotel_nights WHERE stay_date = '2026-10-11'")
            db.commit()
        with patch("backend.app.hotel_advisor.gemini_generate", side_effect=[
            '{"sql": ' + json.dumps(SELECT_TWO_NIGHTS) + '}',
            "A model answer that should be overridden.",
        ]):
            data = self.client.post("/api/hotels/ask", json={
                "question": "Can I stay from 2026-10-10 to 2026-10-12 in ZIP 16802?",
            }).json()
        self.assertEqual(data["status"], "insufficient_data")
        self.assertFalse(data["checked_stays"][0]["complete_and_available"])
        self.assertIsNone(data["checked_stays"][0]["total_cost_cents"])
        self.assertIn("missing night", data["answer"])

    def test_zero_room_night_never_becomes_available(self):
        with closing(sqlite3.connect(self.db_path)) as db:
            db.execute("""UPDATE demo_hotel_nights SET rooms_available = 0
                       WHERE hotel_id = 'fixture-hotel-1' AND stay_date = '2026-10-11'""")
            db.commit()
        with patch("backend.app.hotel_advisor.gemini_generate", side_effect=[
            '{"sql": ' + json.dumps(SELECT_TWO_NIGHTS) + '}',
            "A model answer that should be overridden.",
        ]):
            response = self.client.post("/api/hotels/ask", json={
                "question": "Can I stay from 2026-10-10 to 2026-10-12 in ZIP 16802?",
            })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "insufficient_data")
        self.assertEqual(data["checked_stays"][0]["minimum_rooms_available"], 0)
        self.assertFalse(data["checked_stays"][0]["complete_and_available"])

    def test_two_saved_hotels_can_be_compared_without_inventing_rates(self):
        second = self.client.post("/api/hotels/saved", json=self.fixture["second_save_request"])
        self.assertEqual(second.status_code, 201)
        with patch("backend.app.hotel_advisor.gemini_generate", side_effect=[
            '{"sql": ' + json.dumps(SELECT_TWO_NIGHTS) + '}',
            "Second Fixture Hotel is the lower simulated total at $200; Fixture Hotel is $225.",
        ]) as model:
            response = self.client.post("/api/hotels/ask", json={
                "question": "Compare saved ZIP 16802 hotels from 2026-10-10 to 2026-10-12.",
            })
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        self.assertEqual(len(data["retrieved_records"]), 4)
        totals = {stay["name"]: stay["total_cost_cents"] for stay in data["checked_stays"]}
        self.assertEqual(totals, {"Fixture Hotel": 22500, "Second Fixture Hotel": 20000})
        self.assertTrue(all(stay["complete_and_available"] for stay in data["checked_stays"]))
        self.assertIn("20000", model.call_args_list[1].args[0])

    def test_no_match_and_model_failure_have_distinct_states(self):
        no_match_sql = SELECT_TWO_NIGHTS.replace("'16802'", "'00000'")
        with patch("backend.app.hotel_advisor.gemini_generate", side_effect=[
            '{"sql": ' + json.dumps(no_match_sql) + '}', "ignored answer",
        ]):
            response = self.client.post("/api/hotels/ask", json={"question": "What is saved in ZIP 00000?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "no_match")
        with patch("backend.app.hotel_advisor.gemini_generate", side_effect=AdvisorError("Gemini request limit reached.", 503)):
            failed = self.client.post("/api/hotels/ask", json={"question": "What is saved?"})
        self.assertEqual(failed.status_code, 503)
        self.assertNotIn("GEMINI_API_KEY", failed.text)

    def test_question_and_date_validation(self):
        self.assertEqual(self.client.post("/api/hotels/ask", json={"question": " "}).status_code, 400)
        self.assertEqual(self.client.post("/api/hotels/ask", json={"question": "a" * 501}).status_code, 400)
        with self.assertRaises(AdvisorError):
            stay_window("From 2026-10-14 to 2026-10-10")
        with self.assertRaises(AdvisorError):
            stay_window("From 2026-02-30 to 2026-03-02")

    def test_mocked_quota_response_is_safe_and_not_a_no_match(self):
        fake_client = MagicMock()
        fake_client.__enter__.return_value.post.return_value.status_code = 429
        with patch("backend.app.hotel_advisor.gemini_api_key", return_value="synthetic-test-key"), patch(
            "backend.app.hotel_advisor.httpx.Client", return_value=fake_client
        ), self.assertRaises(AdvisorError) as caught:
            gemini_generate("A synthetic question")
        self.assertEqual(caught.exception.status_code, 503)
        self.assertIn("request limit", caught.exception.message)
        self.assertNotIn("synthetic-test-key", caught.exception.message)
        self.assertEqual(fake_client.__enter__.return_value.post.call_count, 1)


if __name__ == "__main__":
    unittest.main()
