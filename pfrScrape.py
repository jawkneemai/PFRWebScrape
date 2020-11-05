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
#counter = 0
#while (counter < 1):
	# Create URL for data of next 100 players (PFR only lists 100 players per request)
#	temp_url = pass_url + next_page_query + str(url_multiplier*counter) # modifies URL to generate next table of 100 player data
# 
	# Gather and parse player data (this is just for the 100 players)
#	temp_pass_table = getPlayerRows(temp_url)
#	for row in temp_pass_table:	
#		temp_data = parsePlayerRow(row) # temp_data is python dictionary of player data
#		if len(temp_data['pos']) < 1: # If field is empty from PFR
#			temp_data['pos'] = 'QB' # Need this for all positions, for some reason older players don't have a position indicated. 
#		writePlayerRow(temp_data, 'qb_game_logs.csv')
#	print(temp_data)
#	if(int(temp_data['pass_att']) < 1): break
#	counter += 1


# Scraping rushing stats of ALL players
#counter = 0
#while (counter < 1):
#	temp_url = rush_url + next_page_query + str(url_multiplier*counter)
#	temp_rush_table = getPlayerRows(temp_url)
#	for row in temp_rush_table:
#		temp_data = parsePlayerRow(row)
#		if len(temp_data['pos']) < 1:
#			temp_data['pos'] = 'RB'
#		writePlayerRow(temp_data, 'rb_game_logs.csv')
#	print(temp_data)
#	if (int(temp_data['rush_att']) < 1): break
#	counter += 1

# Scraping receiving stats of all players
#counter = 0
#while (counter < 1):
#	temp_url = rec_url + next_page_query + str(url_multiplier*counter)
#	temp_rec_table = getPlayerRows(temp_url)
#	for row in temp_rec_table:
#		temp_data = parsePlayerRow(row)
#		if len(temp_data['pos']) < 1:
#			temp_data['pos'] = 'WR'
#		writePlayerRow(temp_data, 'wr_game_logs.csv')
#	print(temp_data)
#	if (int(temp_data['rec']) < 1): break
#	counter += 1



# ~~ Combining player stats and calculating their fantasy points in 0, 0.5, 1 PPR ~~
# ~ Goes through the game logs in each of passing, rushing, and receiving logs ~
# ~ and combines their stats, based on game date, to calculate their fantasy points. ~

pass_file = 'game_logs/pass_game_logs.csv'
rec_file = 'game_logs/rec_game_logs.csv'
rush_file = 'game_logs/rush_game_logs.csv'
empty_row = [0 for x in range(34)]
rec_ind_ult_start = 23
rec_ind_ult_end = 30
rec_ind_row_start = 13
rec_ind_row_end = 20
rush_ind_ult_start = 30
rush_ind_ult_end = 34
rush_ind_row_start = 13
rush_ind_row_end = 17
fieldnames = {'fieldnames': ['player', 'pos', 'age', 'game_date', 'league_id', 
'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num', 'game_day_of_week', 
'pass_cmp', 'pass_att', 'pass_cmp_perc', 'pass_yds', 'pass_td', 'pass_int', 'pass_rating', 
'pass_sacked', 'pass_sacked_yds', 'pass_yds_per_att', 'pass_adj_yds_per_att', 'targets', 
'rec', 'rec_yds', 'rec_yds_per_rec', 'rec_td', 'catch_pct', 'rec_yds_per_tgt', 'rush_att', 
'rush_yds', 'rush_yds_per_att', 'rush_td']} 
ultimate_game_log = {}
# going to be the ultimate game log with all players' game logs. dict keys will be player names, 
# with value pairs of game log dates, which are dicts themselves. their value pair is a list
# that contains whatever stats they may have for that game log date (stats listed above as 'fieldnames')

with open(pass_file, newline='') as file:
	reader = csv.reader(file)
	for row in reader:
		temp_name = row[1]
		temp_game_date = row[4]
		empty_row = [0 for x in range(34)]

		# First create a dictionary for the player to store all the game log dates as values,
		# then adds game log dates as dictionaries as we go. 
		if temp_name in ultimate_game_log: # If player already exists in the dict, just add a new game date entry.
			ultimate_game_log[temp_name][temp_game_date] = empty_row
			ultimate_game_log[temp_name][temp_game_date][:23] = row[1:]
		else: # If player doesn't exist yet, create an key for them.
			ultimate_game_log[temp_name] = {}
			ultimate_game_log[temp_name][temp_game_date] = empty_row
			ultimate_game_log[temp_name][temp_game_date][:23] = row[1:]

# 'targets' at index 23 in fieldnames, index 13 in row
# 'rec_yds_per_tgt' at index 29 in fieldnames, index 19 in row
with open(rec_file, newline='') as file:
	reader = csv.reader(file)
	for row in reader:
		temp_name = row[1]
		temp_game_date = row[4]
		temp_row = row[rec_ind_row_start:rec_ind_row_end]
		empty_row = [0 for x in range(34)]

		if temp_name in ultimate_game_log: # If player already exists in ultimate_game_log from the passing stats
			if temp_game_date in ultimate_game_log[temp_name]: # If player already has a game log on that date inthe ultimate_game_log
				ultimate_game_log[temp_name][temp_game_date][rec_ind_ult_start:rec_ind_ult_end] = temp_row
				# append rec row to whatever indices they are
			else: # If a player exists but doesn't have a game log already in ultimate_game_log
				ultimate_game_log[temp_name][temp_game_date] = empty_row
				ultimate_game_log[temp_name][temp_game_date] = row[1:]
				# generate empty row and fill in whatever indices rec stats are
		else: # If player doesn't exist in ultimate_game_log, aka doesn't have any pass stats
			ultimate_game_log[temp_name] = {}
			ultimate_game_log[temp_name][temp_game_date] = empty_row
			ultimate_game_log[temp_name][temp_game_date] = row[1:]
			# generate empty row and fill in whatever indices rec stats are

# 'rush_att' at index 30 in fieldnames, index 13 in row
# 'rush_td' at index 33 in fieldnames, index 16 in row
with open(rush_file, newline='') as file:
	reader = csv.reader(file)
	for row in reader:
		temp_name = row[1]
		temp_game_date = row[4]
		temp_row = row[rush_ind_row_start:rush_ind_row_end]
		empty_row = [0 for x in range(34)]

		if temp_name in ultimate_game_log:
			if temp_game_date in ultimate_game_log[temp_name]:
				ultimate_game_log[temp_name][temp_game_date][rush_ind_ult_start:rush_ind_ult_end] = temp_row
				# append rush row to whatever indices they are
			else:
				ultimate_game_log[temp_name][temp_game_date] = empty_row
				ultimate_game_log[temp_name][temp_game_date] = row[1:]
				# generate empty row and fill in whatever indices rush stats are
		else: # If player doesn't exist in ultimate_game_log, aka doesn't have any pass OR rush stats
			ultimate_game_log[temp_name] = {}
			ultimate_game_log[temp_name][temp_game_date] = empty_row
			ultimate_game_log[temp_name][temp_game_date] = row[1:]
			# generate empty row and fill in whatever indices rush stats are

#pp.pprint(len(ultimate_game_log))
#pp.pprint(ultimate_game_log['Marcus Mariota'])
#pp.pprint(ultimate_game_log['Adrian Peterson'])
#pp.pprint(ultimate_game_log['Cooper Kupp'])

# Write ultimate game log into one csv file. 
for player in ultimate_game_log:
	for game in ultimate_game_log[player]:
		with open('ultimate_game_log.csv', 'a', newline='') as file:
			writer = csv.writer(file, delimiter=',')
			writer.writerow(ultimate_game_log[player][game]