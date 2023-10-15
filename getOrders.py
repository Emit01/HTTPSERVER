import mysql.connector as mysql
import os
import subprocess
from subprocess import CREATE_NEW_CONSOLE
import threading
import time
from datetime import datetime
import psutil
import random


def main():
    HOST = "142.44.160.158"  # or "domain.com"
    DATABASE = "upvotebi_SMM"
    USER = "upvotebi_SMM"
    PASSWORD = "Piratemule!"
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    mycursor = db_connection.cursor()
    mycursor.execute("select id,link,quantity,hashtag from orders where status in('inprogress')")
    myresult = mycursor.fetchall()
    os.remove("orders.txt")
    f = open("orders.txt", "w")
    string = ''
    for l in myresult:
        string = string + l[1] + '\n'
    f.write(string)
    f.close()

    # open and read the file after the overwriting:
    f = open("orders.txt", "r")
    print(f.read())
    db_connection.disconnect()


main()