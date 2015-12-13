class Coach:
    def __init__(self, name,surname,age,country,club):
        self.name = name
        self.surname=surname
        self.age=age
        self.country=country
        self.club=club

def init_coach_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS COACHES (
    COACH_ID SERIAL,
    COACH_NAME VARCHAR(80) NOT NULL ,
    COACH_SURNAME VARCHAR(80) ,
    COACH_AGE INTEGER ,
    COACH_COUNTRY INTEGER NOT NULL REFERENCES COUNTRIES(COUNTRY_ID) ON DELETE CASCADE ON UPDATE CASCADE ,
    COACH_CLUB INTEGER NOT NULL REFERENCES CLUBS(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(COACH_ID)
    )"""
    cursor.execute(query)

def add_coach(cursor, request, coach):

        query = """INSERT INTO COACHES
        (COACH_NAME,COACH_SURNAME,COACH_AGE,COACH_COUNTRY,COACH_CLUB) VALUES (
        INITCAP(%s),
        INITCAP(%s),
        %s,
        %s,
        %s)"""
        cursor.execute(query, (coach.name,coach.surname,coach.age,coach.country,coach.club))
        print(0)
def delete_coach(cursor, id):
        query="""DELETE FROM COACHES WHERE COACH_ID = %s"""
        cursor.execute(query, (int(id),))
def update_coach(cursor, id, country):
            query="""
            UPDATE COUNTRIES
            SET COUNTRY_NAME=INITCAP(%s),
            COUNTRY_CURLER=%s,
            COUNTRY_CLUB=%s,
            COUNTRY_TOURNAMENT=%s
            WHERE COUNTRY_ID=%s
            """
            cursor.execute(query,(country.name, country.curler, country.club,
                                country.tournament, id),)
