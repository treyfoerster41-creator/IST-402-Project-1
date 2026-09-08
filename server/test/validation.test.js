import test from 'node:test';
import assert from 'node:assert/strict';
import { validateBooking } from '../src/validation.js';

const validBooking = {
  propertyId: 'blue-ridge-lodge',
  checkIn: '2026-10-18',
  checkOut: '2026-10-21',
  travelerName: 'Jordan Lee',
  travelerEmail: 'jordan@example.test',
};

test('accepts a complete booking and calculates nights', () => {
  const result = validateBooking(validBooking);
  assert.deepEqual(result.value, { ...validBooking, nights: 3 });
});

test('rejects checkout on or before check-in', () => {
  const result = validateBooking({ ...validBooking, checkOut: '2026-10-18' });
  assert.equal(result.errors.checkOut, 'Check-out must be after check-in.');
});

test('rejects a missing traveler and malformed email', () => {
  const result = validateBooking({ ...validBooking, travelerName: ' ', travelerEmail: 'not-an-email' });
  assert.equal(result.errors.travelerName, 'Enter the primary traveler’s name.');
  assert.equal(result.errors.travelerEmail, 'Enter a valid email address.');
});
