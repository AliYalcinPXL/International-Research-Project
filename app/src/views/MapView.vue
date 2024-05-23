<template>
  <div class="container">
    <!-- Upload area -->
    <div class="upload-container mb-4">
      <!-- Image Upload -->
      <div class="upload-section">
        <h2>Upload Image</h2>
        <input type="file" class="form-control" @change="handleFileUpload">
        <button class="btn btn-primary mt-2" @click="uploadImage">Upload</button>
      </div>
    </div>

    <!-- Image container -->
    <div class="image-container mb-4">
      <!-- Uploaded Image Display Area -->
      <div class="uploaded-image-area" v-if="uploadedImage">
        <h2>Uploaded Image</h2>
        <img :src="uploadedImage" alt="Uploaded Image" class="img-fluid uploaded-image">
      </div>
    </div>

    <!-- Coordinate input area -->
    <div class="coordinate-input mb-4">
      <h2>Enter Coordinates</h2>
      <div class="form-group">
        <label for="latitude">Latitude</label>
        <input type="number" class="form-control" id="latitude" v-model="latitude">
        <select v-model="latitudeDirection" class="direction-select">
          <option value="N">N</option>
          <option value="S">S</option>
        </select>
      </div>
      <div class="form-group">
        <label for="longitude">Longitude</label>
        <input type="number" class="form-control" id="longitude" v-model="longitude">
        <select v-model="longitudeDirection" class="direction-select">
          <option value="E">E</option>
          <option value="W">W</option>
        </select>
      </div>
      <button class="btn btn-primary mt-2" @click="showOnMap">Show on Map</button>
    </div>

    <!-- Map container -->
    <div class="map-container mb-4" v-if="latitude && longitude">
      <h2>Location on Map</h2>
      <div id="map"></div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import L from 'leaflet';

export default {
  setup() {
    const uploadedImage = ref(null);
    const latitude = ref(null);
    const longitude = ref(null);
    const latitudeDirection = ref('N');
    const longitudeDirection = ref('E');
    const file = ref(null);

    const handleFileUpload = (event) => {
      file.value = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        uploadedImage.value = e.target.result;
      };
      reader.readAsDataURL(file.value);
    };

    const uploadImage = async () => {
      if (!file.value) {
        alert('Please upload an image first');
        return;
      }

      const formData = new FormData();
      formData.append('image', file.value);

      try {
        const response = await axios.post('http://127.0.0.1:7541/process-image', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        if (response.data.plant_name) {
          // Display detected plant name
          alert('Detected Plant Type: ' + response.data.plant_name);
        } else {
          alert(response.data.error || 'Error processing image');
        }
      } catch (error) {
        console.error('Error uploading the image:', error);
        alert('Error uploading the image');
      }
    };

    const showOnMap = async () => {
      if (!latitude.value || !longitude.value) {
        alert('Please enter both latitude and longitude values');
        return;
      }

      const lat = parseFloat(latitude.value) * (latitudeDirection.value === 'S' ? -1 : 1);
      const lng = parseFloat(longitude.value) * (longitudeDirection.value === 'W' ? -1 : 1);

      if (isNaN(lat) || isNaN(lng)) {
        alert('Please enter valid latitude and longitude values');
        return;
      }

      const map = L.map('map').setView([lat, lng], 7);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      }).addTo(map);

      const locationName = await getLocationName(lat, lng);

      const marker = L.marker([lat, lng]).addTo(map)
        .bindPopup(locationName ? locationName : 'Your Location')
        .openPopup();
    };

    const getLocationName = async (latitude, longitude) => {
      const url = `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`;

      try {
        const response = await axios.get(url);
        const locationName = response.data.display_name;
        return locationName;
      } catch (error) {
        console.error('Error retrieving location name:', error);
        return null;
      }
    };

    return {
      uploadedImage,
      latitude,
      longitude,
      latitudeDirection,
      longitudeDirection,
      handleFileUpload,
      uploadImage,
      showOnMap
    };
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
}

.upload-container,
.image-container,
.coordinate-input,
.map-container {
  border: 1px solid #ccc;
  padding: 10px;
}

.upload-container,
.image-container,
.coordinate-input {
  margin-bottom: 20px;
}

#map {
  width: 100%;
  height: 400px;
}

.direction-select {
  margin-top: 5px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 60px;
  vertical-align: middle;
}
</style>
