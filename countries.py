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

def fill_countries_db(cursor):
    query="""INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'United States',
        'America',
        'Washington,D.C',
        '1776');

        INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'Greece',
        'Europe',
        'Athens',
        '1830');
        INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'Turkey',
        'Asia',
        'Ankara',
        '1923');
        INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'Germany',
        'Europe',
        'Berlin',
        '1875');
         INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'Great Britain',
        'Europe',
        'London',
        '1776');
        INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'Russia',
        'Asia',
        'Moscow',
        '1991');
          INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'China',
        'Asia',
        'Beijing',
        '1912');
         INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'Philippines',
        'Asia',
        'Manila',
        '1898');
        INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'Canada',
        'America',
        'Ottawa',
        '1867');
         INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'Sweden',
        'Europe',
        'Stockholm',
        '1523');
        INSERT INTO COUNTRIES
        (COUNTRY_NAME,COUNTRY_CONTINENT,COUNTRY_CAPITAL,COUNTRY_INDEPEN_YEAR) VALUES (
        'France',
        'Europe',
        'Rome',
        '1789');
        """
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
