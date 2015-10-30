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
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Column, Table
from sqlalchemy import String, Date, Time, Integer
from sqlalchemy.orm import mapper

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
#    query = """DROP TABLE IF EXISTS FIXTURE"""
#    cursor.execute(query)
    #query = """CREATE TABLE FIXTURE (
#TEAM1 varchar(80) NOT NULL,
#TEAM2 varchar(80) NOT NULL,
#DATE date NOT NULL,
#TIME time NOT NULL,
#LOCATION varchar(80),
#PRIMARY KEY (DATE, TIME, LOCATION)
#)"""
#    cursor.execute(query)
###########

    fixture_table = Table('fixture', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('team1', String(80), nullable=False),
                          Column('team2', String(80), nullable=False),
                          Column('date', Date, nullable=False),
                          Column('time', Time, nullable=False),
                          Column('location', String(80), nullable = False),
                          )
    mapper(Match, fixture_table)

    metadata.create_all(bind=engine)
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
        VALUES ('"""+team1+"', '"+team2+"', to_date('"+date+"', 'DD Mon YYYY'), to_timestamp('"+time+"', 'HH24:MI'), '"+location+"')"
        cursor.execute(query)
        connection.commit()
        return redirect(url_for('fixture_page'))


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['uri'] = json.loads(VCAP_SERVICES)["elephantsql"][0]["credentials"]["uri"]
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['uri'] = "postgres://vagrant:vagrant@localhost:54321/itucsdb"
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=54321 dbname='itucsdb'"""
    engine = create_engine(app.config['uri'], echo=True)
    metadata = MetaData()
    app.run(host='0.0.0.0', port=port, debug=debug)
