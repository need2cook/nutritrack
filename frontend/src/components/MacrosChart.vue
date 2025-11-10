<template>
  <div class="macros-chart">
    <div class="chart-layout">
      <!-- Левая часть - общая сводка в граммах -->
      <div class="macros-summary">
        <div class="summary-item">
          <span class="summary-label">Всего белков:</span>
          <span class="summary-value">{{ proteins }} г</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Всего жиров:</span>
          <span class="summary-value">{{ fats }} г</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Всего углеводов:</span>
          <span class="summary-value">{{ carbs }} г</span>
        </div>
      </div>

      <!-- Правая часть - график и легенда -->
      <div class="chart-section">
        <div class="chart-container">
          <svg :width="chartSize" :height="chartSize" viewBox="0 0 100 100" class="chart-svg">
            <!-- Фоновый круг -->
            <circle cx="50" cy="50" r="40" fill="none" stroke="#f0f0f0" stroke-width="20" />

            <!-- Сегменты БЖУ -->
            <circle
              v-for="(segment, index) in segments"
              :key="index"
              cx="50"
              cy="50"
              r="40"
              fill="none"
              :stroke="segment.color"
              stroke-width="20"
              :stroke-dasharray="segment.length + ' ' + (circumference - segment.length)"
              :transform="'rotate(' + segment.rotate + ' 50 50)'"
              stroke-linecap="round"
            />
          </svg>
        </div>

        <!-- Легенда под графиком -->
        <div class="chart-legend">
          <div class="legend-item">
            <div class="legend-color" style="background-color: #4caf50;"></div>
            <span class="legend-label">Белки</span>
            <span class="legend-percent">{{ proteinsPercent }}%</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" style="background-color: #ff9800;"></div>
            <span class="legend-label">Жиры</span>
            <span class="legend-percent">{{ fatsPercent }}%</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" style="background-color: #2196f3;"></div>
            <span class="legend-label">Углеводы</span>
            <span class="legend-percent">{{ carbsPercent }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MacrosChart',
  props: {
    proteins: { type: Number, default: 0 },
    fats: { type: Number, default: 0 },
    carbs: { type: Number, default: 0 },
    size: { type: Number, default: 120 }
  },
  computed: {
    chartSize() {
      return this.size * 0.8;
    },
    circumference() {
      return 2 * Math.PI * 40;
    },
    totalGrams() {
      return Math.round(this.proteins + this.fats + this.carbs);
    },
    proteinsPercent() {
      return this.totalGrams > 0 ? Math.round((this.proteins / this.totalGrams) * 100) : 0;
    },
    fatsPercent() {
      return this.totalGrams > 0 ? Math.round((this.fats / this.totalGrams) * 100) : 0;
    },
    carbsPercent() {
      return this.totalGrams > 0 ? Math.round((this.carbs / this.totalGrams) * 100) : 0;
    },
    segments() {
      const total = this.totalGrams || 1;
      const circumference = this.circumference;
      const data = [
        { value: this.proteins, color: '#4caf50' },
        { value: this.fats, color: '#ff9800' },
        { value: this.carbs, color: '#2196f3' }
      ];

      let rotate = -90;
      return data.map(seg => {
        const length = (seg.value / total) * circumference;
        const item = {
          ...seg,
          length,
          rotate
        };
        rotate += (seg.value / total) * 360;
        return item;
      });
    }
  }
};
</script>

<style scoped>
.macros-chart {
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.chart-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

/* Левая часть - сводка в граммах */
.macros-summary {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.summary-label {
  font-size: 12px;
}

.summary-value {
  font-size: 12px;
}

/* Правая часть - график */
.chart-section {
  display: flex;
  flex-direction: column;
  padding-right: 10px;
  align-items: center;
  flex-shrink: 0;
}

.chart-container {
  margin-bottom: 12px;
}

.chart-svg {
  display: block;
}

/* Легенда под графиком */
.chart-legend {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-start;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  flex-shrink: 0;
}

.legend-label {
  font-size: 12px;
  color: #2e7d32;
  font-weight: 500;
  min-width: 70px;
}

.legend-percent {
  font-size: 12px;
  font-weight: 600;
  color: #2e7d32;
}

/* Адаптивность для мобильных */
@media (max-width: 480px) {
  .macros-chart {
    padding: 12px;
  }
  
  .chart-layout {
    gap: 15px;
  }
  
  .legend-label,
  .legend-percent {
    font-size: 11px;
  }
  
  .legend-label {
    min-width: 65px;
  }
}

/* Для очень маленьких экранов */
@media (max-width: 360px) {
  .chart-layout {
    gap: 12px;
    flex-direction: column;
    align-items: stretch;
  }
  
  .macros-summary {
    gap: 8px;
  }
  
  .summary-item {
    justify-content: space-between;
  }
  
  .chart-section {
    align-self: center;
  }
  
  .chart-legend {
    flex-direction: row;
    justify-content: center;
    gap: 15px;
  }
  
  .legend-item {
    flex-direction: column;
    gap: 4px;
    align-items: center;
    min-width: 60px;
  }
  
  .legend-label {
    min-width: auto;
    text-align: center;
  }
}
</style>