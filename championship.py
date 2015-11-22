class Championship:
    def __init__(self, name, place, date, type, teamNo,reward):
        self.name = name
        self.place = place
        self.date = date
        self.type = type
        self.teamNo = teamNo
        self.reward = reward

def init_championship_db(cursor):
    query = """DROP TABLE IF EXISTS CHAMPIONSHIP"""
    cursor.execute(query)
    query = """CREATE TABLE CHAMPIONSHIP (
ID SERIAL,
NAME VARCHAR(80) NOT NULL,
PLACE VARCHAR(80) NOT NULL,
DATE DATE NOT NULL,
TYPE VARCHAR(80) NOT NULL,
NUMBER_OF_TEAMS INTEGER NOT NULL,
REWARD VARCHAR(80),
PRIMARY KEY(ID)
)"""
    cursor.execute(query)

def add_championship(cursor, request, championship):
        query = """INSERT INTO CHAMPIONSHIP
        (NAME, PLACE, DATE, TYPE, NUMBER_OF_TEAMS,REWARD) VALUES (
        %s,
        %s,
        to_date(%s, 'YYYY-MM-DD'),
        %s,
        %s,
        %s
        )"""
        cursor.execute(query, (Championship.name, Championship.place, Championship.date,
                                Championship.type, Championship.teamNo,Championship.reward))

def delete_championship(cursor, id):
        query="""DELETE FROM CHAMPIONSHIP WHERE ID = %s"""
        cursor.execute(query, (int(id),))

