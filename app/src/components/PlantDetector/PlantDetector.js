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
    const plantType = ref('');
    const locationName = ref('');
    const coordinatesList = ref([]);
    const map = ref(null);

    const handleFileUpload = (event) => {
      file.value = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        uploadedImage.value = e.target.result;
      };
      reader.readAsDataURL(file.value);
    };

    const processImage = async () => {
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
          plantType.value = response.data.plant_name;
        } else {
          plantType.value = response.data.error || 'Error processing image';
        }
      } catch (error) {
        console.error('Error uploading the image:', error);
        plantType.value = 'Error uploading the image';
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

      if (!map.value) {
        map.value = L.map('map').setView([lat, lng], 7);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        }).addTo(map.value);
      }

      const location = await getLocationName(lat, lng);
      locationName.value = location;

      const formattedLat = lat.toFixed(4) + '° ' + (lat >= 0 ? 'N' : 'S');
      const formattedLng = lng.toFixed(4) + '° ' + (lng >= 0 ? 'E' : 'W');
      const coordinatesText = `${formattedLat}, ${formattedLng}`;

      L.marker([lat, lng]).addTo(map.value)
        .bindPopup(locationName.value ? locationName.value : 'Your Location' + '<br>' + coordinatesText)
        .openPopup();

      coordinatesList.value.push({
        latitude: lat,
        longitude: lng,
        location_name: locationName.value
      });
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

    const saveCoordinates = async () => {
      if (coordinatesList.value.length === 0) {
        alert('No coordinates to save');
        return;
      }
    
      try {
        const response = await axios.post('http://127.0.0.1:7541/save-coordinates', {
          coordinates: coordinatesList.value
        });
    
        if (response.data.filePath) {
          alert('Coordinates and location name saved successfully');
        } else {
          alert('Error saving coordinates and location name');
        }
      } catch (error) {
        console.error('Error saving coordinates:', error);
        alert('Error saving coordinates and location name');
      }
    };


    return {
      uploadedImage,
      latitude,
      longitude,
      latitudeDirection,
      longitudeDirection,
      plantType,
      locationName,
      coordinatesList,
      handleFileUpload,
      processImage,
      showOnMap,
      saveCoordinates,
    };
  }
};
