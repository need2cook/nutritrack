import { apiFetch } from './index.js';

export async function authHandshake(initData) {
  return apiFetch('/api/v1/auth/handshake', {
    method: 'POST',
    headers: {
      'X-Telegram-Init-Data': initData
    }
  });
}
