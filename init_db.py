import sqlite3


def init_db():
    conn = sqlite3.connect('database.db')  # 创建数据库文件
    cursor = conn.cursor()

    # 创建表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interview_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            lable TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
