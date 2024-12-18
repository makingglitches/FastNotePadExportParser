
import sqlite3
from .sql_result import SqlResult

class Noteindexes:
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
        query = '''INSERT INTO NoteIndexes (Key, EpochTime, NoteLength, Preview, Sha256Sum, Reviewed, Folder, Starred, Complete, Filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        return Noteindexes.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE NoteIndexes SET Key=?, EpochTime=?, NoteLength=?, Preview=?, Sha256Sum=?, Reviewed=?, Folder=?, Starred=?, Complete=?, Filename=? WHERE Key=?;'''
        return Noteindexes.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM NoteIndexes WHERE Key=?;'''
        return Noteindexes.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM NoteIndexes WHERE Key=?;'''
        return Noteindexes.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM NoteIndexes;'''
        return Noteindexes.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM NoteIndexes LIMIT ? OFFSET ?;'''
        return Noteindexes.execute_query(query, params)
        
    @staticmethod
    def select_by_Filename(params=()):
        query = '''SELECT * FROM NoteIndexes WHERE Filename=?;'''
        return Noteindexes.execute_query(query, params)
        
    @staticmethod
    def delete_by_Filename(params=()):
        query = '''DELETE FROM NoteIndexes WHERE Filename=?;'''
        return Noteindexes.execute_query(query, params)
        
