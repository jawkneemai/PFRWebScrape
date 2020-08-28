import requests
from bs4 import BeautifulSoup

### Functions ###

# Gets the 100 rows of player data on a search query page. 
def getPlayerRows(url):	
	try:
		rush_page = requests.get(url)
		rush_soup = BeautifulSoup(rush_page.content, 'html.parser')
		rush_tbody = rush_soup.find('tbody')
		rush_tr_elements = rush_tbody.find_all('tr')
	except AttributeError:
		print('Error creating or navigating Soup object')

	for tr in rush_tr_elements:
		if tr.has_attr('class'): # if <tr> element has 'thead' class, meaning it is a header row with no player info
			tr.decompose()

	return rush_tr_elements

# Takes a BeautifulSoup tag (from getPlayerRow, should be 100 element list of tags) and returns an object with all player data 
def parsePlayerRow(single_player_row):
	player_data = {}
	for child in single_player_row[0].children:
		print(child.name)
	return player_data

# Takes playerData (list with all player data) and writes to specified csv file
def writePlayerRow(player_data, csv_file):
	return
