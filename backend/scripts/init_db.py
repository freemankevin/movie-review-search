# 初始化数据库脚本
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database


def main():
    """主函数"""
    print("正在初始化数据库...")

    # 创建数据库
    db_path = os.getenv('DATABASE', 'movies.db')
    db = Database(db_path)

    print(f"数据库已创建: {db_path}")
    print("数据库初始化完成！")


if __name__ == '__main__':
    main()
