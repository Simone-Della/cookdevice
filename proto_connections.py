#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyrigth "(C)"2016,  Simone Dellabora
#
# This file is part cook-device
# cook-device is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
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
# Version: 1.0
# Date: 06-2016

# import module
import os
import pexpect

# function for connecting in telnet
def telnet_connections(ip_device):
  os.system('telnet %s' % ip_device)

# function for connecting in ssh
def ssh_connections(ip_device):
  username = raw_input('username: ')
  session = pexpect.spawn('ssh %s@%s' % (username, ip_device))
  session.setwinsize(24, 180)
  session.interact()
