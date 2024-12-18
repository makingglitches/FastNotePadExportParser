
import sqlite3
from .sql_result import SqlResult

class Hashtagslookup:
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
        query = '''INSERT INTO HashTagsLookup (Term) VALUES (?);'''
        return Hashtagslookup.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE HashTagsLookup SET Term=? WHERE Term=?;'''
        return Hashtagslookup.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM HashTagsLookup WHERE Term=?;'''
        return Hashtagslookup.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM HashTagsLookup WHERE Term=?;'''
        return Hashtagslookup.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM HashTagsLookup;'''
        return Hashtagslookup.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM HashTagsLookup LIMIT ? OFFSET ?;'''
        return Hashtagslookup.execute_query(query, params)
        
