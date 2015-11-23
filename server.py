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
from championship import *
from curlers import *
from clubs import *

app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/initdb')
def initialize_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor =connection.cursor()

    init_fixture_db(app)
    init_sponsors_db(cursor)
    init_championships_db(cursor)
    init_curlers_db(cursor)
    init_clubs_db(cursor)

    #championships table creation
    query = """DROP TABLE IF EXISTS CHAMPIONSHIP"""
    cursor.execute(query)
    query = """CREATE TABLE CHAMPIONSHIP (
    ID SERIAL,
    NAME VARCHAR(80) NOT NULL,
    PLACE VARCHAR(80) NOT NULL,
    DATE DATE NOT NULL,
    TYPE VARCHAR(80) NOT NULL,
    NUMBER_OF_TEAMS INTEGER NOT NULL,
    REWARD VARCHAR(80),
    PRIMARY KEY(ID)
    )"""
    cursor.execute(query)
    ###########

    #officialcurlingclubs table creation
    query = """DROP TABLE IF EXISTS CLUBS"""
    cursor.execute(query)
    query = """CREATE TABLE CLUBS (
    ID SERIAL,
    NAME VARCHAR(80) NOT NULL,
    PLACE VARCHAR(80) NOT NULL,
    YEAR NUMERIC(4) NOT NULL,
    CHAIR VARCHAR(80) NOT NULL,
    NUMBER_OF_MEMBERS INTEGER NOT NULL,
    REWARDNUMBER INTEGER,
    PRIMARY KEY(ID)
    )"""
    cursor.execute(query)
    ###########
    connection.commit()
    return redirect(url_for('home_page'))

@app.route('/championships', methods=['GET', 'POST'])
def championships_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM CHAMPIONSHIP"
        cursor.execute(query)

        return render_template('championships.html', championship = cursor, current_time = now.ctime())
    elif "add" in request.form:
        championship1 = Championships(request.form['name'],
                     request.form['place'],
                     request.form['date'],
                     request.form['type'],
                     request.form['number_of_teams'],
                     request.form['reward'])

        add_championship(cursor, request, championship1)

        connection.commit()
        return redirect(url_for('championships_page'))

    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_championship(cursor, int(line[9:]))
                connection.commit()

        return redirect(url_for('championships_page'))

@app.route('/fixture', methods=['GET', 'POST'])
def fixture_page():
    return get_fixture_page(app)
@app.route('/fixture/edit/<match_id>', methods=['GET', 'POST'])
def fixture_edit_page(match_id=0):
    return get_fixture_edit_page(app, match_id);

@app.route('/curlers', methods=['GET', 'POST'])
def curlers_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM curlers"
        cursor.execute(query)

        return render_template('curlers.html', curlers = cursor, current_time=now.ctime())
    elif "add" in request.form:
        curler = Curler(request.form['name'],
                     request.form['surname'],
                     request.form['birthday'],
                     request.form['team'],
                     request.form['nationality'])

        add_curler(cursor, curler)

        connection.commit()
        return redirect(url_for('curlers_page'))

    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_(cursor, int(line[9:]))
                connection.commit()
        return redirect(url_for('curlers_page'))

@app.route('/curlers/<curler_id>', methods=['GET', 'POST'])
def curlers_update_page(curler_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        query = "SELECT * FROM CURLERS WHERE (ID = %s)"
        cursor.execute(query, curler_id)
        now = datetime.datetime.now()
        return render_template('curlers_update.html', curler = cursor, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            curler = Curler(request.form['name'],
                            request.form['surname'],
                            request.form['birthday'],
                            request.form['team'],
                            request.form['nationality'])
            
            update_curler(cursor, curler, request.form['curler_id'])
            connection.commit()
            return redirect(url_for('curlers_page'))
##Sema's Part - Curling Clubs
@app.route('/clubs', methods=['GET', 'POST'])
def clubs_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM CLUBS"
        cursor.execute(query)

        return render_template('clubs.html', clubs = cursor, current_time=now.ctime())
    elif "add" in request.form:
        club = Clubs(request.form['name'],
                     request.form['place'],
                     request.form['year'],
                     request.form['chair'],
                     request.form['number_of_members'],
                     request.form['rewardnumber'])

        add_club(cursor, request, club)

        connection.commit()
        return redirect(url_for('clubs_page'))
    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_club(cursor, int(line[9:]))
                connection.commit()

        return redirect(url_for('clubs_page'))

##Sponsorships arrangements by Muhammed Aziz Ulak
@app.route('/sponsors', methods=['GET', 'POST'])
def sponsors_page():
    return get_sponsors_page(app)


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
#This part is logins the infos
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=54321 dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=debug)
