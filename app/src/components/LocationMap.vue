<template>
  <div ref="map" class="leaflet-map"></div>
</template>

<script>
import { ref, onMounted } from 'vue';
import L from 'leaflet';

export default {
  name: 'LocationMap',
  props: {
    latitude: {
      type: Number,
      required: true,
    },
    longitude: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const map = ref(null);

    onMounted(() => {
      map.value = L.map(map.value).setView([props.latitude, props.longitude], 13);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
      }).addTo(map.value);

      L.marker([props.latitude, props.longitude]).addTo(map.value);
    });

    return {
      map,
    };
  },
};
</script>

<style scoped>
.leaflet-map {
  width: 100%;
  height: 100%;
}
</style>
