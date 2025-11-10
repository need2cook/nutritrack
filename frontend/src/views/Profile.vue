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
      </div>
    </div>

    <!-- Статистика калорий -->
    <div class="calories-stats">
      <div class="stats-card">
        <div class="stats-header">
          <h3>Статистика за сегодня</h3>
          <button class="settings-btn" @click="showSettingsMenu = !showSettingsMenu">
            <font-awesome-icon :icon="['fas', 'cog']" class="stat-icon eaten"/>
          </button>
          
          <!-- Меню настроек -->
          <div v-if="showSettingsMenu" class="settings-menu">
            <button class="menu-item" @click="showWeightModal = true; showSettingsMenu = false">
              Изменить Вес
            </button>
            <button class="menu-item" @click="showGoalModal = true; showSettingsMenu = false">
              Изменить РСК
            </button>
          </div>
        </div>

        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon-wrapper">
              <font-awesome-icon :icon="['fas', 'utensils']" class="stat-icon eaten" />
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ caloriesEaten }} ккал</div>
              <div class="stat-label">Съедено</div>
            </div>
          </div>
          
          <div class="stat-item">
            <div class="stat-icon-wrapper">
              <font-awesome-icon :icon="['fas', 'dumbbell']" class="stat-icon burned" />
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ caloriesBurned }} ккал</div>
              <div class="stat-label">Сожжено</div>
            </div>
          </div>

          <div class="stat-item">
            <div class="stat-icon-wrapper">
              <font-awesome-icon :icon="['fas', 'flag']" class="stat-icon eaten" />
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ goal }} ккал</div>
              <div class="stat-label">РСК</div>
            </div>
          </div>
          
          <div class="stat-item">
            <div class="stat-icon-wrapper">
              <font-awesome-icon :icon="['fas', 'user']" class="stat-icon eaten" />
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ weight }} кг</div>
              <div class="stat-label">Вес</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Окно для веса -->
    <div v-if="showWeightModal" class="modal-overlay" @click="showWeightModal = false">
      <div class="modal-content" @click.stop>
        <h3>Мой Вес</h3>
        <div class="input-section">
          <input type="number" v-model.number="weightInput" class="modal-input" placeholder="Введите вес"/>
          <span class="input-unit">кг</span>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" @click="showWeightModal = false">Отмена</button>
          <button class="btn primary" @click="saveWeight">Сохранить</button>
        </div>
      </div>
    </div>

    <!-- Окно для РСК -->
    <div v-if="showGoalModal" class="modal-overlay" @click="showGoalModal = false">
      <div class="modal-content" @click.stop>
        <h3>РСК</h3>
        <div class="input-section">
          <input type="number" v-model.number="goalInput" class="modal-input" placeholder="Введите РСК"/>
          <span class="input-unit">ккал</span>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" @click="showGoalModal = false">Отмена</button>
          <button class="btn primary" @click="saveGoal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getUserProfile, updateUserWeight, updateUserGoal } from '@/api/user.js'
import { fetchDay } from '@/api/day.js';

export default {
  name: 'ProfilePage',
  data() {
    return {
      username: '',
      firstName: '',
      weight: 0,
      goal: 0,
      showWeightModal: false,
      showGoalModal: false,
      showSettingsMenu: false,
      loading: false,
      
      // Временные значения для модальных окон
      weightInput: 0,
      goalInput: 0,
      
      // Статистика калорий
      caloriesEaten: 0,
      caloriesBurned: 0,
      
      // Храним initData
      initData: null
    }
  },

  computed: {
    calorieBalance() {
      return this.caloriesEaten - this.caloriesBurned;
    }
  },

  watch: {
    showWeightModal(newVal) {
      if (newVal) {
        this.weightInput = this.weight;
      }
    },
    showGoalModal(newVal) {
      if (newVal) {
        this.goalInput = this.goal;
      }
    }
  },

  async mounted() {
  try {
    await new Promise(resolve => setTimeout(resolve, 300));

    // Получаем initData из Telegram WebApp
    const telegramInitData = window?.Telegram?.WebApp?.initData;

    // Если приложение открыто не через Telegram
    if (!telegramInitData) {
      console.warn('Telegram initData не найден — dev fallback.');
      this.initData = 'fake-dev-init-data';
      return;
    }

    // Выполняем handshake с сервером
    const authResult = await authHandshake(telegramInitData);
    console.log('Handshake успешен:', authResult);

    // Сохраняем initData
    this.initData = telegramInitData;

    // Загружаем данные пользователя
    await this.loadUserProfile();
    await this.loadTodayCalories();

  } catch (err) {
    console.error('Ошибка авторизации / handshake:', err);
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
        console.log('Данные пользователя:', user); // Для отладки
        
        this.username = user.username
        this.firstName = user.first_name
        this.weight = user.current_weight
        this.goal = user.goal

      } catch (e) {
        console.error('Ошибка загрузки профиля:', e)
      } finally {
        this.loading = false;
      }
    },

    // Загрузка данных о калориях за сегодня
    async loadTodayCalories() {
      if (!this.initData) {
        console.warn('InitData отсутствует');
        return;
      }

      try {
        const today = new Date();
        const dayData = await fetchDay(today, this.initData);
        
        // Расчет съеденных калорий
        this.caloriesEaten = dayData.product_entries?.reduce(
          (sum, entry) => sum + Math.round((entry.product.kcal_100g * entry.grams) / 100),
          0
        ) || 0;

        // Расчет сожженных калорий
        this.caloriesBurned = dayData.exersice_entries?.reduce(
          (sum, entry) => sum + Math.round((entry.exersice.kcal_30m * entry.minutes) / 30),
          0
        ) || 0;

      } catch (error) {
        console.error('Ошибка загрузки статистики калорий:', error);
        this.caloriesEaten = 0;
        this.caloriesBurned = 0;
      }
    },

    async saveWeight() {
      if (!this.initData) {
        console.warn('InitData отсутствует');
        return;
      }

      if (!this.weightInput || this.weightInput <= 0) {
        alert('Пожалуйста, введите корректный вес');
        return;
      }

      this.loading = true;
      try {
        await updateUserWeight(this.weightInput, this.initData)
        this.weight = this.weightInput;
        this.showWeightModal = false;
      } catch (e) {
        console.error('Ошибка обновления веса:', e);
        alert('Ошибка при сохранении веса');
      } finally {
        this.loading = false;
      }
    },

    async saveGoal() {
      if (!this.initData) {
        console.warn('InitData отсутствует');
        return;
      }

      if (!this.goalInput || this.goalInput <= 0) {
        alert('Пожалуйста, введите корректное значение РСК');
        return;
      }

      this.loading = true;
      try {
        await updateUserGoal(this.goalInput, this.initData)
        this.goal = this.goalInput;
        this.showGoalModal = false;
      } catch (e) {
        console.error('Ошибка обновления РСК:', e);
        alert('Ошибка при сохранении РСК');
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
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
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

.user-username {
  color: #666;
  font-size: 14px;
}

/* Статистика калорий */
.stats-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
}

.stats-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  position: relative;
}

.stats-header h3 {
  margin: 0;
  color: #2e7d32;
  font-weight: bold;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.settings-btn {
  margin-left: auto;
}

/* Кнопка настроек */
.settings-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #4caf50, #66bb6a);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
}

.settings-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

/* Меню настроек */
.settings-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  padding: 8px;
  z-index: 100;
  min-width: 180px;
  margin-top: 8px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 12px;
  border: none;
  background: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 14px;
  color: #333;
  text-align: left;
}

.menu-item:hover {
  background: #f5f5f5;
}

.menu-item .svg-inline--fa {
  width: 16px;
  color: #4caf50;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  border-radius: 16px;
  padding: 16px;
  gap: 12px;
}

.stat-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  background: white;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon {
  font-size: 20px;
}

.stat-icon.eaten {
  color: #4caf50;
}

.stat-icon.burned {
  color: #f44336;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

/* Модальное окно */
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
  border-radius: 20px;
  width: 90%;
  max-width: 320px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  margin: 0 0 20px 0;
  text-align: center;
  color: #333;
}

.input-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
}

.modal-input {
  flex: 1;
  border: none;
  background: none;
  font-weight: 600;
  color: #333;
  outline: none;
}

.input-unit {
  color: #666;
  font-weight: 600;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  gap: 12px;
}

.btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn.secondary {
  background: #f1f3f4;
  color: #666;
}

.btn.secondary:hover {
  background: #e8eaed;
}

.btn.primary {
  background: linear-gradient(135deg, #4caf50, #66bb6a);
  color: white;
}

.btn.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Адаптивность */
@media (max-width: 480px) {
  .profile-page {
    padding: 12px;
  }
  
  .profile-header {
    padding: 20px 16px;
    gap: 12px;
  }
  
  .user-avatar {
    width: 60px;
    height: 60px;
  }
  
  .avatar-test {
    font-size: 24px;
  }
  
  .user-name {
    font-size: 18px;
  }
  
  .stats-card {
    padding: 20px;
  }
  
  .stats-grid {
    gap: 12px;
  }
  
  .stat-item {
    padding: 12px;
    gap: 10px;
  }
  
  .stat-icon-wrapper {
    width: 40px;
    height: 40px;
  }
  
  .stat-icon {
    font-size: 18px;
  }
  
  .stat-value {
    font-size: 14px;
  }
  
  .settings-btn {
    width: 36px;
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    height: 36px;
    font-size: 14px;
  }
  
  .settings-menu {
    min-width: 160px;
  }
}

@media (max-width: 360px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-card {
    padding: 16px;
  }
  
  .stat-item {
    gap: 8px;
  }
}
</style>