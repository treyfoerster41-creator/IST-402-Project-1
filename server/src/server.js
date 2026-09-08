import crypto from 'node:crypto';
import express from 'express';
import { readBookings, saveBooking } from './booking-store.js';
import { findProperty, properties, supportedDestination } from './properties.js';
import { validateBooking } from './validation.js';

export function createApp() {
  const app = express();
  app.use(express.json());

  app.get('/api/health', (_request, response) => {
    response.json({ status: 'ok' });
  });

  app.get('/api/properties', (request, response) => {
    const destination = request.query.destination?.trim();
    const matchesDestination = destination?.toLocaleLowerCase() === supportedDestination.toLocaleLowerCase();

    response.json({
      destination: supportedDestination,
      properties: matchesDestination ? properties : [],
    });
  });

  app.get('/api/bookings', async (_request, response, next) => {
    try {
      response.json({ bookings: await readBookings() });
    } catch (error) {
      next(error);
    }
  });

  app.post('/api/bookings', async (request, response, next) => {
    const validation = validateBooking(request.body ?? {});
    if (validation.errors) {
      return response.status(400).json({ message: 'Please correct the highlighted booking details.', errors: validation.errors });
    }

    const property = findProperty(validation.value.propertyId);
    if (!property) {
      return response.status(400).json({ message: 'That stay is no longer available. Choose another stay.', errors: { propertyId: 'Unknown property.' } });
    }

    try {
      const booking = {
        id: crypto.randomUUID(),
        confirmationCode: `STY-${crypto.randomUUID().slice(0, 6).toUpperCase()}`,
        propertyId: property.id,
        propertyName: property.name,
        city: property.city,
        checkIn: validation.value.checkIn,
        checkOut: validation.value.checkOut,
        travelerName: validation.value.travelerName,
        travelerEmail: validation.value.travelerEmail,
        nights: validation.value.nights,
        nightlyRate: property.nightlyRate,
        total: validation.value.nights * property.nightlyRate,
        status: 'Confirmed',
        createdAt: new Date().toISOString(),
      };

      await saveBooking(booking);
      return response.status(201).json({ booking });
    } catch (error) {
      return next(error);
    }
  });

  app.use((error, _request, response, _next) => {
    console.error(error);
    response.status(500).json({ message: 'Stayfinder could not save or load your booking. Please try again.' });
  });

  return app;
}

if (process.env.NODE_ENV !== 'test') {
  const port = process.env.PORT || 3001;
  createApp().listen(port, () => {
    console.log(`Stayfinder server listening at http://localhost:${port}`);
  });
}
