COOK_DEVICE

Author: Simone Dellabora
email: sdellab83@gmail.com
Version:1.0

 Copyrigth "(C)"2016,  Simone Dellabora

 cook-device is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

###################################################################
Instruction for linux os. 

Description:

Cook Device is a program that allows you to search within a database your devices
(es. Server, Switch...) and connect to them in a few steps across from the command line.


Dependencies:

MySQLdb, pexpect

For install execute:
apt-get or dnf install python-mysqldb
pip install pexpect


Instructions:

- Install Mysql and create a credential to access
  and control service MySQL is running.

- Modify device.csv for import new device in Database
  sample format:

SERVER1,192.168.1.1,ssh
SERVER2,192.168.1.2,telnet


- Run ./manage_db_cook.py for creating o modify database:

run with options:
 ./manage_db_cook.py -c             (create and import .csv)
 ./manage_db_cook.py -m device.csv  (modify)
 ./manage_db_cook.py -l             (list records in table)
 ./manage_db_cook.py -d rec         (delete records in table)
 ./manage_db_cook.py -d db          (delete full database)

- Modify configcook.cfg insert credentials, database and table created with manage-db-cook.

- Run program cook_device.py for use to search and connect to your device.

###################################################################

