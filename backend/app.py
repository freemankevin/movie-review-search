# Flask 主应用
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from database import Database
from database.models import Movie, Review
from crawler import DoubanCrawler, RottenTomatoesCrawler, IMDBCrawler
from utils.helpers import clean_text, extract_year


app = Flask(__name__)
CORS(app)

# 初始化数据库
db_path = os.getenv('DATABASE', 'movies.db')
db = Database(db_path)

# 初始化爬虫
douban_crawler = DoubanCrawler(delay=2.0)
rotten_tomatoes_crawler = RottenTomatoesCrawler(delay=2.0)
imdb_crawler = IMDBCrawler(delay=2.0)

# 爬虫映射
crawlers = {
    'douban': douban_crawler,
    'rotten_tomatoes': rotten_tomatoes_crawler,
    'imdb': imdb_crawler,
}


@app.route('/')
def index():
    """首页"""
    return jsonify({
        'message': '电影影评搜索聚合工具 API',
        'version': '1.0.0',
        'endpoints': {
            'search': '/api/search',
            'movie': '/api/movie/<id>',
            'trending': '/api/trending',
            'sources': '/api/sources',
            'stats': '/api/stats',
        }
    })


@app.route('/api/search', methods=['GET'])
def search_movies():
    """搜索电影"""
    try:
        # 获取查询参数
        query = request.args.get('query', '').strip()
        source = request.args.get('source', '').strip()
        min_score = request.args.get('min_score', type=float)
        sort_by = request.args.get('sort_by', 'popularity').strip()
        limit = request.args.get('limit', 20, type=int)

        # 参数验证
        if limit > 100:
            limit = 100

        # 搜索数据库
        movies = db.search_movies(
            query=query if query else None,
            source=source if source else None,
            min_score=min_score,
            sort_by=sort_by,
            limit=limit
        )

        # 转换为响应格式
        result = [movie.to_dict() for movie in movies]

        return jsonify({
            'success': True,
            'total': len(result),
            'data': result
        })

    except Exception as e:
        print(f"搜索错误: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/movie/<int:movie_id>', methods=['GET'])
def get_movie_detail(movie_id):
    """获取电影详情"""
    try:
        movie_with_reviews = db.get_movie_by_id(movie_id)

        if not movie_with_reviews:
            return jsonify({
                'success': False,
                'error': 'Movie not found'
            }), 404

        return jsonify({
            'success': True,
            'data': movie_with_reviews.to_dict()
        })

    except Exception as e:
        print(f"获取详情错误: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/trending', methods=['GET'])
def get_trending():
    """获取热度排行"""
    try:
        limit = request.args.get('limit', 10, type=int)

        if limit > 50:
            limit = 50

        movies = db.get_trending_movies(limit=limit)
        result = [movie.to_dict() for movie in movies]

        return jsonify({
            'success': True,
            'total': len(result),
            'data': result
        })

    except Exception as e:
        print(f"获取热度排行错误: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sources', methods=['GET'])
def get_sources():
    """获取可用数据源"""
    try:
        sources = db.get_sources()

        return jsonify({
            'success': True,
            'sources': sources
        })

    except Exception as e:
        print(f"获取数据源错误: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        stats = db.get_stats()

        return jsonify({
            'success': True,
            'stats': stats
        })

    except Exception as e:
        print(f"获取统计信息错误: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/crawl', methods=['POST'])
def crawl_movies():
    """爬取电影数据（内部使用）"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        source = data.get('source', 'douban')
        query = data.get('query', '')
        limit = data.get('limit', 20)

        # 获取对应的爬虫
        crawler = crawlers.get(source)
        if not crawler:
            return jsonify({
                'success': False,
                'error': f'Unknown source: {source}'
            }), 400

        # 爬取数据
        movies_data = crawler.search(query, limit=limit)

        # 保存到数据库
        saved_count = 0
        for movie_data in movies_data:
            try:
                # 保存电影
                movie = Movie(
                    title=clean_text(movie_data.get('title', '')),
                    year=extract_year(movie_data.get('description', '')),
                    description=clean_text(movie_data.get('description', '')),
                    poster_url=movie_data.get('poster_url', ''),
                )
                movie_id = db.insert_movie(movie)

                # 保存影评
                review = Review(
                    movie_id=movie_id,
                    source=crawler.get_source_name(),
                    score=movie_data.get('score'),
                    votes=movie_data.get('votes'),
                    url=movie_data.get('url', ''),
                    popularity=movie_data.get('popularity', 0),
                )
                db.insert_review(review)
                saved_count += 1

            except Exception as e:
                print(f"保存电影失败: {e}")
                continue

        return jsonify({
            'success': True,
            'saved': saved_count,
            'total': len(movies_data)
        })

    except Exception as e:
        print(f"爬取错误: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'error': 'Not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"启动 Flask 服务器，端口: {port}")
    print(f"数据库路径: {db_path}")
    print(f"调试模式: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
