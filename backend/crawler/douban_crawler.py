# 豆瓣爬虫
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
import re
from .base_crawler import BaseCrawler


class DoubanCrawler(BaseCrawler):
    """豆瓣电影爬虫"""

    def __init__(self, delay: float = 2.0):
        super().__init__(delay)
        self.base_url = 'https://movie.douban.com'
        self.search_url = f'{self.base_url}/j/search_subjects'

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """搜索豆瓣电影"""
        params = {
            'type': 'movie',
            'tag': '热门',
            'sort': 'recommendation',
            'page_limit': limit,
            'page_start': 0,
        }

        if query:
            params['search_text'] = query

        response = self._request(self.search_url, params)
        if not response:
            return []

        try:
            data = response.json()
            movies = []

            if 'subjects' in data:
                for item in data['subjects'][:limit]:
                    movie_data = self._parse_movie_item(item)
                    if movie_data:
                        movies.append(movie_data)

            return movies
        except Exception as e:
            print(f"解析豆瓣数据失败: {e}")
            return []

    def get_detail(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """获取豆瓣电影详情"""
        url = f'{self.base_url}/subject/{movie_id}/'
        response = self._request(url)

        if not response:
            return None

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_movie_detail(soup, movie_id)
        except Exception as e:
            print(f"解析豆瓣详情失败: {e}")
            return None

    def get_source_name(self) -> str:
        return 'douban'

    def _parse_movie_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """解析电影列表项"""
        try:
            # 提取ID
            movie_id = item.get('id', '')

            # 提取评分
            rating = item.get('rate', '0')
            score = float(rating) if rating else None

            # 提取投票数
            votes = item.get('vote_count', 0)

            # 提取年份
            year = None
            if 'year' in item:
                year_match = re.search(r'\d{4}', str(item['year']))
                if year_match:
                    year = int(year_match.group())

            # 提取海报
            poster = item.get('cover', {}).get('large', '') or item.get('cover', '')

            return {
                'title': item.get('title', ''),
                'year': year,
                'description': item.get('card_subtitle', ''),
                'poster_url': poster,
                'score': score,
                'votes': votes,
                'url': f'{self.base_url}/subject/{movie_id}/',
                'popularity': votes or 0,
            }
        except Exception as e:
            print(f"解析电影项失败: {e}")
            return None

    def _parse_movie_detail(self, soup: BeautifulSoup, movie_id: str) -> Optional[Dict[str, Any]]:
        """解析电影详情页"""
        try:
            # 标题
            title_elem = soup.find('span', property='v:itemreviewed')
            title = title_elem.text.strip() if title_elem else ''

            # 年份
            year = None
            year_elem = soup.find('span', class_='year')
            if year_elem:
                year_match = re.search(r'\((\d{4})\)', year_elem.text)
                if year_match:
                    year = int(year_match.group(1))

            # 评分
            score = None
            rating_elem = soup.find('strong', class_='ll rating_num')
            if rating_elem:
                score = float(rating_elem.text.strip())

            # 投票数
            votes = 0
            votes_elem = soup.find('span', property='v:votes')
            if votes_elem:
                votes_match = re.search(r'\d+', votes_elem.text)
                if votes_match:
                    votes = int(votes_match.group())

            # 简介
            description = ''
            desc_elem = soup.find('span', property='v:summary')
            if desc_elem:
                description = desc_elem.text.strip()

            # 海报
            poster = ''
            poster_elem = soup.find('img', rel='v:image')
            if poster_elem:
                poster = poster_elem.get('src', '')

            return {
                'title': title,
                'year': year,
                'description': description,
                'poster_url': poster,
                'score': score,
                'votes': votes,
                'url': f'{self.base_url}/subject/{movie_id}/',
                'popularity': votes or 0,
            }
        except Exception as e:
            print(f"解析电影详情失败: {e}")
            return None
