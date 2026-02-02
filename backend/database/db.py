# 数据库操作模块
import sqlite3
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
from datetime import datetime
from .models import Movie, Review, MovieWithReviews


class Database:
    """数据库操作类"""

    def __init__(self, db_path: str = 'movies.db'):
        self.db_path = db_path
        self.init_database()

    @contextmanager
    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_database(self):
        """初始化数据库表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 创建 movies 表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL UNIQUE,
                    year INTEGER,
                    description TEXT,
                    poster_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建 reviews 表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movie_id INTEGER NOT NULL,
                    source TEXT NOT NULL,
                    score REAL,
                    votes INTEGER,
                    url TEXT,
                    popularity INTEGER DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(movie_id) REFERENCES movies(id),
                    UNIQUE(movie_id, source)
                )
            ''')

            # 创建索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_title ON movies(title)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_source ON reviews(source)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_popularity ON reviews(popularity)
            ''')

            conn.commit()

    def insert_movie(self, movie: Movie) -> int:
        """插入电影"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute('''
                INSERT OR REPLACE INTO movies (title, year, description, poster_url, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (movie.title, movie.year, movie.description, movie.poster_url, now))
            conn.commit()
            return cursor.lastrowid

    def insert_review(self, review: Review) -> int:
        """插入影评"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute('''
                INSERT OR REPLACE INTO reviews 
                (movie_id, source, score, votes, url, popularity, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (review.movie_id, review.source, review.score, review.votes,
                   review.url, review.popularity, now))
            conn.commit()
            return cursor.lastrowid

    def get_movie_by_id(self, movie_id: int) -> Optional[MovieWithReviews]:
        """根据ID获取电影详情"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 获取电影信息
            cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
            movie_row = cursor.fetchone()

            if not movie_row:
                return None

            movie = Movie(
                id=movie_row['id'],
                title=movie_row['title'],
                year=movie_row['year'],
                description=movie_row['description'],
                poster_url=movie_row['poster_url'],
                created_at=datetime.fromisoformat(movie_row['created_at']) if movie_row['created_at'] else None,
                updated_at=datetime.fromisoformat(movie_row['updated_at']) if movie_row['updated_at'] else None,
            )

            # 获取影评信息
            cursor.execute('SELECT * FROM reviews WHERE movie_id = ?', (movie_id,))
            review_rows = cursor.fetchall()

            reviews = []
            total_score = 0
            total_popularity = 0

            for row in review_rows:
                review = Review(
                    id=row['id'],
                    movie_id=row['movie_id'],
                    source=row['source'],
                    score=row['score'],
                    votes=row['votes'],
                    url=row['url'],
                    popularity=row['popularity'] or 0,
                    updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
                )
                reviews.append(review)
                if review.score:
                    total_score += review.score
                total_popularity += review.popularity or 0

            # 计算平均评分
            avg_score = total_score / len(reviews) if reviews else 0

            return MovieWithReviews(
                movie=movie,
                reviews=reviews,
                avg_score=avg_score,
                popularity=total_popularity
            )

    def search_movies(self, query: str = None, source: str = None,
                   min_score: float = None, sort_by: str = 'popularity',
                   limit: int = 20) -> List[MovieWithReviews]:
        """搜索电影"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 构建查询
            sql = '''
                SELECT m.*, 
                       GROUP_CONCAT(
                           json_object('source', r.source, 'score', r.score, 'votes', r.votes, 'url', r.url, 'popularity', r.popularity),
                           ', '
                       ) as reviews_json
                FROM movies m
                LEFT JOIN reviews r ON m.id = r.movie_id
            '''
            params = []
            conditions = []

            if query:
                conditions.append('m.title LIKE ?')
                params.append(f'%{query}%')

            if source:
                conditions.append('r.source = ?')
                params.append(source)

            if min_score:
                conditions.append('r.score >= ?')
                params.append(min_score)

            if conditions:
                sql += ' WHERE ' + ' AND '.join(conditions)

            sql += ' GROUP BY m.id'

            # 排序
            if sort_by == 'popularity':
                sql += ' ORDER BY COALESCE(SUM(r.popularity), 0) DESC'
            elif sort_by == 'score':
                sql += ' ORDER BY AVG(r.score) DESC'
            elif sort_by == 'votes':
                sql += ' ORDER BY SUM(r.votes) DESC'

            # 限制结果数量
            sql += ' LIMIT ?'
            params.append(limit)

            cursor.execute(sql, params)
            rows = cursor.fetchall()

            movies = []
            for row in rows:
                movie = Movie(
                    id=row['id'],
                    title=row['title'],
                    year=row['year'],
                    description=row['description'],
                    poster_url=row['poster_url'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                    updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
                )

                # 解析影评JSON
                reviews = []
                scores = {}
                total_score = 0
                total_popularity = 0

                if row['reviews_json']:
                    import json
                    try:
                        reviews_data = json.loads(f'[{row["reviews_json"]}]')
                        for r_data in reviews_data:
                            if r_data:
                                review = Review(
                                    movie_id=row['id'],
                                    source=r_data.get('source', ''),
                                    score=r_data.get('score'),
                                    votes=r_data.get('votes'),
                                    url=r_data.get('url'),
                                    popularity=r_data.get('popularity', 0),
                                )
                                reviews.append(review)
                                if r_data.get('score'):
                                    scores[r_data.get('source', '')] = r_data.get('score')
                                    total_score += r_data.get('score', 0)
                                total_popularity += r_data.get('popularity', 0)
                    except (json.JSONDecodeError, TypeError):
                        pass

                avg_score = total_score / len(reviews) if reviews else 0

                movies.append(MovieWithReviews(
                    movie=movie,
                    reviews=reviews,
                    avg_score=avg_score,
                    popularity=total_popularity
                ))

            return movies

    def get_trending_movies(self, limit: int = 10) -> List[MovieWithReviews]:
        """获取热度排行"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            sql = '''
                SELECT m.*, 
                       GROUP_CONCAT(
                           json_object('source', r.source, 'score', r.score, 'votes', r.votes, 'url', r.url, 'popularity', r.popularity),
                           ', '
                       ) as reviews_json
                FROM movies m
                LEFT JOIN reviews r ON m.id = r.movie_id
                GROUP BY m.id
                ORDER BY COALESCE(SUM(r.popularity), 0) DESC
                LIMIT ?
            '''

            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()

            movies = []
            for row in rows:
                movie = Movie(
                    id=row['id'],
                    title=row['title'],
                    year=row['year'],
                    description=row['description'],
                    poster_url=row['poster_url'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                    updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
                )

                # 解析影评JSON
                reviews = []
                scores = {}
                total_score = 0
                total_popularity = 0

                if row['reviews_json']:
                    import json
                    try:
                        reviews_data = json.loads(f'[{row["reviews_json"]}]')
                        for r_data in reviews_data:
                            if r_data:
                                review = Review(
                                    movie_id=row['id'],
                                    source=r_data.get('source', ''),
                                    score=r_data.get('score'),
                                    votes=r_data.get('votes'),
                                    url=r_data.get('url'),
                                    popularity=r_data.get('popularity', 0),
                                )
                                reviews.append(review)
                                if r_data.get('score'):
                                    scores[r_data.get('source', '')] = r_data.get('score')
                                    total_score += r_data.get('score', 0)
                                total_popularity += r_data.get('popularity', 0)
                    except (json.JSONDecodeError, TypeError):
                        pass

                avg_score = total_score / len(reviews) if reviews else 0

                movies.append(MovieWithReviews(
                    movie=movie,
                    reviews=reviews,
                    avg_score=avg_score,
                    popularity=total_popularity
                ))

            return movies

    def get_sources(self) -> List[str]:
        """获取可用的数据源"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT source FROM reviews ORDER BY source')
            rows = cursor.fetchall()
            return [row['source'] for row in rows]

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 电影总数
            cursor.execute('SELECT COUNT(*) as count FROM movies')
            total_movies = cursor.fetchone()['count']

            # 数据源数量
            cursor.execute('SELECT COUNT(DISTINCT source) as count FROM reviews')
            total_sources = cursor.fetchone()['count']

            # 影评总数
            cursor.execute('SELECT COUNT(*) as count FROM reviews')
            total_reviews = cursor.fetchone()['count']

            return {
                'total_movies': total_movies,
                'total_sources': total_sources,
                'total_reviews': total_reviews,
            }
