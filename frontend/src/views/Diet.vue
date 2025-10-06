
<template>
  <div class="diet-page">
    <Hat @dateSelected="loadDayByDate" />

    <!-- Календарь -->
    <WeekCalendar 
      :selected-date="selectedDate"
      @date-selected="onDateSelected"
    />

    <!-- Общая сводка калорий -->
    <section class="summary-card">
      <!-- Макросы -->
      <div class="macros-summary">
        <div class="macro-item">
          <span class="value">{{ totalProteins }}г</span>
          <span class="label">Белки</span>
        </div>
        <div class="macro-item">
          <span class="value">{{ totalFats }}г</span>
          <span class="label">Жиры</span>
        </div>
        <div class="macro-item">
          <span class="value">{{ totalCarbs }}г</span>
          <span class="label">Углеводы</span>
        </div>
      </div>

      <!-- Калории и вода -->
      <div class="daily-summary">
        <div class="summary-block">
          <span class="summary-label">Норма калорий</span>
          <span class="summary-value">{{сalorieIntake}} ккал</span>
        </div>
        <div class="summary-block">
          <span class="summary-label">Съедено</span>
          <span class="summary-value">{{ totalCalories }} ккал</span>
        </div>
        <div class="summary-block">
          <span class="summary-label">Норма воды</span>
          <span class="summary-value">{{ waterGoal }} мл</span>
        </div>
        <div class="summary-block">
          <span class="summary-label">Сожжено</span>
          <span class="summary-value">{{ totalBurnedCalories }} ккал</span>
        </div>
      </div>
    </section>

    <!-- Контейнеры -->
    <div class="containers">
      <!-- Приём пищи -->
      <div class="container">
        <div class="container-header" @click="toggleContainer('meals')">
          <div class="container-title">
            <div class="title-row">
              <font-awesome-icon :icon="['fas', 'utensils']" />
              <h3>Приём пищи</h3>
            </div>
            
            <div class="container-summary">
              <span class="summary-item">Б: {{ totalProteins }} г.</span>
              <span class="summary-item">Ж: {{ totalFats }} г.</span>
              <span class="summary-item">У: {{ totalCarbs }} г.</span>
              <span class="summary-item">{{ totalCalories }} ккал</span>
            </div>
          </div>
          <div class="header-actions">
            <button class="toggle-btn" :class="{ rotated: !expandedContainers.meals }">
              <font-awesome-icon :icon="['fas', 'chevron-down']" />
            </button>
            <div class="btn-add">
              <button class="add-btn" @click="showAddMealPanel = true">
                <font-awesome-icon :icon="['fas', 'plus']" />
              </button>
            </div>
          </div>
        </div>
        
        <!-- Меню при нажатии на Приём пищи -->
        <transition name="slide">
          <div class="container-content" v-show="expandedContainers.meals">
            <div v-if="dayData && dayData.product_entries.length > 0">
              <div 
                v-for="entry in dayData.product_entries" 
                :key="entry.id"
                class="meal-item"
              >
                <div class="meal-header">
                  <span class="meal-name">{{ entry.product.title }}</span>
                  <span class="meal-weight">{{ entry.grams }} г.</span>
                </div>
                <div class="meal-nutrition">
                  <span class="nutrition-info">
                    Б: {{ ((entry.product.proteins_100g * entry.grams) / 100).toFixed(1) }} г. 
                    Ж: {{ ((entry.product.fats_100g * entry.grams) / 100).toFixed(1) }} г. 
                    У: {{ ((entry.product.carbs_100g * entry.grams) / 100).toFixed(1) }} г. 
                    <span class="meal-calories">
                      {{ Math.round((entry.product.kcal_100g * entry.grams) / 100) }} ккал
                    </span>
                  </span>
                </div>
              </div>
            </div>
            
            <div v-else class="empty-state">
              <p>Нет продуктов на этот день</p>
            </div>
          </div>
        </transition>
      </div>

      <!-- Упражнения -->
      <div class="container">
        <div class="container-header" @click="toggleContainer('exercises')">
          <div class="container-title">
            <div class="title-row">
              <font-awesome-icon :icon="['fas', 'dumbbell']" />
              <h3>Упражнения</h3>
            </div>
            
            <div class="container-summary" v-if="dayData.exercise_entries && dayData.exercise_entries.length > 0">
              <span class="summary-item">-{{ totalBurnedCalories }} ккал</span>
              <span class="summary-item">{{ totalExerciseTime }} мин</span>
            </div>
          </div>
          <div class="header-actions">
            <button class="toggle-btn" :class="{ rotated: !expandedContainers.exercises }">
              <font-awesome-icon :icon="['fas', 'chevron-down']" />
            </button>
            <div class="btn-add">
              <button class="add-btn" @click.stop="showAddExercisePanel = true">
                <font-awesome-icon :icon="['fas', 'plus']" />
              </button>
            </div>
          </div>
        </div>
        
        <!-- Меню при нажатии на Упражнения -->
        <transition name="slide">
          <div class="container-content" v-show="expandedContainers.exercises">
            <div v-if="dayData.exercise_entries && dayData.exercise_entries.length > 0">
              <div 
                v-for="entry in dayData.exercise_entries" 
                :key="entry.id"
                class="exercise-item"
              >
                <div class="exercise-info">
                  <span class="exercise-name">{{ entry.exercise.title }}</span>
                  <span class="exercise-duration">{{ entry.minutes }} мин</span>
                </div>
                <div class="exercise-details">
                  <span class="exercise-calories">-{{ entry.calories_burned }} ккал</span>
                </div>
              </div>
            </div>
            
            <div v-else class="empty-state">
              <p>Нет упражнений на этот день</p>
            </div>
          </div>
        </transition>
      </div>

      <!-- Стаканы воды -->
      <div class="container">
        <div class="container-header">
          <div class="container-title">
            <div class="title-row">
              <font-awesome-icon :icon="['fas', 'glass-water']" />
              <h3>Вода</h3>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Панель добавления ПРОДУКТОВ -->
    <div v-if="showAddMealPanel" class="add-panel">
      <div class="add-panel-content">
        <h4>Добавить продукт</h4>
        <input
          v-model="mealSearchQuery"
          type="text"
          placeholder="Поиск продукта..."
          @input="fetchProducts"
          class="search-input"
        />

        <!-- Список продуктов -->
        <div v-if="products.length" class="product-list">
          <div
            v-for="p in products"
            :key="p.id"
            class="product-card"
            @click="selectProduct(p)"
            :class="{ selected: selectedProduct?.id === p.id }"
          >
            <div class="title">{{ p.title }}</div>
            <div class="macros">
              Б: {{ p.proteins_100g }}г | Ж: {{ p.fats_100g }}г | У: {{ p.carbs_100g }}г | {{ p.kcal_100g }} ккал
            </div>
          </div>
        </div>

        <!-- Ввод граммов -->
        <div v-if="selectedProduct" class="grams-panel">
          <label>Количество (грамм):</label>
          <input type="number" v-model.number="grams" class="grams-input" />
        </div>

        <!-- Кнопки -->
        <div class="panel-actions">
          <button @click="addProduct" class="save-btn">Добавить</button>
          <button @click="closeMealPanel" class="cancel-btn">Отмена</button>
        </div>
      </div>
    </div>

    <!-- Панель добавления УПРАЖНЕНИЙ -->
    <div v-if="showAddExercisePanel" class="add-panel">
      <div class="add-panel-content">
        <h4>Добавить упражнение</h4>
        <input
          v-model="exerciseSearchQuery"
          type="text"
          placeholder="Поиск упражнения..."
          @input="fetchExercises"
          class="search-input"
        />

        <!-- Список упражнений -->
        <div v-if="exercisesCatalog.length" class="product-list">
          <div
            v-for="exercise in exercisesCatalog"
            :key="exercise.id"
            class="product-card"
            @click="selectExercise(exercise)"
            :class="{ selected: selectedExercise?.id === exercise.id }"
          >
            <div class="title">{{ exercise.title }}</div>
            <div class="macros">
              {{ exercise.calories_per_minute }} ккал/мин
            </div>
          </div>
        </div>

        <!-- Ввод минут -->
        <div v-if="selectedExercise" class="grams-panel">
          <label>Продолжительность (минут):</label>
          <input type="number" v-model.number="exerciseMinutes" class="grams-input" />
          <div class="calories-preview" v-if="exerciseMinutes > 0">
            Сожжено: {{ Math.round(selectedExercise.calories_per_minute * exerciseMinutes) }} ккал
          </div>
        </div>

        <!-- Кнопки -->
        <div class="panel-actions">
          <button @click="addExercise" class="save-btn">Добавить</button>
          <button @click="closeExercisePanel" class="cancel-btn">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WeekCalendar from '@/components/WeekCalendar.vue';
import Hat from "@/components/Hat.vue";

import { fetchProducts } from '@/api/products.js';
import { fetchExercises } from '@/api/exercises.js';
import { fetchDay, addProductToDay, addExerciseToDay } from '@/api/day.js';
import { authHandshake } from '@/api/auth.js';

export default {
  name: 'DietPage',
  components: { 
    Hat,
    WeekCalendar
  },
  data() {
    return {
      selectedDate: new Date(),
      selectedDateString: new Date().toISOString().split('T')[0],
      waterGoal: 2000,
      сalorieIntake: 2400,
      expandedContainers: {
        meals: true,
        exercises: true,
      },
      loading: false,
      
      // Для добавления продуктов
      dayData: { 
        product_entries: [],
        exercise_entries: [] 
      },
      
      // Продукты
      mealSearchQuery: "",
      products: [],
      selectedProduct: null,
      grams: 100,
      showAddMealPanel: false,
      
      // Упражнения
      exerciseSearchQuery: "",
      exercisesCatalog: [],
      selectedExercise: null,
      exerciseMinutes: 30,
      showAddExercisePanel: false,
      
      // Храним initData
      initData: null
    }
  },
  computed: {
    formattedDate() {
      return this.selectedDate.toISOString().split("T")[0];
    },
    
    totalProteins() {
      return this.dayData.product_entries?.reduce(
        (sum, entry) => sum + (entry.product.proteins_100g * entry.grams / 100),
        0
      ).toFixed(1) || '0.0';
    },
    totalFats() {
      return this.dayData.product_entries?.reduce(
        (sum, entry) => sum + (entry.product.fats_100g * entry.grams / 100),
        0
      ).toFixed(1) || '0.0';
    },
    totalCarbs() {
      return this.dayData.product_entries?.reduce(
        (sum, entry) => sum + (entry.product.carbs_100g * entry.grams / 100),
        0
      ).toFixed(1) || '0.0';
    },
    totalCalories() {
      return this.dayData.product_entries?.reduce(
        (sum, entry) => sum + Math.round((entry.product.kcal_100g * entry.grams) / 100),
        0
      ) || 0;
    },
    totalBurnedCalories() {
      return this.dayData.exercise_entries?.reduce(
        (sum, entry) => sum + entry.calories_burned,
        0
      ) || 0;
    },
    totalExerciseTime() {
      return this.dayData.exercise_entries?.reduce(
        (sum, entry) => sum + entry.minutes,
        0
      ) || 0;
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

      console.log('Получен initData от Telegram');

      // Выполняем handshake авторизацию
      const authResult = await authHandshake(telegramInitData);
      console.log('Handshake успешен:', authResult);

      // Сохраняем initData
      this.initData = telegramInitData;

      // Загружаем данные дня
      await this.fetchDayData();
    } catch (err) {
      console.error('Ошибка авторизации:', err);
    }
  },

  methods: {
    // Загрузка рациона за день
    async fetchDayData() {
      if (!this.initData) {
        console.warn('InitData отсутствует');
        return;
      }

      this.loading = true;
      try {
        this.dayData = await fetchDay(this.selectedDate, this.initData);
      } catch (err) {
        console.error('Ошибка загрузки рациона:', err);
        this.dayData = { 
          date: this.formattedDate, 
          product_entries: [],
          exercise_entries: []
        };
      } finally {
        this.loading = false;
      }
    },
    
    // Поиск продуктов
    async fetchProducts() {
      if (!this.mealSearchQuery) {
        this.products = [];
        return;
      }

      try {
        this.products = await fetchProducts(this.mealSearchQuery, this.initData);
      } catch (err) {
        console.error('Ошибка загрузки продуктов:', err);
        this.products = [];
      }
    },

    // Выбор продукта
    selectProduct(product) {
      this.selectedProduct = product;
    },

    // Добавление продукта в рацион
    async addProduct() {
      if (!this.selectedProduct || !this.grams) return;
      if (!this.initData) {
        console.warn('InitData отсутствует');
        return;
      }

      try {
        await addProductToDay({
          date: this.selectedDate,
          productId: this.selectedProduct.id,
          grams: this.grams,
          initData: this.initData
        });

        await this.fetchDayData();
        this.closeMealPanel();
      } catch (err) {
        console.error('Ошибка добавления продукта:', err);
      }
    },

    // Закрытие панели добавления продуктов
    closeMealPanel() {
      this.showAddMealPanel = false;
      this.mealSearchQuery = "";
      this.products = [];
      this.selectedProduct = null;
      this.grams = 100;
    },

    // Поиск упражнений
    async fetchExercises() {
      if (!this.exerciseSearchQuery) {
        this.exercisesCatalog = [];
        return;
      }

      try {
        this.exercisesCatalog = await fetchExercises(this.exerciseSearchQuery, this.initData);
      } catch (err) {
        console.error('Ошибка загрузки упражнений:', err);
        this.exercisesCatalog = [];
      }
    },

    // Выбор упражнения
    selectExercise(exercise) {
      this.selectedExercise = exercise;
    },

    // Добавление упражнения в рацион
    async addExercise() {
      if (!this.selectedExercise || !this.exerciseMinutes) return;
      if (!this.initData) {
        console.warn('InitData отсутствует');
        return;
      }

      try {
        await addExerciseToDay({
          date: this.selectedDate,
          exerciseId: this.selectedExercise.id,
          minutes: this.exerciseMinutes,
          initData: this.initData
        });

        await this.fetchDayData();
        this.closeExercisePanel();
      } catch (err) {
        console.error('Ошибка добавления упражнения:', err);
      }
    },

    // Закрытие панели добавления упражнений
    closeExercisePanel() {
      this.showAddExercisePanel = false;
      this.exerciseSearchQuery = "";
      this.exercisesCatalog = [];
      this.selectedExercise = null;
      this.exerciseMinutes = 30;
    },

    // Обработчики даты
    onDateSelected(date) {
      this.selectedDate = date;
      this.selectedDateString = date.toISOString().split('T')[0];
      this.fetchDayData();
    },

    onDatePickerChange() {
      this.selectedDate = new Date(this.selectedDateString);
      this.onDateSelected(this.selectedDate);
    },

    // Разворачивание контейнеров
    toggleContainer(container) {
      this.expandedContainers[container] = !this.expandedContainers[container];
    },

    loadDayByDate(date) {
      console.log("Выбрана дата:", date);
      this.selectedDate = date;
      this.fetchDayData();
    }
  }
};
</script>

<style scoped>
.diet-page {
  padding: 15px;
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  color: #2e7d32;
  font-family: 'Arial', sans-serif;
}

.summary-card {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  border-radius: 15px;
  padding: 15px;
  margin-bottom: 15px;
  color: white;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.macros-summary {
  display: flex;
  justify-content: space-around;
  text-align: center;
  gap: 10px;
}

.macro-item .value {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 3px;
}

.macro-item .label {
  font-size: 11px;
  opacity: 0.9;
}

.daily-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  padding-top: 10px;
}

.summary-block {
  text-align: center;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px;
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.summary-label {
  display: block;
  font-size: 11px;
  opacity: 0.9;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 15px;
  font-weight: bold;
  color: #e8f5e9;
}

/* Заголовок дня с кнопкой добавления */
.btn-add {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.btn-add .add-btn {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  color: white;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;

}

.btn-add .add-btn:hover {
  background: linear-gradient(135deg, #43a047 0%, #57bb5c 100%);
  transform: scale(1.1);
}

/* Панель добавления */
.add-panel {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.add-panel-content {
  background: white;
  padding: 20px;
  border-radius: 15px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(46, 125, 50, 0.3);
}

.add-panel-content h4 {
  margin: 0 0 15px 0;
  color: #2e7d32;
  text-align: center;
}

.search-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #c8e6c9;
  border-radius: 8px;
  font-size: 14px;
  color: #2e7d32;
  background: white;
}

.search-input:focus {
  outline: none;
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.search-input::placeholder {
  color: #81c784;
}

.product-list {
  margin-top: 12px;
  max-height: 200px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-card {
  padding: 12px;
  border: 1px solid #e8f5e9;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.product-card:hover {
  background: #f1f8e9;
  transform: translateY(-1px);
}

.product-card.selected {
  border-color: #4caf50;
  background: #e8f5e9;
  box-shadow: 0 2px 4px rgba(76, 175, 80, 0.2);
}

.title {
  font-weight: bold;
  color: #2e7d32;
  margin-bottom: 4px;
}

.macros {
  font-size: 12px;
  color: #4caf50;
}

.grams-panel {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.calories-preview {
  font-size: 12px;
  color: #f44336;
  font-weight: bold;
  margin-top: 5px;
}

.grams-panel label {
  font-size: 14px;
  color: #2e7d32;
  font-weight: 500;
}

.grams-input {
  width: 100px;
  padding: 8px;
  border: 1px solid #c8e6c9;
  border-radius: 6px;
  font-size: 14px;
  color: #2e7d32;
  background: white;
}

.grams-input:focus {
  outline: none;
  border-color: #4caf50;
}

.panel-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.save-btn {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
}

.save-btn:hover {
  background: linear-gradient(135deg, #43a047 0%, #57bb5c 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.4);
}

.cancel-btn {
  background: #e0e0e0;
  color: #666;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #d6d6d6;
  transform: translateY(-1px);
}

.containers {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.container {
  background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
  border: 1px solid #c8e6c9;
}

.container-header {
  background: #f1f8e9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #e8f5e9;
  cursor: pointer;
  transition: all 0.3s ease;
}

.container-header:hover {
  background: #e8f5e9;
}

.container-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-row h3 {
  margin: 0;
  font-size: 15px;
  color: #2e7d32;
}

.title-row svg {
  font-size: 15px;
  color: #4caf50;
}

.container-summary {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-left: 23px;
}

.summary-item {
  font-size: 11px;
  background: #e8f5e9;
  color: #2e7d32;
  padding: 3px 6px;
  border-radius: 6px;
  border: 1px solid #c8e6c9;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toggle-btn {
  background: none;
  border: none;
  color: #4caf50;
  font-size: 12px;
  cursor: pointer;
  transition: transform 0.3s ease;
  padding: 4px;
}

.toggle-btn.rotated {
  transform: rotate(-90deg);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
  overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-8px);
}

.container-content {
  overflow: hidden;
}

.meal-item {
  display: flex;
  flex-direction: column;
  padding: 10px 12px;
  border-bottom: 1px solid #e8f5e9;
  background: white;
}

.meal-item:last-child {
  border-bottom: none;
}

.meal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 5px;
}

.meal-name {
  font-weight: 500;
  font-size: 13px;
  flex: 1;
  color: #2e7d32;
}

.meal-weight {
  font-size: 12px;
  color: #4caf50;
}

.meal-nutrition {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nutrition-info {
  font-size: 11px;
  color: #66bb6a;
  display: flex;
  align-items: center;
  gap: 8px;
}

.meal-calories {
  font-weight: bold;
  color: #2e7d32;
  font-size: 12px;
}

.exercise-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-bottom: 1px solid #e8f5e9;
  background: white;
}

.exercise-item:last-child {
  border-bottom: none;
}

.exercise-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.exercise-name {
  font-weight: 500;
  font-size: 13px;
  color: #2e7d32;
}

.exercise-duration {
  font-size: 11px;
  color: #4caf50;
}

.exercise-details {
  text-align: right;
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-end;
}

.exercise-calories {
  font-size: 13px;
  font-weight: bold;
  color: #f44336;
}

.empty-state {
  text-align: center;
  padding: 25px;
  color: #4caf50;
  font-size: 13px;
  background: white;
}

@media (max-width: 480px) {
  .diet-page {
    padding: 10px;
    padding-bottom: 70px;
  }
  
  .summary-card {
    padding: 12px;
  }
  
  .macros-summary {
    gap: 8px;
  }
  
  .macro-item .value {
    font-size: 14px;
  }
  
  .macro-item .label {
    font-size: 10px;
  }
  
  .summary-value {
    font-size: 14px;
  }
  
  .container-title h3 {
    font-size: 14px;
  }
  
  .summary-item {
    font-size: 10px;
    padding: 2px 4px;
  }
  
  .container-summary {
    margin-left: 20px;
  }
  
  .meal-name {
    font-size: 12px;
  }
  
  .nutrition-info {
    font-size: 10px;
    gap: 6px;
  }
  
  .meal-calories {
    font-size: 11px;
  }
  
  .btn-add {
    margin: 15px 0 10px 0;
  }
  
  .btn-add h3 {
    font-size: 15px;
  }
  
  .add-panel {
    padding: 15px;
  }
  
  .add-panel-content {
    padding: 15px;
  }
  
  .grams-panel {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  
  .grams-input {
    width: 100%;
  }
  
  .panel-actions {
    flex-direction: column;
  }
  
  .save-btn, .cancel-btn {
    width: 100%;
  }
}


</style>