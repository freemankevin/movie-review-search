import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/App.css';
import '../styles/components.css';

function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div className="App">
      <div className="empty-state" style={{ padding: '4rem 2rem' }}>
        <div className="empty-icon">🔍</div>
        <h3>404 - 页面未找到</h3>
        <p>您访问的页面不存在</p>
        <button className="btn btn-primary" onClick={() => navigate('/')}>
          返回首页
        </button>
      </div>
    </div>
  );
}

export default NotFoundPage;
