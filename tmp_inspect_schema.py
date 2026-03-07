import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
print('Tables:', [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])
print('property_property columns:')
for r in cur.execute('PRAGMA table_info(property_property)'):
    print(r)
print('service_userevent foreign keys:')
for r in cur.execute('PRAGMA foreign_key_list(service_userevent)'):
    print(r)
conn.close()
