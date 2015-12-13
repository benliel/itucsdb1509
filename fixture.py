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
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS FIXTURE (
        ID SERIAL,
        TEAM1 INTEGER NOT NULL REFERENCES CLUBS(ID) ON DELETE CASCADE ON UPDATE CASCADE,
        TEAM2 INTEGER NOT NULL REFERENCES CLUBS(ID) ON DELETE CASCADE ON UPDATE CASCADE,
        DATE DATE NOT NULL,
        TIME TIME NOT NULL,
        LOCATION INTEGER NOT NULL REFERENCES STADIUMS(ID) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (ID),
        UNIQUE(DATE,TIME,LOCATION)
        )""")
        add_test_data(cursor)

def add_test_data(cursor):
    cursor.execute("""
    insert into fixture values(
    default,
    1,
    2,
    to_date('01.01.2016','DD.MM.YYYY'),
    to_timestamp('20.00', 'HH24.MM'),
    1
    );
    """)
    cursor.execute("""
    insert into fixture values(
    default,
    3,
    4,
    to_date('01.01.2016','DD.MM.YYYY'),
    to_timestamp('20.00', 'HH24.MM'),
    2
    );
    """)
    cursor.execute("""
    insert into fixture values(
    default,
    1,
    3,
    to_date('08.01.2016','DD.MM.YYYY'),
    to_timestamp('21.00', 'HH24.MM'),
    3
    );
    """)
    cursor.execute("""
    insert into fixture values(
    default,
    2,
    4,
    to_date('08.01.2016','DD.MM.YYYY'),
    to_timestamp('21.00', 'HH24.MM'),
    4
    );
    """)
    cursor.execute("""
    insert into fixture values(
    default,
    1,
    4,
    to_date('15.01.2016','DD.MM.YYYY'),
    to_timestamp('22.00', 'HH24.MM'),
    1
    );
    """)
    cursor.execute("""
    insert into fixture values(
    default,
    2,
    3,
    to_date('15.01.2016','DD.MM.YYYY'),
    to_timestamp('22.00', 'HH24.MM'),
    2
    );
    """)






def add_match(app, request, match):
    if(match.team1 == match.team2):
        return
    if(match.team1>match.team2):
        temp = match.team1
        match.team1=match.team2
        match.team2=temp
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor = connection.cursor()
            cursor.execute("""
            SELECT * FROM FIXTURE,CLUBS AS T1,CLUBS AS T2
            WHERE(
                (%s=TEAM1 OR %s=TEAM2 OR %s=TEAM1 OR %s=TEAM2) AND
                to_date(%s, 'YYYY-MM-DD')=DATE AND
                to_timestamp(%s, 'HH24:MI')=to_timestamp(to_char(TIME, 'HH24:MI'), 'HH24:MI')
            );""", (match.team1, match.team1, match.team2, match.team2,
                    match.date, match.time))
            checkingMatch = cursor.fetchone()
            if(checkingMatch!=None):
                return
            cursor.close()
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO FIXTURE
            (TEAM1, TEAM2, DATE, TIME, LOCATION) VALUES (
            %s,
            %s,
            to_date(%s, 'YYYY-MM-DD'),
            to_timestamp(%s, 'HH24:MI'),
            %s
            )""", (match.team1, match.team2,
                   match.date,match.time,
                   match.location))

        except dbapi2.Error as e:
            print(e.pgerror)
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
            SET TEAM1=%s,
            TEAM2=%s,
            DATE=to_date(%s, 'YYYY-MM-DD'),
            TIME=to_timestamp(%s, 'HH24:MI'),
            LOCATION=%s
            WHERE ID=%s
            """, (match.team1, match.team2,
                  match.date, match.time,
                  match.location, id))
        except dbapi2.Error as e:
            print(e.pgerror)
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
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def search_match(app, name):
    matches = ()
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT F.ID, T1.NAME, T2.NAME, F.DATE, F.TIME, S.NAME
            FROM FIXTURE AS F,CLUBS AS T1, CLUBS AS T2, STADIUMS AS S
            WHERE (
                T1.ID=F.TEAM1 AND T2.ID=F.TEAM2 AND F.LOCATION=S.ID AND
                (UPPER(T1.NAME) LIKE UPPER(%s) OR UPPER(T2.NAME) LIKE UPPER(%s)))
            ORDER BY DATE DESC, TIME """, (name+"%", name+"%"))
            matches = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return matches

def get_match(app, match_id):
    match=None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''
            SELECT F.ID, T1.NAME, T2.NAME, F.DATE, F.TIME, S.NAME
            FROM FIXTURE AS F,CLUBS AS T1, CLUBS AS T2, STADIUMS AS S
            WHERE (
                F.ID=%s AND T1.ID=F.TEAM1 AND T2.ID=F.TEAM2 AND F.LOCATION=S.ID
                )
            ''', match_id);
            match = cursor.fetchone()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return match

def get_all_matches(app):
    matches = ()
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        try:
            cursor.execute('''
            SELECT F.ID, T1.NAME, T2.NAME, F.DATE, F.TIME, S.NAME
            FROM FIXTURE AS F, CLUBS AS T1, CLUBS AS T2, STADIUMS AS S
            WHERE(F.TEAM1=T1.ID AND F.TEAM2=T2.ID AND F.LOCATION=S.ID)
            ORDER BY DATE DESC, TIME
            ''')
            matches = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return matches

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

def get_stadium_names(app):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT ID,NAME FROM STADIUMS')
            stadiums = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return stadiums

def get_filtered_matches(app, stadium_id):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        try:
            cursor.execute("""
            SELECT F.ID,T1.NAME,T2.NAME,F.DATE,F.TIME,S.NAME
            FROM FIXTURE AS F,CLUBS AS T1, CLUBS AS T2, STADIUMS AS S
            WHERE(
                F.TEAM1=T1.ID AND F.TEAM2=T2.ID AND F.LOCATION=S.ID
                AND F.LOCATION=%s
            )
            ORDER BY DATE DESC, TIME
            """,stadium_id)
            print(1)
            matches=cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
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
        clubs = get_club_names(app)
        stadiums = get_stadium_names(app)

        return render_template('fixture.html', matches=matches,
                               clubs=clubs, stadiums=stadiums,
                               current_time=now.ctime())
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

def get_fixture_filter_page(app, stadium_id):
    now = datetime.datetime.now()
    matches = get_filtered_matches(app, stadium_id)
    print(matches)
    clubs = get_club_names(app)
    stadiums = get_stadium_names(app)

    return render_template('fixture.html', matches=matches,
                           clubs=clubs, stadiums=stadiums,
                           current_time=now.ctime())

def get_fixture_edit_page(app, match_id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        match = get_match(app, match_id)
        clubs = get_club_names(app)
        stadiums = get_stadium_names(app)
        return render_template('fixture_edit_page.html', current_time=now.ctime(),
                               match=match, clubs=clubs, stadiums=stadiums)

    if request.method == 'POST':
        match = Match(request.form['team1'],
                      request.form['team2'],
                      request.form['date'],
                      request.form['time'],
                      request.form['location'])
        update_match(app, request.form['id'], match)
        return redirect(url_for('fixture_page'))

