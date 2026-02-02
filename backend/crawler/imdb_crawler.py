# IMDb爬虫
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
import re
from .base_crawler import BaseCrawler


class IMDBCrawler(BaseCrawler):
    """IMDb电影爬虫"""

    def __init__(self, delay: float = 2.0):
        super().__init__(delay)
        self.base_url = 'https://www.imdb.com'
        self.search_url = f'{self.base_url}/find'

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """搜索IMDb电影"""
        params = {
            'q': query,
            's': 'all',
            'ref_': 'nv_sr_sm',
        }

        response = self._request(self.search_url, params)
        if not response:
            return []

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            movies = []

            # 查找电影列表
            find_section = soup.find('div', class_='findSection')
            if find_section:
                results = find_section.find_all('tr', class_='findResult')
                for item in results[:limit]:
                    movie_data = self._parse_movie_item(item)
                    if movie_data:
                        movies.append(movie_data)

            return movies
        except Exception as e:
            print(f"解析IMDb数据失败: {e}")
            return []

    def get_detail(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """获取IMDb电影详情"""
        url = f'{self.base_url}/title/{movie_id}/'
        response = self._request(url)

        if not response:
            return None

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_movie_detail(soup, movie_id)
        except Exception as e:
            print(f"解析IMDb详情失败: {e}")
            return None

    def get_source_name(self) -> str:
        return 'imdb'

    def _parse_movie_item(self, item) -> Optional[Dict[str, Any]]:
        """解析电影列表项"""
        try:
            # 提取链接和ID
            link_elem = item.find('a')
            if not link_elem:
                return None

            url = link_elem.get('href', '')
            movie_id = url.split('/')[2] if len(url.split('/')) > 2 else ''

            # 提取标题
            title_elem = item.find('td', class_='result_text')
            title = title_elem.text.strip() if title_elem else ''

            # 提取年份
            year = None
            year_elem = item.find('span', class_='lister-item-year')
            if year_elem:
                year_match = re.search(r'\((\d{4})\)', year_elem.text)
                if year_match:
                    year = int(year_match.group(1))

            # 提取海报
            poster = ''
            poster_elem = item.find('img')
            if poster_elem:
                poster = poster_elem.get('src', '') or poster_elem.get('loadlate', '')

            # IMDb评分通常在详情页
            return {
                'title': title,
                'year': year,
                'description': '',
                'poster_url': poster,
                'score': None,
                'votes': None,
                'url': f'{self.base_url}{url}',
                'popularity': 0,
            }
        except Exception as e:
            print(f"解析电影项失败: {e}")
            return None

    def _parse_movie_detail(self, soup: BeautifulSoup, movie_id: str) -> Optional[Dict[str, Any]]:
        """解析电影详情页"""
        try:
            # 标题
            title_elem = soup.find('h1', {'data-testid': 'hero-title-block__title'})
            title = title_elem.text.strip() if title_elem else ''

            # 年份
            year = None
            year_elem = soup.find('span', class_='sc-b0691f29-8b76-451a-9d8e-6c7f0e29f8f')
            if year_elem:
                year_match = re.search(r'\d{4}', year_elem.text)
                if year_match:
                    year = int(year_match.group())

            # 评分
            score = None
            score_elem = soup.find('span', {'data-testid': 'hero-rating-bar__aggregate-rating__score'})
            if score_elem:
                score_text = score_elem.text.strip()
                score_match = re.search(r'[\d.]+', score_text)
                if score_match:
                    score = float(score_match.group())

            # 投票数
            votes = 0
            votes_elem = soup.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__count'})
            if votes_elem:
                votes_text = votes_elem.text.strip()
                votes_match = re.search(r'[\d,]+', votes_text.replace(',', ''))
                if votes_match:
                    votes = int(votes_match.group())

            # 简介
            description = ''
            desc_elem = soup.find('span', {'data-testid': 'plot-xl'})
            if desc_elem:
                description = desc_elem.text.strip()

            # 海报
            poster = ''
            poster_elem = soup.find('img', {'data-testid': 'hero-media__poster'})
            if poster_elem:
                poster = poster_elem.get('src', '') or poster_elem.get('data-src', '')

            return {
                'title': title,
                'year': year,
                'description': description,
                'poster_url': poster,
                'score': score,
                'votes': votes,
                'url': f'{self.base_url}/title/{movie_id}/',
                'popularity': votes or 0,
            }
        except Exception as e:
            print(f"解析电影详情失败: {e}")
            return None
