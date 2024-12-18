
import sqlite3
from .sql_result import SqlResult

class Notecontents_updates:
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
        query = '''INSERT INTO NoteContents_Updates (UpdateKey, Key, UpdateEpoch, Contents, ScrollInfo, Sha256Sum) VALUES (?, ?, ?, ?, ?, ?);'''
        return Notecontents_updates.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE NoteContents_Updates SET UpdateKey=?, Key=?, UpdateEpoch=?, Contents=?, ScrollInfo=?, Sha256Sum=? WHERE UpdateKey=?;'''
        return Notecontents_updates.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM NoteContents_Updates WHERE UpdateKey=?;'''
        return Notecontents_updates.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM NoteContents_Updates WHERE UpdateKey=?;'''
        return Notecontents_updates.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM NoteContents_Updates;'''
        return Notecontents_updates.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM NoteContents_Updates LIMIT ? OFFSET ?;'''
        return Notecontents_updates.execute_query(query, params)
        
    @staticmethod
    def select_by_Key(params=()):
        query = '''SELECT * FROM NoteContents_Updates WHERE Key=?;'''
        return Notecontents_updates.execute_query(query, params)
        
    @staticmethod
    def delete_by_Key(params=()):
        query = '''DELETE FROM NoteContents_Updates WHERE Key=?;'''
        return Notecontents_updates.execute_query(query, params)
        
