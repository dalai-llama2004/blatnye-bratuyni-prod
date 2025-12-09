import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Создаем экземпляр axios с базовыми настройками
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерсептор для добавления токена к запросам
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Интерсептор для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Токен истек или невалиден
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        // Перенаправление через Next.js router произойдет в компонентах
      }
    }
    return Promise.reject(error);
  }
);

/**
 * Конвертирует ошибку API в читаемую строку.
 * Гарантирует, что всегда возвращается строка, а не объект.
 * 
 * @param err - Объект ошибки (обычно AxiosError)
 * @param defaultMessage - Сообщение по умолчанию
 * @returns Строка с описанием ошибки
 */
export function formatApiError(err: any, defaultMessage: string = 'Произошла ошибка'): string {
  // Если у ошибки есть response.data.detail
  if (err.response?.data?.detail) {
    const detail = err.response.data.detail;
    
    // Если detail - объект с полем message (например, {code, message})
    if (typeof detail === 'object' && detail !== null) {
      if (detail.message) {
        return String(detail.message);
      }
      if (detail.error) {
        return String(detail.error);
      }
      // Если объект, но без известных полей - сериализуем в JSON
      return JSON.stringify(detail);
    }
    
    // Если detail - строка, возвращаем её
    if (typeof detail === 'string') {
      return detail;
    }
  }
  
  // Если есть response.data.error
  if (err.response?.data?.error && typeof err.response.data.error === 'string') {
    return err.response.data.error;
  }
  
  // Если есть response.data как строка
  if (err.response?.data && typeof err.response.data === 'string') {
    return err.response.data;
  }
  
  // Если есть message в самой ошибке
  if (err.message && typeof err.message === 'string') {
    return err.message;
  }
  
  // Возвращаем сообщение по умолчанию
  return defaultMessage;
}

export default api;
