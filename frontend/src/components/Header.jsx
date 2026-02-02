import React from 'react';

const Header = ({ stats }) => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <span className="logo-icon">🎬</span>
          <span>影评搜索</span>
        </div>
        {stats && (
          <div className="header-stats">
            <span>{stats.total_movies} 部作品</span>
            <span>{stats.total_sources} 个数据源</span>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
