class Federation:
    def __init__(self, federation_name,president_name,president_surname, founding_year, country_id):
        self.federation_name = federation_name
        self.president_name = president_name
        self.president_surname = president_surname
        self.founding_year = founding_year
        self.country_id = country_id
      
def init_federations_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS FEDERATIONS (
            FEDERATION_ID SERIAL,
            FEDERATION_NAME varchar(80) NOT NULL,
            PRESIDENT_NAME varchar(80),
            PRESIDENT_SURNAME varchar(80),
            FOUNDING_YEAR integer,
            COUNTRY integer REFERENCES COUNTRIES ON UPDATE CASCADE ON DELETE RESTRICT, 
            PRIMARY KEY (FEDERATION_ID)
            )"""
    cursor.execute(query)

def add_federation(cursor, request, federation):
    query = """INSERT INTO FEDERATIONS
    (FEDERATION_NAME,PRESIDENT_NAME, PRESIDENT_SURNAME, FOUNDING_YEAR, COUNTRY) VALUES (
    %s,
    %s,
    %s,
    %s,
    %s
    )"""
    cursor.execute(query, (federation.federation_name,federation.president_name, federation.president_surname,federation.founding_year, federation.country_id))

def delete_federation(cursor, id):
    query="""DELETE FROM FEDERATIONS WHERE FEDERATION_ID = %s"""
    cursor.execute(query, (id))

def update_federation(cursor,federation,id):
    query="""UPDATE FEDERATIONS SET FEDERATION_NAME=%s,PRESIDENT_NAME=%s,PRESIDENT_SURNAME=%s,FOUNDING_YEAR=%s,COUNTRY=%s WHERE(FEDERATION_ID=%s)"""
    cursor.execute(query, (federation.federation_name,federation.president_name,federation.president_surname,federation.founding_year,
                   federation.country_id,id))