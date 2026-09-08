import { useMemo, useState } from 'react';

const supportedDestination = 'Asheville';
const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
const day = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

function formatDate(value) {
  return day.format(new Date(`${value}T00:00:00`));
}

function todayInputValue() {
  const today = new Date();
  today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
  return today.toISOString().slice(0, 10);
}

function nightsBetween(checkIn, checkOut) {
  if (!checkIn || !checkOut) return 0;
  return Math.round((new Date(`${checkOut}T00:00:00`) - new Date(`${checkIn}T00:00:00`)) / 86_400_000);
}

async function request(url, options) {
  const response = await fetch(url, options);
  const body = await response.json();
  if (!response.ok) throw body;
  return body;
}

function StayArt({ tone, compact = false }) {
  return (
    <div className={`stay-art ${tone} ${compact ? 'compact' : ''}`} aria-hidden="true">
      <span className="sun" />
      <span className="mountain mountain-back" />
      <span className="mountain mountain-front" />
      <span className="cabin" />
    </div>
  );
}

function SearchForm({ search, setSearch, onSubmit, isLoading, error }) {
  const minDate = todayInputValue();

  return (
    <form className="search-form" onSubmit={onSubmit}>
      <label>
        <span>Where to?</span>
        <input
          aria-label="Destination"
          value={search.destination}
          onChange={(event) => setSearch({ ...search, destination: event.target.value })}
          placeholder="Try Asheville"
        />
      </label>
      <label>
        <span>Check-in</span>
        <input
          aria-label="Check-in date"
          type="date"
          min={minDate}
          value={search.checkIn}
          onChange={(event) => setSearch({ ...search, checkIn: event.target.value })}
        />
      </label>
      <label>
        <span>Check-out</span>
        <input
          aria-label="Check-out date"
          type="date"
          min={search.checkIn || minDate}
          value={search.checkOut}
          onChange={(event) => setSearch({ ...search, checkOut: event.target.value })}
        />
      </label>
      <button className="primary-button search-button" type="submit" disabled={isLoading}>
        {isLoading ? 'Searching…' : 'Search stays'}
      </button>
      {error && <p className="form-message" role="alert">{error}</p>}
    </form>
  );
}

function PropertyCard({ property, onSelect }) {
  return (
    <article className="property-card">
      <StayArt tone={property.imageTone} />
      <div className="property-content">
        <div className="property-main">
          <p className="eyebrow">{property.city}</p>
          <h3>{property.name}</h3>
          <p className="rating"><span>★</span> {property.rating} <span className="review-count">({property.reviewCount} reviews)</span></p>
          <p className="description">{property.description}</p>
          <ul className="amenities">
            {property.amenities.map((amenity) => <li key={amenity}>{amenity}</li>)}
          </ul>
          <p className={property.refundable ? 'policy refundable' : 'policy'}>
            {property.refundable ? 'Free cancellation' : 'Nonrefundable rate'}
          </p>
        </div>
        <div className="property-price">
          <p><strong>{money.format(property.nightlyRate)}</strong> <span>per night</span></p>
          <button className="secondary-button" onClick={() => onSelect(property)}>Select stay</button>
        </div>
      </div>
    </article>
  );
}

function BookingSummary({ property, search }) {
  const nights = nightsBetween(search.checkIn, search.checkOut);
  const total = nights * property.nightlyRate;

  return (
    <aside className="booking-summary">
      <StayArt tone={property.imageTone} compact />
      <div>
        <p className="eyebrow">Your selected stay</p>
        <h2>{property.name}</h2>
        <p>{property.city}</p>
        <p className="dates">{formatDate(search.checkIn)} – {formatDate(search.checkOut)} · {nights} night{nights === 1 ? '' : 's'}</p>
      </div>
      <div className="total-line"><span>{money.format(property.nightlyRate)} × {nights}</span><strong>{money.format(total)}</strong></div>
      <p className="small-print">Taxes and fees are not included in this classroom prototype.</p>
    </aside>
  );
}

function HistoryCard({ booking }) {
  return (
    <article className="history-card">
      <div>
        <p className="eyebrow">{booking.status}</p>
        <h3>{booking.propertyName}</h3>
        <p>{booking.city}</p>
      </div>
      <div className="history-detail">
        <p><strong>{formatDate(booking.checkIn)} – {formatDate(booking.checkOut)}</strong></p>
        <p>{booking.nights} night{booking.nights === 1 ? '' : 's'} · {booking.travelerName}</p>
        <p className="confirmation">Confirmation {booking.confirmationCode}</p>
      </div>
      <strong className="history-total">{money.format(booking.total)}</strong>
    </article>
  );
}

export default function App() {
  const [view, setView] = useState('search');
  const [search, setSearch] = useState({ destination: supportedDestination, checkIn: '', checkOut: '' });
  const [properties, setProperties] = useState([]);
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [searchError, setSearchError] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [traveler, setTraveler] = useState({ travelerName: '', travelerEmail: '' });
  const [bookingError, setBookingError] = useState('');
  const [bookingErrors, setBookingErrors] = useState({});
  const [isBooking, setIsBooking] = useState(false);
  const [confirmedBooking, setConfirmedBooking] = useState(null);
  const [bookings, setBookings] = useState([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [historyError, setHistoryError] = useState('');

  const pageTitle = useMemo(() => ({
    search: 'Find a stay',
    results: `Stays in ${supportedDestination}`,
    booking: 'Complete your booking',
    confirmation: 'Your stay is confirmed',
    history: 'Your bookings',
  }[view]), [view]);

  async function searchProperties(event) {
    event.preventDefault();
    setSearchError('');
    if (!search.destination.trim() || !search.checkIn || !search.checkOut) {
      setSearchError('Enter a destination, check-in date, and check-out date to search.');
      return;
    }
    if (nightsBetween(search.checkIn, search.checkOut) <= 0) {
      setSearchError('Check-out must be after check-in.');
      return;
    }

    setIsSearching(true);
    try {
      const result = await request(`/api/properties?destination=${encodeURIComponent(search.destination)}`);
      setProperties(result.properties);
      setView('results');
    } catch {
      setSearchError('We could not load stays. Check that the local server is running and try again.');
    } finally {
      setIsSearching(false);
    }
  }

  function selectProperty(property) {
    setSelectedProperty(property);
    setBookingError('');
    setBookingErrors({});
    setView('booking');
  }

  async function submitBooking(event) {
    event.preventDefault();
    setBookingError('');
    setBookingErrors({});
    setIsBooking(true);
    try {
      const result = await request('/api/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...search, ...traveler, propertyId: selectedProperty.id }),
      });
      setConfirmedBooking(result.booking);
      setView('confirmation');
    } catch (error) {
      setBookingError(error.message || 'We could not confirm this booking. Please try again.');
      setBookingErrors(error.errors || {});
    } finally {
      setIsBooking(false);
    }
  }

  async function openHistory() {
    setView('history');
    setHistoryError('');
    setIsLoadingHistory(true);
    try {
      const result = await request('/api/bookings');
      setBookings(result.bookings);
    } catch {
      setHistoryError('We could not load your booking history. Check that the local server is running and try again.');
    } finally {
      setIsLoadingHistory(false);
    }
  }

  function startOver() {
    setSelectedProperty(null);
    setTraveler({ travelerName: '', travelerEmail: '' });
    setConfirmedBooking(null);
    setProperties([]);
    setSearchError('');
    setView('search');
  }

  return (
    <div className="app-shell">
      <header className="site-header">
        <button className="brand" onClick={startOver} aria-label="Stayfinder home"><span>◆</span> stayfinder</button>
        <nav><button className={view === 'history' ? 'nav-active' : ''} onClick={openHistory}>My bookings</button></nav>
      </header>

      <main>
        <section className={`hero ${view === 'search' ? '' : 'compact-hero'}`}>
          <p className="kicker">LOCAL TRAVEL, SIMPLY PLANNED</p>
          <h1>{pageTitle}</h1>
          {view === 'search' && <p className="hero-copy">Discover a quieter kind of escape. Search a small collection of thoughtfully selected Asheville stays.</p>}
          {view === 'search' && <SearchForm search={search} setSearch={setSearch} onSubmit={searchProperties} isLoading={isSearching} error={searchError} />}
        </section>

        <section className="content-wrap">
          {view === 'results' && (
            <>
              <div className="section-heading"><div><p className="eyebrow">{search.checkIn && `${formatDate(search.checkIn)} – ${formatDate(search.checkOut)}`}</p><h2>Available stays</h2></div><button className="text-button" onClick={() => setView('search')}>Edit search</button></div>
              {properties.length > 0 ? <div className="property-list">{properties.map((property) => <PropertyCard key={property.id} property={property} onSelect={selectProperty} />)}</div> : <div className="empty-state"><span>⌂</span><h2>No stays found</h2><p>Stayfinder currently has synthetic stays in Asheville only. Try searching for Asheville, then choose dates.</p><button className="primary-button" onClick={() => setView('search')}>Change search</button></div>}
            </>
          )}

          {view === 'booking' && selectedProperty && (
            <div className="booking-layout">
              <div className="booking-form-wrap">
                <button className="back-button" onClick={() => setView('results')}>← Back to stays</button>
                <h2>Who’s staying?</h2>
                <p className="muted">We’ll use these synthetic details only to make your local booking record.</p>
                <form className="traveler-form" onSubmit={submitBooking} noValidate>
                  <label>Primary traveler name<input value={traveler.travelerName} onChange={(event) => setTraveler({ ...traveler, travelerName: event.target.value })} aria-invalid={Boolean(bookingErrors.travelerName)} />{bookingErrors.travelerName && <small>{bookingErrors.travelerName}</small>}</label>
                  <label>Email for confirmation<input type="email" value={traveler.travelerEmail} onChange={(event) => setTraveler({ ...traveler, travelerEmail: event.target.value })} aria-invalid={Boolean(bookingErrors.travelerEmail)} />{bookingErrors.travelerEmail && <small>{bookingErrors.travelerEmail}</small>}</label>
                  {bookingError && <p className="form-message" role="alert">{bookingError}</p>}
                  <button className="primary-button" type="submit" disabled={isBooking}>{isBooking ? 'Confirming…' : 'Confirm booking'}</button>
                  <p className="small-print">This is a simulated booking. No payment is collected and no real reservation is created.</p>
                </form>
              </div>
              <BookingSummary property={selectedProperty} search={search} />
            </div>
          )}

          {view === 'confirmation' && confirmedBooking && (
            <div className="confirmation-card">
              <div className="confirmation-mark">✓</div>
              <p className="eyebrow">SIMULATED BOOKING CONFIRMED</p>
              <h2>You’re going to {confirmedBooking.propertyName}.</h2>
              <p>Your confirmation code is <strong>{confirmedBooking.confirmationCode}</strong>.</p>
              <div className="confirmation-details"><span>{formatDate(confirmedBooking.checkIn)} – {formatDate(confirmedBooking.checkOut)}</span><span>{confirmedBooking.nights} night{confirmedBooking.nights === 1 ? '' : 's'}</span><strong>{money.format(confirmedBooking.total)}</strong></div>
              <div className="button-row"><button className="primary-button" onClick={openHistory}>View my bookings</button><button className="secondary-button" onClick={startOver}>Find another stay</button></div>
            </div>
          )}

          {view === 'history' && (
            <>
              <div className="section-heading"><div><p className="eyebrow">SAVED LOCALLY</p><h2>Booking history</h2></div><button className="text-button" onClick={startOver}>Find a stay</button></div>
              {isLoadingHistory && <p className="loading">Loading your bookings…</p>}
              {historyError && <p className="form-message" role="alert">{historyError}</p>}
              {!isLoadingHistory && !historyError && bookings.length === 0 && <div className="empty-state"><span>◌</span><h2>No bookings yet</h2><p>Once you confirm a stay, it will appear here—even after you refresh the browser.</p><button className="primary-button" onClick={startOver}>Find a stay</button></div>}
              {!isLoadingHistory && bookings.length > 0 && <div className="history-list">{bookings.map((booking) => <HistoryCard key={booking.id} booking={booking} />)}</div>}
            </>
          )}
        </section>
      </main>

      <footer><span>Stayfinder</span> · A local, synthetic classroom prototype inspired by observable travel-search patterns.</footer>
    </div>
  );
}

