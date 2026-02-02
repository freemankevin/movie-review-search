import React, { useState, useEffect } from 'react';
import SearchBar from '../components/SearchBar';
import MovieCard from '../components/MovieCard';
import TrendingMovies from '../components/TrendingMovies';
import FilterPanel from '../components/FilterPanel';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { searchMovies, getSources, getStats } from '../api/movieApi';
import '../styles/App.css';
import '../styles/components.css';
import '../styles/animations.css';

function HomePage() {
  const [movies, setMovies] = useState([]);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);

  // 初始化 - 获取可用数据源和统计信息
  useEffect(() => {
    const init = async () => {
      try {
        const [sourcesData, statsData] = await Promise.all([
          getSources(),
          getStats(),
        ]);
        setSources(sourcesData.sources || []);
        setStats(statsData.stats);
      } catch (error) {
        console.error('Failed to initialize:', error);
      }
    };

    init();
  }, []);

  // 搜索电影
  const handleSearch = async (params) => {
    setLoading(true);
    try {
      const data = await searchMovies(params);
      setMovies(data.data || []);
    } catch (error) {
      console.error('Search error:', error);
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  // 处理电影选择
  const handleMovieSelect = (movieId) => {
    // 导航到详情页或打开模态框
    console.log('Selected movie:', movieId);
  };

  return (
    <div className="App">
      {/* 导航栏 */}
      <Header stats={stats} />

      {/* 搜索栏 */}
      <SearchBar onSearch={handleSearch} sources={sources} />

      {/* 主容器 */}
      <div className="container">
        {/* 热度排行 */}
        <TrendingMovies onMovieSelect={handleMovieSelect} />

        {/* 筛选面板 */}
        <FilterPanel onFilterChange={handleSearch} />

        {/* 搜索结果 */}
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p className="loading-text">搜索中...</p>
          </div>
        ) : movies.length > 0 ? (
          <>
            <div className="results-header">
              <div className="results-count">
                找到 <span className="count">{movies.length}</span> 个结果
              </div>
            </div>
            <div className="movies-grid">
              {movies.map((movie) => (
                <MovieCard
                  key={movie.id}
                  movie={movie}
                  onClick={() => handleMovieSelect(movie.id)}
                />
              ))}
            </div>
          </>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>未找到结果</h3>
            <p>尝试调整搜索条件或浏览热度排行</p>
          </div>
        )}
      </div>

      {/* 页脚 */}
      <Footer />
    </div>
  );
}

export default HomePage;
