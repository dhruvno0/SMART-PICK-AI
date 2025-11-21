import sqlite3
import hashlib
import json
from datetime import datetime

class Database:
    def __init__(self, db_name='smartpick.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User movie history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                movie_id INTEGER,
                movie_title TEXT,
                watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User grocery basket
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_basket (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                recipe_name TEXT,
                ingredients TEXT,
                persons INTEGER DEFAULT 4,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password):
        """Create a new user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            'SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {'id': user[0], 'username': user[1], 'email': user[2]}
        return None
    
    def add_movie_to_history(self, user_id, movie_id, movie_title):
        """Add movie to user's watch history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO user_movies (user_id, movie_id, movie_title) VALUES (?, ?, ?)',
            (user_id, movie_id, movie_title)
        )
        
        conn.commit()
        conn.close()
    
    def get_user_movie_history(self, user_id):
        """Get user's movie watch history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT movie_id, movie_title, watched_at FROM user_movies WHERE user_id = ? ORDER BY watched_at DESC',
            (user_id,)
        )
        
        movies = cursor.fetchall()
        conn.close()
        
        return [{'movie_id': m[0], 'title': m[1], 'watched_at': m[2]} for m in movies]
    
    def add_to_basket(self, user_id, recipe_name, ingredients, persons):
        """Add recipe to user's grocery basket"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        ingredients_json = json.dumps(ingredients)
        cursor.execute(
            'INSERT INTO user_basket (user_id, recipe_name, ingredients, persons) VALUES (?, ?, ?, ?)',
            (user_id, recipe_name, ingredients_json, persons)
        )
        
        conn.commit()
        conn.close()
    
    def get_user_basket(self, user_id):
        """Get user's grocery basket"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT recipe_name, ingredients, persons, added_at FROM user_basket WHERE user_id = ? ORDER BY added_at DESC',
            (user_id,)
        )
        
        basket_items = cursor.fetchall()
        conn.close()
        
        result = []
        for item in basket_items:
            result.append({
                'recipe_name': item[0],
                'ingredients': json.loads(item[1]),
                'persons': item[2],
                'added_at': item[3]
            })
        
        return result
    
    def clear_user_basket(self, user_id):
        """Clear user's grocery basket"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM user_basket WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()