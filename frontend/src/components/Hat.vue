<template>
  <header class="app-header">
    <!-- Логотип -->
    <div class="logo">
      <font-awesome-icon :icon="['fas', 'apple-alt']" class="logo-icon" />
      <span class="app-name">NutriTrack</span>
    </div>

    <!-- Кнопка календаря -->
    <button class="calendar-icon-btn" @click="showCalendarModal = true">
      <font-awesome-icon :icon="['fas', 'calendar']" />
    </button>
  </header>

  <!-- Окно с выбором даты -->
  <div v-if="showCalendarModal" class="calendar-modal" @click="showCalendarModal = false">
    <div class="calendar-modal-content" @click.stop>
      <div class="modal-header">
        <h3>Выберите дату</h3>
        <button class="close-btn" @click="showCalendarModal = false">
          <font-awesome-icon :icon="['fas', 'times']" />
        </button>
      </div>

      <div class="date-picker">
        <input type="date" v-model="selectedDateString" @change="emitDateChange" />
      </div>

      <button class="confirm-btn" @click="showCalendarModal = false">Готово</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Hat",
  emits: ["date-selected"],

  data() {
    return {
      showCalendarModal: false,
      selectedDateString: this.formatDate(new Date()),
    };
  },

  methods: {
    formatDate(date) {
      return date.toISOString().slice(0, 10);
    },

    emitDateChange() {
      this.$emit("date-selected", this.selectedDateString);
    },
  },
};
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 0 10px;
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

.calendar-icon-btn {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.3s ease;
}

.calendar-icon-btn:hover {
  background: linear-gradient(135deg, #43a047 0%, #57bb5c 100%);
  transform: scale(1.05);
}

.calendar-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 15px;
  width: 300px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
}

.date-picker {
  margin: 20px 0;
  text-align: center;
}

.date-picker input {
  padding: 8px;
  font-size: 16px;
  width: 100%;
}

.confirm-btn {
  width: 100%;
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  border: none;
  color: white;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #43a047 0%, #57bb5c 100%);
  transform: scale(1.03);
}
</style>
