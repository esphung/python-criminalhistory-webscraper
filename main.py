# -*- coding: utf-8 -*-
# @Author: eric phung
# @Date:   2017-11-30 08:58:15
# @Last Modified 2018-06-08
# @Last Modified time: 2018-06-08 00:15:42


from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from record import *
from page import *

import json
import sys

import time
import datetime

import os
import math

from subprocess import call

inmate_search_url = 'http://inmateinfo.indy.gov/IML'

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def getCurrentTime():
	'''Return the time in seconds since the epoch as a floating point number'''
	return time.time()

def removeFile(file):
	''' remove trash '''
	try:
		os.remove(file)
	except Exception as e:
		raise e

def getTime():
	''' get current time '''
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	return st

def ASCII(arg):
	''' hashkeys from fullnames '''
	key = 0
	for char in arg:
		key += ord(char)
	return key

def formatJson(r):
	''' doesnt write file '''
	r = str(r)
	r = r.rstrip('\'')
	r = r.lstrip('\'')
	r = r.replace('\'','\"')
	r += '\n'
	r = json.dumps(r)
	loaded_r = json.loads(r)
	return loaded_r

def writeFile(file,data):
	''' simple file writing '''
	# write json file
	fw = open(file, mode='w')
	fw.write(data)
	fw.write('\n')
	fw.close()
	print('file written data/{}_data.json'.format(hashKey))
	return file

def readFile(filename):
	'''simple file reading'''
	try:
		file = open(filename,mode='r');# file object
		data = file.read();# read file
		return data
	except OSError:
		color_print('Failed: ',RED)
		print('cannot open', filename)
		return None

#following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)

def color_print(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)

def console():

	color_print('SUCCESS ', GREEN)
	print('================================')

	call(["prettyjson", file])

keepGoing = True;
fname = "John"
lname = "Doe"


#main loop
while (keepGoing == True):

	color_print('STARTING\n', YELLOW)

	# create record
	record = Record()
	# set fname for search
	record.fname = fname
	# set lname for search
	record.lname = lname
	record.data['fullname'] = { 'lname' : lname, 'fname' : fname }

	# find all info on person
	inmatePage = InmatePage(inmate_search_url)
	record.data['records'] = (inmatePage.getCriminalHistory(record.fname,record.lname))

	# format data for json data
	data = (formatJson(record.data))
	hashKey = ASCII((lname + fname))

	# check if file already exists
	file = 'data/{}_data.json'.format(hashKey)
	writeFile(file,data)

	# print info
	console()

	# cleanup
	removeFile('geckodriver.log')
	
	# end program loop
	keepGoing = False

	color_print('FINISHED\n', MAGENTA)