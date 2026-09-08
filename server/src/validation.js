const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function parseLocalDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    return null;
  }

  const date = new Date(`${value}T00:00:00`);
  return Number.isNaN(date.valueOf()) ? null : date;
}

export function validateBooking(payload) {
  const errors = {};
  const travelerName = payload.travelerName?.trim();
  const travelerEmail = payload.travelerEmail?.trim();
  const checkInDate = parseLocalDate(payload.checkIn);
  const checkOutDate = parseLocalDate(payload.checkOut);

  if (!payload.propertyId) errors.propertyId = 'Choose a stay before booking.';
  if (!travelerName) errors.travelerName = 'Enter the primary traveler’s name.';
  if (!travelerEmail || !emailPattern.test(travelerEmail)) {
    errors.travelerEmail = 'Enter a valid email address.';
  }
  if (!checkInDate) errors.checkIn = 'Choose a valid check-in date.';
  if (!checkOutDate) errors.checkOut = 'Choose a valid check-out date.';

  if (checkInDate && checkOutDate && checkOutDate <= checkInDate) {
    errors.checkOut = 'Check-out must be after check-in.';
  }

  if (Object.keys(errors).length > 0) return { errors };

  const nights = Math.round((checkOutDate - checkInDate) / 86_400_000);
  return {
    value: {
      propertyId: payload.propertyId,
      checkIn: payload.checkIn,
      checkOut: payload.checkOut,
      travelerName,
      travelerEmail,
      nights,
    },
  };
}

