<template>
  <div class="week-calendar">
    <!-- Месяц и год -->
    <div class="month-year">
      <font-awesome-icon :icon="['fas', 'calendar']" class="calendar-icon" />
      <span class="month">{{ currentMonth }}</span>
      <span class="year">{{ currentYear }}</span>
    </div>

    <!-- Дни недели -->
    <div class="week-days-header">
      <button class="nav-btn" @click="prevWeek">
        <font-awesome-icon :icon="['fas', 'chevron-left']" />
      </button>
      
      <div class="week-days">
        <div 
          v-for="day in weekDays" 
          :key="day.date.toString()"
          class="day-circle"
          :class="{
            'active': isActiveDay(day),
            'today': isToday(day),
            'selected': isSelectedDay(day)
          }"
          @click="selectDay(day)"
        >
          <span class="day-name">{{ day.shortName }}</span>
          <span class="day-number">{{ day.number }}</span>
        </div>
      </div>
      
      <button class="nav-btn" @click="nextWeek">
        <font-awesome-icon :icon="['fas', 'chevron-right']" />
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WeekCalendar',
  props: {
    selectedDate: {
      type: Date,
      default: () => new Date()
    }
  },
  emits: ['dateSelected'],
  data() {
    return {
      currentWeekStart: this.getStartOfWeek(new Date()),
      days: ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'],
      dayNames: ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],
      months: [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
      ]
    }
  },
  computed: {
    weekDays() {
      const days = [];
      const startDate = new Date(this.currentWeekStart);
      
      for (let i = 0; i < 7; i++) {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        
        days.push({
          date: date,
          name: this.dayNames[date.getDay()],
          shortName: this.days[i],
          number: date.getDate(),
          month: date.getMonth(),
          year: date.getFullYear()
        });
      }
      
      return days;
    },
    
    currentMonth() {
      const middleDay = this.weekDays[3];
      return this.months[middleDay?.month || new Date().getMonth()];
    },
    
    currentYear() {
      const middleDay = this.weekDays[3];
      return middleDay?.year || new Date().getFullYear();
    }
  },
  methods: {
    getStartOfWeek(date) {
      const targetDate = new Date(date);
      // Находим понедельник (1 - понедельник, 0 - воскресенье)
      const day = targetDate.getDay();
      const diff = targetDate.getDate() - (day === 0 ? 6 : day - 1);
      return new Date(targetDate.setDate(diff));
    },
    
    isActiveDay(day) {
      const today = new Date();
      return day.date.toDateString() === today.toDateString();
    },
    
    isToday(day) {
      const today = new Date();
      return day.date.toDateString() === today.toDateString();
    },
    
    isSelectedDay(day) {
      if (!this.selectedDate) return false;
      return day.date.toDateString() === this.selectedDate.toDateString();
    },
    
    selectDay(day) {
      this.$emit('dateSelected', day.date);
    },
    
    prevWeek() {
      const newDate = new Date(this.currentWeekStart);
      newDate.setDate(newDate.getDate() - 7);
      this.currentWeekStart = newDate;
    },
    
    nextWeek() {
      const newDate = new Date(this.currentWeekStart);
      newDate.setDate(newDate.getDate() + 7);
      this.currentWeekStart = newDate;
    },
    
    setWeekForDate(date) {
      this.currentWeekStart = this.getStartOfWeek(date);
    }
  },
  watch: {
    selectedDate: {
      handler(newDate) {
        if (newDate) {
          this.setWeekForDate(newDate);
        }
      },
      immediate: true
    }
  }
}
</script>

<style scoped>
.week-calendar {
  margin-bottom: 20px;
}

.month-year {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
  gap: 10px;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(102, 187, 106, 0.15) 100%);
  padding: 12px;
  border-radius: 12px;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.calendar-icon {
  font-size: 16px;
  color: #4caf50;
  opacity: 0.8;
}

.month {
  font-size: 16px;
  font-weight: bold;
  color: #2e7d32;
}

.year {
  font-size: 16px;
  color: #2e7d32;
  opacity: 0.8;
}

/* Дни недели */
.week-days-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.nav-btn {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: linear-gradient(135deg, #43a047 0%, #57bb5c 100%);
  transform: scale(1.05);
}

.week-days {
  display: flex;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  flex: 1;
}

.day-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  width: 100%;
  aspect-ratio: 1;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1.8px solid transparent;
  padding: 4px;
  color: #4caf50;
}

.day-circle:hover {
  transform: scale(1.05);
}

.day-circle.active {
  color: white;
}

.day-circle.today {
  color: #4caf50;
  border-color: #4caf50;
}

.day-circle.selected {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  color: white;
}

.day-name {
  font-size: 10px;
  font-weight: 600;
  margin-bottom: 2px;
}

.day-number {
  font-size: 14px;
  font-weight: bold;
}

/* Адаптивность */
@media (max-width: 480px) {
  .month-year {
    padding: 10px;
    gap: 8px;
  }
  
  .calendar-icon {
    font-size: 14px;
  }
  
  .month, .year {
    font-size: 14px;
  }
  
  .week-days {
    gap: 4px;
  }
  
  .day-circle {
    min-height: 35px;
    padding: 3px;
  }
  
  .day-name {
    font-size: 9px;
  }
  
  .day-number {
    font-size: 11px;
  }
  
  .nav-btn {
    width: 28px;
    height: 28px;
    font-size: 10px;
  }
}

@media (max-width: 360px) {
  .week-days {
    gap: 2px;
  }
  
  .day-circle {
    min-height: 32px;
  }
  
  .day-name {
    font-size: 8px;
  }
  
  .day-number {
    font-size: 10px;
  }
  
  .nav-btn {
    width: 25px;
    height: 25px;
  }
}

</style>