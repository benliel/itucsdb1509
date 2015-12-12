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
from countries import *
from stadiums import *
from federations import *
from penalty import *

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
            DROP TABLE IF EXISTS COUNTRIES CASCADE;
            DROP TABLE IF EXISTS STADIUMS CASCADE;
            DROP TABLE IF EXISTS FEDERATIONS CASCADE;
            DROP TABLE IF EXISTS PENALTY CASCADE;
            ''')
            init_countries_db(cursor)
            init_stadiums_db(cursor)
            init_clubs_db(cursor)
            init_fixture_db(cursor)
            init_sponsors_db(cursor)
            init_championships_db(cursor)
            init_curlers_db(cursor)
            init_federations_db(cursor)
            init_penalty_db(cursor)
        except dbapi2.Error as e:
            print(e.pgerror)
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
    now = datetime.datetime.now()
    try:
        cursor = connection.cursor()
        if request.method == 'GET':
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

        elif "search" in request.form:
                result=search_championship(cursor, request.form['search_name'])
                return render_template('championship_search.html', championship = result, current_time=now.ctime())

    except:
        print("exception")
           ## cursor.rollback()
        connection.rollback()
        connection.close()
    finally:
        cursor.close()

def search_championship(cursor,championship1):
    res = None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""SELECT* FROM CHAMPIONSHIP WHERE ((NAME LIKE %s) OR (PLACE LIKE %s))""",('%'+championship1+'%','%'+championship1+'%',))
            res = cursor.fetchall()
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return res
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
            championship1 = Championships(request.form['name'],
                         request.form['place'],
                         request.form['date'],
                         request.form['type'],
                         request.form['number_of_teams'],
                         request.form['reward'])

        update_championship(cursor, request.form['championship_id'], championship1)
        connection.commit()
    return redirect(url_for('championships_page'))
@app.route('/countries',methods=['GET', 'POST'])
def countries_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT DISTINCT ON(COUNTRY_NAME)COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES"
        cursor.execute(query)

        return render_template('countries.html', countries = cursor, current_time=now.ctime())
    elif "add" in request.form:
        country1 = Countries(request.form['country'])
        add_country(cursor, request,country1)
        connection.commit()
        return redirect(url_for('countries_page'))

    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_country(cursor, int(line[9:]))
                connection.commit()
        return redirect(url_for('countries_page'))


@app.route('/fixture', methods=['GET', 'POST'])
def fixture_page():
    return get_fixture_page(app)
@app.route('/fixture/<stadium_id>')
def fixture_filter_page(stadium_id):
    return get_fixture_filter_page(app, stadium_id)
@app.route('/fixture/edit/<match_id>', methods=['GET', 'POST'])
def fixture_edit_page(match_id=0):
    return get_fixture_edit_page(app, match_id);
@app.route('/stadiums', methods=['GET', 'POST'])
def stadiums_page():
    return get_stadiums_page(app)
@app.route('/stadiums/edit/<stadium_id>', methods=['GET', 'POST'])
def stadiums_edit_page(stadium_id=0):
    return get_stadiums_edit_page(app, stadium_id);

@app.route('/curlers', methods=['GET', 'POST'])
def curlers_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT CURLERID, CURLER_NAME, CURLER_SURNAME, BIRTH_DATE, TEAMID, BIRTH_PLACE_ID, NAME, COUNTRY_NAME FROM CURLERS, CLUBS, COUNTRIES WHERE (TEAMID = CLUBS.ID AND BIRTH_PLACE_ID = COUNTRIES.COUNTRY_ID)"
        cursor.execute(query)
        curler = cursor.fetchall()
        query2 = "SELECT ID, NAME FROM clubs"
        cursor.execute(query2)
        _clubs = cursor.fetchall()
        query3 = "SELECT * FROM COUNTRIES"
        cursor.execute(query3)
        return render_template('curlers.html', curlers = curler, clubs = _clubs, countries = cursor, current_time=now.ctime())
    elif "add" in request.form:
        curler = Curler(request.form['name'],
                     request.form['surname'],
                     request.form['birthdate'],
                     request.form['teamid'],
                     request.form['birth_place'])

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
        query = "SELECT CURLERID, CURLER_NAME, CURLER_SURNAME, BIRTH_DATE, TEAMID, COUNTRY, NAME FROM curlers, clubs WHERE ((TEAMID = CLUBS.ID) AND (CURLER_NAME LIKE %s OR CURLER_SURNAME = %s))"
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
        teams = cursor.fetchall()
        query3 = "SELECT COUNTRY_ID, COUNTRY_NAME FROM COUNTRIES"
        cursor.execute(query3)
        now = datetime.datetime.now()
        return render_template('curlers_update.html', curler = curl, clubs = teams, countries = cursor, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            curler = Curler(request.form['name'],
                            request.form['surname'],
                            request.form['birthdate'],
                            request.form['teamid'],
                            request.form['birth_place_id'])
            update_curler(cursor, curler, request.form['curler_id'])
            connection.commit()
            return redirect(url_for('curlers_page'))

@app.route('/federations', methods=['GET', 'POST'])
def federations_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT FEDERATION_ID, FEDERATION_NAME, PRESIDENT_NAME, PRESIDENT_SURNAME, FOUNDING_YEAR, COUNTRY, COUNTRY_NAME FROM FEDERATIONS, COUNTRIES WHERE (COUNTRY = COUNTRY_ID)"
        cursor.execute(query)
        federation = cursor.fetchall()
        query2 = "SELECT COUNTRY_ID, COUNTRY_NAME FROM COUNTRIES"
        cursor.execute(query2)
        _countries = cursor.fetchall()
        return render_template('federations.html', federations = federation, countries = _countries, current_time=now.ctime())
    elif "add" in request.form:
        federation = Federation(
                     request.form['federation_name'],
                     request.form['president_name'],
                     request.form['president_surname'],
                     request.form['founding_year'],
                     request.form['country_id'])

        add_federation(cursor, request, federation)

        connection.commit()
        return redirect(url_for('federations_page'))

    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_federation(cursor, line[9:])
                connection.commit()
        return redirect(url_for('federations_page'))
    elif "search" in request.form:
        now = datetime.datetime.now()
        query = "SELECT FEDERATION_ID, FEDERATION_NAME, PRESIDENT_NAME, PRESIDENT_SURNAME, FOUNDING_YEAR, COUNTRY, COUNTRY_NAME FROM FEDERATIONS, COUNTRIES WHERE (COUNTRY = COUNTRY_ID AND (FEDERATION_NAME LIKE %s OR PRESIDENT_NAME LIKE %s OR PRESIDENT_SURNAME = %s))"
        cursor.execute(query,(request.form['search_name'], request.form['search_name'], request.form['search_name']));
        federation = cursor.fetchall()
        query2 = "SELECT COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES"
        cursor.execute(query2)
        return render_template('federations.html', federations = federation, countries = cursor, current_time=now.ctime())

@app.route('/federations/<federation_id>', methods=['GET', 'POST'])
def federations_update_page(federation_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        query = "SELECT * FROM FEDERATIONS WHERE (FEDERATION_ID = %s)"
        cursor.execute(query, federation_id)
        fed = cursor.fetchall()
        query2 = "SELECT COUNTRY_ID, COUNTRY_NAME FROM COUNTRIES"
        cursor.execute(query2)
        now = datetime.datetime.now()
        return render_template('federations_update.html', federation = fed, countries = cursor, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            federation = Federation(request.form['federation_name'],
                            request.form['president_name'],
                            request.form['president_surname'],
                            request.form['founding_year'],
                            request.form['country_id'])
            update_federation(cursor, federation, request.form['federation_id'])
            connection.commit()
            return redirect(url_for('federations_page'))

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

##Penalty arrangements by Muhammed Aziz Ulak
@app.route('/penalty', methods=['GET', 'POST'])
def penalty_page():
    return get_penalty_page(app)

@app.route('/penalty/edit/<penalty_id>',methods=['GET','POST'])
def penalty_edit_page(penalty_id=0):
    return get_penalty_edit_page(app,penalty_id);


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
