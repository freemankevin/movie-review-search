import React from 'react';

const MovieCard = ({ movie, onClick }) => {
  const avgScore = movie.avg_score?.toFixed(1);
  const topScore = Math.max(...Object.values(movie.scores || {})).toFixed(1);

  return (
    <div className="movie-card stagger-item" onClick={onClick}>
      <div className="movie-poster">
        {movie.poster_url ? (
          <img src={movie.poster_url} alt={movie.title} loading="lazy" />
        ) : (
          <div className="movie-poster-placeholder">🎬</div>
        )}
        <div className="movie-card-overlay">
          <button className="btn btn-accent">查看详情</button>
        </div>

        {topScore && (
          <div className="movie-badge">
            <div className="badge badge-accent">
              ⭐ {topScore}
            </div>
          </div>
        )}
      </div>

      <div className="movie-card-content">
        <h3 className="movie-title" title={movie.title}>
          {movie.title}
        </h3>

        <div className="movie-meta">
          <span className="movie-year">{movie.year || '未知'}</span>
          {avgScore && (
            <span className="movie-rating">
              <span className="rating-value">{avgScore}</span>
              <span className="rating-max">/10</span>
            </span>
          )}
        </div>

        <div className="movie-scores">
          {Object.entries(movie.scores || {})
            .slice(0, 2)
            .map(([source, score]) => (
              <div key={source} className="score-item">
                <span className="score-source">
                  {source.toUpperCase()}
                </span>
                <span className="score-value">{score.toFixed(1)}</span>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default MovieCard;
