export async function apiFetch(url, options = {}) {
  const defaultHeaders = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  };

  const response = await fetch(url, {
    ...options,
    headers: { ...defaultHeaders, ...options.headers }
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`Ошибка ${response.status}: ${message}`);
  }

  try {
    return await response.json();
  } catch {
    return null;
  }
}
