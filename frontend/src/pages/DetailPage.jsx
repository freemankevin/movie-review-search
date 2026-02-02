import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getMovieDetail } from '../api/movieApi';
import '../styles/App.css';
import '../styles/components.css';
import '../styles/animations.css';

function DetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMovieDetail = async () => {
      try {
        const data = await getMovieDetail(id);
        setMovie(data.data);
      } catch (error) {
        console.error('Failed to fetch movie detail:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMovieDetail();
  }, [id]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p className="loading-text">加载中...</p>
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="empty-state">
        <div className="empty-icon">😕</div>
        <h3>未找到该电影</h3>
        <p>可能已被删除或链接错误</p>
      </div>
    );
  }

  return (
    <div className="App">
      <div className="detail-header">
        <div className="detail-container">
          <div className="detail-poster">
            {movie.poster_url ? (
              <img src={movie.poster_url} alt={movie.title} />
            ) : (
              <div style={{
                width: '100%',
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%)',
                color: 'white',
                fontSize: '4rem'
              }}>🎬</div>
            )}
          </div>
          <div className="detail-info">
            <h1>{movie.title}</h1>
            <div className="detail-meta">
              <div className="meta-item">
                <span className="label">年份</span>
                <span className="value">{movie.year || '未知'}</span>
              </div>
              <div className="meta-item">
                <span className="label">综合评分</span>
                <span className="value">{movie.avg_score?.toFixed(1) || 'N/A'}</span>
              </div>
              <div className="meta-item">
                <span className="label">热度</span>
                <span className="value">{movie.popularity || 0}</span>
              </div>
            </div>
            <p className="description">{movie.description || '暂无描述'}</p>
          </div>
        </div>
      </div>

      <div className="container">
        <div className="detail-reviews">
          {movie.reviews && movie.reviews.map((review, index) => (
            <div key={index} className="review-source">
              <div className="source-name">
                <span className="source-badge">{review.source.charAt(0).toUpperCase()}</span>
                {review.source.charAt(0).toUpperCase() + review.source.slice(1)}
              </div>
              <div className="source-score">
                <span className="score">{review.score?.toFixed(1) || 'N/A'}</span>
                <span className="max">/10</span>
              </div>
              <div className="source-votes">
                {review.votes || 0} 人评分
              </div>
              {review.url && (
                <a href={review.url} target="_blank" rel="noopener noreferrer" className="source-link">
                  查看原页面 →
                </a>
              )}
            </div>
          ))}
        </div>

        <div style={{ marginTop: '2rem', textAlign: 'center' }}>
          <button className="btn btn-secondary" onClick={() => navigate('/')}>
            ← 返回首页
          </button>
        </div>
      </div>
    </div>
  );
}

export default DetailPage;
