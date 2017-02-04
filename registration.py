#!/usr/bin/python

import os
import subprocess
import zbar
import MySQLdb as mdb


def register(val):
    global con, studentNum
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM attend WHERE token='%s';" % val)
        data = cur.fetchone()
        if type(data) is type(None):
            cur.execute("INSERT INTO attend (token) VALUES ('%s');" % val)
            studentNum = studentNum + 1
            print "%d - student registered with token: %s" % (studentNum, val)
        else:
            print "Token exists"

    

def mark_present(val):
    global con, studentNum
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM present WHERE token='%s';" % val)
        data = cur.fetchone()
        if type(data) is type(None):
            cur.execute("INSERT INTO present (token) VALUES ('%s');" % val)
            studentNum = studentNum + 1
            print "%d - student presented with token: %s" % (studentNum, val)
        else:
            print "This student is not registered"


def get_qr_code():
    #check for repeats
    res = ""
    while 1:
        #get image
        FNULL = open(os.devnull, 'w')
        subprocess.Popen(["fswebcam -q image.jpg"], stdout=subprocess.PIPE, stderr=FNULL, shell=True)
        p = subprocess.Popen(["zbarimg -q image.jpg"], stdout=subprocess.PIPE, stderr=FNULL, shell=True)
        data = p.communicate()[0]
        if data is None:
            continue
        data = data.split(":")
        if (len(data) == 2):
            data = data[1].split('\n')[0]
            if res != data:
                res = data
                if (registration == True):
                    register(res)
                else:
                    mark_present(res)
        


# connect to db
con = mdb.connect('localhost', 'root', 'root', 'students')

# student count
studentNum = 0

# action
registration = True


print "\n ***  Registration started  *** \n Press Ctrl-C to finish."

try:
    get_qr_code()
except KeyboardInterrupt:
    pass

print "\n ***  Registration finished  *** \n"
print "Students registered:",studentNum
print "\n"
registration = False
studentNum = 0

print " *** Presentation marking started *** \n Press Ctrl-C to finish."


try:
    get_qr_code()
except KeyboardInterrupt:
    pass

print "\n ***  Presentation marking finished  *** \n"
print "Students presented:",studentNum
print "\n"


if con:    
    con.close()
