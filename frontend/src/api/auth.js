import axios from 'axios';

export async function authHandshake(initData) {
  try {
    const response = await axios.post(
      '/api/v1/auth/handshake',
      {},
      {
        headers: {
          'X-Telegram-Init-Data': initData
        }
      }
    );
    return response.data;
  } catch (error) {
    console.error('Ошибка при handshake авторизации:', error);
    throw error;
  }
}
