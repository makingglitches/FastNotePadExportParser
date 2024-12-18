
import sqlite3
from .sql_result import SqlResult

class Unifiedcontentupdates:
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
        query = '''INSERT INTO UnifiedContentUpdates (UpdateKey, Key, UpdateEpoch, Contents, Sha256Sum, EpochTime, NoteLength, Reviewed, Folder, Starred, Complete, Filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        return Unifiedcontentupdates.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE UnifiedContentUpdates SET UpdateKey=?, Key=?, UpdateEpoch=?, Contents=?, Sha256Sum=?, EpochTime=?, NoteLength=?, Reviewed=?, Folder=?, Starred=?, Complete=?, Filename=? WHERE UpdateKey=?;'''
        return Unifiedcontentupdates.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM UnifiedContentUpdates WHERE UpdateKey=?;'''
        return Unifiedcontentupdates.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM UnifiedContentUpdates WHERE UpdateKey=?;'''
        return Unifiedcontentupdates.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM UnifiedContentUpdates;'''
        return Unifiedcontentupdates.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM UnifiedContentUpdates LIMIT ? OFFSET ?;'''
        return Unifiedcontentupdates.execute_query(query, params)
        
    @staticmethod
    def select_by_Filename(params=()):
        query = '''SELECT * FROM UnifiedContentUpdates WHERE Filename=?;'''
        return Unifiedcontentupdates.execute_query(query, params)
        
    @staticmethod
    def delete_by_Filename(params=()):
        query = '''DELETE FROM UnifiedContentUpdates WHERE Filename=?;'''
        return Unifiedcontentupdates.execute_query(query, params)
        
    @staticmethod
    def select_by_Key(params=()):
        query = '''SELECT * FROM UnifiedContentUpdates WHERE Key=?;'''
        return Unifiedcontentupdates.execute_query(query, params)
        
    @staticmethod
    def delete_by_Key(params=()):
        query = '''DELETE FROM UnifiedContentUpdates WHERE Key=?;'''
        return Unifiedcontentupdates.execute_query(query, params)
        
