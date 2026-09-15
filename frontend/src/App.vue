<script setup>
import { computed, onMounted, ref } from 'vue';

const city = ref('Boston');
const stays = ref([]);
const users = ref([]);
const selectedStay = ref(null);
const bookingUserId = ref('U001');
const historyUserId = ref('U001');
const history = ref([]);
const searchMessage = ref('Search a city to see its offered hotel stays.');
const bookingMessage = ref('Select an offered stay to begin a simulated booking.');
const historyMessage = ref('Load a traveler to review their saved booking history.');
const searchLoading = ref(false);
const bookingLoading = ref(false);
const historyLoading = ref(false);

const hasResults = computed(() => stays.value.length > 0);
const hasHistory = computed(() => history.value.length > 0);
const money = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

async function request(url, options = {}) {
  const response = await fetch(url, options);
  const result = await response.json();
  if (!response.ok) throw new Error(result.detail || 'The request could not be completed.');
  return result;
}

async function loadUsers() {
  try {
    const result = await request('/api/users');
    users.value = result.users;
  } catch (error) {
    historyMessage.value = error.message || 'Could not load demo travelers.';
  }
}

async function search() {
  const query = city.value.trim();
  stays.value = [];
  selectedStay.value = null;
  bookingMessage.value = 'Select an offered stay to begin a simulated booking.';
  if (!query) {
    searchMessage.value = 'Enter a city to search. Try Boston, New York, Philadelphia, Washington, or State College.';
    return;
  }

  searchLoading.value = true;
  searchMessage.value = '';
  try {
    const result = await request(`/api/stays?city=${encodeURIComponent(query)}`);
    stays.value = result.stays;
    searchMessage.value = result.stays.length
      ? `${result.stays.length} offered stay${result.stays.length === 1 ? '' : 's'} found in ${result.stays[0].city}.`
      : `No offered stays match "${query}." Try another city.`;
  } catch (error) {
    searchMessage.value = error.message || 'Search could not be completed. Confirm the local backend is running.';
  } finally {
    searchLoading.value = false;
  }
}

function selectStay(stay) {
  selectedStay.value = stay;
  bookingMessage.value = `Ready to book ${stay.trip_name} for a selected demo traveler.`;
  document.querySelector('#booking-panel')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function createBooking() {
  if (!selectedStay.value) {
    bookingMessage.value = 'Select an offered stay before creating a booking.';
    return;
  }
  bookingLoading.value = true;
  try {
    const result = await request('/api/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: bookingUserId.value, trip_id: selectedStay.value.trip_id }),
    });
    historyUserId.value = bookingUserId.value;
    bookingMessage.value = `Booking ${result.booking.booking_id} is confirmed and saved in SQLite.`;
    await loadHistory();
  } catch (error) {
    bookingMessage.value = error.message || 'Booking could not be created.';
  } finally {
    bookingLoading.value = false;
  }
}

async function loadHistory() {
  historyLoading.value = true;
  try {
    const result = await request(`/api/bookings?user_id=${encodeURIComponent(historyUserId.value)}`);
    history.value = result.bookings;
    historyMessage.value = result.bookings.length
      ? `${result.bookings.length} saved booking${result.bookings.length === 1 ? '' : 's'} for the selected traveler.`
      : 'This traveler has no saved bookings yet.';
  } catch (error) {
    history.value = [];
    historyMessage.value = error.message || 'Booking history could not be loaded.';
  } finally {
    historyLoading.value = false;
  }
}

async function cancelBooking(booking) {
  try {
    const result = await request(`/api/bookings/${booking.booking_id}/cancel`, { method: 'PATCH' });
    history.value = history.value.map((item) => item.booking_id === result.booking.booking_id ? result.booking : item);
    historyMessage.value = `Booking ${result.booking.booking_id} is cancelled and remains in history.`;
  } catch (error) {
    historyMessage.value = error.message || 'Booking could not be cancelled.';
  }
}

async function deleteBooking(booking) {
  try {
    await request(`/api/bookings/${booking.booking_id}`, { method: 'DELETE' });
    history.value = history.value.filter((item) => item.booking_id !== booking.booking_id);
    historyMessage.value = `Test booking ${booking.booking_id} was deleted from SQLite.`;
  } catch (error) {
    historyMessage.value = error.message || 'Booking could not be deleted.';
  }
}

onMounted(async () => {
  await loadUsers();
  await loadHistory();
});
</script>

<template>
  <main class="page-shell">
    <header class="site-header">
      <p class="brand">expedia<span>lite</span></p>
      <p class="part-label">PART 2 - SQLITE CRUD</p>
    </header>

    <section class="hero">
      <p class="eyebrow">LOCAL CLASSROOM PROTOTYPE</p>
      <h1>Find, book, and revisit a hotel stay.</h1>
      <p class="intro">Search fictional supplied stays by city, make a simulated reservation, then manage its saved history. No live inventory, payments, or accounts are used.</p>

      <form class="search-form" @submit.prevent="search">
        <label for="city">City</label>
        <div class="search-controls">
          <input id="city" v-model="city" type="search" placeholder="e.g., Boston" autocomplete="off" />
          <button type="submit" :disabled="searchLoading">{{ searchLoading ? 'Searching...' : 'Search' }}</button>
        </div>
      </form>
      <p class="hint">Try: Boston, New York, Philadelphia, Washington, State College, or Miami.</p>
    </section>

    <section class="content-section" aria-live="polite">
      <p class="message">{{ searchMessage }}</p>
      <div v-if="hasResults" class="table-wrap">
        <table>
          <caption>Matching offered hotel stays</caption>
          <thead>
            <tr>
              <th scope="col">Trip</th>
              <th scope="col">Hotel</th>
              <th scope="col">Dates</th>
              <th scope="col">Price</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="stay in stays" :key="stay.trip_id">
              <td><strong>{{ stay.trip_name }}</strong><span class="trip-id">{{ stay.trip_id }}</span></td>
              <td>{{ stay.hotel_name }}<span class="subline">{{ stay.city }}, {{ stay.state }}</span></td>
              <td>{{ stay.check_in }} to {{ stay.check_out }}<span class="subline">{{ stay.nights }} nights</span></td>
              <td><strong>{{ money.format(stay.stay_price_usd) }}</strong><span class="subline">{{ money.format(stay.nightly_rate_usd) }} per night</span></td>
              <td><button class="secondary-button" type="button" @click="selectStay(stay)">Book this stay</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section id="booking-panel" class="content-section booking-section">
      <div class="section-heading">
        <div>
          <p class="eyebrow">SIMULATED BOOKING</p>
          <h2>Create a reservation</h2>
        </div>
        <p class="message compact">{{ bookingMessage }}</p>
      </div>
      <div class="booking-card">
        <div v-if="selectedStay" class="selected-stay">
          <strong>{{ selectedStay.trip_name }}</strong>
          <span>{{ selectedStay.hotel_name }} in {{ selectedStay.city }}, {{ selectedStay.state }}</span>
          <span>{{ selectedStay.check_in }} to {{ selectedStay.check_out }} - {{ money.format(selectedStay.stay_price_usd) }}</span>
        </div>
        <p v-else class="empty-card">Choose "Book this stay" from search results to select an offered stay.</p>
        <div>
          <label for="booking-user">Demo traveler</label>
          <select id="booking-user" v-model="bookingUserId" :disabled="!users.length">
            <option v-for="user in users" :key="user.user_id" :value="user.user_id">{{ user.display_name }} ({{ user.user_id }})</option>
          </select>
        </div>
        <button class="primary-button" type="button" :disabled="bookingLoading || !selectedStay" @click="createBooking">
          {{ bookingLoading ? 'Saving booking...' : 'Confirm simulated booking' }}
        </button>
      </div>
    </section>

    <section class="content-section history-section" aria-live="polite">
      <div class="section-heading">
        <div>
          <p class="eyebrow">SAVED HISTORY</p>
          <h2>Review booking history</h2>
        </div>
        <div class="history-picker">
          <label for="history-user">Demo traveler</label>
          <select id="history-user" v-model="historyUserId" :disabled="!users.length">
            <option v-for="user in users" :key="user.user_id" :value="user.user_id">{{ user.display_name }} ({{ user.user_id }})</option>
          </select>
          <button class="secondary-button" type="button" :disabled="historyLoading" @click="loadHistory">{{ historyLoading ? 'Loading...' : 'Load history' }}</button>
        </div>
      </div>
      <p class="message">{{ historyMessage }}</p>
      <div v-if="hasHistory" class="table-wrap">
        <table>
          <caption>Saved bookings</caption>
          <thead>
            <tr>
              <th scope="col">Booking</th>
              <th scope="col">Stay</th>
              <th scope="col">Status</th>
              <th scope="col">Booked on</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in history" :key="booking.booking_id">
              <td><strong>{{ booking.booking_id }}</strong><span class="subline">{{ booking.display_name }}</span></td>
              <td>{{ booking.trip_name }}<span class="subline">{{ booking.hotel_name }} - {{ booking.check_in }} to {{ booking.check_out }}</span></td>
              <td><span class="status" :class="booking.status">{{ booking.status }}</span></td>
              <td>{{ booking.booked_on }}</td>
              <td class="actions">
                <button v-if="booking.status !== 'cancelled'" class="text-button" type="button" @click="cancelBooking(booking)">Cancel</button>
                <button class="text-button delete" type="button" @click="deleteBooking(booking)">Delete test booking</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <footer>Supplied records are fictional classroom data. Saved changes persist locally in SQLite across browser refreshes and server restarts.</footer>
  </main>
</template>
