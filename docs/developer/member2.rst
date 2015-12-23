Parts Implemented by M. Aziz ULAK
=================================
"Sponsors Table" , "Penalty Table" and "Equipments Table" are written by me.

Sponsors Table
   Columns:
      ID serial,

      NAME varchar(80) not null,

      SUPPORTEDTEAM integer not null references clubs(id) on delete cascade on update cascade,

      BUDGET integer not null

   Constraints:
     PRIMARY KEY (id)

Penalty Table
   Columns:
      ID serial not null,

      PERSONNAME integer not null references curlers(curlerid) on delete cascade on update cascade,

      STARTDATE varchar(20) not null,

      ENDDATE varchar(20) not null,

      TYPE varchar(20) not null

   Constraints:
      PRIMARY KEY(id)

Equipments Table
   Columns:
      ID serial not null,

      NAME varchar(80) not null,

      MANUFACTURER varchar(80) not null,

      PRICE integer not null,

      COUNTRY integer not null references countries(country_id) on delete cascade on update cascade

   Constraints:
      PRIMARY KEY(ID)

"Sponsors","Penalty" and "Equipments" classes are written by me.::

   .. code-block:: Pyhton

      class Sponsors:
        def __init__(self, name, supportedteam, budget):
        self.name = name
        self.supportedteam = supportedteam
        self.budget = budget

      class Penalty:
        def __init__(self, personname, startdate, enddate, type):
        self.personname = personname
        self.startdate = startdate
        self.enddate = enddate
        self.type = type


      class Equipments:
        def __init__(self, name, manufacturer, price , country):
        self.name = name
        self.manufacturer = manufacturer
        self.price = price
        self.country = country


I have worked in "sponsors.py" , "penalty.py" and "equipments.py" sources

***sponsors.py***
   Functions:
      add_sponsor
         Used for adding sponsors in the Sponsors Table
      delete_sponsor
         Used to delete sponsor with given id
      update_sponsor
         Used to change data of the sponsor with given id
      search_sponsor
         Returns the sponsors that matches the given search line
      get_sponsor
         Returns the data of single sponsor to be editted.
      get_all_sponsors
         Returns all of the sponsors to be viewed in the main sponsors page
      get_sponsors_page
         Handles sponsors_page requests
      get_sponsors_edit_page
         Handles sponsors_edit_page requests
      fill_table
         Fills the table for initialization of database

***penalty.py***
   Functions:
      add_penalty
         Used for adding penalties in the Penalty Table
      delete_penalty
         Used to delete penalty with given id
      update_penalty
         Used to change data of the penalty with given id
      search_penalty
         Returns the penalty that matches the given search line
      get_penalty
         Returns the data of single penalty to be editted.
      get_all_penalties
         Returns all of the penalties to be viewed in the main penalty page
      get_penalty_page
         Handles stadiums_page requests
      get_penalty_edit_page
         Handles penalty_edit_page requests
      fill_table
         Fills the table for initialization of database

***equipments.py***
   Functions:
      add_equipment
         Used for adding equipments data in the Equipments Table
      delete_equipment
         Used to delete equipment data with given id
      update_equipment
         Used to change data of the equipment data with given id
      search_equipment
         Returns the equipment that matches the given search line
      get_equipment
         Returns the data of single equipment to be editted.
      get_all_equipments
         Returns all of the equipments to be viewed in the main penalty page
      get_equipments_page
         Handles equipments_page requests
      get_equipments_edit_page
         Handles equipments_edit_page requests
      fill_table
         Fills the table for initialization of database

Common:
   Functions:
      get_club_names
         Get club names to be listed for user interface
      get_country_names
         Get country names to be listed for user interface