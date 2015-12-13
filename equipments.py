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
from psycopg2.tests import dbapi20

class Equipments:
    def __init__(self, name, manufacturer, price , country):
        self.name = name
        self.manufacturer = manufacturer
        self.price = price
        self.country = country

def init_equipments_db(cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS EQUIPMENTS (
        ID SERIAL,
        NAME VARCHAR(80) NOT NULL,
        MANUFACTURER VARCHAR(80) NOT NULL,
        PRICE INTEGER NOT NULL,
        COUNTRY INTEGER NOT NULL REFERENCES COUNTRIES(COUNTRY_ID) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (ID)
        )""")
        fill_table(cursor)

def add_equipment(app, request, equipment):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO EQUIPMENTS
            (NAME, MANUFACTURER, PRICE, COUNTRY) VALUES (
            %s,
            %s,
            %s,
            %s
            )""", (equipment.name, equipment.manufacturer,
                   equipment.price, equipment.country))

        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def delete_equipment(app, id):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM EQUIPMENTS WHERE ID = %s', (id,))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()


def get_equipments_page(app):
    if request.method == 'GET':
        now = datetime.datetime.now()
        equipments = get_all_equipments(app)
        countries = get_country_names(app)

        return render_template('equipments.html', equipments = equipments,
                               countries=countries, current_time=now.ctime())
    elif "add" in request.form:

        equipment = Equipments(request.form['name'],
                     request.form['manufacturer'],
                     request.form['price'],
                     request.form['country'])

        add_equipment(app, request, equipment)
        return redirect(url_for('equipments_page'))
    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_equipment(app, int(line[9:]))

        return redirect(url_for('equipments_page'))
    elif 'search' in request.form:
        equipments = search_equipment(app, request.form['equipment_to_search'])
        return render_template('equipments_search_page.html', equipments = equipments)


def get_equipments_edit_page(app,equipment_id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        equipment = get_equipment(app, equipment_id)
        countries = get_country_names(app)
        return render_template('equipments_edit_page.html', current_time=now.ctime(), equipment=equipment, countries=countries)

    if request.method == 'POST':
        equipment = Equipments(request.form['name'],
                      request.form['manufacturer'],
                      request.form['price'],
                      request.form['country'])
        update_equipment(app, request.form['id'], equipment)
        return redirect(url_for('equipments_page'))

def get_country_names(app):
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT COUNTRY_ID,COUNTRY_NAME FROM COUNTRIES')
            country = cursor.fetchall()
            print(country)
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return country

def get_equipment(app, equipment_id):
    equipment=None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''
            SELECT E.ID, E.NAME, E.MANUFACTURER , E.PRICE, C.COUNTRY_NAME
            FROM EQUIPMENTS AS E,COUNTRIES AS C
            WHERE (
                E.ID=%s AND C.COUNTRY_ID=E.COUNTRY
                )
            ''', equipment_id);
            equipment = cursor.fetchone()
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
        return equipment

def update_equipment(app, id, equipment):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            UPDATE EQUIPMENTS
            SET NAME = %s,
            MANUFACTURER = %s,
            PRICE = %s,
            COUNTRY = %s
            WHERE ID= %s
            """, (equipment.name, equipment.manufacturer,
                   equipment.price, equipment.country,id))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def get_all_equipments(app):
    equipments=None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        try:
            cursor.execute('''
            SELECT E.ID, E.NAME, E.MANUFACTURER , E.PRICE, C.COUNTRY_NAME
            FROM EQUIPMENTS AS E,COUNTRIES AS C
            WHERE (E.COUNTRY = C.COUNTRY_ID)
            ORDER BY 1
            ''');
            equipments = cursor.fetchall()
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.close()
        return equipments

def search_equipment(app, name):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT E.ID, E.NAME, E.MANUFACTURER , E.PRICE, C.COUNTRY_NAME
            FROM EQUIPMENTS AS E, COUNTRIES AS C
            WHERE(
                UPPER(E.NAME)=UPPER(%s) AND
                E.COUNTRY=C.COUNTRY_ID
            )""", (name,))
            equipments = cursor.fetchall()
        except dbapi2.Error as e:
            print(e.pgerror)
            cursor.rollback()
        finally:
            cursor.close()
    except bapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return equipments
def fill_table(cursor):
    cursor.execute("""
            INSERT INTO EQUIPMENTS
            (NAME, MANUFACTURER, PRICE, COUNTRY) VALUES (
            'Broom',
            'Mazula Holding',
            300,
            1
            );
            INSERT INTO EQUIPMENTS
            (NAME, MANUFACTURER, PRICE, COUNTRY) VALUES (
            'Rink',
            'Mazula A.Ş.',
            11100,
            1
            );
            INSERT INTO EQUIPMENTS
            (NAME, MANUFACTURER, PRICE, COUNTRY) VALUES (
            'Shoes',
            'Mazula Inc.',
            100,
            1
            );
            INSERT INTO EQUIPMENTS
            (NAME, MANUFACTURER, PRICE, COUNTRY) VALUES (
            'Rock',
            'Mazula San. Tic. LTD.',
            400,
            1
            );

            """)