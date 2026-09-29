<script setup>
import { onMounted, ref } from 'vue';

const zipCode = ref('16802');
const location = ref(null);
const loading = ref(false);
const errorMessage = ref('');
const invalidInput = ref(false);
const statusMessage = ref('Enter a ZIP code or try the original 16802 demonstration.');
const healthStatus = ref('Checking backend configuration...');

async function checkHealth() {
  try {
    const response = await fetch('/api/health');
    const data = await response.json();
    if (!response.ok || !['key is configured', 'key is not configured'].includes(data.geoapify)) {
      throw new Error('Invalid health response');
    }
    healthStatus.value = `Backend health: ${data.status}. Geoapify ${data.geoapify}.`;
  } catch {
    healthStatus.value = 'Backend health unavailable. Confirm the backend is running on port 8000.';
  }
}

function clearResult() {
  location.value = null;
  errorMessage.value = '';
  invalidInput.value = false;
  statusMessage.value = 'Submit this ZIP code to look up its location.';
}

async function lookup(fixedDemo = false) {
  if (loading.value) return;
  clearResult();
  const requestedZip = fixedDemo ? '16802' : zipCode.value.trim();
  zipCode.value = requestedZip;
  if (!/^[0-9]{5}$/.test(requestedZip)) {
    invalidInput.value = true;
    statusMessage.value = '';
    errorMessage.value = 'Enter a five-digit U.S. ZIP code, such as 16802. Keep any leading zero.';
    return;
  }

  loading.value = true;
  statusMessage.value = `Looking up ZIP ${requestedZip}...`;
  const abortController = new AbortController();
  const timeout = setTimeout(() => abortController.abort(), 20000);
  try {
    const url = fixedDemo
      ? '/api/demo/zip-location'
      : `/api/zip-location?zip_code=${encodeURIComponent(requestedZip)}`;
    const response = await fetch(url, { signal: abortController.signal });
    const data = await response.json();
    if (!response.ok) {
      errorMessage.value = typeof data.detail === 'string'
        ? data.detail
        : 'The location lookup could not be completed. Please try again.';
      statusMessage.value = '';
      return;
    }
    if (data.postcode !== requestedZip || data.country_code !== 'us'
        || !Number.isFinite(data.latitude) || !Number.isFinite(data.longitude)) {
      throw new Error('Invalid location response');
    }
    location.value = data;
    statusMessage.value = `Location returned for ZIP ${data.postcode}.`;
  } catch (error) {
    statusMessage.value = '';
    errorMessage.value = error.name === 'AbortError'
      ? 'The lookup took too long. Please try again.'
      : 'Could not load the location. Confirm the local backend is running, then try again.';
  } finally {
    clearTimeout(timeout);
    loading.value = false;
  }
}

onMounted(checkHealth);
</script>

<template>
  <section id="zip-lookup" class="zip-panel" aria-labelledby="zip-heading" :aria-busy="loading">
    <p class="eyebrow">PUBLIC API ACTIVITY</p>
    <h2 id="zip-heading">ZIP lookup demonstration</h2>
    <p class="zip-intro">Find a U.S. ZIP code's location using real Geoapify data. This lookup does not search hotels or create bookings.</p>
    <p class="health-status" role="status">{{ healthStatus }}</p>
    <form class="zip-form" novalidate @submit.prevent="lookup(false)">
      <label for="zip-code">U.S. ZIP code</label>
      <div class="zip-controls">
        <input id="zip-code" v-model="zipCode" type="text" inputmode="numeric"
          autocomplete="postal-code" placeholder="e.g., 16802" aria-describedby="zip-hint"
          :aria-invalid="invalidInput" :disabled="loading" @input="clearResult" />
        <button class="primary-button" type="submit" :disabled="loading">{{ loading ? 'Looking up...' : 'Look up ZIP' }}</button>
        <button class="secondary-button" type="button" :disabled="loading" @click="lookup(true)">Look up ZIP 16802</button>
      </div>
      <p id="zip-hint" class="hint">Use five digits. Leading zeros are kept (for example, 02108).</p>
    </form>
    <p v-if="statusMessage" class="zip-message" role="status">{{ statusMessage }}</p>
    <p v-if="errorMessage" class="zip-error" role="alert">{{ errorMessage }}</p>
    <div v-if="location" class="table-wrap">
      <table class="zip-table">
        <caption>Returned location for ZIP {{ location.postcode }}</caption>
        <thead><tr>
          <th scope="col">ZIP code</th><th scope="col">Locality</th><th scope="col">Country</th>
          <th scope="col">Latitude</th><th scope="col">Longitude</th>
        </tr></thead>
        <tbody><tr>
          <td><strong>{{ location.postcode }}</strong></td>
          <td>{{ location.locality || 'Not provided' }}</td><td>{{ location.country_code.toUpperCase() }}</td>
          <td>{{ location.latitude }}</td><td>{{ location.longitude }}</td>
        </tr></tbody>
      </table>
    </div>
    <p class="zip-attribution">Powered by <a href="https://www.geoapify.com/">Geoapify</a>.
      Location data: <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>,
      <a href="https://www.geoapify.com/credits/">other credited sources</a>.
      API credentials stay in the backend.</p>
  </section>
</template>

<style scoped>
.zip-panel { padding: 32px 48px; background: #f2f6ed; border-bottom: 1px solid #ced9c5; }
.zip-panel h2 { margin: 4px 0 10px; }
.zip-intro { max-width: 760px; line-height: 1.5; }
.health-status { display: inline-block; padding: 9px 12px; border: 1px solid #b9cbb3; border-radius: 8px; font-size: 14px; background: #fff; }
.zip-form { margin-top: 10px; }
.zip-controls { display: flex; flex-wrap: wrap; align-items: stretch; gap: 10px; margin-top: 8px; }
.zip-controls input { min-width: 150px; width: 200px; min-height: 46px; border: 1px solid #9eae97; border-radius: 8px; padding: 10px 14px; font: inherit; }
.zip-controls button { min-height: 46px; }
.zip-message, .zip-error { margin: 16px 0; line-height: 1.5; }
.zip-error { padding: 12px 16px; color: #842f27; background: #fff0eb; border-left: 4px solid #ac473d; }
.zip-table { min-width: 620px; }
.zip-attribution { margin-top: 16px; font-size: 12px; line-height: 1.5; color: #435144; }
.zip-attribution a { color: #25543d; }
@media (max-width: 700px) {
  .zip-panel { padding: 24px 20px; }
  .zip-controls input { flex: 1; width: 100%; }
}
</style>
