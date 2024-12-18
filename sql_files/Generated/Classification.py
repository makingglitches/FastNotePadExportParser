
import sqlite3
from .sql_result import SqlResult

class Classification:
    @staticmethod
    def execute_query(query, params=()):
        try:
            conn = sqlite3.connect('your_database.db')
            cursor = conn.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall()
            conn.commit()
            return SqlResult(data=data)
        except sqlite3.Error as e:
            return SqlResult(error=str(e))
        finally:
            conn.close()
    
    @staticmethod
    def insert(params=()):
        query = '''INSERT INTO Classification (Key, ClassKey) VALUES (?, ?);'''
        return Classification.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE Classification SET Key=?, ClassKey=? WHERE ClassKey=? AND Key=?;'''
        return Classification.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM Classification WHERE ClassKey=? AND Key=?;'''
        return Classification.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM Classification WHERE ClassKey=? AND Key=?;'''
        return Classification.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM Classification;'''
        return Classification.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM Classification LIMIT ? OFFSET ?;'''
        return Classification.execute_query(query, params)
        
    @staticmethod
    def select_by_ClassKey(params=()):
        query = '''SELECT * FROM Classification WHERE ClassKey=?;'''
        return Classification.execute_query(query, params)
        
    @staticmethod
    def delete_by_ClassKey(params=()):
        query = '''DELETE FROM Classification WHERE ClassKey=?;'''
        return Classification.execute_query(query, params)
        
    @staticmethod
    def select_by_Key(params=()):
        query = '''SELECT * FROM Classification WHERE Key=?;'''
        return Classification.execute_query(query, params)
        
    @staticmethod
    def delete_by_Key(params=()):
        query = '''DELETE FROM Classification WHERE Key=?;'''
        return Classification.execute_query(query, params)
        
