# 爬虫基类
import requests
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod
import time
import random


class BaseCrawler(ABC):
    """爬虫基类"""

    def __init__(self, delay: float = 2.0):
        """
        初始化爬虫
        
        Args:
            delay: 请求延迟（秒），默认2秒
        """
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

    def _request(self, url: str, params: Optional[Dict] = None) -> Optional[requests.Response]:
        """
        发送HTTP请求
        
        Args:
            url: 请求URL
            params: 请求参数
            
        Returns:
            Response对象或None
        """
        try:
            # 添加随机延迟，避免被封
            time.sleep(self.delay + random.uniform(0, 1))
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"请求失败: {url}, 错误: {e}")
            return None

    @abstractmethod
    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        搜索电影
        
        Args:
            query: 搜索关键词
            limit: 结果数量限制
            
        Returns:
            电影数据列表
        """
        pass

    @abstractmethod
    def get_detail(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """
        获取电影详情
        
        Args:
            movie_id: 电影ID
            
        Returns:
            电影详情数据
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """获取数据源名称"""
        pass

    def normalize_movie_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化电影数据
        
        Args:
            raw_data: 原始数据
            
        Returns:
            标准化后的数据
        """
        return {
            'title': raw_data.get('title', ''),
            'year': raw_data.get('year'),
            'description': raw_data.get('description'),
            'poster_url': raw_data.get('poster_url'),
            'score': raw_data.get('score'),
            'votes': raw_data.get('votes'),
            'url': raw_data.get('url'),
            'popularity': raw_data.get('popularity', 0),
        }
