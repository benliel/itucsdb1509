class Match:
    def __init__(self, team1, team2, date, time, location):
        self.team1 = team1
        self.team2 = team2
        self.date = date
        self.time = time
        self.location = location

def init_fixture_db(cursor):
    query = """DROP TABLE IF EXISTS FIXTURE"""
    cursor.execute(query)
    query = """CREATE TABLE FIXTURE (
ID SERIAL,
TEAM1 varchar(80) NOT NULL,
TEAM2 varchar(80) NOT NULL,
DATE date NOT NULL,
TIME time NOT NULL,
LOCATION varchar(80),
PRIMARY KEY (ID)
)"""
    cursor.execute(query)

def add_match(cursor, request, match):
        query = """INSERT INTO FIXTURE
        (TEAM1, TEAM2, DATE, TIME, LOCATION) VALUES (
        %s,
        %s,
        to_date(%s, 'YYYY-MM-DD'),
        to_timestamp(%s, 'HH24:MI'),
        %s
        )"""
        cursor.execute(query, (match.team1, match.team2, match.date,
                                match.time, match.location))

def delete_match(cursor, id):
        query="""DELETE FROM FIXTURE WHERE ID = %s"""
        cursor.execute(query, (int(id),))

