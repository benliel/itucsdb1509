class Countries:
    def __init__(self, name,curler,club,tournament):
        self.name = name
        self.curler=curler
        self.club=club
        self.tournament=tournament

def init_countries_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS COUNTRIES (
    COUNTRY_ID SERIAL,
    COUNTRY_NAME VARCHAR(80) NOT NULL ,
    COUNTRY_CURLER INTEGER ,
    COUNTRY_CLUB INTEGER ,
    COUNTRY_TOURNAMENT INTEGER ,
    PRIMARY KEY(COUNTRY_ID)
    )"""
    cursor.execute(query)

def add_country(cursor, request, country):

        query = """INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CURLER,COUNTRY_CLUB,COUNTRY_TOURNAMENT) VALUES (
        INITCAP(%s),
        %s,
        %s,
        %s)"""
        cursor.execute(query, (country.name,country.curler,country.club,country.tournament))

def delete_country(cursor, id):
        query="""DELETE FROM COUNTRIES WHERE COUNTRY_ID = %s"""
        cursor.execute(query, (int(id),))
def update_country(cursor, id, country):
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
