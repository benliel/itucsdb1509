class Curler:
    def __init__(self, name, surname, birthdate, team, country):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.team = team
        self.country = country

def init_curlers_db(cursor):
    query = """DROP TABLE IF EXISTS CURLERS"""
    cursor.execute(query)
    query = """CREATE TABLE CURLERS (
            ID SERIAL,
            NAME varchar(80) NOT NULL,
            SURNAME varchar(80) NOT NULL,
            BIRTH_DATE varchar(20),
            TEAM varchar(20),
            COUNTRY varchar(80),
            PRIMARY KEY (ID)
            )"""
    cursor.execute(query)

def add_curler(cursor, request, curler):
    query = """INSERT INTO CURLERS
    (NAME, SURNAME, BIRTH_DATE, TEAM, COUNTRY) VALUES (
    %s,
    %s,
    %s,
    %s,
    %s
    )"""
    cursor.execute(query, (curler.name, curler.surname, curler.birthdate,
                           curler.team, curler.country))

def delete_curler(cursor, id):
    query="""DELETE FROM CURLERS WHERE ID = %s"""
    cursor.execute(query, (int(id),))

def update_curler(cursor,curler,id):
    query="""UPDATE CURLERS SET NAME=%s,SURNAME=%s,BIRTH_DATE=%s,TEAM=%s,COUNTRY=%s WHERE(ID=%s)"""
    cursor.execute(query, (curler.name,curler.surname,curler.birthdate, 
                   curler.team,curler.country,id))