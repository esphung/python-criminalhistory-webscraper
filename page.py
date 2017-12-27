# -*- coding: utf-8 -*-
# @Author: homeuser
# @Date:   2017-11-30 06:50:38
# @Last Modified 2017-12-02
# @Last Modified time: 2017-12-02 03:13:00

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

from matches import *

class Pages(object):
	"""docstring for Pages"""
	def __init__(self):
		super(Pages, self).__init__()
		self.url = ""
		self.binary = FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox-bin')
		self.driver = webdriver.Firefox(firefox_binary=self.binary)

	def __del__(self):
		pass

	def tearDown(self):
		try:
			self.previousUrl = self.driver.current_url
			self.driver.delete_all_cookies()
			self.driver.quit()
			self.__del__()
		except:
			pass

class NamePage(Pages):
	"""docstring for NamePage"""
	def __init__(self,url):
		super(NamePage, self).__init__()
	
		self.url = url
		self.driver.get(self.url)

	def getName(self):
		elem = self.driver.find_element_by_name("usage_eng")
		elem.click()

		elem = self.driver.find_element_by_name("norare")
		elem.click()

		elem = self.driver.find_element_by_name("nodiminutives")
		elem.click()

		select = Select(self.driver.find_element_by_name('number'))
		select.select_by_index(0)

		select = Select(self.driver.find_element_by_name('gender'))
		select.select_by_index(0)

		elem = self.driver.find_element_by_xpath("/html/body/div[2]/div/center/table/tbody/tr[1]/td/form/table/tbody/tr[1]/td/input")
		elem.click()

		soup = BeautifulSoup(self.driver.page_source, 'html.parser')
		for link in soup.find_all('p'):
			firstname = link.text

		if firstname:
			firstname = firstname.rstrip(" ")
			return firstname
		
		self.tearDown()

class InmatePage(Pages):
	"""docstring for InmatePage"""
	def __init__(self,url):
		super(InmatePage, self).__init__()
		self.url = url

	def getCriminalHistory(self,fname,lname):
		self.driver.get(self.url);
		self.driver.implicitly_wait(10) # seconds

		elem = self.driver.find_element_by_name("systemUser_firstName")
		elem.send_keys(fname)

		elem = self.driver.find_element_by_name("systemUser_lastName")
		elem.send_keys(lname)

		elem = self.driver.find_element_by_name("releasedA")
		elem.click()

		elem = self.driver.find_element_by_xpath("/html/body/form[2]/table[2]/tbody/tr[4]/td[3]/table/tbody/tr[3]/td[1]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/a[1]/img")
		elem.click()

		# pull down info about person
		soup = BeautifulSoup(self.driver.page_source, 'html.parser')
		links = soup.find_all('a')

		keys = [ 'bookingNumber', 'inmateName', 'releaseDate', 'dateOfBirth','permanentId' ]
		values = []
		for link in links:
			values.append(str(link.text.rstrip(" ")))

		count = (len(values)//5)

		data = ( { 'results' : count, 'data' : getMatchedDataFromLinks(keys,values) } )

		self.tearDown()
		return data
