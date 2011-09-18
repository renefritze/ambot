# -*- coding: utf-8 -*-
import string
from time import *
import cPickle as pickle

from tasbot.config import Config
from tasbot.utilities import *
from tasbot.plugin import IPlugin


class Message:
	def __init__(self, from_u, to_u, msg ):
		self.msg_text = msg
		self.from_user = from_u
		self.to_user = to_u
		self.added = ctime()

	def send ( self, socket ):
		msg = ( "(%s) - %s: %s" % (strftime(self.added),self.from_user,self.msg_text) )
		for line in msg.split("\n"):
			socket.send("SAYPRIVATE %s %s\n" % (self.to_user,line) )


class Main(IPlugin):
	def __init__(self,name,tasc):
		super(Main,self).__init__(name,tasc)
		self.chans = []
		self.admins = []
		self.user_online = []
		self.user_optout = []
		self.msgs = dict()
		self.filename = ""
		self.min_pause = 5.0
		self.message_dump = 'messages.bin'

	def storeMsg( self, from_user, to_user, msg ):
		if not to_user in self.user_optout:
			if not to_user in self.msgs:
				self.msgs[to_user] = []
			self.msgs[to_user].append( Message( from_user, to_user, msg ) )

	def deliverPending( self, user ):
		if user in self.msgs:
			user_msgs = self.msgs[user]
			for msg in user_msgs:
				msg.send( self.tasclient.socket )
			del self.msgs[user]

	def printhelp(self,user):
		self.tasclient.saypm( user,"To deliver a message to an offline user, pm"
			"to this bot: \"USERNAME MESSAGE\"\nYou can queue multiple messages if you like." )

	def cmd_saidprivate(self, args, tas_command):
		message = ''.join(args[1:])
		user = args[0]
		if message == "optout" :
			self.logger.error("not implemented")
		if message == "!help":
			self.printhelp( user )
		if message == ("help"):
			self.printhelp( user )
		else:
			tokens = args[1:]
			if len(tokens) > 1:
				to_user = tokens[0]
				msg = ' '.join( tokens[1:] )
				if  user in self.users or user in self.admins:
					self.storeMsg( user, to_user, msg )
					if to_user in self.user_online:
						self.deliverPending( to_user )
						self.tasclient.saypm( user,
							"the user was found online, the message was sent immediately" )
					else:
						self.tasclient.saypm( user,
							"message queued, will be delivered as soon as the user gets online" )
			else:
				self.printhelp( user )

	def cmd_removeuser(self, args, tas_command):
		try:
			self.user_online.remove( args[0] )
		except:
			self.logger.info("failed to remove %s from online users" % (args[0]) )

	def cmd_adduser(self, args, tas_command):
		self.user_online.append( args[0] )
		self.deliverPending( args[0] )

	def onload(self,tasc):
		self.app = tasc.main
		self.admins = self.app.config.get_optionlist('tasbot', "admins")
		self.users = self.app.config.get_optionlist('ambot', "users")
		try:
			self.msgs = pickle.load(open(self.message_dump, 'rb'))
		except:
			self.msgs = dict()

	def onexit(self):
		pickle.dump( self.msgs, open(self.message_dump, 'wb'))
