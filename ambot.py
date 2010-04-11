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
		self.sayprivate( to_user, msg )

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


	def deliverPending( self, user ):
		if user in self.msgs:
			user_msgs = self.msgs[user]
			for msg in user_msgs:
				msg.send( self.client.sock )
			del user_msgs

	def sayprivate(self,user,msg):
		for line in msg.split("\n"):
			self.client.sock.send("SAYPRIVATE %s %s\n" % (user,line) )

	def printhelp(self,user):
		self.sayprivate( user,"To deliver a message to an offline user, pm to this bot: \"USERNAME MESSAGE\"\nYou can queue multiple messages if you like." )

	def onsaidprivate(self,user,message):
		if message == "optout" :
			print "not implemented"
		if message == "!help":
			self.printhelp( user )
		if message == ("help"):
			self.printhelp( user )
		else:
			tokens = message.split()
			if len(tokens) > 1:
				to_user = tokens[0]
				msg = ' '.join( tokens[1:] )
				if  user in self.users or user in self.admins:
					self.storeMsg( user, to_user, msg )
					if to_user in self.user_online:
						self.deliverPending( to_user )
						self.sayprivate( user, "the user was found online, the message was sent immediately" )
					else:
						self.sayprivate( user, "message queued, will be delivered as soon as the user gets online" )
			else:
				self.printhelp( user )

	def oncommandfromserver(self,command,args,socket):
		if command == "REMOVEUSER" and len(args) > 0:
			try:
				self.user_online.remove( args[0] )
			except:
				print ("failed to remove %s from online users" % (args[0]) )

		if command == "ADDUSER" and len(args) > 2:
			self.user_online.append( args[0] )
			self.deliverPending( args[0] )

	def onload(self,tasc):
	  self.client = tasc
	  self.app = tasc.main
	  self.admins = parselist(self.app.config["admins"],',')
	  self.users = parselist(self.app.config["users"],',')
