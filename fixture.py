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
from gi.overrides.Gdk import Cursor

class Match:
    def __init__(self, team1, team2, date, time, location):
        self.team1 = team1
        self.team2 = team2
        self.date = date
        self.time = time
        self.location = location

def init_fixture_db(app):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS FIXTURE (
            ID SERIAL,
            TEAM1 varchar(80) NOT NULL,
            TEAM2 varchar(80) NOT NULL,
            DATE date NOT NULL,
            TIME time NOT NULL,
            LOCATION varchar(80),
            PRIMARY KEY (ID)
            )""")
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()


def add_match(app, request, match):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO FIXTURE
            (TEAM1, TEAM2, DATE, TIME, LOCATION) VALUES (
            INITCAP(%s),
            INITCAP(%s),
            to_date(%s, 'YYYY-MM-DD'),
            to_timestamp(%s, 'HH24:MI'),
            INITCAP(%s)
            )""", (match.team1, match.team2,
                   match.date,match.time,
                   match.location))

        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()


def update_match(app, id, match):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            UPDATE FIXTURE
            SET TEAM1=INITCAP(%s),
            TEAM2=INITCAP(%s),
            DATE=to_date(%s, 'YYYY-MM-DD'),
            TIME=to_timestamp(%s, 'HH24:MI'),
            LOCATION=INITCAP(%s)
            WHERE ID=%s
            """, (match.team1, match.team2,
                  match.date, match.time,
                  match.location, id))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()



def delete_match(app, id):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM FIXTURE WHERE ID = %s', (id,))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def get_match(app, match_id):
    match = None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT * FROM FIXTURE WHERE (ID=%s)', match_id);
            match = cursor.fetchone()
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return match


def search_match(app, name):
    matches = None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT * FROM FIXTURE
            WHERE (UPPER(TEAM1)=UPPER(%s) OR UPPER(TEAM2)=UPPER(%s))
            ORDER BY DATE DESC, TIME """, (name, name))
            matches = cursor.fetchall()
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return matches

def get_all_matches(app):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        try:
            cursor.execute('''
            SELECT * FROM FIXTURE
            ORDER BY DATE DESC, TIME
            ''')
            matches = cursor.fetchall()
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return matches


def get_fixture_page(app):
    if request.method == 'GET':
        now = datetime.datetime.now()
        matches = get_all_matches(app)

        return render_template('fixture.html', matches = matches, current_time=now.ctime())
    elif 'add' in request.form:
        match = Match(request.form['team1'],
                     request.form['team2'],
                     request.form['date'],
                     request.form['time'],
                     request.form['location'])
        add_match(app, request, match)
        return redirect(url_for('fixture_page'))

    elif 'delete' in request.form:
        for line in request.form:
            if 'checkbox' in line:
                delete_match(app, int(line[9:]))

        return redirect(url_for('fixture_page'))
    elif 'search' in request.form:
        matches = search_match(app, request.form['team_to_search'])
        return render_template('fixture_search_page.html', matches = matches)

def get_fixture_edit_page(app, match_id):
    if request.method == 'GET':
        match = Match
        now = datetime.datetime.now()
        match = get_match(app, match_id)
        return render_template('fixture_edit_page.html', current_time=now.ctime(), match=match)

    if request.method == 'POST':
        match = Match(request.form['team1'],
                      request.form['team2'],
                      request.form['date'],
                      request.form['time'],
                      request.form['location'])
        update_match(app, request.form['id'], match)
        return redirect(url_for('fixture_page'))

