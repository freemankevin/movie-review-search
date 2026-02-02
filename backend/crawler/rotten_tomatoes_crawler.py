# 烂番茄爬虫
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
import re
from .base_crawler import BaseCrawler


class RottenTomatoesCrawler(BaseCrawler):
    """烂番茄电影爬虫"""

    def __init__(self, delay: float = 2.0):
        super().__init__(delay)
        self.base_url = 'https://www.rottentomatoes.com'

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """搜索烂番茄电影"""
        # 烂番茄搜索API（简化版）
        search_url = f'{self.base_url}/api/private/v2.0/search'

        params = {
            'q': query,
            'limit': limit,
            'type': 'movie',
        }

        response = self._request(search_url, params)
        if not response:
            return []

        try:
            data = response.json()
            movies = []

            if 'movies' in data:
                for item in data['movies'][:limit]:
                    movie_data = self._parse_movie_item(item)
                    if movie_data:
                        movies.append(movie_data)

            return movies
        except Exception as e:
            print(f"解析烂番茄数据失败: {e}")
            return []

    def get_detail(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """获取烂番茄电影详情"""
        url = f'{self.base_url}/m/{movie_id}'
        response = self._request(url)

        if not response:
            return None

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_movie_detail(soup, movie_id)
        except Exception as e:
            print(f"解析烂番茄详情失败: {e}")
            return None

    def get_source_name(self) -> str:
        return 'rotten_tomatoes'

    def _parse_movie_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """解析电影列表项"""
        try:
            # 提取ID
            movie_id = item.get('url', '').split('/')[-1] or item.get('id', '')

            # 提取评分
            score = None
            if 'meterScore' in item:
                score = item['meterScore'] / 10  # 转换为10分制

            # 提取投票数
            votes = item.get('reviews', 0)

            # 提取年份
            year = None
            if 'year' in item:
                year = int(item['year'])

            # 提取海报
            poster = item.get('image', '') or ''

            return {
                'title': item.get('name', ''),
                'year': year,
                'description': item.get('description', ''),
                'poster_url': poster,
                'score': score,
                'votes': votes,
                'url': f'{self.base_url}/m/{movie_id}',
                'popularity': votes or 0,
            }
        except Exception as e:
            print(f"解析电影项失败: {e}")
            return None

    def _parse_movie_detail(self, soup: BeautifulSoup, movie_id: str) -> Optional[Dict[str, Any]]:
        """解析电影详情页"""
        try:
            # 标题
            title_elem = soup.find('h1', slot='title')
            title = title_elem.text.strip() if title_elem else ''

            # 年份
            year = None
            year_elem = soup.find('p', slot='releaseYear')
            if year_elem:
                year_match = re.search(r'\d{4}', year_elem.text)
                if year_match:
                    year = int(year_match.group())

            # 评分
            score = None
            score_elem = soup.find('score-board-deprecated')
            if score_elem:
                score_text = score_elem.text.strip()
                score_match = re.search(r'(\d+)', score_text)
                if score_match:
                    score = float(score_match.group(1)) / 10

            # 投票数
            votes = 0
            votes_elem = soup.find('span', slot='count')
            if votes_elem:
                votes_match = re.search(r'\d+', votes_elem.text)
                if votes_match:
                    votes = int(votes_match.group())

            # 简介
            description = ''
            desc_elem = soup.find('p', slot='description')
            if desc_elem:
                description = desc_elem.text.strip()

            # 海报
            poster = ''
            poster_elem = soup.find('img', slot='posterImage')
            if poster_elem:
                poster = poster_elem.get('src', '')

            return {
                'title': title,
                'year': year,
                'description': description,
                'poster_url': poster,
                'score': score,
                'votes': votes,
                'url': f'{self.base_url}/m/{movie_id}',
                'popularity': votes or 0,
            }
        except Exception as e:
            print(f"解析电影详情失败: {e}")
            return None
