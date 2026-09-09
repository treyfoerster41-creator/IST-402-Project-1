<script setup>
import { computed, ref } from 'vue';

const city = ref('Boston');
const stays = ref([]);
const message = ref('Search a city to see its offered hotel stays.');
const messageType = ref('info');
const loading = ref(false);

const hasResults = computed(() => stays.value.length > 0);
const money = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

async function search() {
  const query = city.value.trim();
  stays.value = [];

  if (!query) {
    message.value = 'Enter a city to search. Try Boston, New York, Philadelphia, Washington, or State College.';
    messageType.value = 'error';
    return;
  }

  loading.value = true;
  message.value = '';
  try {
    const response = await fetch(`/api/stays?city=${encodeURIComponent(query)}`);
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Search could not be completed.');

    stays.value = result.stays;
    if (result.stays.length === 0) {
      message.value = `No offered stays match "${query}." Try another city.`;
      messageType.value = 'empty';
    } else {
      message.value = `${result.stays.length} offered stay${result.stays.length === 1 ? '' : 's'} found in ${result.stays[0].city}.`;
      messageType.value = 'success';
    }
  } catch (error) {
    message.value = error.message || 'Search could not be completed. Confirm the local backend is running.';
    messageType.value = 'error';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <main class="page-shell">
    <header class="site-header">
      <p class="brand">expedia<span>lite</span></p>
      <p class="part-label">PART 1 - CSV CITY SEARCH</p>
    </header>

    <section class="hero">
      <p class="eyebrow">LOCAL CLASSROOM PROTOTYPE</p>
      <h1>Find a hotel stay.</h1>
      <p class="intro">Search the supplied fictional travel records by city. Results combine hotel and trip data through <code>hotel_id</code>.</p>

      <form class="search-form" @submit.prevent="search">
        <label for="city">City</label>
        <div class="search-controls">
          <input id="city" v-model="city" type="search" placeholder="e.g., Boston" autocomplete="off" />
          <button type="submit" :disabled="loading">{{ loading ? 'Searching...' : 'Search' }}</button>
        </div>
      </form>
      <p class="hint">Try: Boston, New York, Philadelphia, Washington, State College, or Miami.</p>
    </section>

    <section class="results" aria-live="polite">
      <p v-if="message" class="message" :class="messageType">{{ message }}</p>

      <div v-if="hasResults" class="table-wrap">
        <table>
          <caption>Matching offered hotel stays</caption>
          <thead>
            <tr>
              <th scope="col">Trip</th>
              <th scope="col">Hotel</th>
              <th scope="col">City</th>
              <th scope="col">Check-in</th>
              <th scope="col">Check-out</th>
              <th scope="col">Nights</th>
              <th scope="col">Nightly rate</th>
              <th scope="col">Stay price</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="stay in stays" :key="stay.trip_id">
              <td><strong>{{ stay.trip_name }}</strong><span class="trip-id">{{ stay.trip_id }}</span></td>
              <td>{{ stay.hotel_name }}</td>
              <td>{{ stay.city }}, {{ stay.state }}</td>
              <td>{{ stay.check_in }}</td>
              <td>{{ stay.check_out }}</td>
              <td>{{ stay.nights }}</td>
              <td>{{ money.format(stay.nightly_rate_usd) }}</td>
              <td><strong>{{ money.format(stay.stay_price_usd) }}</strong></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <footer>Supplied records are fictional classroom data. No live Expedia inventory or booking is used.</footer>
  </main>
</template>
