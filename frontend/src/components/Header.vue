<template>
  <header class="app-header">
    <!-- Логотип -->
    <div class="logo">
      <font-awesome-icon :icon="['fas', 'apple-alt']" class="logo-icon" />
      <span class="app-name">NutriTrack</span>
    </div>

  </header>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      
    }
  },
};
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  color: #2e7d32;
  font-family: 'Arial', sans-serif;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
  color: #4caf50;
}

.app-name {
  font-size: 20px;
  font-weight: bold;
  color: #2e7d32;
}
</style>
