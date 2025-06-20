import sqlite3

def view_feedback():
    conn = sqlite3.connect('bloombyte.db')
    c = conn.cursor()
    c.execute('SELECT id, message FROM feedback')
    rows = c.fetchall()
    conn.close()

    for row in rows:
        print(f'ID: {row[0]} | Message: {row[1]}')

if __name__ == '__main__':
    view_feedback()