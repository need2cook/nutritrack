<template>
  <div id="app">
    <main class="main-content">
      <router-view />
    </main>
    <BottomNav />
  </div>
</template>

<script>
import BottomNav from './components/BottomNav.vue'

export default {
  name: 'App',
  components: {
    BottomNav
  }
}
</script>

<style>
* {
  margin: 0;
  box-sizing: border-box;
}
</style>