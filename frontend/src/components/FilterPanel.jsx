import React, { useState } from 'react';

const FilterPanel = ({ onFilterChange }) => {
  const [filters, setFilters] = useState({
    minScore: 0,
    maxScore: 10,
    year: null,
    type: 'all',
  });

  const handleChange = (name, value) => {
    const newFilters = { ...filters, [name]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="filter-panel">
      <div className="filter-grid">
        {/* 评分范围 */}
        <div className="filter-group">
          <label className="filter-label">评分范围</label>
          <div className="filter-range">
            <input
              type="range"
              min="0"
              max="10"
              step="0.5"
              value={filters.minScore}
              onChange={(e) => handleChange('minScore', parseFloat(e.target.value))}
            />
            <div className="filter-value">{filters.minScore.toFixed(1)}</div>
          </div>
        </div>

        {/* 发行年份 */}
        <div className="filter-group">
          <label className="filter-label">发行年份</label>
          <select
            className="input-base"
            value={filters.year || ''}
            onChange={(e) => handleChange('year', e.target.value || null)}
          >
            <option value="">全部年份</option>
            {Array.from({ length: 30 }).map((_, i) => {
              const year = new Date().getFullYear() - i;
              return (
                <option key={year} value={year}>
                  {year}
                </option>
              );
            })}
          </select>
        </div>

        {/* 内容类型 */}
        <div className="filter-group">
          <label className="filter-label">内容类型</label>
          <div className="filter-options">
            <label className="filter-option">
              <input
                type="radio"
                name="type"
                value="all"
                checked={filters.type === 'all'}
                onChange={(e) => handleChange('type', e.target.value)}
              />
              <label>全部</label>
            </label>
            <label className="filter-option">
              <input
                type="radio"
                name="type"
                value="movie"
                checked={filters.type === 'movie'}
                onChange={(e) => handleChange('type', e.target.value)}
              />
              <label>电影</label>
            </label>
            <label className="filter-option">
              <input
                type="radio"
                name="type"
                value="anime"
                checked={filters.type === 'anime'}
                onChange={(e) => handleChange('type', e.target.value)}
              />
              <label>动漫</label>
            </label>
            <label className="filter-option">
              <input
                type="radio"
                name="type"
                value="series"
                checked={filters.type === 'series'}
                onChange={(e) => handleChange('type', e.target.value)}
              />
              <label>电视剧</label>
            </label>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilterPanel;
