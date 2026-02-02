# 数据模型定义
from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime


@dataclass
class Movie:
    """电影数据模型"""
    id: Optional[int] = None
    title: str = ""
    year: Optional[int] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'description': self.description,
            'poster_url': self.poster_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class Review:
    """影评数据模型"""
    id: Optional[int] = None
    movie_id: int = 0
    source: str = ""
    score: Optional[float] = None
    votes: Optional[int] = None
    url: Optional[str] = None
    popularity: int = 0
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'source': self.source,
            'score': self.score,
            'votes': self.votes,
            'url': self.url,
            'popularity': self.popularity,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class MovieWithReviews:
    """带影评的电影数据模型"""
    movie: Movie
    reviews: list
    avg_score: float = 0.0
    popularity: int = 0

    def to_dict(self):
        """转换为字典"""
        scores = {}
        for review in self.reviews:
            if review.score is not None:
                scores[review.source] = review.score

        return {
            **self.movie.to_dict(),
            'scores': scores,
            'avg_score': self.avg_score,
            'popularity': self.popularity,
            'reviews': [r.to_dict() for r in self.reviews],
        }
