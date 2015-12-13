class Federation:
    def __init__(self,news_header, news_description, date ,team_id, curler_id):
        self.news_header = news_header
        self.news_description = news_description
        self.date = date
        self.team_id = team_id
        self.curler_id = curler_id

def init_news_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS NEWS (
            NEWS_ID SERIAL,
            NEWS_HEADER varchar(80) NOT NULL,
            NEWS_DESCRIPTION varchar(80),
            DATE DATE,
            TEAM_ID integer REFERENCES CLUBS ON UPDATE CASCADE ON DELETE CASCADE,
            CURLER_ID integer REFERENCES CURLERS ON UPDATE CASCADE ON DELETE CASCADE, 
            PRIMARY KEY (NEWS_ID)
            )"""
    cursor.execute(query)

def add_news(cursor, request, news):
    query = """INSERT INTO NEWS
    (NEWS_HEADER,NEWS_DESCRIPTION, DATE, TEAM_ID, CURLER_ID) VALUES (
    %s,
    %s,
    %s,
    %s,
    %s
    )"""
    cursor.execute(query, (news.news_header, news.news_description, news.date,news.team_id, news.curler_id))

def delete_news(cursor, id):
    query="""DELETE FROM NEWS WHERE NEWS_ID = %s"""
    cursor.execute(query, (id))

def update_news(cursor,news,id):
    query="""UPDATE NEWS SET NEWS_HEADER=%s,NEWS_DESCRIPTION=%s,DATE=%s,TEAM_ID=%s,CURLER_ID=%s WHERE(NEWS_ID=%s)"""
    cursor.execute(query, (news.news_header, news.news_description, news.date,news.team_id,news.curler_id, id))