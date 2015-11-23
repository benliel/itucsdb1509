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

class Sponsors:
    def __init__(self, name, supportedteam, budget):
        self.name = name
        self.supportedteam = supportedteam
        self.budget = budget

def init_sponsors_db(cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS SPONSORS (
        ID SERIAL,
        NAME VARCHAR(80) NOT NULL,
        SUPPORTEDTEAM INTEGER NOT NULL REFERENCES CLUBS(ID),
        BUDGET INTEGER NOT NULL,
        PRIMARY KEY (ID)
        )""")

def add_sponsor(app, request, sponsor):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO SPONSORS
            (NAME, SUPPORTEDTEAM, BUDGET) VALUES (
            %s,
            %s,
            %s
            )""", (sponsor.name, sponsor.supportedteam,
                   sponsor.budget))

        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def delete_sponsor(app, id):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM SPONSORS WHERE ID = %s', (id,))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def search_sponsor(curser,name):
        query="""SELECT * FROM SPONSORS WHERE NAME = '%s%';"""
        curser.execute(query,name)

def get_sponsors_page(app):
    if request.method == 'GET':
        now = datetime.datetime.now()
        sponsors = get_all_sponsors(app)
        clubs = get_club_names(app)

        return render_template('sponsors.html', sponsors = sponsors,
                               clubs=clubs, current_time=now.ctime())
    elif "add" in request.form:

        sponsor = Sponsors(request.form['name'],
                     request.form['supportedteam'],
                     request.form['budget'])

        add_sponsor(app, request, sponsor)
        return redirect(url_for('sponsors_page'))
    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_sponsor(app, int(line[9:]))

        return redirect(url_for('sponsors_page'))

def get_sponsors_edit_page(app,sponsor_id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        sponsor = get_sponsor(app, sponsor_id)
        clubs = get_club_names(app)
        return render_template('sponsors_edit_page.html', current_time=now.ctime(), sponsor=sponsor, clubs=clubs)

    if request.method == 'POST':
        sponsor = Sponsors(request.form['name'],
                      request.form['supportedteam'],
                      request.form['budget'])
        update_sponsor(app, request.form['id'], sponsor)
        return redirect(url_for('sponsors_page'))

def get_club_names(app):
    clubs=None
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT ID,NAME FROM CLUBS')
            clubs = cursor.fetchall()
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
        return clubs

def get_sponsor(app, sponsor_id):
    sponsor=None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''
            SELECT S.ID, T.NAME, S.NAME, S.BUDGET
            FROM SPONSORS AS S,CLUBS AS T
            WHERE (
                S.ID=%s AND T.ID=S.SUPPORTEDTEAM
                )
            ''', sponsor_id);
            sponsor = cursor.fetchone()
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
        return sponsor

def update_sponsor(app, id, sponsor):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            UPDATE SPONSORS
            SET NAME = %s,
            SUPPORTEDTEAM = %s,
            BUDGET = %s
            WHERE ID= %s
            """, (sponsor.name, sponsor.supportedteam,
                  sponsor.budget, id))
            print("done")
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def get_all_sponsors(app):
    sponsors=None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        try:
            cursor.execute('''
            SELECT S.ID, T.NAME, S.NAME, S.BUDGET
            FROM SPONSORS AS S, CLUBS AS T
            WHERE(S.SUPPORTEDTEAM=T.ID)
            ORDER BY 1
            ''')
            sponsors = cursor.fetchall()
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return sponsors