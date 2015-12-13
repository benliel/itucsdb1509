import datetime
import os
import json
import re
import psycopg2 as dbapi2

from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
from flask.helpers import url_for
from store import Store
from fixture import *
from sponsors import *
from curlers import *
from psycopg2.tests import dbapi20

class Penalty:
    def __init__(self, personname, startdate, enddate, type):
        self.personname = personname
        self.startdate = startdate
        self.enddate = enddate
        self.type = type

def init_penalty_db(cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS PENALTY (
        ID SERIAL,
        PERSONNAME INTEGER NOT NULL REFERENCES CURLERS(CURLERID) ON DELETE CASCADE ON UPDATE CASCADE,
        STARTDATE VARCHAR(20) NOT NULL,
        ENDDATE VARCHAR(20) NOT NULL,
        TYPE  VARCHAR(20) NOT NULL,
        PRIMARY KEY (ID)
        )""")

def add_penalty(app, request, penalty):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO PENALTY
            (PERSONNAME, STARTDATE, ENDDATE, TYPE) VALUES (
            %s,
            %s,
            %s,
            %s
            )""", (penalty.personname, penalty.startdate,
                   penalty.enddate , penalty.type))

        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
    finally:
        connection.commit()
        connection.close()

def delete_penalty(app, id):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM PENALTY WHERE ID = %s', (id,))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()


def get_penalty_page(app):
    if request.method == 'GET':
        now = datetime.datetime.now()
        penalties = get_all_penalties(app)
        curlers = get_curlers_names(app)

        return render_template('penalty.html', penalties = penalties,
                               curlers=curlers, current_time=now.ctime())
    elif "add" in request.form:
        print(request.form)
        penalty = Penalty(request.form['personname'],
                     request.form['startdate'],
                     request.form['enddate'],
                     request.form['type'])

        add_penalty(app, request, penalty)
        return redirect(url_for('penalty_page'))
    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_penalty(app, int(line[9:]))

        return redirect(url_for('penalty_page'))
    elif 'search' in request.form:
        penalties = search_penalty(app, request.form['penalty_to_search'])
        return render_template('penalty_search_page.html', penalties = penalties)


def get_penalty_edit_page(app,penalty_id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        penalty = get_penalty(app, penalty_id)
        curlers = get_curlers_names(app)
        return render_template('penalty_edit_page.html', current_time=now.ctime(), penalty=penalty, curlers=curlers)

    if request.method == 'POST':
        penalty = Penalty(request.form['personname'],
                      request.form['startdate'],
                      request.form['enddate'],
                      request.form['type'])
        update_penalty(app, request.form['id'], penalty)
        return redirect(url_for('penalty_page'))

def get_curlers_names(app):
    curlers=None
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT CURLERID,CURLER_NAME FROM CURLERS')
            curlers = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
            cursor.rollback()
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return curlers

def get_penalty(app, penalty_id):
    penalty=None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''
            SELECT P.ID, C.CURLER_NAME, P.STARTDATE, P.ENDDATE , P.TYPE
            FROM PENALTY AS P,CURLERS AS C
            WHERE (
                P.ID=%s AND C.CURLERID=P.PERSONNAME
                )
            ''', penalty_id);
            penalty = cursor.fetchone()
        except dbapi2.Error as e:
            print(e.pgerror)
            cursor.rollback()
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return penalty

def update_penalty(app, id, penalty):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            UPDATE PENALTY
            SET PERSONNAME = %s,
            STARTDATE = %s,
            ENDDATE = %s,
            TYPE = %s
            WHERE ID= %s
            """, (penalty.personname, penalty.startdate,
                  penalty.enddate,penalty.type, id))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def get_all_penalties(app):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        try:
            cursor.execute('''
            SELECT P.ID, C.CURLER_NAME, P.STARTDATE, P.ENDDATE, P.TYPE
            FROM PENALTY AS P, CURLERS AS C
            WHERE(P.PERSONNAME=C.CURLERID)
            ORDER BY 1
            ''')
            penalties = cursor.fetchall()
            print(penalties)
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return penalties

def search_penalty(app, name):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT P.ID, C.CURLER_NAME, P.STARTDATE, P.ENDDATE , P.TYPE
            FROM PENALTY AS P, CURLERS AS C
            WHERE(
                UPPER(C.CURLER_NAME)=UPPER(%s) AND
                P.PERSONNAME=C.CURLERID
            )""", (name,))
            penalties = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
            cursor.rollback()
        finally:
            cursor.close()
    except bapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return penalties
