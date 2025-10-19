import { apiFetch } from './index.js';

// Получить конкретный день
export async function fetchDay(date, initData) {
  const targetDate = date.toISOString().split('T')[0];
  const isToday = targetDate === new Date().toISOString().split('T')[0];

  const url = isToday ? '/api/v1/diaries/day/today' : `/api/v1/diaries/day/${targetDate}`;

  return apiFetch(url, { initData });
}

// Добавить продукт в рацион
export async function addProductToDay({ date, productId, grams, initData }) {
  return apiFetch('/api/v1/diaries/day/product', {
    method: 'POST',
    body: JSON.stringify({
      target_date: date.toISOString().split('T')[0],
      product_id: productId,
      grams
    }),
    initData
  });
}

// Добавить упражнение в рацион
export async function addExerciseToDay({ date, exerciseId, minutes, initData }) {
  const res = await apiFetch('/api/v1/diaries/day/exercise', {
    method: 'POST',
    body: JSON.stringify({
      target_date: date.toISOString().split('T')[0],
      exercise_id: exerciseId,
      minutes
    }),
    initData
  });
}

// Добавление воды
export async function addWaterToDay({ date, waterMls, initData }) {
  const res = await apiFetch('/api/v1/diaries/day/water', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-Telegram-Init-Data': initData
    },
    body: JSON.stringify({
      target_date: date.toISOString().split('T')[0],
      water_mls: waterMls
    })
  });

  return res;
}