<script setup>
import { computed, ref } from 'vue';

const question = ref('For ZIP 16802, which saved hotel has rooms from 2026-10-10 to 2026-10-12, and what is the total simulated cost?');
const result = ref(null);
const state = ref('idle');
const message = ref('Ask about hotels saved locally and their simulated October 10-14, 2026 nightly data.');
const canSubmit = computed(() => question.value.trim().length > 0 && question.value.length <= 500 && state.value !== 'loading');
const dollars = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });

async function ask() {
  const text = question.value.trim();
  result.value = null;
  if (!text || text.length > 500) {
    state.value = 'invalid';
    message.value = 'Enter a question of 1 to 500 characters.';
    return;
  }
  state.value = 'loading';
  message.value = 'Checking the saved hotel database and preparing an answer...';
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 70000);
  try {
    const response = await fetch('/api/hotels/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: text }),
      signal: controller.signal,
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(typeof data.detail === 'string' ? data.detail : 'The hotel question could not be answered.');
    }
    if (typeof data.answer !== 'string' || !Array.isArray(data.retrieved_records)
      || !Array.isArray(data.checked_stays) || typeof data.proposed_sql !== 'string') {
      throw new Error('The backend returned an incomplete hotel answer.');
    }
    result.value = data;
    state.value = data.status === 'no_match' ? 'no_match' : data.status === 'insufficient_data' ? 'insufficient_data' : 'answered';
    message.value = data.status === 'no_match'
      ? 'No matching saved records were found.'
      : data.status === 'insufficient_data'
        ? 'The local records cannot support a complete available stay for those dates.'
        : 'Answer based on saved local records.';
  } catch (error) {
    state.value = 'failure';
    message.value = error.name === 'AbortError'
      ? 'The request took too long. Please try again.'
      : error.message || 'Could not reach the hotel advisor. Check the backend connection.';
  } finally {
    clearTimeout(timeout);
  }
}
</script>

<template>
  <section id="hotel-advisor" class="advisor-panel" aria-labelledby="advisor-heading" :aria-busy="state === 'loading'">
    <div class="advisor-inner">
      <p class="advisor-eyebrow">ASSIGNMENT 2 · LOCAL HOTEL ADVISOR</p>
      <h2 id="advisor-heading">Ask about saved hotels.</h2>
      <p class="advisor-intro">Compare the hotels you saved locally using their fictional classroom nightly rates and room counts. This does not search all nearby hotels or make a booking.</p>
      <form @submit.prevent="ask">
        <label for="hotel-question">Your question</label>
        <textarea id="hotel-question" v-model="question" rows="3" maxlength="500" :disabled="state === 'loading'"
          aria-describedby="question-hint" placeholder="Ask about a saved ZIP, dates, or simulated nightly rates"></textarea>
        <p id="question-hint" class="advisor-hint">For a stay, include check-in and checkout as YYYY-MM-DD. Checkout is not a billed night.</p>
        <button type="submit" :disabled="!canSubmit">{{ state === 'loading' ? 'Checking records...' : 'Ask saved hotels' }}</button>
      </form>

      <p class="advisor-message" :class="{ problem: ['invalid', 'failure'].includes(state) }"
        :role="['invalid', 'failure'].includes(state) ? 'alert' : 'status'">{{ message }}</p>

      <div v-if="result" class="advisor-answer" aria-live="polite">
        <h3>Answer</h3>
        <p>{{ result.answer }}</p>
        <p class="advisor-disclaimer">Only saved local hotels were considered. Rates and room counts are simulated, not live offers or bookable inventory.</p>

        <div v-if="result.checked_stays.length" class="advisor-table-wrap">
          <table>
            <caption>Backend-checked stay coverage (checkout excluded)</caption>
            <thead><tr><th scope="col">Saved hotel</th><th scope="col">ZIP</th><th scope="col">Nights found</th><th scope="col">Total</th><th scope="col">Lowest rooms</th><th scope="col">Whole stay</th></tr></thead>
            <tbody>
              <tr v-for="stay in result.checked_stays" :key="`${stay.hotel_id}-${stay.zip_code}`">
                <td>{{ stay.name || 'Name not provided' }}</td>
                <td>{{ stay.zip_code }}</td>
                <td>{{ stay.nights_found }} / {{ stay.nights_required }}</td>
                <td>{{ stay.total_cost_cents === null ? 'Not enough data' : dollars.format(stay.total_cost_cents / 100) }}</td>
                <td>{{ stay.minimum_rooms_available === null ? 'Not enough data' : stay.minimum_rooms_available }}</td>
                <td>{{ stay.complete_and_available ? 'Simulated rooms shown' : 'Not confirmed by local data' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <details class="advisor-evidence">
          <summary>View proposed SQL and retrieved local records</summary>
          <p>The backend accepted a read-only, bounded query. These are local simulated records, not an external hotel offer.</p>
          <pre>{{ result.proposed_sql }}</pre>
          <p>{{ result.retrieved_records.length }} retrieved row{{ result.retrieved_records.length === 1 ? '' : 's' }}{{ result.truncated ? ' (capped at 40)' : '' }}.</p>
          <div v-if="result.retrieved_records.length" class="advisor-table-wrap">
            <table>
              <caption>Retrieved saved hotel nights</caption>
              <thead><tr><th scope="col">Hotel</th><th scope="col">ZIP</th><th scope="col">Date</th><th scope="col">Rate</th><th scope="col">Rooms</th></tr></thead>
              <tbody>
                <tr v-for="(record, index) in result.retrieved_records" :key="`${record.hotel_id}-${record.zip_code}-${record.stay_date}-${index}`">
                  <td>{{ record.name || 'Name not provided' }}</td>
                  <td>{{ record.zip_code }}</td>
                  <td>{{ record.stay_date }}</td>
                  <td>{{ dollars.format(record.nightly_rate_cents / 100) }}</td>
                  <td>{{ record.rooms_available }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </details>
      </div>
    </div>
  </section>
</template>

<style scoped>
.advisor-panel { background: #f5f2e9; color: #1c4239; padding: 4rem 1.5rem; }
.advisor-inner { max-width: 1200px; margin: 0 auto; }
.advisor-eyebrow { color: #b55542; font-size: .78rem; font-weight: 700; letter-spacing: .12em; }
h2 { font-family: Georgia, serif; font-size: clamp(2.2rem, 5vw, 4rem); margin: .6rem 0 1rem; }
.advisor-intro { max-width: 760px; line-height: 1.55; font-size: 1.08rem; }
form { display: grid; gap: .7rem; max-width: 850px; margin-top: 2rem; }
label { font-weight: 700; }
textarea { box-sizing: border-box; width: 100%; padding: 1rem; border: 1px solid #a6beb3; border-radius: .35rem; font: inherit; resize: vertical; background: #fff; color: #173d34; }
textarea:focus-visible, button:focus-visible, summary:focus-visible { outline: 3px solid #bc5c42; outline-offset: 2px; }
button { justify-self: start; border: 0; border-radius: .3rem; padding: .9rem 1.2rem; background: #205b4b; color: #fff; font: inherit; font-weight: 700; cursor: pointer; }
button:disabled { opacity: .6; cursor: not-allowed; }
.advisor-hint, .advisor-disclaimer { color: #526e62; font-size: .9rem; margin: 0; }
.advisor-message { margin: 1.5rem 0; padding: .85rem 1rem; background: #e2eee5; max-width: 850px; }
.advisor-message.problem { background: #f9e7e1; color: #8f392c; }
.advisor-answer { background: #fff; border: 1px solid #d6e0d8; padding: 1.5rem; max-width: 1100px; }
h3 { margin-top: 0; font-family: Georgia, serif; font-size: 1.5rem; }
.advisor-answer > p { line-height: 1.55; }
.advisor-table-wrap { max-width: 100%; overflow-x: auto; margin: 1.2rem 0; }
table { border-collapse: collapse; width: 100%; min-width: 620px; font-size: .9rem; }
caption { text-align: left; font-weight: 700; padding: .7rem 0; }
th, td { border-bottom: 1px solid #d9e2dc; padding: .6rem; text-align: left; vertical-align: top; }
th { background: #edf3ef; }
.advisor-evidence { border-top: 1px solid #d9e2dc; margin-top: 1.5rem; padding-top: 1rem; }
summary { cursor: pointer; font-weight: 700; }
pre { overflow-x: auto; white-space: pre-wrap; overflow-wrap: anywhere; padding: 1rem; background: #f0f4f1; font-size: .85rem; }
</style>
