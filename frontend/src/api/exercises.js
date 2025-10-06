import { apiFetch } from './index.js';


// Получить список упражнений из каталога
export async function fetchExercises(query = '', initData) {
  const data = await apiFetch('/api/v1/exercises_catalog/', { initData });

  if (!query) return data;
  return data.filter(exercise =>
    exercise.title.toLowerCase().includes(query.toLowerCase())
  );
}