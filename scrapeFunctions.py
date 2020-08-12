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
		print(tr.prettify())
		if tr.has_attr('class'): # if <tr> element has 'thead' class, meaning it is a header row with no player info
			tr.decompose()

	return rush_tr_elements

# Takes a BeautifulSoup tag (from getPlayerRows, should be 100 element list of player data) and writes it to .csv 
def writePlayerRows():
	return