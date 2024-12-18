
import sqlite3
from .sql_result import SqlResult

class Statistics:
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
        query = '''INSERT INTO Statistics (Key, SavedCount, KillingsCount, DruggingsCount, TheftsCount, InformedCount, FamilyKilled) VALUES (?, ?, ?, ?, ?, ?, ?);'''
        return Statistics.execute_query(query, params)
        
    @staticmethod
    def update(params=()):
        query = '''UPDATE Statistics SET Key=?, SavedCount=?, KillingsCount=?, DruggingsCount=?, TheftsCount=?, InformedCount=?, FamilyKilled=? WHERE Key=?;'''
        return Statistics.execute_query(query, params)
        
    @staticmethod
    def delete(params=()):
        query = '''DELETE FROM Statistics WHERE Key=?;'''
        return Statistics.execute_query(query, params)
        
    @staticmethod
    def select(params=()):
        query = '''SELECT * FROM Statistics WHERE Key=?;'''
        return Statistics.execute_query(query, params)
        
    @staticmethod
    def select_all(params=()):
        query = '''SELECT * FROM Statistics;'''
        return Statistics.execute_query(query, params)
        
    @staticmethod
    def select_paged(params=()):
        query = '''SELECT * FROM Statistics LIMIT ? OFFSET ?;'''
        return Statistics.execute_query(query, params)
        
    @staticmethod
    def select_by_Key(params=()):
        query = '''SELECT * FROM Statistics WHERE Key=?;'''
        return Statistics.execute_query(query, params)
        
    @staticmethod
    def delete_by_Key(params=()):
        query = '''DELETE FROM Statistics WHERE Key=?;'''
        return Statistics.execute_query(query, params)
        
