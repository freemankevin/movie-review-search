# 插入测试数据脚本
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database
from database.models import Movie, Review


def insert_test_data():
    """插入测试数据"""
    print("正在插入测试数据...")

    # 初始化数据库
    db_path = os.getenv('DATABASE', 'movies.db')
    db = Database(db_path)

    # 测试电影数据
    test_movies = [
        {
            'title': '你的名字。',
            'year': 2016,
            'description': '日本动画电影，讲述了一个关于时空交换的浪漫故事',
            'poster_url': 'https://example.com/poster1.jpg',
        },
        {
            'title': '泰坦尼克号',
            'year': 1997,
            'description': '一部关于1912年泰坦尼克号沉船事件的史诗爱情灾难电影',
            'poster_url': 'https://example.com/poster2.jpg',
        },
        {
            'title': '流浪地球',
            'year': 2019,
            'description': '中国科幻电影，讲述太阳即将毁灭，人类寻找新家园的故事',
            'poster_url': 'https://example.com/poster3.jpg',
        },
        {
            'title': '肖申克的救赎',
            'year': 1994,
            'description': '一部关于希望和友谊的经典剧情片',
            'poster_url': 'https://example.com/poster4.jpg',
        },
        {
            'title': '千与千寻',
            'year': 2001,
            'description': '宫崎骏执导的日本动画电影，讲述了一个女孩在神秘世界的冒险',
            'poster_url': 'https://example.com/poster5.jpg',
        },
        {
            'title': '盗梦空间',
            'year': 2010,
            'description': '克里斯托弗·诺兰执导的科幻惊悚片，关于梦境和现实的界限',
            'poster_url': 'https://example.com/poster6.jpg',
        },
        {
            'title': '阿凡达',
            'year': 2009,
            'description': '詹姆斯·卡梅隆执导的科幻史诗，讲述在潘多拉星球上的冒险',
            'poster_url': 'https://example.com/poster7.jpg',
        },
        {
            'title': '复仇者联盟',
            'year': 2012,
            'description': '漫威超级英雄团队电影，讲述英雄们联手拯救世界',
            'poster_url': 'https://example.com/poster8.jpg',
        },
        {
            'title': '星际穿越',
            'year': 2014,
            'description': '克里斯托弗·诺兰执导的科幻片，关于太空探索和时间穿越',
            'poster_url': 'https://example.com/poster9.jpg',
        },
        {
            'title': '寄生虫',
            'year': 2019,
            'description': '奉俊昊执导的韩国电影，关于社会阶层和贫富差距',
            'poster_url': 'https://example.com/poster10.jpg',
        },
    ]

    # 测试影评数据
    test_reviews = [
        {'movie_idx': 0, 'source': 'douban', 'score': 8.4, 'votes': 15000},
        {'movie_idx': 0, 'source': 'imdb', 'score': 8.2, 'votes': 12000},
        {'movie_idx': 1, 'source': 'douban', 'score': 9.4, 'votes': 200000},
        {'movie_idx': 1, 'source': 'rotten_tomatoes', 'score': 8.9, 'votes': 180000},
        {'movie_idx': 2, 'source': 'douban', 'score': 7.9, 'votes': 80000},
        {'movie_idx': 2, 'source': 'imdb', 'score': 7.4, 'votes': 60000},
        {'movie_idx': 3, 'source': 'douban', 'score': 9.7, 'votes': 250000},
        {'movie_idx': 3, 'source': 'imdb', 'score': 9.3, 'votes': 220000},
        {'movie_idx': 4, 'source': 'douban', 'score': 9.4, 'votes': 180000},
        {'movie_idx': 4, 'source': 'imdb', 'score': 8.6, 'votes': 160000},
        {'movie_idx': 5, 'source': 'douban', 'score': 9.3, 'votes': 190000},
        {'movie_idx': 5, 'source': 'rotten_tomatoes', 'score': 8.8, 'votes': 170000},
        {'movie_idx': 6, 'source': 'douban', 'score': 8.7, 'votes': 160000},
        {'movie_idx': 6, 'source': 'imdb', 'score': 8.8, 'votes': 150000},
        {'movie_idx': 7, 'source': 'douban', 'score': 8.1, 'votes': 140000},
        {'movie_idx': 7, 'source': 'rotten_tomatoes', 'score': 8.3, 'votes': 130000},
        {'movie_idx': 8, 'source': 'douban', 'score': 9.3, 'votes': 170000},
        {'movie_idx': 8, 'source': 'imdb', 'score': 8.6, 'votes': 160000},
        {'movie_idx': 9, 'source': 'douban', 'score': 8.7, 'votes': 150000},
        {'movie_idx': 9, 'source': 'imdb', 'score': 8.5, 'votes': 140000},
    ]

    # 插入电影数据
    movie_ids = []
    for idx, movie_data in enumerate(test_movies):
        try:
            movie = Movie(
                title=movie_data['title'],
                year=movie_data['year'],
                description=movie_data['description'],
                poster_url=movie_data['poster_url'],
            )
            movie_id = db.insert_movie(movie)
            movie_ids.append(movie_id)
            print(f"插入电影: {movie_data['title']}")
        except Exception as e:
            print(f"插入电影失败: {e}")
            continue

    # 插入影评数据
    for review_data in test_reviews:
        try:
            movie_id = movie_ids[review_data['movie_idx']]
            review = Review(
                movie_id=movie_id,
                source=review_data['source'],
                score=review_data['score'],
                votes=review_data['votes'],
                url=f'https://example.com/movie/{movie_id}',
                popularity=review_data['votes'],
            )
            db.insert_review(review)
            print(f"插入影评: {review_data['source']} - {review_data['score']}")
        except Exception as e:
            print(f"插入影评失败: {e}")
            continue

    print(f"\n测试数据插入完成！")
    print(f"电影: {len(movie_ids)} 部")
    print(f"影评: {len(test_reviews)} 条")


def main():
    """主函数"""
    insert_test_data()


if __name__ == '__main__':
    main()
