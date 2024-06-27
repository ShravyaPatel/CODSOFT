import sqlite3

# Create database and table
conn = sqlite3.connect('todo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              description TEXT,
              priority INTEGER,
              due_date TEXT,
              completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))''')
conn.commit()
conn.close()
