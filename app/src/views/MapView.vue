<script setup>

</script>

<template>
  <div class="container">
    <!-- Left column -->
    <div class="left-column">
      <!-- Legend -->
      <div class="legend">
        <h2>Legend</h2>
        <ul>
          <li>Legend Item 1</li>
          <li>Legend Item 2</li>
          <li>Legend Item 3</li>
        </ul>
      </div>
      <!-- Search Bar -->

      <!-- Show Images -->
      <div class="show-images">
        <img src="/src/assets/images/image1.jpg" alt="Image 1">
        <img src="/src/assets/images/image2.png" alt="Image 2">
      </div>
      <div class="search-bar">
        <input type="text" placeholder="Search..." class="search-input">
        <button class="search-button">Search</button>
      </div>
    </div>

    <!-- Right column -->
    <div class="right-column">
      <!-- Map -->
      <div class="map">
        <img src="/src/assets/images/image3.png" alt="Map" class="map-image">
      </div>
      <!-- Navigation bar -->
      <div class="navigation-bar">
        <ul>
          <li><a href="#">About</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>


<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
}

.left-column,
.right-column {
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
  padding: 20px;
}

.left-column {
  width: 30%;
}

.right-column {
  width: 68%; /* Adjust to account for padding and border */
}

.legend {
  margin-bottom: 20px;
}

.legend h2 {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.legend ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.legend li {
  margin-bottom: 5px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
}

.search-input {
  flex: 1;
  border: none;
  padding: 10px;
  border-radius: 4px;
  font-size: 1rem;
}

.search-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: #0056b3;
}

.show-images {
  display: flex;
  flex-wrap: wrap;
}

.show-images img {
  width: calc(33.333% - 20px);
  margin: 5px;
  border-radius: 4px;
}

.map {
  height: 300px;
  background-color: #e6e6e6;
  border-radius: 8px;
  overflow: hidden;
}

.map-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.navigation-bar ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.navigation-bar li {
  display: inline-block;
  margin-right: 20px;
}

.navigation-bar a {
  text-decoration: none;
  color: #333;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.navigation-bar a:hover {
  color: #007bff;
}
</style>