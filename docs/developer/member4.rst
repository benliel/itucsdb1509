Parts Implemented by Chousein Giousouf (Huseyin Yusuf)
======================================================
"Countries Table","Championships Table" and "Coaches Table" are owned by me.

Countries Table
   Columns:
      COUNTRY_ID serial,

      COUNTRY_ID SERIAL,

      COUNTRY_NAME VARCHAR(80) UNIQUE NOT NULL ,

      COUNTRY_CONTINENT VARCHAR(80) NOT NULL ,

      COUNTRY_CAPITAL VARCHAR(80)  NOT NULL ,

      COUNTRY_INDEPEN_YEAR VARCHAR(80) NOT NULL ,

   Constraints:
     PRIMARY KEY (COUNTRY_ID),

     UNIQUE(COUNTRY_NAME)

Championships Table
   Columns:
        ID SERIAL,

   	NAME VARCHAR(80) NOT NULL,

    	PLACE INTEGER NOT NULL REFERENCES COUNTRIES(COUNTRY_ID) ON DELETE CASCADE ON UPDATE CASCADE,

   	DATE DATE NOT NULL,

    	TYPE VARCHAR(80) NOT NULL,

    	NUMBER_OF_TEAMS INTEGER NOT NULL,

    	REWARD VARCHAR(80),

   Constraints:
      PRIMARY KEY(ID),

Coaches Table
   Columns:
        COACH_ID SERIAL,
   	COACH_NAME VARCHAR(80) NOT NULL ,
        COACH_SURNAME VARCHAR(80) ,
        COACH_AGE INTEGER ,
    	COACH_COUNTRY INTEGER NOT NULL REFERENCES COUNTRIES(COUNTRY_ID) ON DELETE CASCADE ON UPDATE CASCADE ,
        COACH_CLUB INTEGER NOT NULL REFERENCES CLUBS(ID) ON DELETE CASCADE ON UPDATE CASCADE,

   Constraints:
        PRIMARY KEY(COACH_ID),

"Coach", "Championships" and "Countries" classes are owned by me.

.. code-block:: Pyhton
   class Coach:
      def __init__(self, name,surname,age,country,club):
         self.name = name
         self.surname=surname
         self.age=age
         self.country=country
         self.club=club
 
   class Championships:
      def __init__(self, name, place, date, type, teamNo,reward):
         self.name = name
         self.place = place
         self.date = date
         self.type = type
         self.teamNo = teamNo
         self.reward = reward


   class Countries:
     def __init__(self, name,continent,capital,independency):
        self.name = name
        self.continent=continent
        self.capital=capital
        self.independency=independency

I have worked in "countries.py", "coach.py","championship.py" and "server.py" sources

countries.py
   Functions:
      init_countries_db
         Used for initialising countries table

      fill_countries_db
         Used to add some countries to Countries Table

      add_country
         Used for adding countries in the Countries Table

      delete_country
         Used to delete countries with given id from Countries Table

      update_country
         Used to change data of the country with given id



coach.py
   Functions:
      init_coach_db
         Used for initialising coaches table

      fill_coach_db
         Used to add some coaches to Coaches Table

      add_coach
         Used for adding coaches in the Coaches Table

      delete_coach
         Used to delete coaches with given id from Coaches Table

      update_coach
         Used to change data of the coach with given id



championship.py
   Functions:
      init_championships_db
         Used for initialising Championships table

      fill_championships_db
         Used to add some championships to Championships Table

      add_championship
         Used for adding championships in the Championships Table

      delete_championship
         Used to delete championships with given id from Championships Table

      update_championship
         Used to change data of the championships with given id


server.py
   Functions:
      search_championship
         Returns championships according to the text entered (Search both by name and Place)

      championship_update_page
         Used to update championship info of the given id at Championships Table

      search_country
         Returns countries according to the text entered (Search both by country-name and country continent)

      country_update_page
         Used to update country info of the given id at Countries Table

      country_update_page
         Used to update coach info of the given id at Coaches Table

      search_coach
	 Returns coaches according to the text entered (Search by Name of the Coach)



