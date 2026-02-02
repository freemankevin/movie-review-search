import React, { useEffect, useState } from 'react';
import { getTrendingMovies } from '../api/movieApi';

const TrendingMovies = ({ onMovieSelect }) => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrending = async () => {
      try {
        const data = await getTrendingMovies(10);
        setMovies(data.data || []);
      } catch (error) {
        console.error('Failed to fetch trending movies:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrending();
  }, []);

  if (loading) {
    return (
      <div className="trending-section">
        <div className="section-header">
          <h2>
            <span className="icon">🔥</span>
            热度排行
          </h2>
        </div>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p className="loading-text">加载中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="trending-section">
      <div className="section-header">
        <h2>
          <span className="icon">🔥</span>
          热度排行 Top 10
        </h2>
      </div>
      <div className="trending-list">
        {movies.map((movie, index) => (
          <div
            key={movie.id}
            className="trending-item"
            onClick={() => onMovieSelect(movie.id)}
          >
            <div className="trending-rank">{index + 1}</div>
            <div className="trending-info">
              <div className="trending-title">{movie.title}</div>
              <div className="trending-meta">
                <span>{movie.year || '未知'}</span>
                {movie.avg_score && (
                  <div className="trending-score">
                    <span className="score">⭐ {movie.avg_score.toFixed(1)}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TrendingMovies;
