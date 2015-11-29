class Countries:
    def __init__(self, name):
        self.name = name

def init_countries_db(cursor):
    query = """DROP TABLE IF EXISTS COUNTRIES"""
    cursor.execute(query)
    query = """CREATE TABLE COUNTRIES (
    COUNTRY_ID SERIAL,
    COUNTRY_NAME VARCHAR(80) NOT NULL,
    PRIMARY KEY(COUNTRY_ID)
    )"""
    cursor.execute(query)

def add_country(cursor, request, country):

        query = """INSERT INTO COUNTRIES
        (COUNTRY_NAME) VALUES (
        INITCAP(%s))"""
        cursor.execute(query, (country.name,))

def delete_country(cursor, id):
        query="""DELETE FROM COUNTRIES WHERE COUNTRY_ID = %s"""
        cursor.execute(query, (int(id),))


