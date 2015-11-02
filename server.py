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
from match import Match
from store import Store

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

    query = """DROP TABLE IF EXISTS COUNTER"""
    cursor.execute(query)
    query = """CREATE TABLE COUNTER (N INTEGER)"""
    cursor.execute(query)
    query = """INSERT INTO COUNTER(N) VALUES(0)"""
    cursor.execute(query)

    #fixture table creation
    query = """DROP TABLE IF EXISTS FIXTURE"""
    cursor.execute(query)
    query = """CREATE TABLE FIXTURE (
TEAM1 varchar(80) NOT NULL,
TEAM2 varchar(80) NOT NULL,
DATE date NOT NULL,
TIME time NOT NULL,
LOCATION varchar(80),
PRIMARY KEY (DATE, TIME, LOCATION)
)"""
    cursor.execute(query)
###########

#Sponsorship table creation
    query = """DROP TABLE IF EXISTS SPONSORS"""
    cursor.execute(query)
    query = """CREATE TABLE SPONSORS (
ID SERIAL,
NAME VARCHAR(80) NOT NULL,
SUPPORTEDTEAM VARCHAR(80) NOT NULL,
BUDGET INTEGER NOT NULL,
PRIMARY KEY (ID)
)"""
    cursor.execute(query)
###########

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
    query = """DROP TABLE IF EXISTS OFFICIALCURLINGCLUBS"""
    cursor.execute(query)
    query = """CREATE TABLE OFFICIALCURLINGCLUBS (
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

@app.route('/count')
def counter_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    query = "UPDATE COUNTER SET N = N + 1"
    cursor.execute(query)
    connection.commit()

    query = "SELECT N FROM COUNTER"
    cursor.execute(query)
    count = cursor.fetchone()[0]

    return "This page was accesed %d times." % count


@app.route('/movies')
def movies_page():
    now = datetime.datetime.now()
    return render_template('movies.html', current_time=now.ctime())

@app.route('/championships', methods=['GET', 'POST'])
def championships_page():
    now = datetime.datetime.now()
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        query = """SELECT * FROM CHAMPIONSHIP"""
        cursor.execute(query)

        return render_template('championships.html', championships = cursor, current_time = now.ctime())
    else:
        name =request.form['name']
        place =request.form['place']
        date =request.form['date']
        type =request.form['type']
        teamNumber =request.form['number_of_teams']
        reward =request.form['reward']

        query = """INSERT INTO CHAMPIONSHIP(NAME, PLACE, DATE, TYPE, NUMBER_OF_TEAMS, REWARD) VALUES (
        '"""+ name +"""',
        '"""+ place +"""',
        to_date('"""+date+"""', 'DD.MM.YYYY'),
        '"""+ type +"""',
        """+ teamNumber +""",
        '"""+ reward+"')"
        cursor.execute(query)

        connection.commit()
        return redirect(url_for('championships_page'))

@app.route('/fixture', methods=['GET', 'POST'])
def fixture_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM FIXTURE"
        cursor.execute(query)

        return render_template('fixture.html', matches = cursor, current_time=now.ctime())
    else:
        team1 = request.form['team1']
        team2 = request.form['team2']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        query = """INSERT INTO FIXTURE (TEAM1, TEAM2, DATE, TIME, LOCATION)
        VALUES ('"""+team1+"', '"+team2+"', to_date('"+date+"', 'DD.MM.YYYY'), to_timestamp('"+time+"', 'HH24:MI'), '"+location+"')"
        cursor.execute(query)
        connection.commit()
        return redirect(url_for('fixture_page'))

##Sema's Part - Curling Clubs
@app.route('/clubs', methods=['GET', 'POST'])
def clubs_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM OFFICIALCURLINGCLUBS"
        cursor.execute(query)

        return render_template('clubs.html', clubs = cursor, current_time=now.ctime())
    else:
        name = request.form['name']
        place = request.form['place']
        year = request.form['year']
        chair = request.form['chair']
        number_of_members = request.form['number_of_members']
        reward_number = request.form['reward_number']
        query = """INSERT INTO OFFICIALCURLINGCLUBS (NAME, PLACE, YEAR, CHAIR, NUMBER_OF_MEMBERS,REWARDNUMBER)
        VALUES ('"""+name+"', '"+place+"', '"+year+"' , '"+chair+"', '"+number_of_members+"', '"+reward_number+"')"
        cursor.execute(query)
        connection.commit()
        return redirect(url_for('clubs_page'))


##Sponsorships arrangements by Muhammed Aziz Ulak
@app.route('/sponsors', methods=['GET', 'POST'])
def sponsors_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM SPONSORS"
        cursor.execute(query)

        return render_template('sponsors.html', sponsors = cursor, current_time=now.ctime())
    else:
        name = request.form['name']
        supportedteam = request.form['supportedteam']
        budget = request.form['budget']
        query = """INSERT INTO SPONSORS (name, supportedteam, budget)
        VALUES ('"""+name+"', '"+supportedteam+"', '"+budget+"')"
        cursor.execute(query)
        connection.commit()
        return redirect(url_for('sponsors_page'))


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
