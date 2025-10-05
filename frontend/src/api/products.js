import { apiFetch } from './index.js';

export async function fetchProducts(query) {
  if (!query) return [];

  const data = await apiFetch('/api/v1/public/products');
  return data.filter(p => p.title.toLowerCase().includes(query.toLowerCase()));
}
