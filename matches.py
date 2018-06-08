import re

# matches
inmateName = r'^[a-z ,.-]+$'
permanentId = r'([0[1-9]{12})'
dates = r'(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.](19|20)\d\d'
bookingId = r'[0-9]{7}'



def findValue(key,value_list):

	# filter out names
	for item in value_list:
		value = item.lower()
		pattern = re.compile(key)
		match = pattern.match(value)
		if match:
			return item

def getDataSet(data):
	keepGoing = True
	while keepGoing:
		#print(len(data))

		i = 0
		data_set = {}
		# match if name
		if findValue(inmateName,data):
			data_set['inmateName'] = findValue(inmateName,data)
			data.remove(findValue(inmateName,data))

		# match if date
		if findValue(dates,data):
			data_set['birthdate'] = findValue(dates,data)
			data.remove(findValue(dates,data))

		# match if permanent id
		if findValue(permanentId,data):
			data_set['permanentId'] = findValue(permanentId,data)
			data.remove(findValue(permanentId,data))

		# match if booking id
		if findValue(bookingId,data):
			data_set['bookingId'] = findValue(bookingId,data)
			data.remove(findValue(bookingId,data))

		# match if date
		if findValue(dates,data):
			data_set['arrestdate'] = findValue(dates,data)
			data.remove(findValue(dates,data))

		return data_set
		keepGoing = False


def getMatchedDataFromLinks(keys,raw_values):
	data = []
	limit = (len(raw_values) - len(keys))

	keepGoing = True
	while keepGoing:
		#print('Remaining {}: {}'.format(len(raw_values),raw_values))

		if (len(raw_values)) <= 2:
			keepGoing = False
		else:
			data.append(getDataSet(raw_values))
			#keepGoing = False

	return data

"""
pattern = re.compile(inmateName)
results = pattern.match(test)

print(results)"""




