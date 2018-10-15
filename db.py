import sqlite3
import traceback
import datetime

TABLE = 'execution_history'

def _execute_db_query(query):
    print query
    conn = sqlite3.connect('command_tool.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()

def create_execution_history_table():
    try:
        query = '''
        CREATE TABLE IF NOT EXISTS %s (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            result TEXT NOT NULL,
            date_of_execution TEXT NOT NULL
        )''' % TABLE
        _execute_db_query(query)
    except:
        print traceback.format_exc()

def insert_command_result(cmd, result, time_now):
    try:
        query = '''
        INSERT INTO %s(command, result, date_of_execution)
        VALUES ("%s", "%s", "%s")
        ''' % (TABLE, cmd, result, time_now)
        _execute_db_query(query)
    except:
        print traceback.format_exc()


# the below main block is used only to unit test the above methods.
if __name__ == "__main__":
    print "only for testing"
    create_execution_history_table()
    time_now = datetime.datetime.now()
    insert_command_result('command-1','result-1',time_now)
    conn = sqlite3.connect('command_tool.db')
    for row in conn.execute('SELECT * FROM %s' % TABLE):
        print row
