Parts Implemented by Sema KARAKAŞ
=================================
"Money Balance Table" and "Clubs Table" are written by me.

**Clubs Table**

   Columns:
      id serial,

      name varchar(80) not null,

      places integer not null references countries(country_id) on delete cascade on update cascade,

      year numeric(4) not null,

      chair varchar(80) not null,

      number_of_members integer not null,

      rewardnumber integer,

   Constraints:
     PRIMARY KEY (id)


**Money Balance Table**

   Columns:
      id serial,

      clubs integer not null references clubs(id) on delete cascade on update cascade,

      incomes integer not null,

      expenses integer not null,

      profit integer not null,

   Constraints:
      PRIMARY KEY(id)


"Clubs" and "Money_balances" classes are written by me.::

   .. code-block:: pyhton
      class Clubs:
         def __init__(self, name, place, year, chair, number_of_members, rewardnumber):
            self.name = name
            self.place = place
            self.year = year
            self.chair = chair
            self.number_of_members = number_of_members
            self.rewardnumber = rewardnumber

      class Money_balances:
         def __init__(self, club, incomes, expenses, profit):
            self.club = club
            self.incomes = incomes
            self.expenses = expenses
            self.profit = profit


I have worked in "clubs.py" and "money_balance.py" sources

*clubs.py*

   Functions:
      add_club
         add_club function is used for adding club in the clubs table

      delete_club
         delete_club function is used to delete club with given id

      update_club
         update_club function is used to change data of the club with given id

      search_club
         search_club function returns the clubs that matches club name which given in search line

      get_club
         get_club function returns the data of single club to be editted.

      get_all_clubs
         get_all_clubs function returns all of the clubs to be viewed in the main clubs page

      get_country_names
         get_country_names function gets all country names to be listed for user interface

      get_clubs_page
         get_clubs_page function handles clubs_page requests

      get_clubs_edit_page
         get_clubs_edit_page function handles clubs_edit_page requests

*money_balance.py*

   Functions:
      add_money_balance
         add_money_balance function is used for adding money balance row in the money balance table

      delete_money_balance
         delete_money_balance function is used to delete money balance row with given id

      update_money_balance
         update_money_balance function is used to change data of the money balance row with given id

      search_money_balance
         search_money_balance function returns the money balance row that matches clubs name which given in search line

      get_money_balance
         get_money_balance function returns the data of single money balance row to be editted.

      get_all_money_balances
         get_all_money_balances function returns all of the money balance row to be viewed in the main money balance page

      get_clubs_names
         get_clubs_names function gets all clubs names to be listed for user interface

      get_money_balances_page
         get_money_balances_page function handles get_money_balances_page requests

      get_money_balances_edit_page
         get_money_balances_edit_page function handles get_money_balances_edit_page requests

Common:

   Functions:
      add_test_data
         add_test_data function is used to add sample data in database