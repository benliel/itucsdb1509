class Countries:
    def __init__(self, name):
        self.name = name

def init_countries_db(cursor):
    query = """DROP TABLE IF EXISTS COUNTRIES"""
    cursor.execute(query)
    query = """CREATE TABLE COUNTRIES (
    ID SERIAL,
    NAME VARCHAR(80) NOT NULL,
    PRIMARY KEY(ID)
    )"""
    cursor.execute(query)

def add_country(cursor, request, country):
        query = """INSERT INTO COUNTRIES
        (NAME) VALUES (
        INITCAP(%s))"""
        cursor.execute(query, (country.name,))

def delete_country(cursor, id):
        query="""DELETE FROM COUNTRIES WHERE ID = %s"""
        cursor.execute(query, (int(id),))


