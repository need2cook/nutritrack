import { apiFetch } from './index.js';

export async function deleteProduct({date, productId, initData}) {
    const targetDate = date.toISOString().split('T')[0];

    return apiFetch(`/api/v1/diaries/day/${targetDate}/product/${productId}`, {
        method: 'DELETE',
        headers: {
            'X-Telegram-Init-Data': initData
        }
    });
}

export async function deleteExercise({date, exerciseId, initData}) {
    const targetDate = date.toISOString().split('T')[0];

    return apiFetch(`/api/v1/diaries/day/${targetDate}/exercise/${exerciseId}`, {
        method: 'DELETE',
        headers: {
            'X-Telegram-Init-Data': initData
        }
    });
}