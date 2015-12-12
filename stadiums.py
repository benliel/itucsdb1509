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

class Stadium:
    def __init__(self,name,location,capacity,ticket_cost):
        self.name=name
        self.location=location
        self.capacity=capacity
        self.ticket_cost=ticket_cost

def init_stadiums_db(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS STADIUMS(
    ID SERIAL NOT NULL,
    NAME VARCHAR(80) NOT NULL,
    LOCATION INTEGER NOT NULL REFERENCES COUNTRIES(COUNTRY_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    CAPACITY INTEGER DEFAULT -1,
    COST INTEGER DEFAULT -1,
    PRIMARY KEY(ID),
    CHECK(COST>=-1),
    CHECK(CAPACITY>=-1),
    UNIQUE(NAME,LOCATION)
    )
    """)

def get_stadiums_page(app):
    if request.method == 'GET':
        now = datetime.datetime.now()
        stadiums = get_all_stadiums(app)
        clubs = get_club_names(app)
        countries = get_country_names(app)

        return render_template('stadiums.html', stadiums=stadiums,
                               clubs=clubs, countries=countries,
                               current_time=now.ctime())
    elif 'add' in request.form:
        stadium = Stadium(request.form['name'],
                     request.form['location'],
                     request.form['capacity'],
                     request.form['ticket_cost'])
        add_stadium(app, request, stadium)
        return redirect(url_for('stadiums_page'))

    elif 'delete' in request.form:
        for line in request.form:
            if 'checkbox' in line:
                delete_stadium(app, int(line[9:]))

        return redirect(url_for('stadiums_page'))
    elif 'search' in request.form:
        stadiums = search_stadium(app, request.form['line_to_search'])
        return render_template('stadiums_search_page.html', stadiums = stadiums)

def get_stadiums_edit_page(app, stadium_id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        stadium = get_stadium(app, stadium_id)
        clubs = get_club_names(app)
        countries = get_country_names(app)
        return render_template('stadiums_edit_page.html', current_time=now.ctime(),
                               stadium=stadium, clubs=clubs, countries = countries)

    if request.method == 'POST':
        stadium = Stadium(request.form['name'],
                      request.form['location'],
                      request.form['capacity'],
                      request.form['ticket_cost'])
        update_stadium(app, request.form['id'], stadium)
        return redirect(url_for('stadiums_page'))

def get_all_stadiums(app):
    stadiums = ()
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        try:
            cursor.execute('''
            SELECT S.ID,S.NAME,C.COUNTRY_NAME,S.CAPACITY,S.COST
            FROM STADIUMS AS S,COUNTRIES AS C
            WHERE(S.LOCATION=C.COUNTRY_ID)
            ''')
            stadiums = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return stadiums

def get_club_names(app):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT ID,NAME FROM CLUBS')
            clubs = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return clubs

def get_country_names(app):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES')
            clubs = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return clubs

def get_stadium(app, id):
    stadium=()
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''
            SELECT S.ID,S.NAME,C.COUNTRY_NAME,S.CAPACITY,S.COST
            FROM STADIUMS AS S,COUNTRIES AS C
            WHERE(
            S.LOCATION=C.COUNTRY_ID AND %s=S.ID
            )
            ''', id);
            stadium = cursor.fetchone()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return stadium

def add_stadium(app, request, stadium):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            INSERT INTO STADIUMS
            (NAME, LOCATION, CAPACITY, COST) VALUES (
            %s,
            %s,
            %s,
            %s
            )""", (stadium.name, stadium.location,
                   stadium.capacity, stadium.ticket_cost))

        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def delete_stadium(app, id):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM STADIUMS WHERE ID = %s', (id,))
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def update_stadium(app, id, stadium):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            UPDATE STADIUMS
            SET NAME=%s,
            LOCATION=%s,
            CAPACITY=%s,
            COST=%s
            WHERE (ID=%s)
            """, (stadium.name, stadium.location,
                  stadium.capacity, stadium.ticket_cost, id))
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def search_stadium(app, line):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT S.ID,S.NAME,C.COUNTRY_NAME,S.CAPACITY,S.COST
            FROM STADIUMS AS S,COUNTRIES AS C
            WHERE(
                S.LOCATION=C.COUNTRY_ID AND
                (UPPER(S.NAME) LIKE UPPER(%s) OR UPPER(C.COUNTRY_NAME) LIKE UPPER(%s))
            )
            """, (line+"%", line+"%"))
            stadiums = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        connection.rollback()
    finally:
        connection.close()
        return stadiums

