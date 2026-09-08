import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const bookingsFile = fileURLToPath(new URL('../data/bookings.json', import.meta.url));

export async function readBookings() {
  const source = await readFile(bookingsFile, 'utf8');
  const bookings = JSON.parse(source);
  return bookings.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
}

export async function saveBooking(booking) {
  const bookings = await readBookings();
  bookings.unshift(booking);
  await writeFile(bookingsFile, `${JSON.stringify(bookings, null, 2)}\n`, 'utf8');
  return booking;
}

