class Sponsors:
    def __init__(self, name, supportedteam, budget):
        self.name = name
        self.supportedteam = supportedteam
        self.budget = budget

def init_sponsors_db(cursor):
    query = """DROP TABLE IF EXISTS SPONSORS"""
    cursor.execute(query)
    query = """CREATE TABLE SPONSORS (
ID SERIAL,
NAME VARCHAR(80) NOT NULL,
SUPPORTEDTEAM VARCHAR(80) NOT NULL,
BUDGET INTEGER NOT NULL,
PRIMARY KEY (ID)
)"""
    cursor.execute(query)

def add_sponsor(cursor, request, sponsor):
        query = """INSERT INTO SPONSORS
        (NAME, SUPPORTEDTEAM, BUDGET) VALUES (
        %s,
        %s,
        %s
        )"""
        cursor.execute(query, (sponsor.name, sponsor.supportedteam, sponsor.budget))

def delete_sponsor(cursor, id):
        query="""DELETE FROM SPONSORS WHERE ID = %s"""
        cursor.execute(query, (int(id),))

