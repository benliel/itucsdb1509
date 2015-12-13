import datetime
import time
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
from coach import *
from federations import *
from news import *
from money_balance import *
from penalty import *
from equipments import *
from points import *

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
            DROP TABLE IF EXISTS COACHES CASCADE;
            DROP TABLE IF EXISTS FEDERATIONS CASCADE;
            DROP TABLE IF EXISTS NEWS CASCADE;
            DROP TABLE IF EXISTS PENALTY CASCADE;
            DROP TABLE IF EXISTS EQUIPMENTS CASCADE;
            DROP TABLE IF EXISTS POINTS CASCADE;
            DROP TABLE IF EXISTS MONEY_BALANCE CASCADE;
            ''')
            init_countries_db(cursor)
            init_stadiums_db(cursor)
            init_clubs_db(cursor)
            init_fixture_db(cursor)
            init_sponsors_db(cursor)
            init_championships_db(cursor)
            init_curlers_db(cursor)
            init_coach_db(cursor)
            init_federations_db(cursor)
            init_news_db(cursor)
            init_money_balances_db(cursor)
            init_penalty_db(cursor)
            init_equipments_db(cursor)
            init_points_db(cursor)

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
        try:
            cursor = connection.cursor()
            if request.method == 'GET':
                query = "SELECT CH.ID,CH.NAME,C.COUNTRY_NAME,CH.DATE,CH.TYPE,CH.NUMBER_OF_TEAMS,CH.REWARD FROM CHAMPIONSHIP AS CH,COUNTRIES AS C WHERE(CH.PLACE=C.COUNTRY_ID)"
                cursor.execute(query)
                championship=cursor.fetchall()
                cursor.close()
                cursor = connection.cursor()
                cursor.execute("SELECT COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES")
                countries=cursor.fetchall()
                return render_template('championships.html', championship = championship,countries=countries, current_time = now.ctime())
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
                    print(request.form['search_name'])
                    result=search_championship(cursor, request.form['search_name'])
                    return render_template('championship_search.html', championship = result, current_time=now.ctime())
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
           ## cursor.rollback()
        connection.rollback()
       ## connection.close()
    finally:
        connection.commit()
        connection.close()

def search_championship(cursor,championship1):
    res = ()
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            query = """SELECT CH.ID,CH.NAME,C.COUNTRY_NAME,CH.DATE,CH.TYPE,CH.NUMBER_OF_TEAMS,CH.REWARD
                           FROM CHAMPIONSHIP AS CH,COUNTRIES AS C
                           WHERE(
                               (CH.PLACE=C.COUNTRY_ID) AND ((CH.NAME LIKE %s)OR(C.COUNTRY_NAME LIKE %s)))
                               """
            cursor.execute(query,('%'+championship1+'%','%'+championship1+'%'))
            res = cursor.fetchall()
            ##print(res)
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return res
@app.route('/championships/<championship_id>', methods=['GET', 'POST'])
def championship_update_page(championship_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.close()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES")
        countries=cursor.fetchall()
        query = """SELECT * FROM CHAMPIONSHIP WHERE (ID = %s)"""
        cursor.execute(query,championship_id)
        now = datetime.datetime.now()
        return render_template('championship_update.html', championship = cursor,countries=countries, current_time=now.ctime())
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
    now = datetime.datetime.now()
    if request.method == 'GET':

        query = """SELECT COUNTRY_ID,COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR
         FROM COUNTRIES GROUP BY COUNTRY_ID
         ORDER BY COUNTRY_NAME DESC """
        cursor.execute(query)

        return render_template('countries.html', countries = cursor.fetchall(), current_time=now.ctime())
    elif "add" in request.form:
        country1 = Countries(request.form['country'],
                             request.form['continent'],
                             request.form['capital'],
                             request.form['independency'])
        add_country(cursor, request,country1)
        connection.commit()
        return redirect(url_for('countries_page'))

    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_country(cursor, int(line[9:]))
                connection.commit()
        return redirect(url_for('countries_page'))
    elif "search" in request.form:
            print(request.form['search_name'])
            result=search_country(cursor, request.form['search_name'])
            return render_template('Country_search.html', countries = result, current_time=now.ctime())
def search_country(cursor,country):
    res = ()
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            print(0)
            print(country)
            query = """SELECT*
            FROM COUNTRIES WHERE((COUNTRY_NAME LIKE %s)OR (COUNTRY_CONTINENT LIKE %s))"""
            cursor.execute(query,('%'+country+'%','%'+country+'%'))
            res = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        print(res)
        return res
@app.route('/contries/<country_id>', methods=['GET', 'POST'])
def country_update_page(country_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        query = """SELECT * FROM COUNTRIES WHERE (COUNTRY_ID = %s)"""
        now = datetime.datetime.now()
        cursor.execute(query,country_id)
        country1=cursor.fetchall()
        cursor.close()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES")
        countries1=cursor.fetchall()
        return render_template('Country_update.html', countries=country1, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            country1 = Countries(request.form['name'],
                         request.form['curler'],
                         request.form['club'],
                         request.form['tournament'])

            update_country(cursor, request.form['country_id'], country1)
            connection.commit()

    return redirect(url_for('countries_page'))
@app.route('/coaches',methods=['GET', 'POST'])
def coach_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()
    if request.method == 'GET':
        query2 = "SELECT ID, NAME FROM CLUBS"
        cursor.execute(query2)
        clubs1 = cursor.fetchall()
        query = """SELECT CO.COACH_ID,CO.COACH_NAME,CO.COACH_SURNAME,CO.COACH_AGE,C.COUNTRY_NAME,CL.NAME
                           FROM COACHES AS CO,COUNTRIES AS C,CLUBS AS CL
                           WHERE(
                               (CO.COACH_COUNTRY=C.COUNTRY_ID) AND (CO.COACH_CLUB=CL.ID))
                               """
        cursor.execute(query)
        coach1=cursor.fetchall()
        cursor.close()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES")
        countries=cursor.fetchall()
        return render_template('coach.html', coach = coach1,countries=countries,clubs=clubs1, current_time=now.ctime())
    elif "add" in request.form:
        Coach1 = Coach(request.form['name'],
                         request.form['surname'],
                         request.form['age'],
                         request.form['country'],
                         request.form['club'])
        add_coach(cursor, request,Coach1)
        connection.commit()
        return redirect(url_for('coach_page'))

    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_coach(cursor, int(line[9:]))
                connection.commit()
        return redirect(url_for('coach_page'))
    elif "search" in request.form:
            print(request.form['search_name'])
            result=search_coach(cursor, request.form['search_name'])
            return render_template('coach_search.html', coach = result, current_time=now.ctime())
def search_coach(cursor,coach):
    res = ()
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            print(0)
            print(coach)
            query = """SELECT*
            FROM COACHES WHERE(COACH_NAME LIKE %s)"""
            cursor.execute(query,('%'+coach+'%',))
            res = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        print(res)
        return res
@app.route('/coaches/<coach_id>', methods=['GET', 'POST'])
def coach_update_page(coach_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        query2 = "SELECT ID, NAME FROM CLUBS"
        cursor.execute(query2)
        clubs1 = cursor.fetchall()
        cursor.close()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES")
        countries1=cursor.fetchall()
        query = """SELECT * FROM COACHES WHERE (COACH_ID = %s)"""
        now = datetime.datetime.now()
        cursor.execute(query,coach_id)
        coach1=cursor.fetchall()
        return render_template('coach_update.html', coach=coach1,countries=countries1,clubs=clubs1, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
             Coach1 = Coach(request.form['name'],
                         request.form['surname'],
                         request.form['age'],
                         request.form['country'],
                         request.form['club'])
        print(request.form['coach_id'])
        update_coach(cursor, request.form['coach_id'], Coach1)
        connection.commit()

    return redirect(url_for('coach_page'))
@app.route('/fixture', methods=['GET', 'POST'])
def fixture_page():
    return get_fixture_page(app)
@app.route('/fixture/<stadium_id>')
def fixture_filter_page(stadium_id):
    return get_fixture_filter_page(app, stadium_id)
@app.route('/fixture/edit/<match_id>', methods=['GET', 'POST'])
def fixture_edit_page(match_id=0):
    return get_fixture_edit_page(app, match_id);
@app.route('/points', methods=['GET', 'POST'])
def points_page():
    return get_points_page(app)
@app.route('/points/edit/<points_id>', methods=['GET', 'POST'])
def points_edit_page(points_id=0):
    return get_points_edit_page(app, points_id)
@app.route('/stadiums', methods=['GET', 'POST'])
def stadiums_page():
    return get_stadiums_page(app)
@app.route('/stadiums/edit/<stadium_id>', methods=['GET', 'POST'])
def stadiums_edit_page(stadium_id=0):
    return get_stadiums_edit_page(app, stadium_id);

#region ilkan engin 150120137
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
        query3 = "SELECT COUNTRY_ID, COUNTRY_NAME FROM COUNTRIES"
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
        query = "SELECT CURLERID, CURLER_NAME, CURLER_SURNAME, BIRTH_DATE, TEAMID, BIRTH_PLACE_ID,COUNTRY_NAME, NAME FROM curlers LEFT JOIN clubs ON (TEAMID = CLUBS.ID) LEFT JOIN COUNTRIES ON (BIRTH_PLACE_ID = COUNTRY_ID) WHERE (CURLER_NAME LIKE '%%' || %s || '%%' OR CURLER_SURNAME LIKE '%%' || %s || '%%')"
        cursor.execute(query,('%' + request.form['search_name'] + '%', '%' + request.form['search_name'] + '%'));
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
        federation = Federation(request.form['federation_name'],
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
        query = "SELECT FEDERATION_ID, FEDERATION_NAME, PRESIDENT_NAME, PRESIDENT_SURNAME, FOUNDING_YEAR, COUNTRY, COUNTRY_NAME FROM FEDERATIONS LEFT JOIN COUNTRIES ON COUNTRY = COUNTRY_ID WHERE ((FEDERATION_NAME LIKE '%%' || %s || '%%' OR PRESIDENT_NAME LIKE '%%' || %s || '%%' OR PRESIDENT_SURNAME LIKE '%%' || %s || '%%'))"
        cursor.execute(query,('%' + request.form['search_name'] + '%', '%' + request.form['search_name'] + '%', '%' + request.form['search_name'] + '%'));
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

@app.route('/news',methods=['GET','POST'])
def news_page():
    connection=dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT NEWS_ID, NEWS_HEADER, NEWS_DESCRIPTION,DATE, CLUBS.ID, CLUBS.NAME, CLUBS.CHAIR, CURLERS.CURLERID, CURLERS.CURLER_NAME, CURLERS.CURLER_SURNAME FROM NEWS n LEFT JOIN CLUBS ON (CLUBS.ID = n.TEAM_ID) LEFT JOIN CURLERS ON (CURLERS.CURLERID = n.CURLER_ID)"
        cursor.execute(query)
        news = cursor.fetchall()
        return render_template('news.html', news = news, current_time = now.ctime())
    elif "search" in request.form:
        now = datetime.datetime.now()
        query = """SELECT NEWS_ID, NEWS_HEADER, NEWS_DESCRIPTION,DATE, CLUBS.ID, CLUBS.NAME, CLUBS.CHAIR, CURLERS.CURLERID, CURLERS.CURLER_NAME, CURLERS.CURLER_SURNAME FROM NEWS n LEFT JOIN CLUBS ON (CLUBS.ID = n.TEAM_ID) LEFT JOIN CURLERS ON (CURLERS.CURLERID = n.CURLER_ID) WHERE (NEWS_HEADER LIKE  '%%' || %s || '%%')"""
        search = request.form['search_name']
        cursor.execute(query, ('%' + search + '%',))
        news = cursor.fetchall()
        return render_template('news.html', news = news, current_time = now.ctime())
@app.route('/newsadd',methods=['GET','POST'])
def news_add_page():
    connection=dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT CURLERID, CURLER_NAME FROM CURLERS"
        cursor.execute(query)
        curlers = cursor.fetchall()
        query2 = "SELECT ID, NAME FROM CLUBS"
        cursor.execute(query2)
        return render_template('news_add_page.html', curlers = curlers, clubs = cursor , current_time = now.ctime())
    elif request.method == 'POST':
        news = News(request.form['news_header'],
            request.form['news_description'],
            time.strftime("%Y-%m-%d"),
            request.form['team_id'],
            request.form['curler_id'])
        add_news(cursor, request, news)
        connection.commit()
        return redirect(url_for('news_page'))
    
@app.route('/news/<news_id>', methods=['GET','POST'])
def news_edit_page(news_id):
    now = datetime.datetime.now()
    connection=dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        query = "SELECT * FROM NEWS WHERE (NEWS_ID = %s)"
        cursor.execute(query, news_id)
        news = cursor.fetchall()
        query2 = "SELECT CURLERID, CURLER_NAME, CURLER_SURNAME FROM CURLERS"
        cursor.execute(query2)
        curlers = cursor.fetchall()
        query3 = "SELECT ID, NAME FROM CLUBS"
        cursor.execute(query3)
        return render_template('news_edit_page.html', news = news, curlers = curlers, clubs = cursor, current_time = now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            news = News(request.form['news_header'],
                        request.form['news_description'],
                        time.strftime("%Y-%m-%d"),
                        request.form['curler'],
                        request.form['club'])
            update_news(cursor, news, request.form['news_id'])
            connection.commit()
            return redirect(url_for('news_page'))
#end region ilkan engin 150120137

#Sema's Part - Curling Clubs
@app.route('/clubs', methods=['GET', 'POST'])
def clubs_page():
    return get_clubs_page(app)

@app.route('/clubs/edit/<club_id>',methods=['GET','POST'])
def clubs_edit_page(club_id=0):
    return get_clubs_edit_page(app,club_id);

@app.route('/clubs_money_balances', methods=['GET', 'POST'])
def money_balances_page():
    return get_money_balances_page(app)

@app.route('/clubs_money_balances/edit/<money_balance_id>',methods=['GET','POST'])
def money_balances_edit_page(money_balance_id=0):
    return get_money_balances_edit_page(app,money_balance_id);

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

##Equipment arrangements by Muhammed Aziz Ulak
@app.route('/equipments', methods=['GET', 'POST'])
def equipments_page():
    return get_equipments_page(app)

@app.route('/equipments/edit/<equipment_id>',methods=['GET','POST'])
def equipments_edit_page(equipment_id=0):
    return get_equipments_edit_page(app,equipment_id);


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
