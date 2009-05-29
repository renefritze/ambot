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
	def sync(self,item):
		#write to file
	def contains(self,item):
		return item in data

class Main:
	chans = []
	admins = []
	faqs = dict()
	filename = ""
	last_faq = ""
	last_time = time()
	min_pause = 5.0
	def getFAQ(self,key,socket):
	    return "der"

	def printhelp(self):
		print "help msg"

	def onsaidprivate(self,user,message):
		tokens = message.split()
		if tokens[0] == "optout" :
			print "not implemented"
		if tokens[0].find("help") > 0 :
			self.printhelp
		else:
			if len(tokens) > 2:
				user = tokens[0]
				msg = tokens[1:]
			else:
				print "error: not enough arguments"
		
	def oncommandfromserver(self,command,args,socket):
	    if command == "ADDUSER" and len(args) > 2:
			if args[2] == "!faq" and len(args) > 3:
				now = time()
				user = args[1]
				diff = now - self.last_time
				if diff > self.min_pause :
					chan = args[0]
				#if self.chans.find(args[0]) > 0:
					msg = self.faqs[args[3]]
					lines = msg.split('\n')
					for line in lines :
						socket.send("SAY %s %s\n" % (chan,line))
						print ("SAY %s %s\n" % (chan,line))
				self.last_time = time()
			if args[2] == "!faqlearn" and args[1] in self.admins and len(args) > 4:
				self.addFaq( args[3], args[4:] )
			if args[2] == "!faqlist":
				faqstring = "available faq items are: "
				for key in self.faqs:
				    faqstring += key + " "
				socket.send("SAY %s %s\n" % (args[0],faqstring ))

	def ondestroy( self ):
	    self.saveFaqs()

	def onload(self,tasc):
	  self.app = tasc.main
	  self.admins = parselist(self.app.config["admins"],',')
	  self.users = parselist(self.app.config["users"],',')
	  self.loadFaqs()

		