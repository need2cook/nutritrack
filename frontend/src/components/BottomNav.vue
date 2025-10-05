<template>
  <nav class="bottom-nav">
    <router-link 
      v-for="item in navItems" 
      :key="item.name"
      :to="item.route"
      :class="['nav-item', { active: $route.path === item.route }]"
    >
      <font-awesome-icon :icon="item.icon" />
      <span class="label">{{ item.label }}</span>
    </router-link>
  </nav>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUser, faAppleAlt } from '@fortawesome/free-solid-svg-icons'

export default {
  name: 'BottomNav',
  components: {
    FontAwesomeIcon
  },
  data() {
    return {
      navItems: [
        { name: 'profile', label: 'Я', icon: faUser, route: '/profile' },
        { name: 'diet', label: 'Рацион', icon: faAppleAlt, route: '/diet' }
      ]
    }
  }
}
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  padding: 8px 0;

}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  font-family: Arial, Helvetica, sans-serif;
  color: white;
  transition: all 0.3s ease;
  flex: 1;
}

.nav-item.active {
  color: rgb(129, 240, 129)
}

.nav-item svg {
  font-size: 20px;
  margin-bottom: 4px;
  
}

.nav-item .label {
  font-size: 12px;
}
</style>