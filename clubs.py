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
from clubs import *
from psycopg2.tests import dbapi20


class Clubs:
    def __init__(self, name, place, year, chair, number_of_members, rewardnumber):
        self.name = name
        self.place = place
        self.year = year
        self.chair = chair
        self.number_of_members = number_of_members
        self.rewardnumber = rewardnumber

def init_clubs_db(cursor):
    cursor.execute( """CREATE TABLE IF NOT EXISTS CLUBS (
            ID SERIAL,
            NAME VARCHAR(80) NOT NULL,
            PLACES INTEGER NOT NULL REFERENCES COUNTRIES(COUNTRY_ID) ON DELETE CASCADE ON UPDATE CASCADE,
            YEAR NUMERIC(4) NOT NULL,
            CHAIR VARCHAR(80) NOT NULL,
            NUMBER_OF_MEMBERS INTEGER NOT NULL,
            REWARDNUMBER INTEGER,
            PRIMARY KEY(ID)
            )""")


def add_club(app, request, club):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO CLUBS
        (NAME, PLACES, YEAR, CHAIR, NUMBER_OF_MEMBERS, REWARDNUMBER) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
        )""", (club.name, club.place, club.year,
                club.chair, club.number_of_members, club.rewardnumber))

        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()


def delete_club(app, id):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM CLUBS WHERE ID = %s', (id,))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def get_clubs_page(app):
    if request.method == 'GET':
        now = datetime.datetime.now()
        clubs = get_all_clubs(app)
        countries = get_country_names(app)

        return render_template('clubs.html',
                               clubs=clubs, countries=countries,
                               current_time=now.ctime())

    elif "add" in request.form:
        club = Clubs(request.form['name'],
                     request.form['place'],
                     request.form['year'],
                     request.form['chair'],
                     request.form['number_of_members'],
                     request.form['rewardnumber'])

        add_club(app, request, club)
        return redirect(url_for('clubs_page'))

    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_club(app, int(line[9:]))

        return redirect(url_for('clubs_page'))

    elif 'search' in request.form:
        clubs = search_club(app, request.form['club_to_search'])
        return render_template('clubs_search_page.html', clubs = clubs)

def get_clubs_edit_page(app,club_id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        club = get_club(app, club_id)
        countries = get_country_names(app)
        return render_template('clubs_edit_page.html', current_time=now.ctime(), club=club, countries=countries)

    if request.method == 'POST':
        club = Clubs(request.form['name'],
                     request.form['place'],
                     request.form['year'],
                     request.form['chair'],
                     request.form['number_of_members'],
                     request.form['rewardnumber'])
        update_club(app, request.form['id'], club)
        return redirect(url_for('clubs_page'))

def get_country_names(app):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES')
            countries = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return countries


def get_club(app, club_id):
    club=None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''
            SELECT C.ID, C.NAME, S.COUNTRY_NAME, C.YEAR, C.CHAIR, C.NUMBER_OF_MEMBERS, C.REWARDNUMBER
            FROM CLUBS AS C,COUNTRIES AS S
            WHERE (
                C.ID=%s AND C.PLACES=S.COUNTRY_ID
                )
            ''', club_id);
            club = cursor.fetchone()
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
        return club

def update_club(app, id, club):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            UPDATE CLUBS
            SET NAME = %s,
            PLACES = %s,
            YEAR = %s,
            CHAIR=%s,
            NUMBER_OF_MEMBERS=%s,
            REWARDNUMBER= %s
            WHERE ID= %s
            """, (club.name, club.place, club.year,
                club.chair, club.number_of_members, club.rewardnumber, id))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def get_all_clubs(app):
    clubs=None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        try:
            cursor.execute('''
            SELECT C.ID, C.NAME, K.COUNTRY_NAME, C.YEAR, C.CHAIR, C.NUMBER_OF_MEMBERS, C.REWARDNUMBER
            FROM CLUBS AS C, COUNTRIES AS K
            WHERE C.PLACES=K.COUNTRY_ID
            ''')
            clubs = cursor.fetchall()
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return clubs

def search_club(app, name):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT C.ID, C.NAME, S.COUNTRY_NAME, C.YEAR, C.CHAIR, C.NUMBER_OF_MEMBERS, C.REWARDNUMBER
            FROM CLUBS AS C , COUNTRIES AS S
            WHERE(
                UPPER(C.NAME)=UPPER(%s) AND
                C.PLACES=S.COUNTRY_ID
            )""", (name,))
            clubs = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except bapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return clubs


