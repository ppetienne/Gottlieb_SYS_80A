from Contacts import conn
import time

while True:
    conn.J4['S'].set_level(0)
    time.sleep(0.1)
    conn.J4['S'].set_level(1)
    time.sleep(0.1)
    