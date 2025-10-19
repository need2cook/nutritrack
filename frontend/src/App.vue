<template>
  <div id="app">
    <header>
      <Header />
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer>
        <BottomNav />
    </footer>
  </div>
</template>

<script>
import BottomNav from './components/BottomNav.vue'
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    BottomNav,
    Header
  }
}
</script>

<style>
* {
  margin: 0;
  box-sizing: border-box;
}

</style>