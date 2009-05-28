# -*- coding: utf-8 -*-
from colors import *
from ParseConfig import *
import string
from utilities import *
from time import *
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

	def oncommandfromserver(self,command,args,socket):
	    if command == "SAID" and len(args) > 2:
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
	
	def loadFaqs( self ):
		faqfile = open(self.filename,'r')
		content = faqfile.read()
		entries = content.split('|')
		i = 0
		while i < len(entries) - 1  :
			self.faqs[entries[i]] = entries[i+1]
			i += 2
		faqfile.close()
	
	def saveFaqs( self ):
		faqfile = open(self.filename,'w')
		for key,msg in self.faqs.items():
			faqfile.write( key + "|" + msg + "|" )
		faqfile.flush()
		faqfile.close()

	def addFaq( self, key, args ):
		msg = " "
		for arg in args :
			msg +=  arg + " "
		if msg != "" :
			msg = msg.replace( "\\n", '\n' )
			self.faqs[key] = msg
		self.saveFaqs()
		
	def ondestroy( self ):
	    self.saveFaqs()
	
	def onload(self,tasc):
	  self.app = tasc.main
	  self.chans = parselist(self.app.config["channels"],',')
	  self.admins = parselist(self.app.config["admins"],',')
	  self.filename = parselist(self.app.config["faqfile"],',')[0]
	  self.loadFaqs()