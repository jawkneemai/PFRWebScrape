# Scrapes the Pro Football Reference website for player
# data (passing, rushing, receiving stats). Need this for
# ALL player's post merger (1970-2019) game logs for every
# single game they've played.

from bs4 import BeautifulSoup
import requests
import pprint
import scrapeFunctions
import csv

# Modules
pp = pprint.PrettyPrinter(indent=4)
getPlayerRows = scrapeFunctions.getPlayerRows
parsePlayerRow = scrapeFunctions.parsePlayerRow
writePlayerRow = scrapeFunctions.writePlayerRow


# URLs: Queries list every player that has the respective stats. 
# Format: 100 players listed in a table element every page, click next button to get the next 100 players
rush_url = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=1970&year_max=2019&season_start=1&season_end=-1&pos%5B%5D=QB&pos%5B%5D=WR&pos%5B%5D=RB&pos%5B%5D=TE&is_starter=E&game_type=R&game_num_min=0&game_num_max=99&week_num_min=0&week_num_max=99&c5val=1.0&order_by=rush_att'
rec_url = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=1970&year_max=2019&season_start=1&season_end=-1&pos%5B%5D=QB&pos%5B%5D=WR&pos%5B%5D=RB&pos%5B%5D=TE&is_starter=E&game_type=R&game_num_min=0&game_num_max=99&week_num_min=0&week_num_max=99&c5val=1.0&order_by=rec'
pass_url = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=1970&year_max=2019&season_start=1&season_end=-1&pos%5B%5D=QB&pos%5B%5D=WR&pos%5B%5D=RB&pos%5B%5D=TE&is_starter=E&game_type=R&game_num_min=0&game_num_max=99&week_num_min=0&week_num_max=99&c5val=1.0&order_by=pass_yds'


# Other Variables
next_page_query = '&offset=' 
# Query to move to specified rank of the stat. (PFR only displays 100 players at a time)
# Add an integer after '=' to jump to specific rank.
# i.e.: Rushing: 41679 players with rushing attempts in any game
url_multiplier = 100
isDone = 0 # Boolean for checking if end of stats table on PFR

#qbrows = getPlayerRows(pass_url)
#player_data = parsePlayerRow(qbrows[0])
#print(player_data)

# ~~ All scraping done below ~~ #

# Scraping Passing Stats of ALL Players
counter = 0
while (counter < 1):
	# Create URL for data of next 100 players (PFR only lists 100 players per request)
	temp_url = pass_url + next_page_query + str(url_multiplier*counter) # modifies URL to generate next table of 100 player data
 
	# Gather and parse player data (this is just for the 100 players)
	temp_pass_table = getPlayerRows(temp_url)
	for row in temp_pass_table:	
		temp_data = parsePlayerRow(row) # temp_data is python dictionary of player data
		if len(temp_data['pos']) < 1: # If field is empty from PFR
			temp_data['pos'] = 'QB' # Need this for all positions, for some reason older players don't have a position indicated. 
		writePlayerRow(temp_data, 'qb_game_logs.csv')
	print(temp_data)
	if(int(temp_data['pass_att']) < 1): break
	counter += 1


# Scraping rushing stats of ALL players
counter = 0
while (counter < 1):
	temp_url = rush_url + next_page_query + str(url_multiplier*counter)
	temp_rush_table = getPlayerRows(temp_url)
	for row in temp_rush_table:
		temp_data = parsePlayerRow(row)
		if len(temp_data['pos']) < 1:
			temp_data['pos'] = 'RB'
		writePlayerRow(temp_data, 'rb_game_logs.csv')
	print(temp_data)
	if (int(temp_data['rush_att']) < 1): break
	counter += 1

# Scraping receiving stats of all players
counter = 0
while (counter < 1):
	temp_url = rec_url + next_page_query + str(url_multiplier*counter)
	temp_rec_table = getPlayerRows(temp_url)
	for row in temp_rec_table:
		temp_data = parsePlayerRow(row)
		if len(temp_data['pos']) < 1:
			temp_data['pos'] = 'WR'
		writePlayerRow(temp_data, 'wr_game_logs.csv')
	print(temp_data)
	if (int(temp_data['rec']) < 1): break
	counter += 1
