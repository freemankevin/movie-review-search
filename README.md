# 🎬 影评搜索聚合工具

一个强大的电影/动漫/电视剧影评聚合搜索平台，整合豆瓣、烂番茄等多家影评网站的数据，帮助你快速找到热度最高、评分最好的作品。

![React](https://img.shields.io/badge/React-18-61dafb?logo=react)
![Python](https://img.shields.io/badge/Python-3.9+-3776ab?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3-003b57?logo=sqlite)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask)

## ✨ 核心功能

- 🔍 **多源搜索** - 同时搜索豆瓣、烂番茄、IMDb 等多个平台
- 🔥 **热度排序** - 实时显示最受欢迎的电影/动漫/电视剧
- ⭐ **综合评分** - 对比多个平台的评分，看一目了然
- 📊 **智能筛选** - 按评分范围、发行年份、内容类型筛选
- 💾 **本地缓存** - SQLite 数据库存储，快速查询
- 🎨 **现代 UI** - 响应式设计，流畅交互体验

## 🏗️ 项目结构

```
movie-review-search/
├── frontend/                    # React 前端应用
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchBar.jsx          # 搜索框组件
│   │   │   ├── MovieCard.jsx          # 电影卡片组件
│   │   │   ├── FilterPanel.jsx        # 筛选面板
│   │   │   └── TrendingMovies.jsx     # 热度排行
│   │   ├── pages/
│   │   │   ├── HomePage.jsx           # 首页
│   │   │   └── DetailPage.jsx         # 详情页
│   │   ├── api/
│   │   │   └── movieApi.js            # API 调用模块
│   │   ├── styles/
│   │   │   ├── App.css                # 全局样式
│   │   │   ├── components.css         # 组件样式
│   │   │   └── animations.css         # 动画样式
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── .env.example
│
├── backend/                     # Python Flask 后端
│   ├── app.py                   # Flask 主应用
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── base_crawler.py      # 爬虫基类
│   │   ├── douban_crawler.py    # 豆瓣爬虫
│   │   ├── rotten_tomatoes_crawler.py  # 烂番茄爬虫
│   │   └── imdb_crawler.py      # IMDb 爬虫
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py                # 数据库操作
│   │   └── models.py            # 数据模型
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py           # 工具函数
│   ├── requirements.txt
│   └── .env.example
│
├── database/
│   └── movies.db                # SQLite 数据库文件
│
└── docs/
    ├── API.md                   # API 文档
    ├── DEPLOYMENT.md            # 部署指南
    └── DATABASE_SCHEMA.md       # 数据库架构
```

## 🚀 快速开始

### 前置要求

- Node.js 14+ 和 npm/yarn
- Python 3.9+
- pip（Python 包管理器）

### 安装与运行

#### 1. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件
cp .env.example .env

# 初始化数据库并启动爬虫（可选）
python scripts/init_db.py
python scripts/crawl_data.py

# 启动 Flask 服务
python app.py
# 服务将在 http://localhost:5000 运行
```

#### 2. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 创建 .env 文件
cp .env.example .env

# 启动开发服务器
npm start
# 应用将在 http://localhost:3000 运行
```

## 📡 API 文档

### 搜索电影

```
GET /api/search?query=心能&source=douban&min_score=7.0&sort_by=popularity&limit=20
```

**参数：**
- `query` (string) - 搜索关键词
- `source` (string, optional) - 数据源 (douban/rotten_tomatoes/imdb)
- `min_score` (float, optional) - 最低评分
- `sort_by` (string, optional) - 排序方式 (popularity/score/votes)
- `limit` (integer, optional) - 结果数量限制，默认 20

**响应示例：**
```json
{
  "success": true,
  "total": 5,
  "data": [
    {
      "id": 1,
      "title": "你的名字。",
      "year": 2016,
      "description": "日本动画电影...",
      "poster_url": "https://...",
      "scores": {
        "douban": 8.4,
        "imdb": 8.2
      },
      "avg_score": 8.3,
      "popularity": 15000
    }
  ]
}
```

### 获取电影详情

```
GET /api/movie/{movie_id}
```

### 获取热度排行

```
GET /api/trending?limit=10
```

### 获取可用数据源

```
GET /api/sources
```

### 获取统计信息

```
GET /api/stats
```

## 🗄️ 数据库架构

### movies 表
```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    year INTEGER,
    description TEXT,
    poster_url TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### reviews 表
```sql
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    source TEXT NOT NULL,           -- douban, rotten_tomatoes, imdb 等
    score REAL,                     -- 评分 (1-10)
    votes INTEGER,                  -- 投票数/热度
    url TEXT,                       -- 原页面链接
    popularity INTEGER,             -- 热度指标
    updated_at TIMESTAMP,
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    UNIQUE(movie_id, source)
);
```

## 🛠️ 技术栈详解

### 前端
- **React 18** - UI 框架
- **Tailwind CSS** - 样式框架（可选）
- **Axios** - HTTP 客户端
- **React Router** - 路由管理
- **React Query** 或 **SWR** - 数据获取和缓存

### 后端
- **Flask** - Web 框架
- **Flask-CORS** - 跨域支持
- **requests** - HTTP 库
- **BeautifulSoup4** - HTML 解析（爬虫）
- **Selenium**（可选）- 动态网页爬取

### 数据库
- **SQLite 3** - 轻量级关系型数据库

## 🎯 开发路线

- [ ] 基础搜索功能
- [ ] 豆瓣数据爬虫
- [ ] 烂番茄数据爬虫
- [ ] IMDb 数据爬虫
- [ ] 热度排行功能
- [ ] 高级筛选功能
- [ ] 用户收藏功能
- [ ] 历史搜索记录
- [ ] 评论同步功能
- [ ] 推荐系统
- [ ] Docker 部署
- [ ] 性能优化
- [ ] 自动化爬虫任务

## 🔧 配置说明

### 前端 .env.example
```
REACT_APP_API_BASE_URL=http://localhost:5000
REACT_APP_API_TIMEOUT=10000
```

### 后端 .env.example
```
FLASK_ENV=development
DATABASE_URL=sqlite:///movies.db
DOUBAN_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:3000
```

## 📝 爬虫使用指南

### 定期更新数据

```bash
# 后端目录下执行
python scripts/crawl_data.py --source douban --limit 100
python scripts/crawl_data.py --source rotten_tomatoes --limit 100
```

### 爬虫注意事项

- 遵守网站 robots.txt 规则
- 设置合理的请求延迟（1-3秒）
- 使用合法的 User-Agent
- 尊重网站服务条款
- 建议定时任务（每天 1-2 次）更新数据

## 🐛 常见问题

### Q: 爬虫无法获取数据？
A: 检查网站是否有反爬虫机制，可能需要：
- 更新 User-Agent
- 使用代理 IP
- 增加请求延迟
- 使用 Selenium 处理动态内容

### Q: 数据库性能下降？
A: 尝试以下优化：
- 为常用字段建立索引
- 定期清理过期数据
- 分页查询而不是一次加载全部
- 使用 Redis 缓存热门查询

### Q: 跨域请求错误？
A: 确保后端启用了 CORS：
```python
from flask_cors import CORS
CORS(app)
```

## 🤝 贡献指南

欢迎贡献！请：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📧 联系方式

如有问题或建议，欢迎：
- 提交 Issue
- 发起讨论
- 发送邮件

## ⚖️ 法律声明

本项目仅供学习研究使用。爬取数据时请遵守相关网站的使用条款和法律规定。用户对使用本工具造成的后果承担全部责任。

