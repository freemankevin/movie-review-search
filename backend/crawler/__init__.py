# 爬虫模块初始化
from .base_crawler import BaseCrawler
from .douban_crawler import DoubanCrawler
from .rotten_tomatoes_crawler import RottenTomatoesCrawler
from .imdb_crawler import IMDBCrawler

__all__ = ['BaseCrawler', 'DoubanCrawler', 'RottenTomatoesCrawler', 'IMDBCrawler']
