class Curler:
    def __init__(self, name, surname, age, team, country):
        self.name = name
        self.surname = surname
        self.age = age
        self.team = team
        self.country = country

def init_curlers_db(cursor):
    query = """DROP TABLE IF EXISTS CURLERS"""
    cursor.execute(query)
    query = """CREATE TABLE CURLERS (
ID SERIAL,
NAME varchar(80) NOT NULL,
SURNAME varchar(80) NOT NULL,
AGE integer NOT NULL,
TEAM varchar(20) NOT NULL,
COUNTRY varchar(80),
PRIMARY KEY (ID)
)"""
    cursor.execute(query)

def add_curler(cursor, request, curler):
        query = """INSERT INTO CURLERS
        (NAME, SURNAME, AGE, TEAM, COUNTRY) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s
        )"""
        cursor.execute(query, (curler.name, curler.surname, curler.age,
                               curler.team, curler.country))

def delete_curler(cursor, id):
        query="""DELETE FROM CURLERS WHERE ID = %s"""
        cursor.execute(query, (int(id),))

