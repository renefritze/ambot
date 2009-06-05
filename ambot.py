# -*- coding: utf-8 -*-
from colors import *
from ParseConfig import *
import string
from utilities import *
from time import *

class PersistentList:
	filename = ""
	data = []
	def __init__(self,name):
		self.filename = name + ".list"

	def add(self,item):
		self.data.append(item)
	def remove(self,item):
		try:
			self.data.erase(item)
		except:
			print "error in erase"
			
	def sync(self,item):
		print "not impl"
		
	def contains(self,item):
		return item in data

class Message:
	from_user = ""
	to_user = ""
	added = ""
	msg_text = ""

	def __init__(self, from_u, to_u, msg ):
		self.msg_text = msg
		self.from_user = from_u
		self.to_user = to_u
		self.added = ctime()

	def send ( self, socket ):
		msg = ( "(%s) - %s: %s" % (strftime(self.added),self.from_user,self.msg_text) )
		socket.send( "SAYPRIVATE %s \"%s\" \n" % (self.to_user, msg) )

class Main:
	chans = []
	admins = []
	user_online = []
	user_optout = []
	msgs = dict()
	filename = ""

	min_pause = 5.0

	def storeMsg( self, from_user, to_user, msg ):
		if not to_user in self.user_optout:
			if not to_user in self.msgs:
				self.msgs[to_user] = []
			self.msgs[to_user].append( Message( from_user, to_user, msg ) )
		

	def deliverPending( self, user, socket ):
		if user in self.msgs:
			print "pre sending"
			user_msgs = self.msgs[user]
			for msg in user_msgs:
				print "sending"
				msg.send( socket )
			del user_msgs
		print "PENDING"
		print self.msgs

	def printhelp(self):
		print "help msg"

	def onsaidprivate(self,user,message):
		if message == "optout" :
			print "not implemented"
		if message == ("help"):
			self.printhelp
		else:
			tokens = message.split()
			if len(tokens) > 1:
				to_user = tokens[0]
				msg = ' '.join( tokens[1:] )
				print msg
				if  user in self.users or user in self.admins:		
					self.storeMsg( user, to_user, msg )
			else:
				print "error: not enough arguments"
		
	def oncommandfromserver(self,command,args,socket):
		if command == "REMOVEUSER" and len(args) > 0:
			try:
				self.user_online.remove( args[0] )
			except:
				print ("failed to remove %s from online users" % (args[0]) )
			
		if command == "ADDUSER" and len(args) > 2:
			self.user_online.append( args[0] )
			self.deliverPending( args[0], socket )
			


	def onload(self,tasc):
	  self.app = tasc.main
	  self.admins = parselist(self.app.config["admins"],',')
	  self.users = parselist(self.app.config["users"],',')

		