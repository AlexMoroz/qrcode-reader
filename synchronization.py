#!/usr/bin/python

import json
import requests
import MySQLdb as mdb


def do_request(url, data, token):
    api = "http://automatedattendancetracker.appspot.com/api"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    if token is not None:
        headers['Authorization'] = "Bearer %s" % token
    r = requests.post(api+url, data=data, headers=headers)
    if r.text == "":
        return r.status_code, ""
    else:    
        return r.status_code, json.loads(r.text)


print "Please, login to your tutor account to send the data to the server:"
email = raw_input("Email -> ")
password = raw_input("Password -> ")

#authenticate
if(email != "" and password != ""):
    status,response = do_request("/authenticate", "email=%s&password=%s" % (email, password), None)
    if status == requests.codes.unauthorized or str(response['type']) != "tutor":
        print "Wrong email ro password."
        exit()
    session_id = str(response['token'])
else:
    print "Empty fields, login is not possible"
    exit()

# connect to db
con = mdb.connect('localhost', 'root', 'root', 'students')

#get number of rows in table
with con:
    cur = con.cursor()
    cur.execute("select (select count(*) from attend)+(select count(*) from present) from dual;")
    rows_num = cur.fetchall()
    if rows_num[0][0] == 0:
        print "No data to send."
        exit()


print "\n Sending data ... %d rows ... please wait ... " % rows_num[0][0]

#get number of rows in attend
with con:
    cur = con.cursor()
    cur.execute("select * from attend;")
    rows = cur.fetchall()


for row in rows:
    #send registered
    url = "/confirm/attendance"
    data = "code=%s" % row[0]
    status, response = do_request(url, data, session_id)
    if status == requests.codes.not_found:
        print "Code %s was not recognized on server." % row[0]
        break

    #delete from database
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM attend WHERE token='%s'" % row[0])

#get number of rows in attend
with con:
    cur = con.cursor()
    cur.execute("select * from present;")
    rows = cur.fetchall()


for row in rows:
    #mark presentation
    url = "/confirm/presentation"
    data = "code=%s" % row[0]
    status, response = do_request(url, data, session_id)
    if status == requests.codes.not_found:
        print "Code %s was not recognized on server." % row[0]
        break

    #delete from database
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM present WHERE token='%s'" % row[0])
        

print "*** Data successfully sent ***"

if con:    
    con.close()
