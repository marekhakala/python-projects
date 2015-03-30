#!/usr/bin/python
# ***************************************************************************
# *   Copyright (C) 2012 by Marek Hakala   *
# *   hakala.marek@gmail.com   *
# *   What is my public IP python script 0.0.1   *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Library General Public License as       *
# *   published by the Free Software Foundation; either version 2 of the    *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the                 *
# *   Free Software Foundation, Inc.,                                       *
# *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
# ***************************************************************************

''' IP Info '''

import os
import re
import sys
import getopt
import urllib
import urllib.request

# Globals variables 
URL = 'http://wtfismyip.com/xml'
VERSION = "0.0.1"

from xml.dom.minidom import parseString

class IpInfo(object):

  def __init__(self,
	      addr=None,
	      location=None,
	      hostname=None):
    self.addr = addr
    self.location = location
    self.hostname = hostname

  def GetAddr(self):
    return self.cmd

  def GetLocation(self):
    return self.name

  def GetHostname(self):
    return self.hostname

  def __repr__(self):
    line = "========================================================"
    before = line + "\n"
    after = "\n" + line + "\n"
    
    return "{0}IP \t\t\t= {1}\nLocation \t\t= {2}\nHostname \t\t= {3} {4}".format(before, self.addr,
    self.location, self.hostname, after)

class IPXMLParser(object):
  def __init__(self, dom=None):
    self.dom = dom
    self.doc = dom.getElementsByTagName("wtf")
    self.handle(self.doc[0])
  
  def getInfo(self):
    return self.info;
  
  def getElement(self, element):
    return self.getText(element.childNodes)
        
  def getText(self, nodeList):
    rc = ""
  
    for node in nodeList:
      rc += self.getRc(node)
      
    return rc
        
  def getRc(self, node):
    if node.nodeType == node.TEXT_NODE:
      return node.data
    return ""

  def handle(self, appt):
    addr = self.getElement(appt.getElementsByTagName("your-fucking-ip-address")[0])
    location = self.getElement(appt.getElementsByTagName("your-fucking-location")[0])
    hostname = self.getElement(appt.getElementsByTagName("your-fucking-hostname")[0])
    
    self.info = IpInfo(addr, location, hostname)

# main function
def main():
  #download the content
  req = urllib.request.Request(URL)
  response = urllib.request.urlopen(req)

  # read
  data = response.read()

  # parse the xml
  dom = parseString(data)
  parser = IPXMLParser(dom)

  # print
  print( "\n:: IP addr info (script) {0}\n".format(VERSION) ) 
  print( parser.getInfo() )

if __name__ == "__main__":
    main()

