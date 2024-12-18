
import sqlite3
from .sql_result import SqlResult

class Unifiedcontent:
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
        query = '''INSERT INTO UnifiedContent (Key, EpochTime, NoteLength, Sha256Sum, Folder, Starred, Reviewed, Complete, Contents, Filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        return Unifiedcontent.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE UnifiedContent SET Key=?, EpochTime=?, NoteLength=?, Sha256Sum=?, Folder=?, Starred=?, Reviewed=?, Complete=?, Contents=?, Filename=? WHERE Key=?;'''
        return Unifiedcontent.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM UnifiedContent WHERE Key=?;'''
        return Unifiedcontent.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM UnifiedContent WHERE Key=?;'''
        return Unifiedcontent.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM UnifiedContent;'''
        return Unifiedcontent.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM UnifiedContent LIMIT ? OFFSET ?;'''
        return Unifiedcontent.execute_query(query, params)
        
    @staticmethod
    def select_by_Filename(params=()):
        query = '''SELECT * FROM UnifiedContent WHERE Filename=?;'''
        return Unifiedcontent.execute_query(query, params)
        
    @staticmethod
    def delete_by_Filename(params=()):
        query = '''DELETE FROM UnifiedContent WHERE Filename=?;'''
        return Unifiedcontent.execute_query(query, params)
        
