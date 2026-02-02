# 工具函数
from typing import List, Optional
from datetime import datetime


def format_date(date_obj: Optional[datetime], format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    格式化日期
    
    Args:
        date_obj: 日期对象
        format_str: 格式字符串
        
    Returns:
        格式化后的日期字符串
    """
    if not date_obj:
        return ''
    return date_obj.strftime(format_str)


def calculate_avg_score(scores: List[Optional[float]]) -> float:
    """
    计算平均评分
    
    Args:
        scores: 评分列表
        
    Returns:
        平均评分
    """
    valid_scores = [s for s in scores if s is not None]
    if not valid_scores:
        return 0.0
    return sum(valid_scores) / len(valid_scores)


def normalize_score(score: Optional[float], max_score: float = 10.0) -> float:
    """
    标准化评分到指定范围
    
    Args:
        score: 原始评分
        max_score: 最大评分
        
    Returns:
        标准化后的评分
    """
    if score is None:
        return 0.0
    return min(score, max_score) / max_score * 10.0


def clean_text(text: Optional[str]) -> str:
    """
    清理文本，去除多余空格和特殊字符
    
    Args:
        text: 原始文本
        
    Returns:
        清理后的文本
    """
    if not text:
        return ''
    return ' '.join(text.strip().split())


def extract_year(text: Optional[str]) -> Optional[int]:
    """
    从文本中提取年份
    
    Args:
        text: 包含年份的文本
        
    Returns:
        提取的年份
    """
    if not text:
        return None
    
    import re
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    if year_match:
        return int(year_match.group())
    return None
