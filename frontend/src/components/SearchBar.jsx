import React, { useState } from 'react';

const SearchBar = ({ onSearch, onFilterChange, sources = [] }) => {
  const [query, setQuery] = useState('');
  const [selectedSource, setSelectedSource] = useState('');
  const [minScore, setMinScore] = useState(0);
  const [sortBy, setSortBy] = useState('popularity');

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch({
      query,
      source: selectedSource,
      min_score: minScore > 0 ? minScore : null,
      sort_by: sortBy,
    });
  };

  return (
    <div className="search-section">
      <div className="search-container">
        <div className="search-title">
          <h1>🎬 电影影评搜索</h1>
          <p>汇集豆瓣、烂番茄等多家影评网站的热门作品</p>
        </div>

        <form onSubmit={handleSearch} className="search-wrapper">
          <div className="search-input-group">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              className="search-input"
              placeholder="搜索电影、动漫或电视剧..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <div className="search-filters">
            <select
              className="filter-select"
              value={selectedSource}
              onChange={(e) => setSelectedSource(e.target.value)}
            >
              <option value="">全部来源</option>
              {sources.map((source) => (
                <option key={source} value={source}>
                  {source.charAt(0).toUpperCase() + source.slice(1)}
                </option>
              ))}
            </select>

            <select
              className="filter-select"
              value={minScore}
              onChange={(e) => setMinScore(parseFloat(e.target.value))}
            >
              <option value="0">评分 ≥ 全部</option>
              <option value="6">评分 ≥ 6.0</option>
              <option value="7">评分 ≥ 7.0</option>
              <option value="8">评分 ≥ 8.0</option>
              <option value="9">评分 ≥ 9.0</option>
            </select>

            <select
              className="filter-select"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="popularity">按热度排序</option>
              <option value="score">按评分排序</option>
              <option value="votes">按投票数排序</option>
            </select>

            <button type="submit" className="btn btn-accent btn-md">
              搜索
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SearchBar;
