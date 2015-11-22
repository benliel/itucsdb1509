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

class Sponsors:
    def __init__(self, name, supportedteam, budget):
        self.name = name
        self.supportedteam = supportedteam
        self.budget = budget

def init_sponsors_db(cursor):
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

def add_sponsor(cursor, request, sponsor):
        query = """INSERT INTO SPONSORS
        (NAME, SUPPORTEDTEAM, BUDGET) VALUES (
        %s,
        %s,
        %s
        )"""
        cursor.execute(query, (sponsor.name, sponsor.supportedteam, sponsor.budget))

def delete_sponsor(cursor, id):
        query="""DELETE FROM SPONSORS WHERE ID = %s"""
        cursor.execute(query, (int(id),))

def update_sponsor(curser, id, name, supportedteam, budget):
        query="""UPDATE SPONSORS
        SET NAME = '%s' , SUPPORTEDTEAM = '%s', BUDGET = %s
        WHERE ID = %s;"""
        cursor.execute(query, (name,supportedteam,int(budget),int(id)))
def search_sponsor(curser,name):
        query="""SELECT * FROM SPONSORS WHERE NAME = '%s%';"""
        curser.execute(query,name)
def get_sponsors_page(app):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM SPONSORS"
        cursor.execute(query)

        return render_template('sponsors.html', sponsors = cursor, current_time=now.ctime())
    elif "add" in request.form:
        sponsor = Sponsors(request.form['name'],
                     request.form['supportedteam'],
                     request.form['budget'])

        add_sponsor(cursor, request, sponsor)

        connection.commit()
        return redirect(url_for('sponsors_page'))
    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_sponsor(cursor, int(line[9:]))
                connection.commit()

        return redirect(url_for('sponsors_page'))


