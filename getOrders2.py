import mysql.connector as mysql
import os
import subprocess
from subprocess import CREATE_NEW_CONSOLE
import threading
import time
from datetime import datetime
import psutil
import random


def updateOrderStatus(orderId, upvotes, howMany):
    HOST = "142.44.160.158"  # or "domain.com"
    DATABASE = "upvotebi_SMM"
    USER = "upvotebi_SMM"
    PASSWORD = "Piratemule!"
    if (int(howMany) == 3221225786):
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        mycursor = db_connection.cursor()
        mycursor.execute("update orders set status = 'canceled' where id in(" + str(orderId) + ")")
        db_connection.commit()
        db_connection.disconnect()

    elif (int(upvotes) <= int(howMany)):
        try:
            db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
            mycursor = db_connection.cursor()
            mycursor.execute("update orders set status = 'completed' where id in(" + orderId + ")")
            db_connection.commit()
            db_connection.disconnect()

            flag = 1
        finally:
            if (flag == 0):
                db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
                mycursor = db_connection.cursor()
                mycursor.execute("update orders set status = 'completed' where id in(" + orderId + ")")
                db_connection.commit()
                db_connection.disconnect()

    elif (int(upvotes) > howMany and howMany > 0):
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        mycursor = db_connection.cursor()
        mycursor.execute("update orders set status = 'partial' where id in(" + orderId + ")")
        mycursor.execute(
            "update orders set remains = " + (str(int(upvotes) - int(howMany)) + " where id in(" + orderId + ")"))
        db_connection.commit()
        db_connection.disconnect()


def threadFunc(orderId, link, upvotes, speed):
    HOST = "142.44.160.158"  # or "domain.com"
    DATABASE = "upvotebi_SMM"
    USER = "upvotebi_SMM"
    PASSWORD = "Piratemule!"
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    orderId = str(orderId)
    mycursor = db_connection.cursor()
    mycursor.execute("update orders set status = 'inprogress' where id in(" + orderId + ")")
    db_connection.commit()
    db_connection.disconnect()
    link = str(link)
    speed = str(speed)
    upvotes = int(upvotes)
    upvotes = str(upvotes)
    p = subprocess.Popen(["node", "index.js", '2', link, upvotes, orderId, str(speed)],
                         cwd="C:/Users/Administrator/Desktop/UPVOTE", creationflags=CREATE_NEW_CONSOLE)
    howMany2 = p.wait()
    if (int(howMany2) <= (int(upvotes) * 1.15) or howMany2 == 3221225786):
        howMany = howMany2
    print(howMany)
    print(link)
    if (int(howMany) > 2000 and int(howMany) != 3221225786):
        howMany = 0
        print(howMany)
    if (int(howMany) == 3221225786):
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        mycursor = db_connection.cursor()
        mycursor.execute("update orders set status = 'canceled' where id in(" + str(orderId) + ")")
        db_connection.commit()
        db_connection.disconnect()
    while (howMany < int(upvotes)):
        upvotes = str(int(upvotes) - (howMany))
        howMany = 0
        p = subprocess.Popen(["node", "index.js", '2', link, upvotes, orderId, str(speed)],
                             cwd="C:/Users/Administrator/Desktop/UPVOTE", creationflags=CREATE_NEW_CONSOLE)
        howMany2 = p.wait()
        if (int(howMany2) <= (int(upvotes) * 1.15) or howMany2 == 3221225786):
            howMany = howMany2
        print(link)
        if (int(howMany) > 2000 and int(howMany) != 3221225786):
            howMany = 0
            print(howMany)
        if (int(howMany) == 3221225786):
            db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
            mycursor = db_connection.cursor()
            mycursor.execute("update orders set status = 'canceled' where id in(" + str(orderId) + ")")
            db_connection.commit()
            db_connection.disconnect()
        print(int(howMany))

    updateOrderStatus(orderId, int(upvotes), howMany)
    db_connection.close()
    mycursor.reset()
    flag = 0
    db_connection.close()
    mycursor.reset()
    print(p)


def main():
    HOST = "142.44.160.158"  # or "domain.com"
    DATABASE = "upvotebi_SMM"
    USER = "upvotebi_SMM"
    PASSWORD = "Piratemule!"
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    print("Connected to:", db_connection.get_server_info())
    mycursor = db_connection.cursor()

    while (1):
        while (int(threading.active_count()) >= 16):
            flag = 0
            print('Threads:')
            print(threading.active_count())
            start = datetime.now().minute
            now = datetime.now().minute
            while (flag == 0):
                print('Pause until:' + str(start + 8))
                if (start >= 50 and now <= 10):
                    now = now + 60
                while (start > now - 8):
                    now = datetime.now().minute
                    if (start >= 50 and now <= 10):
                        now = now + 60
                flag = 1
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        mycursor = db_connection.cursor()
        mycursor.execute("select id,link,quantity,hashtag from orders where status in('pending')")
        myresult = mycursor.fetchall()
        db_connection.disconnect()
        orderLength = 0
        number = 0
        orderNumber = 0
        orderLength = len(myresult)
        if (orderLength > 10):
            orderNumber = 10
        else:
            orderNumber = len(myresult)
        while (number < orderNumber):
            print(myresult[number])
            th = threading.Thread(target=threadFunc, args=(
            myresult[number][0], myresult[number][1], float(myresult[number][2]) * 1.15, myresult[number][3]))
            th.start()
            number += 1
        temp = list(myresult)
        temp.clear()
        myresult = tuple(temp)
        mycursor.reset()
        db_connection.disconnect()
        start = datetime.now().minute
        now = datetime.now().minute
        flag = 0
        print('Threads:')
        print(threading.active_count())
        while (flag == 0):
            print('Pause until:' + str(start + 8))
            if (start >= 50 and now <= 10):
                now = now + 60
            while (start > now - 8):
                now = datetime.now().minute
                if (start >= 50 and now <= 10):
                    now = now + 60
                time.sleep(5)
            flag = 1
        print('DONE SLEEPING')

def countProcess(name):
    processlist=list()
    for process in psutil.process_iter():
        processlist.append(process.name())
    count = processlist.count(str(name))
    return count
main()




