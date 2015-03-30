#!/usr/bin/python
# ***************************************************************************
# *   Copyright (C) 2012 by Marek Hakala   *
# *   hakala.marek@gmail.com   *
# *   Remote script launcher python script 0.0.1a   *
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

''' Remote script launcher '''

import os
import re
import sys
import getopt
import subprocess
import urllib.request

# Globals variables 
COMMANDS_FILES = "/home/marek/commands.csv"
TASKLIST_URL = 'http://my.server.ltd/~marek/remotecontrol/todolist.txt'

VERSION = "0.0.1a"

class CommandDef(object):
  '''
    A class representing the Command definition struct used by Remote script launcher API. 
  '''
  def __init__(self,
	      name=None,
	      cmd=None):
    self.name = name
    self.cmd = cmd

  def GetCmd(self):
    return self.cmd

  def Compare(self, info):
    if self.name == info.GetCommand():
      return True
    return False

  def GetName(self):
    return self.name

  def Run(self):
    os.system(self.cmd)

  def __repr__(self):
    return "name={0}|cmd={1}".format(self.name,self.cmd)

class CommandInfo(object):
  ''' 
  A class representing the Command info struct used by Remote script launcher API. 
  '''
  def __init__(self,
	   id=None,
	   ctype=None,
	   command=None,
	   note=None,
	   created=None):
    self.id = id
    self.ctype = ctype
    self.command = command
    self.note = note
    self.created = created

  def GetId(self):
    return self.id

  def GetType(self):
    return self.ctype

  def GetCommand(self):
    return self.command

  def GetNote(self):
    return self.note

  def GetCreated(self):
    return self.created
  
  def __repr__(self):
    return "id={0}|ctype={1}|command={2}|note={3}|created={4}".format(
	    self.id,self.ctype,self.command,self.note,self.created)
    

class CommandsWorker(object):
  ''' 
  A class representing the class for process commands. 
  '''
  def __init__(self,
	      commandsFilename=None):
    self.commandsFilename = commandsFilename
    self.LoadCommandsList()

  def GetFilename(self):
    return self.commandsFilename

  def LoadCommandsList(self):
    self.prepCommandsList = []
    print ( ":: Load commands list : {0}".format(self.commandsFilename) )
    
    self.f = open(self.commandsFilename)
    lines = self.f.readlines()
   
    for line in lines:
      line = line.replace("\n", "")
      largs = line.split("|")
      
      cmdDef = CommandDef(largs[0], largs[1])
      self.prepCommandsList.append(cmdDef)

  def DoRunCommand(self, info):
    print( ":: Search {0} command ...".format(info.GetCommand()) )
    
    for cmd in self.prepCommandsList:
      return self.CompareCommand(cmd, info)
    return False

  def CompareCommand(self, cmd, info):
    if cmd.Compare(info):
      print(":: {0} command found".format(info.GetCommand()))
      print ( ":: Start {0} command ... ".format(info.GetCommand()) )
      cmd.Run()
      return True
    
    print ( ":: {0} command not found".format(info.GetCommand()) )
    return False

# main function
def main():
    print ( ":: Remote command launcher v. {0}".format(VERSION) )
    # Fetch tasklist from web server
    req = urllib.request.Request(TASKLIST_URL)
    response = urllib.request.urlopen(req)

    # read site
    taskList = response.read()
    taskList = taskList.splitlines()

    # init empty commands list
    commandsList = []
    
    # init Commands worker
    if os.path.isfile(COMMANDS_FILES) is False:
      print ( ":: Error >> Commands file not exist : {0}".format(COMMANDS_FILES) )
      sys.exit(2)
    
    cmdWorker = CommandsWorker(COMMANDS_FILES)

    # parse input & insert into array
    for line in taskList:
      l = str(line, encoding='utf8')
      largs = l.split(";")
  
      # create command object & append to list
      command = CommandInfo(largs[0], largs[1], largs[2], largs[3], largs[4])
      commandsList.append(command)
      
      #print ( ":: DEBUG >> {0}".format(command), end="\n" )
      cmdWorker.DoRunCommand(command)
      sys.exit(0)

if __name__ == "__main__":
    main()
