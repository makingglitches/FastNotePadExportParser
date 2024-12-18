
import sqlite3
from .sql_result import SqlResult

class Classlookup:
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
        query = '''INSERT INTO ClassLookup (Key, Name, Code) VALUES (?, ?, ?);'''
        return Classlookup.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE ClassLookup SET Key=?, Name=?, Code=? WHERE Key=?;'''
        return Classlookup.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM ClassLookup WHERE Key=?;'''
        return Classlookup.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM ClassLookup WHERE Key=?;'''
        return Classlookup.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM ClassLookup;'''
        return Classlookup.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM ClassLookup LIMIT ? OFFSET ?;'''
        return Classlookup.execute_query(query, params)
        
