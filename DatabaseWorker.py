from datetime import datetime as dt
import sqlite3 as sql

from Constants import DB_NAME, USERS_TABLE

def set_connection(command, chat_id, **kwargs):
    connection = sql.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS {USERS_TABLE} (ID INTEGER PRIMARY KEY, Chat_id INT NOT NULL, Session_position INT,
        Last_request TEXT, Query_type TEXT, UNIQUE(Chat_id));''')

    try:
         result = globals()[command](cursor, chat_id, kwargs=kwargs)
    except Exception as ex:
        result = f'The exception is "{ex}"'
        print(result)

    connection.commit()
    connection.close()
    return result

def insert(cursor, chat_id, kwargs):
    cursor.execute(
        f'''INSERT INTO {USERS_TABLE} 
                        (Chat_id, Session_position, Last_request, Query_type) VALUES ({chat_id}, 0, 
                        '{now()}', '{kwargs.get("query_type")}');''')
    return 1

def update(cursor, chat_id, kwargs):
    if kwargs.get("query_type") is None:
        return 0
    cursor.execute(
        f'''UPDATE {USERS_TABLE} SET Last_request = '{now()}', Query_type = '{kwargs.get("query_type")}', Session_position = '{kwargs.get("session")}' WHERE Chat_id = {chat_id};''')#
    return 1

def select_session(cursor, chat_id, kwargs):

    res = cursor.execute(
        f'''SELECT Session_position, Query_type FROM {USERS_TABLE} WHERE Chat_id = {chat_id};''')
    return res.fetchone()

def now():
    return str(dt.now())


