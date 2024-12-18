
import sqlite3
from .sql_result import SqlResult

class Notecontents:
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
        query = '''INSERT INTO NoteContents (Key, Contents, ScrollInfo, Sha256Sum) VALUES (?, ?, ?, ?);'''
        return Notecontents.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE NoteContents SET Key=?, Contents=?, ScrollInfo=?, Sha256Sum=? WHERE Key=?;'''
        return Notecontents.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM NoteContents WHERE Key=?;'''
        return Notecontents.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM NoteContents WHERE Key=?;'''
        return Notecontents.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM NoteContents;'''
        return Notecontents.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM NoteContents LIMIT ? OFFSET ?;'''
        return Notecontents.execute_query(query, params)
        
