class Clubs:
    def __init__(self, name, place, year, chair, number_of_members, rewardnumber):
        self.name = name
        self.place = place
        self.year = year
        self.chair = chair
        self.number_of_members = number_of_members
        self.rewardnumber = rewardnumber

def init_clubs_db(cursor):
    query = """DROP TABLE IF EXISTS CLUBS CASCADE"""
    cursor.execute(query)
    query = """CREATE TABLE CLUBS (
            ID SERIAL,
            NAME VARCHAR(80) NOT NULL,
            PLACE VARCHAR(80) NOT NULL,
            YEAR NUMERIC(4) NOT NULL,
            CHAIR VARCHAR(80) NOT NULL,
            NUMBER_OF_MEMBERS INTEGER NOT NULL,
            REWARDNUMBER INTEGER,
            PRIMARY KEY(ID)
            )"""
    cursor.execute(query)

def add_club(cursor, request, club):
        query = """INSERT INTO CLUBS
        (NAME, PLACE, YEAR, CHAIR, NUMBER_OF_MEMBERS, REWARDNUMBER) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
        )"""
        cursor.execute(query, (club.name, club.place, club.year,
                                club.chair, club.number_of_members, club.rewardnumber))

def delete_club(cursor, id):
        query="""DELETE FROM CLUBS WHERE ID = %s"""
        cursor.execute(query, (int(id),))



