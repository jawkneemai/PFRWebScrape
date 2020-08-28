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
def parsePlayerRow(single_player_row, player_type):
	# Player Type: 0 = RB, 1 = WR, 2 = QB
	player_data = {}
	unparsed_data = [];

	# Gets all descendant elements of BeautifulSoup Tag object
	for child in single_player_row.children:
		for descendants in child.descendants:
			unparsed_data.append(descendants)

	# Player Stat Categories listed below
	if player_type == 0: # for RBs
		player_data.update({'name': unparsed_data[2],
							'position': unparsed_data[3],
							'age': unparsed_data[4],
							'game_date': unparsed_data[6],
							'team': unparsed_data[10],
							'week': unparsed_data[15],
							'attempts': unparsed_data[17],
							'yardage': unparsed_data[18],
							'tds': unparsed_data[20] })
	elif player_type == 1: # for WRs
		player_data.update({'name': unparsed_data[2],
							'position': unparsed_data[3],
							'age': unparsed_data[4],
							'game_date': unparsed_data[6],
							'team': unparsed_data[10],
							'week': unparsed_data[16],
							'targets': unparsed_data[18],
							'receptions': unparsed_data[19],
							'yardage': unparsed_data[20],
							'tds': unparsed_data[22] })		
	elif player_type == 2: # for QBs
		player_data.update({'name': unparsed_data[3],
							'position': unparsed_data[4],
							'age': unparsed_data[5],
							'game_date': unparsed_data[7],
							'team': unparsed_data[11],
							'week': unparsed_data[16],
							'completions': unparsed_data[18],
							'attempts': unparsed_data[19],
							'yardage': unparsed_data[21],
							'tds': unparsed_data[22],
							'interceptions': unparsed_data[23],
							'pass_rating': unparsed_data[24] })
	else: print('Invalid Player Type')
	return player_data

# Takes playerData (list with all player data) and writes to specified csv file
def writePlayerRow(player_data, csv_file):
	return
