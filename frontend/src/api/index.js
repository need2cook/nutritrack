export async function apiFetch(url, options = {}) {
  const defaultHeaders = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Telegram-Init-Data': options.initData || ''
  };

  const response = await fetch(url, {
    ...options,
    headers: { ...defaultHeaders, ...options.headers }
  });

  if (!response.ok) {
    throw new Error(`Ошибка ${response.status}`);
  }

  return response.json();
}
