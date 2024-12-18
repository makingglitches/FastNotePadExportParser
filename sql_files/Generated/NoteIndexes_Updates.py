
import sqlite3
from .sql_result import SqlResult

class Noteindexes_updates:
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
        query = '''INSERT INTO NoteIndexes_Updates (UpdateKey, Key, UpdateTime, EpochTime, NoteLength, Preview, Sha256Sum, Reviewed, Folder, Starred, Complete, FileName) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        return Noteindexes_updates.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE NoteIndexes_Updates SET UpdateKey=?, Key=?, UpdateTime=?, EpochTime=?, NoteLength=?, Preview=?, Sha256Sum=?, Reviewed=?, Folder=?, Starred=?, Complete=?, FileName=? WHERE UpdateKey=?;'''
        return Noteindexes_updates.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM NoteIndexes_Updates WHERE UpdateKey=?;'''
        return Noteindexes_updates.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM NoteIndexes_Updates WHERE UpdateKey=?;'''
        return Noteindexes_updates.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM NoteIndexes_Updates;'''
        return Noteindexes_updates.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM NoteIndexes_Updates LIMIT ? OFFSET ?;'''
        return Noteindexes_updates.execute_query(query, params)
        
    @staticmethod
    def select_by_FileName(params=()):
        query = '''SELECT * FROM NoteIndexes_Updates WHERE FileName=?;'''
        return Noteindexes_updates.execute_query(query, params)
        
    @staticmethod
    def delete_by_FileName(params=()):
        query = '''DELETE FROM NoteIndexes_Updates WHERE FileName=?;'''
        return Noteindexes_updates.execute_query(query, params)
        
    @staticmethod
    def select_by_Key(params=()):
        query = '''SELECT * FROM NoteIndexes_Updates WHERE Key=?;'''
        return Noteindexes_updates.execute_query(query, params)
        
    @staticmethod
    def delete_by_Key(params=()):
        query = '''DELETE FROM NoteIndexes_Updates WHERE Key=?;'''
        return Noteindexes_updates.execute_query(query, params)
        
