<script setup>
import { computed, nextTick, ref } from 'vue';
import HotelMap from './HotelMap.vue';

const zipCode = ref('16802');
const center = ref(null);
const hotels = ref([]);
const radiusMeters = ref(5000);
const resultLimit = ref(50);
const selectedId = ref(null);
const listElement = ref(null);
const state = ref('idle');
const message = ref('Enter a five-digit U.S. ZIP code to search for nearby hotels.');

const selectedHotel = computed(() => hotels.value.find((hotel) => hotel.place_id === selectedId.value) || null);

function clearResults() {
  center.value = null;
  hotels.value = [];
  selectedId.value = null;
  state.value = 'idle';
  message.value = 'Submit this ZIP code to search for nearby hotels.';
}

async function selectHotel(placeId, fromMap = false) {
  selectedId.value = placeId;
  if (fromMap) {
    await nextTick();
    const list = listElement.value;
    const button = Array.from(list?.querySelectorAll('.hotel-choice') || [])
      .find((item) => item.dataset.placeId === placeId);
    if (list && button) {
      list.scrollTop += button.getBoundingClientRect().top - list.getBoundingClientRect().top - list.clientHeight / 3;
    }
  }
}

async function searchHotels() {
  if (state.value === 'loading') return;
  clearResults();
  const requestedZip = zipCode.value.trim();
  zipCode.value = requestedZip;
  if (!/^[0-9]{5}$/.test(requestedZip)) {
    state.value = 'invalid';
    message.value = 'Enter exactly five digits for a U.S. ZIP code. Leading zeros are kept.';
    return;
  }

  state.value = 'loading';
  message.value = `Resolving ZIP ${requestedZip} and loading nearby hotels...`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 25000);
  try {
    const response = await fetch(`/api/hotels/nearby?zip_code=${encodeURIComponent(requestedZip)}`, { signal: controller.signal });
    const data = await response.json();
    if (!response.ok) {
      state.value = response.status === 404 ? 'unresolved' : response.status === 400 ? 'invalid' : 'failure';
      message.value = typeof data.detail === 'string' ? data.detail : 'Hotel search could not be completed. Please try again.';
      return;
    }
    if (data.center?.postcode !== requestedZip || data.center?.country_code !== 'us'
      || !Number.isFinite(data.center?.latitude) || !Number.isFinite(data.center?.longitude)
      || !Array.isArray(data.hotels) || !Number.isFinite(data.radius_meters)) {
      throw new Error('Invalid hotel response');
    }
    center.value = data.center;
    hotels.value = data.hotels;
    radiusMeters.value = data.radius_meters;
    resultLimit.value = data.result_limit;
    state.value = data.hotels.length ? 'results' : 'empty';
    message.value = data.hotels.length
      ? `${data.hotels.length} hotel place${data.hotels.length === 1 ? '' : 's'} returned near ZIP ${requestedZip}. Select a list item or map marker.`
      : `No hotel places were returned within 5 km of ZIP ${requestedZip}. Try another ZIP.`;
  } catch (error) {
    state.value = 'failure';
    message.value = error.name === 'AbortError'
      ? 'The hotel search took too long. Please try again.'
      : 'Hotel search could not be completed. Check the backend connection and try again.';
  } finally {
    clearTimeout(timeout);
  }
}
</script>

<template>
  <section id="hotel-discovery" class="discovery-panel" aria-labelledby="discovery-heading" :aria-busy="state === 'loading'">
    <div class="discovery-inner">
      <p class="eyebrow">ASSIGNMENT 2 · LIVE PLACE DISCOVERY</p>
      <h1 id="discovery-heading">Find hotels near a ZIP code.</h1>
      <p class="discovery-intro">Explore hotel places returned by Geoapify within 5 km of a resolved U.S. ZIP location. These are places, not confirmed rooms or bookable offers.</p>
      <form class="discovery-form" novalidate @submit.prevent="searchHotels">
        <label for="hotel-zip">U.S. ZIP code</label>
        <div class="discovery-controls">
          <input id="hotel-zip" v-model="zipCode" type="text" inputmode="numeric" autocomplete="postal-code"
            placeholder="e.g., 16802" aria-describedby="hotel-zip-hint" :aria-invalid="state === 'invalid'"
            :disabled="state === 'loading'" @input="clearResults" />
          <button class="primary-button" type="submit" :disabled="state === 'loading'">{{ state === 'loading' ? 'Searching...' : 'Find nearby hotels' }}</button>
        </div>
        <p id="hotel-zip-hint" class="hint">Five digits, including any leading zero. Search is centered on the returned ZIP point.</p>
      </form>

      <p class="discovery-status" :class="{ problem: ['invalid', 'unresolved', 'failure'].includes(state) }"
        :role="['invalid', 'unresolved', 'failure'].includes(state) ? 'alert' : 'status'">{{ message }}</p>

      <div v-if="center" class="discovery-results">
        <div class="result-context">
          <h2>Near ZIP {{ center.postcode }}<span v-if="center.locality"> · {{ center.locality }}</span></h2>
          <p>Search center {{ center.latitude }}, {{ center.longitude }} · 5 km radius · at most {{ resultLimit }} returned places. Results are not exhaustive inventory.</p>
        </div>
        <div class="list-map-grid">
          <div ref="listElement" class="hotel-list" role="group" aria-label="Returned hotel places">
            <h3>Hotel places <span>{{ hotels.length }}</span></h3>
            <p v-if="!hotels.length" class="empty-results">No nearby hotel places were returned. The map shows the ZIP center and search area.</p>
            <ol v-else>
              <li v-for="(hotel, index) in hotels" :key="hotel.place_id">
                <button type="button" class="hotel-choice" :data-place-id="hotel.place_id" :class="{ selected: selectedId === hotel.place_id }"
                  :aria-pressed="selectedId === hotel.place_id" @click="selectHotel(hotel.place_id)">
                  <span class="hotel-number">{{ index + 1 }}</span>
                  <span class="hotel-copy"><strong>{{ hotel.name || 'Name not provided' }}</strong>
                    <span>{{ hotel.address || 'Address not provided' }}</span>
                    <small>{{ hotel.latitude }}, {{ hotel.longitude }}</small></span>
                </button>
              </li>
            </ol>
          </div>
          <HotelMap :center="center" :hotels="hotels" :selected-id="selectedId"
            :radius-meters="radiusMeters" @select="(placeId) => selectHotel(placeId, true)" />
        </div>
        <p v-if="selectedHotel" class="selected-summary" role="status">Selected in list and map: {{ selectedHotel.name || 'Name not provided' }}.</p>
      </div>
      <p class="discovery-attribution">Hotel place data: <a href="https://www.geoapify.com/">Geoapify</a> and credited sources. Map imagery: OpenStreetMap contributors (attribution also appears on the map). No prices, ratings, availability, or bookings are inferred.</p>
    </div>
  </section>
</template>

<style scoped>
.discovery-panel { padding: 52px 24px 56px; background: radial-gradient(circle at 95% 0%, #d7e8d8, transparent 36%), #edf2e9; border-bottom: 1px solid #cfdbce; }
.discovery-inner { width: min(1200px, 100%); margin: auto; }
.discovery-panel h1 { max-width: 760px; margin: 12px 0 16px; color: #173a31; font-family: Fraunces, Georgia, serif; font-size: clamp(2.4rem, 5vw, 4.6rem); font-weight: 500; letter-spacing: -.045em; line-height: 1; }
.discovery-intro { max-width: 820px; margin: 0 0 28px; color: #405b51; font-size: 1.05rem; line-height: 1.55; }
.discovery-form { max-width: 610px; }
.discovery-controls { display: flex; gap: 9px; }
.discovery-controls input { flex: 1; min-height: 48px; border-radius: 6px; background: #fff; }
.discovery-controls button { min-height: 48px; border-radius: 6px; }
.discovery-status { display: inline-block; margin: 22px 0 0; padding: 11px 15px; color: #24513f; background: #e0eee0; line-height: 1.45; }
.discovery-status.problem { color: #842f27; background: #fff0eb; border-left: 4px solid #ac473d; }
.discovery-results { margin-top: 34px; }
.result-context { margin-bottom: 20px; }
.result-context h2 { margin: 0 0 5px; font-size: 1.7rem; }
.result-context p { margin: 0; color: #5c7468; font-size: .9rem; line-height: 1.5; }
.list-map-grid { display: grid; grid-template-columns: minmax(300px, 440px) minmax(0, 1fr); gap: 18px; align-items: stretch; }
.hotel-list { min-height: 0; max-height: 540px; overflow: auto; border: 1px solid #c8d6c9; background: #fffdf9; }
.hotel-list h3 { position: sticky; top: 0; z-index: 1; display: flex; justify-content: space-between; margin: 0; padding: 19px; color: #173a31; background: #fffdf9; border-bottom: 1px solid #dfe5dc; font-family: Fraunces, Georgia, serif; font-size: 1.4rem; font-weight: 500; }
.hotel-list h3 span { font-family: 'DM Mono', monospace; font-size: .8rem; }
.hotel-list ol { margin: 0; padding: 0; list-style: none; }
.hotel-list li + li { border-top: 1px solid #e1e6dd; }
.hotel-choice { display: flex; width: 100%; gap: 12px; padding: 16px; border: 0; background: transparent; color: #315146; text-align: left; font-weight: 400; }
.hotel-choice.selected { background: #e4efe5; box-shadow: inset 4px 0 #a34a3a; }
.hotel-choice:focus-visible { outline: 3px solid #db674b; outline-offset: -4px; }
.hotel-number { display: grid; flex: 0 0 28px; width: 28px; height: 28px; place-items: center; border-radius: 50%; background: #1d5848; color: white; font: 700 .8rem 'DM Mono', monospace; }
.hotel-choice.selected .hotel-number { background: #a34a3a; }
.hotel-copy { display: grid; gap: 5px; min-width: 0; line-height: 1.35; }
.hotel-copy strong { color: #173a31; font-size: .95rem; }
.hotel-copy span, .hotel-copy small { color: #60756b; font-size: .78rem; overflow-wrap: anywhere; }
.empty-results { padding: 17px; color: #526b60; line-height: 1.5; }
.selected-summary { margin: 18px 0 0; padding: 10px 14px; background: #e4efe5; color: #24513f; }
.discovery-attribution { max-width: 950px; margin: 28px 0 0; color: #536d61; font-size: .78rem; line-height: 1.5; }
.discovery-attribution a { color: #24513f; }
@media (max-width: 900px) { .list-map-grid { grid-template-columns: 1fr; } .hotel-list { max-height: 390px; } }
@media (max-width: 600px) { .discovery-panel { padding: 36px 16px; } .discovery-controls { flex-direction: column; } .discovery-controls button { padding: 12px; } }
</style>
