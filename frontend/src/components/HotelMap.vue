<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
import * as L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  center: { type: Object, required: true },
  hotels: { type: Array, required: true },
  selectedId: { type: String, default: null },
  radiusMeters: { type: Number, required: true },
});
const emit = defineEmits(['select']);
const mapElement = ref(null);
let map;
let circle;
const markers = new Map();

function markerIcon(index, selected) {
  return L.divIcon({
    className: `hotel-map-marker${selected ? ' selected' : ''}`,
    html: `<span>${index + 1}</span>`,
    iconSize: [34, 34],
    iconAnchor: [17, 17],
  });
}

function refreshMarkers() {
  if (!map) return;
  for (const marker of markers.values()) marker.remove();
  markers.clear();
  props.hotels.forEach((hotel, index) => {
    const marker = L.marker([hotel.latitude, hotel.longitude], {
      icon: markerIcon(index, hotel.place_id === props.selectedId),
      keyboard: true,
      title: hotel.name || 'Name not provided',
      alt: `Hotel ${index + 1}: ${hotel.name || 'Name not provided'}`,
    }).addTo(map);
    marker.on('click', () => emit('select', hotel.place_id));
    markers.set(hotel.place_id, marker);
  });
}

function refreshSelection() {
  if (!map) return;
  props.hotels.forEach((hotel, index) => {
    const marker = markers.get(hotel.place_id);
    if (!marker) return;
    const selected = hotel.place_id === props.selectedId;
    marker.setIcon(markerIcon(index, selected));
    marker.setZIndexOffset(selected ? 1000 : 0);
    if (selected) map.panTo([hotel.latitude, hotel.longitude]);
  });
}

onMounted(() => {
  map = L.map(mapElement.value, { scrollWheelZoom: false })
    .setView([props.center.latitude, props.center.longitude], 12);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
  }).addTo(map);
  circle = L.circle([props.center.latitude, props.center.longitude], {
    radius: props.radiusMeters,
    color: '#1d5848',
    fillColor: '#82ae92',
    fillOpacity: 0.08,
    weight: 2,
    dashArray: '7 6',
  }).addTo(map);
  L.circleMarker([props.center.latitude, props.center.longitude], {
    radius: 5,
    color: '#a34a3a',
    fillColor: '#a34a3a',
    fillOpacity: 1,
    weight: 1,
  }).addTo(map);
  map.fitBounds(circle.getBounds(), { padding: [16, 16], maxZoom: 13 });
  refreshMarkers();
  requestAnimationFrame(() => map?.invalidateSize());
});

watch(() => props.selectedId, refreshSelection);
watch(() => props.hotels, refreshMarkers);
onBeforeUnmount(() => map?.remove());
</script>

<template>
  <div class="hotel-map-wrap">
    <div ref="mapElement" class="hotel-map" role="region" aria-label="Map of returned hotels around the ZIP center"></div>
    <p class="map-key"><span class="center-dot" aria-hidden="true"></span> ZIP center <span class="radius-key" aria-hidden="true"></span> 5 km search area</p>
  </div>
</template>

<style scoped>
.hotel-map-wrap { min-width: 0; border: 1px solid #c8d6c9; background: #fff; }
.hotel-map { width: 100%; height: 490px; z-index: 0; }
.map-key { display: flex; align-items: center; gap: 7px; margin: 0; padding: 12px 14px; font-size: .78rem; color: #405b51; }
.center-dot { width: 10px; height: 10px; border-radius: 50%; background: #a34a3a; }
.radius-key { width: 16px; height: 12px; margin-left: 12px; border: 2px dashed #1d5848; border-radius: 50%; }
:global(.hotel-map-marker) { display: grid; place-items: center; border: 2px solid white; border-radius: 50%; background: #1d5848; color: white; box-shadow: 0 2px 8px #183b2f66; font: 700 14px Arial, sans-serif; }
:global(.hotel-map-marker.selected) { background: #a34a3a; transform: scale(1.12); }
:global(.hotel-map-marker span) { line-height: 1; }
@media (max-width: 760px) { .hotel-map { height: 350px; } }
</style>
