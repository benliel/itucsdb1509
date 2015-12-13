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


def init_points_db(cursor):
    cursor.execute("""
    create table if not exists points(
    id serial not null primary key,
    championship integer not null references championship(id)
    on update cascade on delete cascade,
    club integer not null references clubs(id)
    on update cascade on delete cascade,
    points integer default 0,
    wins integer default 0,
    check(points>=0),
    check(wins>=0),
    unique(championship, club)
    );
    """)

def get_points_page(app):
    if(request.method=='GET'):
        now = datetime.datetime.now()
        clubs=get_all_clubs(app)
        championships=get_all_championships(app)
        data=get_all_points_data(app)
        return render_template('points.html', data=data,
                               clubs=clubs, championships=championships,
                               current_time=now.ctime())
    elif('add' in request.form):
        add_points_data(app, request.form)
        return redirect(url_for('points_page'))
    elif('delete' in request.form):
        for line in request.form:
            if('checkbox' in line):
                delete_points_data(app, int(line[9:]))
        return redirect(url_for('points_page'))
    elif('search' in request.form):
        now = datetime.datetime.now()
        clubs=get_all_clubs(app)
        championships=get_all_championships(app)
        data=get_filtered_points_data(app, request.form['line_to_search'])
        return render_template('points.html', data=data,
                               clubs=clubs, championships=championships,
                               current_time=now.ctime())

def get_points_edit_page(app, points_id):
    if(request.method=="GET"):
        now=datetime.datetime.now()
        clubs=get_all_clubs(app)
        championships=get_all_championships(app)
        data=get_points_data(app, points_id)
        return render_template('points_edit_page.html', current_time=now.ctime(), data=data,
                               clubs=clubs, championships=championships)
    else:
        update_points_data(app, request.form)
        return redirect(url_for('points_page'))

def get_all_points_data(app):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        cursor.execute("""
        select points.id,ch.name,c.name,points,wins from points, clubs as c, championship as ch
        where(ch.id=championship AND c.id=club)
        order by championship, wins desc, points desc
        """)
        data=cursor.fetchall()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return data

def get_filtered_points_data(app, line):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        cursor.execute("""
        select points.id,ch.name,c.name,points,wins from points,clubs as c, championship as ch
        where(
            c.id=club AND ch.id=championship AND
            (UPPER(c.name) like UPPER(%s) OR UPPER(ch.name) like UPPER(%s))
        )
        order by championship, wins desc, points desc
        """, (line+'%', line+'%'))
        data=cursor.fetchall()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return data

def get_points_data(app, points_id):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        cursor.execute("""
        select p.id, ch.name, c.name, points, wins from points as p, championship as ch, clubs as c
        where(
            championship=ch.id AND club=c.id AND p.id=%s
        )
        """, (points_id,))
        data=cursor.fetchone()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return data

def get_all_clubs(app):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        cursor.execute("""
        select id,name from clubs
        """)
        data=cursor.fetchall()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return data

def get_all_championships(app):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        cursor.execute("""
        select id,name from championship
        """)
        data=cursor.fetchall()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return data

def add_points_data(app, data):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        cursor.execute("""
        insert into points(championship, club, points, wins) values(
        %s,
        %s,
        %s,
        %s
        )
        """,(data['championship'], data['club'],
             data['points'], data['wins']))
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def delete_points_data(app, id):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        cursor.execute("""
        delete from points where(id=%s);
        """, (id,))
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def update_points_data(app, data):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        cursor.execute("""
        update points
        set championship=%s,
            club=%s,
            points=%s,
            wins=%s
        where(id=%s);
        """, (data['championship'], data['club'], data['points'], data['wins'], data['id']))
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()