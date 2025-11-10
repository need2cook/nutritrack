import { apiFetch } from './index.js'

export async function getUserProfile(initData) {
  return apiFetch('/api/v1/users/me', {
    headers: {
      'X-Telegram-Init-Data': initData
    }
  })
}

export async function updateUserWeight(newWeight, initData) {
  return apiFetch('/api/v1/users/me/weight', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-Telegram-Init-Data': initData
    },
    body: JSON.stringify({ new_weight: newWeight })
  })
}

export async function updateUserGoal(newGoal, initData) {
  return apiFetch('/api/v1/users/me/goal', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-Telegram-Init-Data': initData
    },
    body: JSON.stringify({ new_goal: newGoal })
  })
}

