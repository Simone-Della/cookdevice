#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  --- Cook Device ---
# Search device in mysql and connect with network protocol ssh or telnet
# Connect to Mysql in Database with one table
# Author: Simone Dellabora
# Os: Linux
# Version: 1.0
# Date: 06-2016
#
# Copyrigth "(C)"2016,  Simone Dellabora
#
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

# import module
# import proto_connections as a module file: proto_connections.py
import MySQLdb
import re
import sys
import proto_connections

# Colore text
GREEN =  '\033[32m'
YELLOW = '\033[33m'
RESET =  '\033[0m'

# Global
FILENAME = "configcook.cfg"
fileopen = open(FILENAME, 'r')
fileopen.readline()
line = []
for item in fileopen:
  line.append(item)

# GLlobal variable
CONN = MySQLdb.connect(user=line[1][:-1], passwd=line[3][:-1], db=line[5][:-1])
CUR = CONN.cursor()

# perform banner
def banner():
  print YELLOW,'Cook Device v1.0\r'
  print '','Search and connect to the device\r'
  print RESET,'\r'

# Function search in database mysql
def search(userdate):

  CUR.execute("SELECT Id, Ip, DeviceName FROM %s" % line[7][:-1])
  row = CUR.fetchone()

  while row is not None:
    rows = str(row[0]), row[1], row[2]
    row = CUR.fetchone()
    for items in rows:
      word = re.search(userdate, items, re.IGNORECASE)
      ra = ' '+rows[0]+' - '
      rb = rows[1] #ip dispositivo
      rc =' - '+rows[2]
      # print row searched in database
      ItemFound = ra + rb + rc
      if word:
        # [global] variable in condition in def main(), if no match word in userdate exit()
        global global_ItemFound
        global_ItemFound = word.group()
        print GREEN, ItemFound, RESET

# Function search ID in database mysql and perform connection to device
def search_ID_in_list_and_connect(search_ID):

  CUR.execute("SELECT Id, Ip, DeviceName, Session FROM %s" % line[7][:-1])
  row = CUR.fetchone()

  while row is not None:
    rows = {row[0] : row[1]}
    type_protocol = row[3]
    row = CUR.fetchone()
    for key in rows.keys():
      if search_ID == key:
        rb1 = str(rows.values())
        ip_device = rb1[2:-2]
        # verify where you try to connect
        print 'Connect to: ' + ip_device
        # condition which protocol use, view in coloumn session in db
        if 'ssh' in type_protocol:
          proto_connections.ssh_connections(ip_device)
        else:
          proto_connections.telnet_connections(ip_device)

  CUR.close()
  CONN.close()

# main function
def main():

  banner()
  # search device but is empty return device not found!
  try:
    userdate = raw_input('Search: ')
    while len(userdate) <= 0:
      userdate = raw_input('Search: ')
    search(userdate)
    # search ID for connect but if empty exit
    global_ItemFound
    search_ID = input('Connect to ID: ')
    search_ID_in_list_and_connect(search_ID)
  # manage exception KeyboardError ctrl+c and NameError
  except KeyboardInterrupt, e:
      print "\nexit"
  except NameError, e:
      print "%s, not found !" % userdate
  except EOFError, e:
      print "\nEOFError, exit"
  except SyntaxError, e:
      print "\nSyntaxError, exit"

if __name__== '__main__':
  main()
