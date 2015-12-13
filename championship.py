import datetime
import os
import json
import re
import psycopg2 as dbapi2
class Championships:
    def __init__(self, name, place, date, type, teamNo,reward):
        self.name = name
        self.place = place
        self.date = date
        self.type = type
        self.teamNo = teamNo
        self.reward = reward

def init_championships_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS CHAMPIONSHIP (
    ID SERIAL,
    NAME VARCHAR(80) NOT NULL,
    PLACE INTEGER NOT NULL REFERENCES COUNTRIES(COUNTRY_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    DATE DATE NOT NULL,
    TYPE VARCHAR(80) NOT NULL,
    NUMBER_OF_TEAMS INTEGER NOT NULL,
    REWARD VARCHAR(80),
    PRIMARY KEY(ID)
    )"""
    cursor.execute(query)
def fill_championships_db(cursor):
    query="""INSERT INTO CHAMPIONSHIP
        (NAME, PLACE, DATE, TYPE, NUMBER_OF_TEAMS,REWARD) VALUES (
        'Air Canada S.B',
        9,
        to_date('13.09.2019', 'DD-MM-YYYY'),
        'Single Elimination',
        5,
        '5.000.000$');

        INSERT INTO CHAMPIONSHIP
        (NAME, PLACE, DATE, TYPE, NUMBER_OF_TEAMS,REWARD) VALUES (
        'France Curling Championship',
        11,
        to_date('23.11.2018', 'DD-MM-YYYY'),
        'League',
        5,
        '20.000.000$');

        INSERT INTO CHAMPIONSHIP
        (NAME, PLACE, DATE, TYPE, NUMBER_OF_TEAMS,REWARD) VALUES (
        'World Golden Broom',
        5,
        to_date('20.10.2020', 'DD-MM-YYYY'),
        'Round Robin',
        4,
        '100.000.000$');

         INSERT INTO CHAMPIONSHIP
        (NAME, PLACE, DATE, TYPE, NUMBER_OF_TEAMS,REWARD) VALUES (
        ' Ford World Curling Ch.',
        7,
        to_date('08.09.2022', 'DD-MM-YYYY'),
        'Round Robin',
        4,
        '150.000.000$');

         INSERT INTO CHAMPIONSHIP
        (NAME, PLACE, DATE, TYPE, NUMBER_OF_TEAMS,REWARD) VALUES (
        'World Mixed Doubles Curling Ch.',
        8,
        to_date('18.01.2020', 'DD-MM-YYYY'),
        'Double Elimination',
        4,
        '300.000.000$');
        INSERT INTO CHAMPIONSHIP
        (NAME, PLACE, DATE, TYPE, NUMBER_OF_TEAMS,REWARD) VALUES (
        'WCF Championships',
        1,
        to_date('18.01.2020', 'DD-MM-YYYY'),
        'Double Elimination',
        4,
        '120.000.000$');
        """
    cursor.execute(query)
def add_championship(cursor, request, championship1):
        query = """INSERT INTO CHAMPIONSHIP
        (NAME, PLACE, DATE, TYPE, NUMBER_OF_TEAMS,REWARD) VALUES (
        INITCAP(%s),
        %s,
        to_date(%s, 'DD-MM-YYYY'),
        INITCAP(%s),
        %s,
        INITCAP(%s)
        )"""
        cursor.execute(query, (championship1.name, championship1.place, championship1.date,
                                championship1.type, championship1.teamNo,championship1.reward))

def delete_championship(cursor, id):
        query="""DELETE FROM CHAMPIONSHIP WHERE ID = %s"""
        cursor.execute(query, (int(id),))


def update_championship(cursor, id, championship1):
            query="""
            UPDATE CHAMPIONSHIP
            SET NAME=INITCAP(%s),
            PLACE=%s,
            DATE=to_date(%s, 'DD-MM-YYYY'),
            TYPE=INITCAP(%s),
            NUMBER_OF_TEAMS=%s,
            REWARD=INITCAP(%s)
            WHERE ID=%s
            """
            cursor.execute(query,(championship1.name, championship1.place, championship1.date,
                                championship1.type, championship1.teamNo,championship1.reward, id))



