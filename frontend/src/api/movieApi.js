import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';
const API_TIMEOUT = parseInt(process.env.REACT_APP_API_TIMEOUT) || 10000;

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
});

// 搜索电影
export const searchMovies = async (params) => {
  try {
    const response = await api.get('/api/search', { params });
    return response.data;
  } catch (error) {
    console.error('Search failed:', error);
    throw error;
  }
};

// 获取电影详情
export const getMovieDetail = async (movieId) => {
  try {
    const response = await api.get(`/api/movie/${movieId}`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch movie detail:', error);
    throw error;
  }
};

// 获取热度排行
export const getTrendingMovies = async (limit = 10) => {
  try {
    const response = await api.get('/api/trending', { params: { limit } });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch trending movies:', error);
    throw error;
  }
};

// 获取可用数据源
export const getSources = async () => {
  try {
    const response = await api.get('/api/sources');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch sources:', error);
    throw error;
  }
};

// 获取统计信息
export const getStats = async () => {
  try {
    const response = await api.get('/api/stats');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch stats:', error);
    throw error;
  }
};
