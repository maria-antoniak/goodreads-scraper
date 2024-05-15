import sqlite3

def create_database(db_path):
    db_path=db_path + '/book_reviews.db'
    conn = sqlite3.connect(db_path)
    
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS book_reviews (
                 book_id TEXT,
                 reviewer_id TEXT,
                 reviewer_name TEXT,
                 likes_on_review TEXT,
                 review_content TEXT,
                 reviewer_followers TEXT,
                 reviewer_total_reviews TEXT,
                 review_date TEXT,
                 review_rating TEXT
                 )''')
    conn.commit()
    conn.close()

def insert_review(conn, review_info):
    c = conn.cursor()
    c.execute('''INSERT INTO book_reviews (book_id, reviewer_id, reviewer_name, likes_on_review, review_content, reviewer_followers, reviewer_total_reviews, review_date, review_rating)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                 review_info['book_id'],
                 review_info['reviewer_id'],
                 review_info['reviewer_name'],
                 review_info['likes_on_review'],
                 review_info['review_content'],
                 review_info['reviewer_followers'],
                 review_info['reviewer_total_reviews'],
                 review_info['review_date'],
                 review_info['review_rating']
                 ))
    conn.commit()


