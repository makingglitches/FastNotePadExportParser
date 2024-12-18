
import sqlite3
from .sql_result import SqlResult

class Files:
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
        query = '''INSERT INTO Files (Filename, FileSha256, Completed) VALUES (?, ?, ?);'''
        return Files.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE Files SET Filename=?, FileSha256=?, Completed=? WHERE Filename=?;'''
        return Files.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM Files WHERE Filename=?;'''
        return Files.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM Files WHERE Filename=?;'''
        return Files.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM Files;'''
        return Files.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM Files LIMIT ? OFFSET ?;'''
        return Files.execute_query(query, params)
        
