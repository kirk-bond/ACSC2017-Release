#!/usr/bin/env python

import sqlite3
import os
import hashlib

def main():
    create_db()
    user_query()

#Initialize the database connection and populate the contents
def create_db():
    conn = sqlite3.connect('/home/flag/users.db')
    cur = conn.cursor()
    cur.executescript('''
	DROP TABLE IF EXISTS users;
        CREATE table users(username TEXT,salt TEXT,password TEXT)

	''')
    with open('names.txt') as f:
	for name in f:
	    name = name.strip()
	    password = name.split("@")
	    password = password[0][::-1]
	    salt = (str(ord(name[3:4])) + str(ord(name[1:2])))
	    #print salt, password
	    hashpassword = hashlib.sha256(password + salt)
	    cur.execute("INSERT INTO users (username,salt,password) values (?,?,?)", (name,salt,hashpassword.hexdigest()))

    conn.commit()
    conn.close()

#Takes user input and queries the database
def user_query():
    userq = ''
    while userq.lower() != 'quit':
        try:
	    userq = raw_input("Enter your SQL query, type quit to stop \n")
	    userq = userq.strip()
	    conn = sqlite3.connect('/home/flag/users.db')
	    conn.text_factory = str
	    cur = conn.cursor()
	    results = cur.execute(userq)
	    print cur.fetchall()
	except (sqlite3.Error, KeyboardInterrupt, EOFError) as e:
	    print 'You broke it'
    conn.close()



#prints out the database for troubleshooting
def print_db():
    conn = sqlite3.connect('/home/flag/users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    conn.close()







if __name__ == '__main__':
    main()


