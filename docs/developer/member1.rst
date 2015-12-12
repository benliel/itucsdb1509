Parts Implemented by Sercan Bayındır
====================================
"Fixture Table" and "Stadiums Table" is owned by me.

Fixture Table
   Columns:
     ID SERIAL,

     TEAM1 INTEGER NOT NULL REFERENCES CLUBS(ID) ON DELETE CASCADE ON UPDATE CASCADE,

     TEAM2 INTEGER NOT NULL REFERENCES CLUBS(ID) ON DELETE CASCADE ON UPDATE CASCADE,

     DATE DATE NOT NULL,

     TIME TIME NOT NULL,

     LOCATION INTEGER NOT NULL REFERENCES STADIUMS(ID) ON DELETE CASCADE ON UPDATE CASCADE,

   Constraints:
     PRIMARY KEY (ID),

     UNIQUE(DATE,TIME,LOCATION)

Stadiums Table
   Columns:
      ID SERIAL NOT NULL,

      NAME VARCHAR(80) NOT NULL,

      LOCATION INTEGER NOT NULL REFERENCES COUNTRIES(COUNTRY_ID) ON DELETE CASCADE ON UPDATE CASCADE,

      CAPACITY INTEGER DEFAULT -1,

      COST INTEGER DEFAULT -1,

   Constraints:
      PRIMARY KEY(ID),

      CHECK(COST>=-1),

      CHECK(CAPACITY>=-1),

      UNIQUE(NAME,LOCATION)


"Stadium" and "Match" classes has been owned by me.

.. code-block:: Pyhton
   class Match:
      def __init__(self, team1, team2, date, time, location):
         self.team1 = team1
         self.team2 = team2
         self.date = date
         self.time = time
         self.location = location

   class Stadium:
      def __init__(self,name,location,capacity,ticket_cost):
         self.name=name
         self.location=location
         self.capacity=capacity
         self.ticket_cost=ticket_cost


 I have worked in "fixture.py" and "stadiums.py" sources

 fixture.py
   Functions:
      add_match
         Used for adding matches in the fixture table

         Checks if the teams are free for the given date and time
      delete_match
         Used to delete match with given id
      update_match
         Used to change data of the match with given id
      search_match
         Returns the matches that matches the given search line
      get_match
         Returns the data of single match to be editted.
      get_all_matches
         Returns all of the matches to be viewed in the main fixture page
      get_stadium_names
         Gets all stadium names to be listed for user interface
      get_filtered_matches
         Returns all of the mathces for given stadium id
      get_fixture_page
         Handles fixture_page requests
      get_fixture_edit_page
         Handles fixture_edit_page requests
      get_fixture_filter_page
         Handles filter by stadium requests

stadium.py
   Functions:
      add_stadium
         Used for adding stadiums in the stadiums table
      delete_stadium
         Used to delete stadium with given id
      update_stadium
         Used to change data of the stadium with given id
      search_stadium
         Returns the stadiums that matches the given search line
      get_match
         Returns the data of single stadium to be editted.
      get_all_matches
         Returns all of the stadiums to be viewed in the main stadiums page
      get_stadiums_page
         Handles stadiums_page requests
      get_stadiums_edit_page
         Handles stadiums_edit_page requests

Common:
   Functions:
      get_club_names
         Get club names to be listed for user interface