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

class Match:
    def __init__(self, team1, team2, date, time, location):
        self.team1 = team1
        self.team2 = team2
        self.date = date
        self.time = time
        self.location = location

def init_fixture_db(cursor):
    query = """DROP TABLE IF EXISTS FIXTURE"""
    cursor.execute(query)
    query = """CREATE TABLE FIXTURE (
            ID SERIAL,
            TEAM1 varchar(80) NOT NULL,
            TEAM2 varchar(80) NOT NULL,
            DATE date NOT NULL,
            TIME time NOT NULL,
            LOCATION varchar(80),
            PRIMARY KEY (ID)
            )"""
    cursor.execute(query)

def add_match(cursor, request, match):
        query = """INSERT INTO FIXTURE
        (TEAM1, TEAM2, DATE, TIME, LOCATION) VALUES (
        %s,
        %s,
        to_date(%s, 'YYYY-MM-DD'),
        to_timestamp(%s, 'HH24:MI'),
        %s
        )"""
        cursor.execute(query, (match.team1, match.team2, match.date,
                                match.time, match.location))

def update_match(cursor, id, match):
    cursor.execute("""
    UPDATE FIXTURE
    SET TEAM1=%s,
        TEAM2=%s,
        DATE=to_date(%s, 'YYYY-MM-DD'),
        TIME=to_timestamp(%s, 'HH24:MI'),
        LOCATION=%s
    WHERE ID=%s
    """, (match.team1, match.team2, match.date, match.time, match.location, id))


def delete_match(cursor, id):
    query="""DELETE FROM FIXTURE WHERE ID = %s"""
    cursor.execute(query, (int(id),))

def get_fixture_page(app):
    try:
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()

        if request.method == 'GET':
            now = datetime.datetime.now()
            query = "SELECT * FROM FIXTURE"
            cursor.execute(query)

            return render_template('fixture.html', matches = cursor, current_time=now.ctime())
        elif "add" in request.form:
            match = Match(request.form['team1'],
                         request.form['team2'],
                         request.form['date'],
                         request.form['time'],
                         request.form['location'])

            add_match(cursor, request, match)

            connection.commit()
            return redirect(url_for('fixture_page'))

        elif "delete" in request.form:
            for line in request.form:
                if "checkbox" in line:
                    delete_match(cursor, int(line[9:]))
                    connection.commit()

            return redirect(url_for('fixture_page'))
    except:
        connection.rollback()
        now = datetime.datetime.now()
        return render_template('home_page', current_time=now.ctime())

def get_fixture_edit_page(app, match_id):
    if request.method == 'GET':
        match = Match
        now = datetime.datetime.now()
        try:
            connection = dbapi2.connect(app.config['dsn'])
            try:
                cursor = connection.cursor()
                cursor.execute("""
                SELECT * FROM FIXTURE WHERE (ID=%s)
                """, match_id);
                match = cursor.fetchone()

            except:
                cursor.rollback()
            finally:
                cursor.close()
        except:
            connection.rollback()
        finally:
            connection.close()
        return render_template('fixture_edit_page.html', current_time=now.ctime(), match=match)

    if request.method == 'POST':
        match = Match(request.form['team1'],
                      request.form['team2'],
                      request.form['date'],
                      request.form['time'],
                      request.form['location'])
        try:
            connection = dbapi2.connect(app.config['dsn'])
            try:
                cursor = connection.cursor()
                update_match(cursor, request.form['id'], match)
            except:
                cursor.rollback()
            finally:
                cursor.close()
        except:
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
        return redirect(url_for('fixture_page'))

