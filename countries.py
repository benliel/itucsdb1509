class Countries:
    def __init__(self, name,continent,capital,independency):
        self.name = name
        self.continent=continent
        self.capital=capital
        self.independency=independency

def init_countries_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS COUNTRIES (
    COUNTRY_ID SERIAL,
    COUNTRY_NAME VARCHAR(80) UNIQUE NOT NULL ,
    COUNTRY_CONTINENT VARCHAR(80) NOT NULL ,
    COUNTRY_CAPITAL VARCHAR(80)  NOT NULL ,
    COUNTRY_INDEPEN_YEAR VARCHAR(80) NOT NULL ,
    PRIMARY KEY(COUNTRY_ID)
    )"""
    cursor.execute(query)

def add_country(cursor, request, country):

        query = """INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        INITCAP(%s),
        %s,
        %s,
        %s)"""
        cursor.execute(query, (country.name, country.continent, country.capital,
                                country.independency))

def delete_country(cursor, id):
        query="""DELETE FROM COUNTRIES WHERE COUNTRY_ID = %s"""
        cursor.execute(query, (int(id),))
def update_country(cursor, id, country):
            query="""
            UPDATE COUNTRIES
            SET COUNTRY_NAME=INITCAP(%s),
            COUNTRY_CONTINENT=INITCAP(%s),
            COUNTRY_CAPITAL=INITCAP(%s),
            COUNTRY_INDEPEN_YEAR=%s
            WHERE COUNTRY_ID=%s
            """
            cursor.execute(query,(country.name, country.continent, country.capital,
                                country.independency, id),)
