<template>
  <div class="profile-page">
    <!-- Шапка профиля -->
    <div class="profile-header">
      
      <div class="user-avatar">
        <div class="avatar-test">
          {{ firstName.charAt(0) }}
        </div>
      </div>
      <div class="user-info">
        <div class="user-name">{{ firstName }}</div>
        <div class="user-username"> {{ username }} </div>
        <div class="user-weight"> {{ weight }} кг</div>
      </div>
    </div>

    <div>
      <button class="edit-weight-btn" @click="showWeightModal = true">
        <font-awesome-icon :icon="['fas', 'pen']" />
      </button>
    </div>

    <!-- Окно для веса -->
    <div v-if="showWeightModal" class="modal-overlay" @click="showWeightModal = false">
      <div class="modal-content" @click.stop>
        <h3>Мой Вес</h3>
        <div class="weight-input-section">
          <input type="number"v-model.number="weight" class="weight-input" placeholder="Введите вес"/>
          <span class="weight-unit">кг</span>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" @click="showWeightModal = false">Отмена</button>
          <button class="btn primary" @click="saveWeight">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getUserProfile, updateUserWeight } from '@/api/user.js'
import { authHandshake } from '@/api/auth.js';

export default {
  name: 'ProfilePage',
  data() {
    return {
      username: '',
      firstName: '',
      weight: 0,
      showWeightModal: false,
      loading: false,
      
      // Храним initData
      initData: null
    }
  },

  async mounted() {
    try {
      // Получаем initData
      const telegramInitData = window?.Telegram?.WebApp?.initData || null;

      if (!telegramInitData) {
        this.initData = "fallback-init-data-for-development";
        await this.fetchDayData();
        return;
      }

      // Выполняем handshake авторизацию
      const authResult = await authHandshake(telegramInitData);
      console.log('Handshake успешен:', authResult);

      // Сохраняем initData
      this.initData = telegramInitData;

      // Загружаем данные дня
      await this.loadUserProfile();
    } catch (err) {
      console.error('Ошибка авторизации:', err);
    }
  },

  methods: {
    async loadUserProfile() {
      if (!this.initData) {
        console.warn('InitData отсутствует');
        return;
      }

      this.loading = true;
      try {
        const user = await getUserProfile(this.initData)
        this.username = user.username
        this.firstName = user.first_name
        this.weight = user.current_weight
        console.log('Профиль пользователя загружен:', user);
      } catch (e) {
        console.error('Ошибка загрузки профиля:', e)
      } finally {
        this.loading = false;
      }
    },

    async saveWeight() {
      if (!this.initData) {
        console.warn('InitData отсутствует');
        return;
      }

      this.loading = true;
      try {
        const res = await updateUserWeight(this.weight, this.initData)
        console.log('Вес обновлен:', res);
        this.showWeightModal = false;
        
      } catch (e) {
        console.error('Ошибка обновления веса:', e);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.profile-page {
  padding: 16px;
  max-width: 480px;
  margin: 0 auto;
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  min-height: 100vh;
}

/* Шапка профиля */
.profile-header {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(102, 187, 106, 0.15) 100%);
  border-radius: 20px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  gap: 16px;
  
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}

.avatar-test {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 32px;
  font-weight: bold;
}

.user-info {
  line-height: 1.2;
}

.user-name {
  font-weight: bold;
  color: #333;
  line-height: 1.2;
}

.user-weight {
  font-size: 20px;
  font-weight: 500;
  color: #4caf50;
  margin: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 24px;
  border-radius: 16px;
  width: 90%;
  max-width: 320px;
}

.modal-content h3 {
  margin: 0 0 20px 0;
  text-align: center;
  color: #333;
}

.weight-input-section {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.weight-input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

.weight-unit {
  color: #666;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  gap: 12px;
}

.btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn.secondary {
  background: #f1f3f4;
  color: #333;
}

.btn.primary {
  background: #4caf50;
  color: white;
}

.btn.primary:hover {
  background: #45a049;
}

.btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.edit-weight-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #4caf50;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-left: auto;
}

.edit-weight-btn:hover {
  background: #45a049;
}

/* Адаптивность */
@media (max-width: 480px) {
  .profile-header {
    padding: 16px;
  }
  
  .user-avatar {
    width: 70px;
    height: 70px;
  }
  
  .user-name {
    font-size: 20px;
  }
  
  .user-weight {
    font-size: 18px;
  }
}
</style>

