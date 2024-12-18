
import sqlite3
from .sql_result import SqlResult

class Hashtagnotes:
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
        query = '''INSERT INTO HashTagNotes (ContentKey, HashTag) VALUES (?, ?);'''
        return Hashtagnotes.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE HashTagNotes SET ContentKey=?, HashTag=? WHERE HashTag=? AND ContentKey=?;'''
        return Hashtagnotes.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM HashTagNotes WHERE HashTag=? AND ContentKey=?;'''
        return Hashtagnotes.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM HashTagNotes WHERE HashTag=? AND ContentKey=?;'''
        return Hashtagnotes.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM HashTagNotes;'''
        return Hashtagnotes.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM HashTagNotes LIMIT ? OFFSET ?;'''
        return Hashtagnotes.execute_query(query, params)
        
    @staticmethod
    def select_by_HashTag(params=()):
        query = '''SELECT * FROM HashTagNotes WHERE HashTag=?;'''
        return Hashtagnotes.execute_query(query, params)
        
    @staticmethod
    def delete_by_HashTag(params=()):
        query = '''DELETE FROM HashTagNotes WHERE HashTag=?;'''
        return Hashtagnotes.execute_query(query, params)
        
    @staticmethod
    def select_by_ContentKey(params=()):
        query = '''SELECT * FROM HashTagNotes WHERE ContentKey=?;'''
        return Hashtagnotes.execute_query(query, params)
        
    @staticmethod
    def delete_by_ContentKey(params=()):
        query = '''DELETE FROM HashTagNotes WHERE ContentKey=?;'''
        return Hashtagnotes.execute_query(query, params)
        
