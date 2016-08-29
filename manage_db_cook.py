#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Create an Database in MySQL and a table
# Insert new item in table
# Wizard mode for cook device
# Os: Linux
#
# Data:06-2016
#
# Copyrigth "(C)"2016,  Simone Dellabora
#
# This file is part cook-device
# cook-device is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Function for connect with network protocol ssh or telnet
# functions used in cookdevice.py
#
# run ./manage_db_cook.py -c             (create and import .csv)
# run ./manage_db_cook.py -m device.csv  (modify)
# run ./manage_db_cook.py -l             (list records in table)
# run ./manage_db_cook.py -d rec         (delete records in table)
# run ./manage_db_cook.py -d db          (delete full database)


# import module
import MySQLdb
import sys
import os
import re

# Color for text
GREEN =  '\033[32m'
RED =    '\033[31m'
YELLOW = '\033[33m'
BRIGHT = '\033[1m'
RESET =  '\033[0m'

# Function connect to mysql and create database, table and import a file csv
def create_db():
  try:
    print YELLOW,'Wizard creation Database for COOK DEVICE'
    print '','verify you have installed mysql and configured credential for access'
    print '','and verify if service of mysql is running (systemctl status mariadb.service \ mysql.service)'
    print '','or you start the mysql (systemctl start mariadb.service \ mysql.service)\n'
    print RESET

    user = raw_input('user: ')
    password  = raw_input('password: ')
    CONN = MySQLdb.connect(user=user, passwd=password)
    CUR = CONN.cursor()

    # create database
    database = raw_input('create new database: ')
    CUR.execute("CREATE DATABASE %s" % database)
    CUR.fetchone()
    print GREEN,'result: ok, %s' % database
    print RESET

    # use database created
    CUR.execute("USE %s" % database)

    # create table
    table = raw_input('insert new table name: ')
    CUR.execute("CREATE TABLE %s (Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, DeviceName VARCHAR(32), Ip VARCHAR(16), Session VARCHAR(8))" % table)
    CUR.fetchone()
    print GREEN,'result: ok, %s' % table
    print RESET

    # insert device in table
    path_file = raw_input('import file (.csv): ')
    query = "LOAD DATA LOCAL INFILE"
    query2 = " '%s'" % path_file
    query3 = " INTO TABLE %s FIELDS TERMINATED BY ',' (DeviceName, Ip, Session);\n" % table
    CUR.execute(query + query2 + query3)
    CONN.commit()
    CUR.fetchall()
    print GREEN,'ok, uploaded, %s' % path_file
    print RESET

    CUR.close()
    CONN.close()

  except MySQLdb.Error, e:
    try:
      print YELLOW, "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
      print 'exit', RESET
    except IndexError:
      print YELLOW, "MySQL Error: %s" % str(e), RESET
      print 'exit', RESET

      CUR.close()
      CONN.close()


# Function for insert new item into tables
def modify_table_db():
  try:
    print 'Modify database table for insert new device.'

    file_add_in_table = sys.argv[2]

    user = raw_input('user: ')
    password  = raw_input('password: ')
    CONN = MySQLdb.connect(user=user, passwd=password)
    CUR = CONN.cursor()

    print 'Databases found: \n'

    db = ("SHOW DATABASES")
    CUR.execute(db)
    response_db_list = CUR.fetchall()

    for row in response_db_list:
      print BRIGHT,'-',row[0]
    print RESET

    print ''

    database  = raw_input('database to modify: ')
    CUR.execute("USE %s" % database)

    print 'table found in %s: \n' % database
    tables = ("SHOW TABLES")
    CUR.execute(tables)
    response_tables_list = CUR.fetchall()

    for row in response_tables_list:
      print BRIGHT,'-',row[0]
    print RESET

    print ''

    table = raw_input('table name to insert new row: ')

    # insert device in table
    query = "LOAD DATA LOCAL INFILE"
    query2 = " '%s'" % file_add_in_table
    query3 = " INTO TABLE %s FIELDS TERMINATED BY ',' (DeviceName, Ip, Session);\n" % table
    CUR.execute(query + query2 + query3)
    CONN.commit()
    CUR.fetchall()
    print GREEN,'ok, uploaded file: %s' % file_add_in_table
    print RESET

    print 'records in %s: ' % table
    data = ("SELECT * FROM %s" % table)
    CUR.execute(data)
    response_tables_all_data = CUR.fetchall()

    for row in response_tables_all_data:
      print GREEN,'-',row[0],'-', row[1],'-', row[2],'-', row[3]
    print RESET

    CUR.close()
    CONN.close()

  except MySQLdb.Error, e:
    try:
      print YELLOW, "MySQL Error [%d]: %s" % (e.args[0], e.args[1]), RESET
    except IndexError:
      print YELLOW, "MySQL Error: %s" % str(e), RESET

      CUR.close()
      CONN.close()


# List data in database table
def list_table_db():
  try:
    print 'List all records of table'

    user = raw_input('user: ')
    password  = raw_input('password: ')
    CONN = MySQLdb.connect(user=user, passwd=password)
    CUR = CONN.cursor()

    print 'Databases found: \n'

    db = ("SHOW DATABASES")
    CUR.execute(db)
    response_db_list = CUR.fetchall()

    for row in response_db_list:
      print BRIGHT,'-',row[0]
    print RESET # reset color text

    print ''

    database  = raw_input('database: ')
    CUR.execute("USE %s" % database)

    print 'table found in %s : \n' % database
    tables = ("SHOW TABLES")
    CUR.execute(tables)
    response_tables_list = CUR.fetchall()

    for row in response_tables_list:
      print BRIGHT,'-',row[0]
    print RESET

    print ''

    table = raw_input('table: ')

    print 'records in %s: ' % table
    data = ("SELECT * FROM %s" % table)
    CUR.execute(data)
    response_tables_all_data = CUR.fetchall()

    for row in response_tables_all_data:
      print GREEN,'-',row[0],'-', row[1],'-', row[2],'-', row[3]
    print RESET

    CUR.close()
    CONN.close()

  except MySQLdb.Error, e:
    try:
      print YELLOW, "MySQL Error [%d]: %s" % (e.args[0], e.args[1]), RESET
    except IndexError:
      print YELLOW, "MySQL Error: %s" % str(e), RESET

      CUR.close()
      CONN.close()


# delete row in database table
def delete_row_in_table():
  try:
    print 'Delete record in table'

    user = raw_input('user: ')
    password  = raw_input('password: ')
    CONN = MySQLdb.connect(user=user, passwd=password)
    CUR = CONN.cursor()

    print 'Databases found: \n'

    db = ("SHOW DATABASES")
    CUR.execute(db)
    response_db_list = CUR.fetchall()

    for row in response_db_list:
      print BRIGHT,'-',row[0]
    print RESET

    print ''
    database  = raw_input('database: ')
    CUR.execute("USE %s" % database)

    print 'table found in %s: \n' % database
    tables = ("SHOW TABLES")
    CUR.execute(tables)
    response_tables_list = CUR.fetchall()

    for row in response_tables_list:
      print BRIGHT,'-',row[0]
    print RESET

    print ''

    table = raw_input('table: ')

    print 'records in %s: ' % table
    data = ("SELECT * FROM %s" % table)
    CUR.execute(data)
    response_tables_all_data = CUR.fetchall()

    for row in response_tables_all_data:
      print GREEN,'-',row[0],'-', row[1],'-', row[2],'-', row[3]
    print RESET

    print ''

    Id_List = raw_input('Enter the ID or more to be deleted: ').split()

    # Delete one or more records in database table
    List = []
    for Ids in Id_List:
        List.append(Ids)

    for Item in List:
      delete = ("DELETE FROM %s WHERE Id="'%s'"" % (table, Item))
      CUR.execute(delete)
      response_delete = CUR.fetchall()
      CONN.commit()

    print RED,'deleted'
    print RESET

    print ''

    print 'records in %s: ' % table
    data = ("SELECT * FROM %s" % table)
    CUR.execute(data)
    response_tables_all_data = CUR.fetchall()

    for row in response_tables_all_data:
      print GREEN,'-',row[0],'-', row[1],'-', row[2],'-', row[3]
    print RESET

    CUR.close()
    CONN.close()

  except MySQLdb.Error, e:
    try:
      print YELLOW,"MySQL Error [%d]: %s" % (e.args[0], e.args[1]), RESET
    except IndexError:
      print YELLOW,"MySQL Error: %s" % str(e), RESET

      CUR.close()
      CONN.close()


# Function to delete the full Database
def delete_full_database():
  try:
    print "Delete the full Database from MySQL"

    user = raw_input('user: ')
    password  = raw_input('password: ')
    CONN = MySQLdb.connect(user=user, passwd=password)
    CUR = CONN.cursor()

    print 'Databases found: \n'

    db = ("SHOW DATABASES")
    CUR.execute(db)
    response_db_list = CUR.fetchall()

    for row in response_db_list:
      print BRIGHT,'-',row[0],RESET
    print ''

    database = raw_input("Database: ")

    for line in response_db_list:
      data = re.search(database, str(line))
      if data:
        data.group(0)
        CUR.execute("DROP DATABASE %s;" % database)
        CUR.fetchall()
        CONN.commit()

    print RED,'deleted', RESET
    print ''

    db = ("SHOW DATABASES")
    CUR.execute(db)
    response_db_list = CUR.fetchall()

    for row in response_db_list:
      print BRIGHT,'-',row[0],RESET
    print ''

    CUR.close()
    CONN.close()

  except MySQLdb.Error, e:
    try:
      print YELLOW,"MySQL Error [%d]: %s" % (e.args[0], e.args[1]), RESET
    except IndexError:
      print YELLOW,"MySQL Error: %s" % str(e), RESET

      CUR.close()
      CONN.close()


# Main function
def main():

  banner_Option = """Use ./manage-db-cook.py with option:

 -c (Create db, table and import file CSV)
 -m device.csv (Modify one DB, table)
 -l (List all records table)
 -d rec (Delete records in table)
 -d db (Delete full database)
 """

  mod_option = "Use -m device.csv"

  delete_option = """ Use:
 -d rec (Delete records in table)
 -d db (Delete full database)"""

  option_ext = sys.argv

  try:
    if len(option_ext) > 1:
      if option_ext[1] == "-m": # modify database table
        if len(option_ext) > 2:
          modify_table_db()
        else:
          print mod_option
      elif option_ext[1] == "-c": # create new database and table
        create_db()
      elif option_ext[1] == "-l": # list records in table
        list_table_db()
      try:
        if option_ext[1] == "-d" and option_ext[2] == "db": # delete full database
          delete_full_database()
        elif option_ext[1] == "-d" and option_ext[2] == "rec":# delete records in table
          delete_row_in_table()
      except IndexError, e:
        print delete_option
    else:
      print banner_Option
  except KeyboardInterrupt, e:
    print "\nexit"

if __name__== '__main__':
  main()
