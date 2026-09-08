import test, { after, before } from 'node:test';
import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { createApp } from '../src/server.js';

const bookingsFile = fileURLToPath(new URL('../data/bookings.json', import.meta.url));
let server;
let baseUrl;

before(async () => {
  await writeFile(bookingsFile, '[]\n');
  const app = createApp();
  await new Promise((resolve, reject) => {
    server = app.listen(0, (error) => {
      if (error) reject(error);
      else resolve();
    });
  });
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(async () => {
  await new Promise((resolve) => server.close(resolve));
  await writeFile(bookingsFile, '[]\n');
});

test('returns synthetic Asheville properties and no properties for another destination', async () => {
  const matching = await fetch(`${baseUrl}/api/properties?destination=Asheville`);
  const matchingBody = await matching.json();
  assert.equal(matching.status, 200);
  assert.equal(matchingBody.properties.length, 3);

  const missing = await fetch(`${baseUrl}/api/properties?destination=Boston`);
  assert.deepEqual((await missing.json()).properties, []);
});

test('persists a confirmed booking and returns it in history', async () => {
  const create = await fetch(`${baseUrl}/api/bookings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      propertyId: 'blue-ridge-lodge',
      checkIn: '2026-10-18',
      checkOut: '2026-10-21',
      travelerName: 'Jordan Lee',
      travelerEmail: 'jordan@example.test',
    }),
  });
  const created = await create.json();
  assert.equal(create.status, 201);
  assert.equal(created.booking.nights, 3);
  assert.equal(created.booking.total, 435);
  assert.match(created.booking.confirmationCode, /^STY-[A-F0-9]{6}$/);

  const history = await fetch(`${baseUrl}/api/bookings`);
  const historyBody = await history.json();
  assert.equal(historyBody.bookings.length, 1);
  assert.equal(historyBody.bookings[0].id, created.booking.id);
});
