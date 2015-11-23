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
from clubs import *
from curlers import *

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
    try:
        cursor =connection.cursor()
        try:
            cursor.execute('''
            DROP TABLE IF EXISTS CLUBS CASCADE;
            DROP TABLE IF EXISTS FIXTURE CASCADE;
            DROP TABLE IF EXISTS SPONSORS CASCADE;
            DROP TABLE IF EXISTS CHAMPIONSHIP CASCADE;
            DROP TABLE IF EXISTS CURLERS CASCADE;
            ''')
            init_clubs_db(cursor)
            init_fixture_db(cursor)
            init_sponsors_db(cursor)
            init_championships_db(cursor)
            init_curlers_db(cursor)
        except dbapi2.Error as e:
            print(e.pgerror)
            cursor.rollback()
        finally:
            cursor.close()
        ###########
    except dbapi2.Error as e:
        print(e.pgerror)
        cursor.rollback()
    finally:
        connection.commit()
        connection.close()
    return redirect(url_for('home_page'))

@app.route('/championships', methods=['GET', 'POST'])
def championships_page():
    connection = dbapi2.connect(app.config['dsn'])
    try:
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

    except:
            cursor.rollback()
            connection.rollback()
            connection.close()
    finally:
            cursor.close()
@app.route('/championships/<championship_id>', methods=['GET', 'POST'])
def championship_update_page(championship_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        query = """SELECT * FROM CHAMPIONSHIP WHERE (ID = %s)"""
        cursor.execute(query,championship_id)
        now = datetime.datetime.now()
        return render_template('championship_update.html', championship = cursor, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            print("DDD")
            championship1 = Championships(request.form['name'],
                         request.form['place'],
                         request.form['date'],
                         request.form['type'],
                         request.form['number_of_teams'],
                         request.form['reward'])

        update_championship(cursor, request.form['championship_id'], championship1)
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
        query = "SELECT CURLERID, CURLER_NAME, CURLER_SURNAME, BIRTH_DATE, TEAMID, COUNTRY, NAME FROM CURLERS, CLUBS WHERE (TEAMID = CLUBS.ID)"
        cursor.execute(query)
        curler = cursor.fetchall()
        query2 = "SELECT ID, NAME FROM clubs"
        cursor.execute(query2)
        return render_template('curlers.html', curlers = curler, clubs = cursor, current_time=now.ctime())
    elif "add" in request.form:
        curler = Curler(request.form['name'],
                     request.form['surname'],
                     request.form['birthdate'],
                     request.form['teamid'],
                     request.form['nationality'])

        add_curler(cursor, request, curler)

        connection.commit()
        return redirect(url_for('curlers_page'))

    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_curler(cursor, int(line[9:]))
                connection.commit()
        return redirect(url_for('curlers_page'))
    elif "search" in request.form:
        now = datetime.datetime.now()
        query = "SELECT CURLERID, CURLER_NAME, CURLER_SURNAME, BIRTH_DATE, TEAMID, COUNTRY, NAME FROM curlers, clubs WHERE ((TEAMID = CLUBS.ID) AND (NAME LIKE '%s' OR SURNAME = '%s'))"
        cursor.execute(query,(request.form['search_name'], request.form['search_name']));
        curler = cursor.fetchall()
        query2 = "SELECT ID,NAME FROM clubs"
        cursor.execute(query2)
        return render_template('curlers.html', curlers = curler, clubs = cursor, current_time=now.ctime())
    
@app.route('/curlers/<curler_id>', methods=['GET', 'POST'])
def curlers_update_page(curler_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        query = "SELECT * FROM CURLERS WHERE (CURLERID = %s)"
        cursor.execute(query, curler_id)
        curl = cursor.fetchall()
        query2 = "SELECT ID, NAME FROM CLUBS"
        cursor.execute(query2)
        now = datetime.datetime.now()
        return render_template('curlers_update.html', curler = curl, clubs = cursor, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            curler = Curler(request.form['name'],
                            request.form['surname'],
                            request.form['birthdate'],
                            request.form['teamid'],
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

@app.route('/sponsors/edit/<sponsor_id>',methods=['GET','POST'])
def sponsors_edit_page(sponsor_id=0):
    return get_sponsors_edit_page(app,sponsor_id);


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
