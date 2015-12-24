Parts Implemented by Ilkan Engin
================================
"Curlers Table","Federations Table" and "News Table" are owned by me.

Curlers Table
    Columns:
        CURLERID SERIAL,

        CURLER_NAME VARCHAR(80) NOT NULL,

        CURLER_SURNAME VARCHAR(80) NOT NULL,

        BIRTH_DATE VARCHAR(20),

        TEAMID INTEGER REFERENCES CLUBS(ID) ON UPDATE CASCADE ON DELETE RESTRICT,

        BIRTH_PLACE_ID INTEGER REFERENCES COUNTRIES ON UPDATE CASCADE ON DELETE RESTRICT,

    Constraints:
        PRIMARY KEY (CURLERID)

Federations Table
    Columns:
        FEDERATION_ID SERIAL,

        FEDERATION_NAME VARCHAR(80) NOT NULL,

        PRESIDENT_NAME VARCHAR(80),

        PRESIDENT_SURNAME VARCHAR(80),

        FOUNDING_YEAR INTEGER,

        COUNTRY INTEGER REFERENCES COUNTRIES ON UPDATE CASCADE ON DELETE RESTRICT

    Constraints:
        PRIMARY KEY(FEDERATION_ID),

News Table
    Columns:
        NEWS_ID SERIAL,

        NEWS_HEADER varchar(80) NOT NULL,

        NEWS_DESCRIPTION varchar(80),

        DATE DATE,

        TEAM_ID INTEGER REFERENCES CLUBS ON UPDATE CASCADE ON DELETE CASCADE,

        CURLER_ID INTEGER REFERENCES CURLERS ON UPDATE CASCADE ON DELETE CASCADE

    Constraints:
        PRIMARY KEY(NEWS_ID),

"Curler", "Federation" and "News" classes are owned by me.

.. code-block:: Pyhton
    class Curler:
        def __init__(self, name, surname, birthdate, teamid, birthplaceId):
            self.curler_name = name
            self.curler_surname = surname
            self.birthdate = birthdate
            self.teamid = teamid
            self.birth_place_id = birthplaceId

    class Federation:
        def __init__(self, federation_name,president_name,president_surname, founding_year, country_id):
            self.federation_name = federation_name
            self.president_name = president_name
            self.president_surname = president_surname
            self.founding_year = founding_year
            self.country_id = country_id


    class News:
        def __init__(self,news_header, news_description, date ,team_id, curler_id):
            self.news_header = news_header
            self.news_description = news_description
            self.date = date
            self.team_id = team_id
            self.curler_id = curler_i

I have worked in "curlers.py", "federations.py","news.py" and "server.py" sources

curlers.py
   Functions:
      init_curlers_db
         Used for initialising countries table

      add_curler
         Used for adding countries in the Countries Table

      delete_curler
         Used to delete countries with given id from Countries Table

      update_curler
         Used to change data of the country with given id



federations.py
   Functions:
      init_federations_db
         Used for initialising coaches table

      add_federation
         Used for adding coaches in the Coaches Table

      delete_federation
         Used to delete coaches with given id from Coaches Table

      update_federation
         Used to change data of the coach with given id



news.py
   Functions:
      init_news_db
         Used for initialising Championships table

      add_news
         Used for adding championships in the Championships Table

      update_news
         Used to change data of the championships with given id


server.py
   Functions:
      search_news
         Returns news according to the text entered (Search by header or description of news)

      news_update_page
         Used to update news info of the given id at News Table

      search_curlers
         Returns curlers according to the text entered (Search both by curler name ad surname)

      curlers_update_page
         Used to update curlers info of the given id at Curlers Table

      federations_update_page
         Used to update federations info of the given id at Federations Table

      search_federations
	 Returns federations according to the text entered (Search by federation name, president name and president surname)

