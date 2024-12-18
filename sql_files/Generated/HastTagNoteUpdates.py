
import sqlite3
from .sql_result import SqlResult

class Hasttagnoteupdates:
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
        query = '''INSERT INTO HastTagNoteUpdates (Key, HashTag) VALUES (?, ?);'''
        return Hasttagnoteupdates.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE HastTagNoteUpdates SET Key=?, HashTag=? WHERE HashTag=? AND Key=?;'''
        return Hasttagnoteupdates.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM HastTagNoteUpdates WHERE HashTag=? AND Key=?;'''
        return Hasttagnoteupdates.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM HastTagNoteUpdates WHERE HashTag=? AND Key=?;'''
        return Hasttagnoteupdates.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM HastTagNoteUpdates;'''
        return Hasttagnoteupdates.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM HastTagNoteUpdates LIMIT ? OFFSET ?;'''
        return Hasttagnoteupdates.execute_query(query, params)
        
    @staticmethod
    def select_by_HashTag(params=()):
        query = '''SELECT * FROM HastTagNoteUpdates WHERE HashTag=?;'''
        return Hasttagnoteupdates.execute_query(query, params)
        
    @staticmethod
    def delete_by_HashTag(params=()):
        query = '''DELETE FROM HastTagNoteUpdates WHERE HashTag=?;'''
        return Hasttagnoteupdates.execute_query(query, params)
        
    @staticmethod
    def select_by_Key(params=()):
        query = '''SELECT * FROM HastTagNoteUpdates WHERE Key=?;'''
        return Hasttagnoteupdates.execute_query(query, params)
        
    @staticmethod
    def delete_by_Key(params=()):
        query = '''DELETE FROM HastTagNoteUpdates WHERE Key=?;'''
        return Hasttagnoteupdates.execute_query(query, params)
        
