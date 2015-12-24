Parts Implemented by Sercan Bayındır
====================================
"Fixture Table", "Stadiums Table" and "Points Table" are created by me.

Fixture Table
   Columns:
      ID serial,

      TEAM1 integer not null references clubs(id) on delete cascade on update cascade,

      TEAM2 integer not null references clubs(id) on delete cascade on update cascade,

      DATE date not null,

      TIME time not null,

      LOCATION integer not null references stadiums(id) on delete cascade on update cascade,

   Constraints:
     PRIMARY KEY (id),

     UNIQUE(date, time, location)

Stadiums Table
   Columns:
      ID serial not null,

      NAME vachar(80) not null,

      LOCATION integer not null references countries(country_id) on delete cascade on update cascade,

      CAPACITY integer default -1,

      COST integer default -1,

   Constraints:
      PRIMARY KEY(id),

      CHECK(cost>=-1),

      CHECK(capacity>=-1),

      UNIQUE(name,location)

Points Table
   Columns:
      ID serial not null,

      CHAMPIONSHIP integer not null references championship(id) on update cascade on delete cascade,

      CLUB integer not null references clubs(id) on update cascade on delete cascade,

      POINTS integer default 0,

      WINS integer default 0,

   Constraints:
      PRIMARY KEY(ID),

      CHECK(points>=0),

      CHECK(wins>=0),

      UNIQUE(championship, club)


"Stadium" and "Match" classes are created by me.::

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


I have worked in "fixture.py", "stadiums.py" and "points.py" sources

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
      get_all_stadiums
         Returns all of the stadiums to be viewed in the main stadiums page
      get_stadiums_page
         Handles stadiums_page requests
      get_stadiums_edit_page
         Handles stadiums_edit_page requests

points.py
   Functions:
      add_points_data
         Used for adding points data in the points table
      delete_points_data
         Used to delete points data with given id
      update_points_data
         Used to change data of the points data with given id
      get_filtered_points_data
         Returns the points that matches the given search line
      get_points_data
         Returns the data of single points data to be editted.
      get_all_championships
         Returns all of the championship id and names to be listed.
      get_all_points_data
         Returns all of the points data to be viewed in the main points page
      get_points_page
         Handles points_page requests
      get_points_edit_page
         Handles points_edit_page requests

Common:
   Functions:
      get_club_names
         Get club names to be listed for user interface