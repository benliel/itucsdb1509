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
from clubs import *
from money_balance import *
from psycopg2.tests import dbapi20

class Money_balances:
    def __init__(self, club, incomes, expenses, profit):
        self.club = club
        self.incomes = incomes
        self.expenses = expenses
        self.profit = profit

def init_money_balances_db(cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS MONEY_BALANCE (
        ID SERIAL,
        CLUB INTEGER NOT NULL REFERENCES CLUBS(ID) ON DELETE CASCADE ON UPDATE CASCADE,
        INCOMES INTEGER NOT NULL,
        EXPENSES INTEGER NOT NULL,
        PROFIT INTEGER NOT NULL,
        PRIMARY KEY (ID)
        )""")
        add_test_data(cursor)


def add_test_data(cursor):
     cursor.execute(
                       """
            INSERT INTO MONEY_BALANCE
            (CLUB, INCOMES, EXPENSES, PROFIT) VALUES (
            1,
            '35000',
            '20000',
            '15000'
            )"""
                       )

def add_money_balance(app, request, money_balance):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO MONEY_BALANCE
            (CLUB, INCOMES, EXPENSES, PROFIT) VALUES (
            %s,
            %s,
            %s,
            %s
            )""", (money_balance.club, money_balance.incomes,
                   money_balance.expenses, money_balance.profit))

        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def delete_money_balance(app, id):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM MONEY_BALANCE WHERE ID = %s', (id,))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()


def get_money_balances_page(app):
    print(request.form)

    if request.method == 'GET':
        now = datetime.datetime.now()
        money_balances = get_all_money_balances(app)
        clubs = get_club_names(app)

        return render_template('money_balances.html', money_balances = money_balances,
                               clubs=clubs, current_time=now.ctime())
    elif "add" in request.form:
        money_balance = Money_balances(request.form['club'],
                     request.form['incomes'],
                     request.form['expenses'],
                     request.form['profit'])

        add_money_balance(app, request, money_balance)
        return redirect(url_for('money_balances_page'))
    elif "delete" in request.form:
        for line in request.form:
            if "checkbox" in line:
                delete_money_balance(app, int(line[9:]))

        return redirect(url_for('money_balances_page'))
    elif 'search' in request.form:
        money_balances = search_money_balance(app, request.form['money_balance_to_search'])
        return render_template('money_balance_search_page.html', money_balances = money_balances)


def get_money_balances_edit_page(app,money_balance_id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        money_balance = get_money_balance(app, money_balance_id)
        clubs = get_club_names(app)
        return render_template('money_balance_edit_page.html', current_time=now.ctime(), money_balance=money_balance, clubs=clubs)

    if request.method == 'POST':
        money_balance = Money_balances(request.form['club'],
                     request.form['incomes'],
                     request.form['expenses'],
                     request.form['profit'])
        update_money_balance(app, request.form['id'], money_balance)
        return redirect(url_for('money_balances_page'))

def get_club_names(app):
    clubs=None
    connection=dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT ID,NAME FROM CLUBS')
            clubs = cursor.fetchall()
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
        return clubs

def get_money_balance(app, money_balance_id):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''
            SELECT M.ID, C.NAME, M.INCOMES, M.EXPENSES, M.PROFIT
            FROM MONEY_BALANCE AS M,CLUBS AS C
            WHERE (
                M.ID=%s AND C.ID=M.CLUB
                )
            ''', money_balance_id);
            money_balance = cursor.fetchone()
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
        return money_balance

def update_money_balance(app, id, money_balance):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            UPDATE MONEY_BALANCE
            SET CLUB = %s,
            INCOMES = %s,
            EXPENSES = %s,
            PROFIT = %s
            WHERE ID= %s
            """, (money_balance.club, money_balance.incomes,
                   money_balance.expenses, money_balance.profit, id))
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except:
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

def get_all_money_balances(app):
    money_balances=None
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor=connection.cursor()
        try:

            cursor.execute('''
            SELECT M.ID, C.NAME, M.INCOMES, M.EXPENSES, M. PROFIT
            FROM MONEY_BALANCE AS M, CLUBS AS C
            WHERE(M.CLUB=C.ID)
            ORDER BY 1
            ''')
            money_balances = cursor.fetchall()
        except:
            cursor.rollback()
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.close()
        return money_balances

def search_money_balance(app, name):
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT M.ID, C.NAME, M.INCOMES, M.EXPENSES, M. PROFIT
            FROM MONEY_BALANCE AS M, CLUBS AS C
            WHERE(
                UPPER(C.NAME)=UPPER(%s) AND M.CLUB=C.ID
            )""", (name,))
            money_balances = cursor.fetchall()
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
        return money_balances
