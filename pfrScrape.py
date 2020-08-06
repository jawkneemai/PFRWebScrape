# Scrapes the Pro Football Reference website for player
# data (passing, rushing, receiving stats). Need this for
# ALL player's post merger (1970-2019) game logs for every
# single game they've played.

from bs4 import BeautifulSoup
import requests
import pprint

# Modules
pp = pprint.PrettyPrinter(indent=4)

# URLs: Queries list every player that has the respective stats. 
# Format: 100 players listed in a table element every page, click next button to get the next 100 players
rush_url = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=1970&year_max=2019&season_start=1&season_end=-1&pos%5B%5D=QB&pos%5B%5D=WR&pos%5B%5D=RB&pos%5B%5D=TE&is_starter=E&game_type=R&game_num_min=0&game_num_max=99&week_num_min=0&week_num_max=99&c5val=1.0&order_by=rush_att'
rec_url = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=1970&year_max=2019&season_start=1&season_end=-1&pos%5B%5D=QB&pos%5B%5D=WR&pos%5B%5D=RB&pos%5B%5D=TE&is_starter=E&game_type=R&game_num_min=0&game_num_max=99&week_num_min=0&week_num_max=99&c5val=1.0&order_by=rec'
pass_url = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=1970&year_max=2019&season_start=1&season_end=-1&pos%5B%5D=QB&pos%5B%5D=WR&pos%5B%5D=RB&pos%5B%5D=TE&is_starter=E&game_type=R&game_num_min=0&game_num_max=99&week_num_min=0&week_num_max=99&c5val=1.0&order_by=pass_yds'

# Other Variables
next_page_url = '&offset=' 
# Query to move to specified rank of the stat. (PFR only displays 100 players at a time)
# Add an integer after '=' to jump to specific rank.
# i.e.: Rushing: 41679 players with rushing attempts in any game

# Scraping Rushing Stats of ALL Players

isDone = 0 # Boolean for checking if end of stats table on PFR
counter = 0
#rush_url = rush_url + next_page_url + '200'
try:
	rush_page = requests.get(rush_url)
	rush_soup = BeautifulSoup(rush_page.content, 'html.parser')
	rush_tbody = rush_soup.find('tbody')
	rush_tr_elements = rush_tbody.find_all('tr')
except AttributeError:
	print('Error creating or navigating Soup object')

for tr in rush_tr_elements:
	if tr.has_attr('class'):
		print(tr.prettify())
	else:
		#print(tr.prettify())
		counter += 1
		print(counter)

while isDone == 0:
	counter += 1
	print(counter)
	isDone = 1
	#rush_page = requests.get(rush_url)
	#rush_soup = BeautifulSoup(rush_page.content, 'html.parser')

#rush_tr_elements = rush_soup.find_all('tr')
#for i in rush_tr_elements:
#	print(i, end='\n'*2)




#rec_page = requests.get(rec_url)
#pass_page = requests.get(pass_url)
#rec_soup = BeautifulSoup(rec_page.content, 'html.parser')
#pass_soup = BeautifulSoup(pass_page.content, 'html.parser')

#rec_tr_elements = rec_soup.find_all('tr')
#for i in rec_tr_elements:
#	print(i, end='\n'*2)

#pass_tr_elements = pass_soup.find_all('tr')
#for i in pass_tr_elements:
#	print(i, end='\n'*2)



### Functions ###
