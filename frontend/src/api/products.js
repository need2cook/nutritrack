import { apiFetch } from './index.js';

// Получить список продуктов из каталога
export async function fetchProducts(query = '', initData) {
  const data = await apiFetch('/api/v1/products_catalog/', { initData });

  if (!query) return data;
  return data.filter(p =>
    p.title.toLowerCase().includes(query.toLowerCase())
  );
}

