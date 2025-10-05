import { apiFetch } from './index.js';

// Получить рацион на конкретный день
export async function fetchDay(date, initData) {
  const targetDate = date.toISOString().split('T')[0];
  const isToday = targetDate === new Date().toISOString().split('T')[0];

  const url = isToday ? '/api/v1/private/day/today' : `/api/v1/private/day/${targetDate}`;

  return apiFetch(url, { initData });
}

// Добавить продукт в рацион
export async function addProductToDay({ date, productId, grams, initData }) {
  return apiFetch('/api/v1/private/day', {
    method: 'POST',
    body: JSON.stringify({
      target_date: date.toISOString().split('T')[0],
      product_id: productId,
      grams
    }),
    initData
  });
}
