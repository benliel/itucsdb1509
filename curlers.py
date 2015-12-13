class Curler:
    def __init__(self, name, surname, birthdate, teamid, birthplaceId):
        self.curler_name = name
        self.curler_surname = surname
        self.birthdate = birthdate
        self.teamid = teamid
        self.birth_place_id = birthplaceId

def init_curlers_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS CURLERS (
            CURLERID SERIAL,
            CURLER_NAME varchar(80) NOT NULL,
            CURLER_SURNAME varchar(80) NOT NULL,
            BIRTH_DATE varchar(20),
            TEAMID integer REFERENCES CLUBS(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
            BIRTH_PLACE_ID integer REFERENCES COUNTRIES ON UPDATE CASCADE ON DELETE RESTRICT, 
            PRIMARY KEY (CURLERID)
            )"""
    cursor.execute(query)

def add_curler(cursor, request, curler):
    query = """INSERT INTO CURLERS
    (CURLER_NAME, CURLER_SURNAME, BIRTH_DATE, TEAMID, BIRTH_PLACE_ID) VALUES (
    %s,
    %s,
    %s,
    %s,
    %s
    )"""
    cursor.execute(query, (curler.curler_name, curler.curler_surname, curler.birthdate,
                           curler.teamid, curler.birth_place_id))

def delete_curler(cursor, id):
    query="""DELETE FROM CURLERS WHERE CURLERID = %s"""
    cursor.execute(query, (int(id),))

def update_curler(cursor,curler,id):
    query="""UPDATE CURLERS SET CURLER_NAME=%s,CURLER_SURNAME=%s,BIRTH_DATE=%s,TEAMID=%s,BIRTH_PLACE_ID=%s WHERE(CURLERID=%s)"""
    cursor.execute(query, (curler.curler_name,curler.curler_surname,curler.birthdate,
                   curler.teamid,curler.birth_place_id,id))