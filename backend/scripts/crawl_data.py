# 数据爬取脚本
import sys
import os
import argparse

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database
from database.models import Movie, Review
from crawler import DoubanCrawler, RottenTomatoesCrawler, IMDBCrawler
from utils.helpers import clean_text, extract_year


def crawl_source(source: str, query: str = '', limit: int = 50):
    """
    爬取指定数据源的数据
    
    Args:
        source: 数据源名称 (douban/rotten_tomatoes/imdb)
        query: 搜索关键词
        limit: 爬取数量
    """
    print(f"开始爬取 {source} 数据...")

    # 初始化数据库
    db_path = os.getenv('DATABASE', 'movies.db')
    db = Database(db_path)

    # 获取对应的爬虫
    crawlers = {
        'douban': DoubanCrawler(delay=2.0),
        'rotten_tomatoes': RottenTomatoesCrawler(delay=2.0),
        'imdb': IMDBCrawler(delay=2.0),
    }

    crawler = crawlers.get(source)
    if not crawler:
        print(f"错误: 未知的数据源 '{source}'")
        return 0

    # 爬取数据
    movies_data = crawler.search(query, limit=limit)
    print(f"从 {source} 爬取到 {len(movies_data)} 条数据")

    # 保存到数据库
    saved_count = 0
    for idx, movie_data in enumerate(movies_data, 1):
        try:
            print(f"[{idx}/{len(movies_data)}] 保存: {movie_data.get('title', 'N/A')}")

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
            print(f"保存失败: {e}")
            continue

    print(f"成功保存 {saved_count}/{len(movies_data)} 条数据")
    return saved_count


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='爬取电影数据')
    parser.add_argument('--source', type=str, default='douban',
                        help='数据源 (douban/rotten_tomatoes/imdb)')
    parser.add_argument('--query', type=str, default='',
                        help='搜索关键词')
    parser.add_argument('--limit', type=int, default=50,
                        help='爬取数量')

    args = parser.parse_args()

    # 验证数据源
    valid_sources = ['douban', 'rotten_tomatoes', 'imdb']
    if args.source not in valid_sources:
        print(f"错误: 无效的数据源 '{args.source}'")
        print(f"有效数据源: {', '.join(valid_sources)}")
        return

    # 开始爬取
    saved_count = crawl_source(args.source, args.query, args.limit)

    print(f"\n爬取完成！共保存 {saved_count} 条数据")


if __name__ == '__main__':
    main()
