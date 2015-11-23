class Countries:
    def __init__(self, name):
        self.name = name

def init_countries_db(cursor):
    query = """DROP TABLE IF EXISTS COUNTRIES CASCADE"""
    cursor.execute(query)
    query = """CREATE TABLE COUNTRIES (
    ID SERIAL,
    NAME VARCHAR(80) NOT NULL
    PRIMARY KEY(ID)
    )"""
    cursor.execute(query)

def add_countries(cursor, request, country1):
        query = """INSERT INTO COUNTRIES
        (NAME) VALUES (
        INITCAP(%s)
        )"""
        cursor.execute(query, (country1.name))

def delete_championship(cursor, id):
        query="""DELETE FROM CHAMPIONSHIP WHERE ID = %s"""
        cursor.execute(query, (int(id),))

def update_championship(cursor, id, championship1):
            query="""
            UPDATE CHAMPIONSHIP
            SET NAME=INITCAP(%s),
            PLACE=INITCAP(%s),
            DATE=to_date(%s, 'YYYY-MM-DD'),
            TYPE=INITCAP(%s),
            NUMBER_OF_TEAMS=%s,
            REWARD=INITCAP(%s)
            WHERE ID=%s
            """
            cursor.execute(query,(championship1.name, championship1.place, championship1.date,
                                championship1.type, championship1.teamNo,championship1.reward, id))
            print("done update")
