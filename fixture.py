class Match:
    def __init__(self, team1, team2, date, clock, location):
        self.team1 = team1
        self.team2 = team2
        self.date = date
        self.clock = clock
        self.location = location

def init_fixture_db(cursor):
    query = """DROP TABLE IF EXISTS FIXTURE"""
    cursor.execute(query)
    query = """CREATE TABLE FIXTURE (
TEAM1 varchar(80) NOT NULL,
TEAM2 varchar(80) NOT NULL,
DATE date NOT NULL,
TIME time NOT NULL,
LOCATION varchar(80),
PRIMARY KEY (DATE, TIME, LOCATION)
)"""
    cursor.execute(query)

def add_match(cursor, request, variables):
        query = """INSERT INTO FIXTURE
        (TEAM1, TEAM2, DATE, TIME, LOCATION) VALUES (
        %s,
        %s,
        to_date(%s, 'YYYY-MM-DD'),
        to_timestamp(%s, 'HH24:MI'),
        %s
        )"""
        cursor.execute(query, variables)

