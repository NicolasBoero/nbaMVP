import pandas as pd
import requests
from bs4 import BeautifulSoup

#-----------------MVP RESULTS---------------------------------------------------------------------------------------------------------------------------------------------------------

mvp_voting = []

for year in range(1977, 2023):
  link = f'https://www.basketball-reference.com/awards/awards_{year}.html#mvp'
  r = requests.get(link)
  soup = BeautifulSoup(r.content, features='lxml')
  mvp = soup.find('tr', class_='over_header').decompose()
  mvp = soup.find(id='mvp')
  mvp = pd.read_html(str(mvp))[0]
  mvp['year'] = year
  mvp_voting.append(mvp)

mvp_voting = pd.concat(mvp_voting)
mvp_voting = mvp_voting[['Player', 'Share', 'year', 'Tm']]
mvp_voting = mvp_voting[mvp_voting['Tm'] != 'TOT']

# -------------------PLAYERS PER GAME STATS-----------------------------------------------------------------------------------------------------------------------

per_game_stats = []

for year in range(1977, 2023):
  link = f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html'
  r = requests.get(link)
  soup = BeautifulSoup(r.content, features='lxml')
  stats = soup.find('tr', class_='thead')
  stats = soup.find(id='div_per_game_stats')
  stats = pd.read_html(str(stats))[0]
  stats['year'] = year
  per_game_stats.append(stats)

per_game_stats = pd.concat(per_game_stats)
per_game_stats['Player'] = per_game_stats['Player'].str.replace('*', '')
per_game_stats = per_game_stats[per_game_stats['Player'] != 'Player']
per_game_stats = per_game_stats.drop_duplicates(subset = ['Player', 'year'], keep = 'first').reset_index(drop = True)
per_game_stats = per_game_stats[per_game_stats['Tm'] != 'TOT']
per_game_stats = per_game_stats.drop(columns = 'Rk')


# -----------------PLAYERS ADVANCED STATS---------------------------------------------------------------------------------------------------------------------------------------------------------

adv_stats = []

for year in range(1977, 2023):
  link = f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html'
  r = requests.get(link)
  soup = BeautifulSoup(r.content, features='lxml')
  adv = soup.find('tr', class_='thead')
  adv = soup.find(id='div_advanced_stats')
  adv = pd.read_html(str(adv))[0]
  adv['year'] = year
  adv_stats.append(adv)

adv_stats = pd.concat(adv_stats)
adv_stats['Player'] = adv_stats['Player'].str.replace('*', '')
adv_stats = adv_stats.drop_duplicates(subset = ['Player', 'year'], keep = 'first').reset_index(drop = True)
adv_stats = adv_stats[adv_stats['Tm'] != 'TOT']
adv_stats = adv_stats[['Player', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 
                       'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP', 'year']]


players_stats = per_game_stats.merge(adv_stats, on = ['Player', 'year']).merge(mvp_voting, on = ['Player', 'year', 'Tm'], how = 'left')
players_stats = players_stats.fillna(0)

# players_stats.to_excel('players_stats.xlsx')

# -----------------TEAMS STATS---------------------------------------------------------------------------------------------------------------------------------------------------------------------


teams = []

for year in range(1977, 2023):
  link = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
  r = requests.get(link)
  soup = BeautifulSoup(r.content, features='lxml')
  tm = soup.find('tr', class_='over_header').decompose()
  tm = soup.find(id='advanced-team')
  tm = pd.read_html(str(tm))[0]
  tm['year'] = year
  teams.append(tm)
  
teams = pd.concat(teams)
teams = teams[['Team', 'W', 'L', 'year']]
teams = teams[teams['Team'] != 'League Average']
print(teams)
teams['Team'] = teams['Team'].str.replace('*', '')
teams['Tm'] = teams['Team'].replace(('Los Angeles Lakers', 'Houston Rockets', 'Golden State Warriors', 'Atlanta Hawks', 'Portland Trail Blazers', 'San Antonio Spurs', 'Phoenix Suns', 'Utah Jazz', 'Cleveland Cavaliers','Washington Wizards','Denver Nuggets', 'Los Angeles Clippers', 'Boston Celtics', 'Dallas Mavericks', 'Toronto Raptors', 'Milwaukee Bucks', 'Orlando Magic', 'Philadelphia 76ers', 'Detroit Pistons', 'New York Knicks', 'Minnesota Timberwolves','Sacramento Kings', 'Miami Heat', 'Chicago Bulls', 'Memphis Grizzlies', 'Indiana Pacers', 'Oklahoma City Thunder', 'New Jersey Nets', 'Charlotte Hornets', 'Charlotte Bobcats', 'Brooklyn Nets', 'Seattle SuperSonics', 'New Orleans Hornets', 'New Orleans Pelicans', 'Vancouver Grizzlies', 'New Orleans/Oklahoma City Hornets', 'Washington Bullets', 'Kansas City Kings', 'San Diego Clippers', 'New Orleans Jazz', 'Buffalo Braves', 'Kansas City-Omaha Kings', 'New York Nets'), 
                      ('LAL', 'HOU', 'GSW', 'ATL', 'POR', 'SAS', 'PHO', 'UTA', 'CLE', 'WAS', 'DEN', 'LAC', 'BOS', 'DAL', 'TOR' ,'MIL', 'ORL', 'PHI', 'DET', 'NYK', 'MIN', 'SAC', 'MIA', 'CHI', 'MEM', 'IND', 'OKC', 'NJN', 'CHO', 'CHA', 'BKN', 'SEA', 'NOH', 'NOP', 'VAN', 'NOK', 'WSB', 'KCK', 'SDC', 'NOJ', 'BUF', 'KCO', 'NYN'))
teams.loc[(teams['year'] < 2003) & (teams['Tm'] == 'CHO'), 'Tm'] = 'CHH'
teams['W/L%'] = round(teams['W'] /( teams['L'] + teams['W']), 3)
teams['TG'] = teams['W'] + teams['L']

# teams.to_excel('team_stats.xlsx')

# -----------------MERGING ALL DATAS INTO ONE DF---------------------------------------------------------------------------------------------------------------------------------------------------------

final = players_stats.merge(teams, on = ['Tm', 'year'])
final = final.rename(columns = {'PF' : 'FOULS'})
final = final.astype({'Age': 'int64', 'G': 'int64', 'GS': 'int64', 'MP': 'float64', 'FG': 'float64', 'FGA': 'float64', 'FG%': 'float64', '3P': 'float64',
       '3PA': 'float64', '3P%': 'float64', '2P': 'float64', '2PA': 'float64', '2P%': 'float64', 'eFG%': 'float64', 'FT': 'float64', 'FTA': 'float64', 'FT%': 'float64', 'ORB': 'float64',
       'DRB': 'float64', 'TRB': 'float64', 'AST': 'float64', 'STL': 'float64', 'BLK': 'float64', 'TOV': 'float64', 'PTS': 'float64', 'year': 'int64',
       'PER': 'float64', 'TS%': 'float64', '3PAr': 'float64', 'FTr': 'float64', 'ORB%': 'float64', 'DRB%': 'float64', 'TRB%': 'float64', 'AST%': 'float64', 'STL%': 'float64',
       'BLK%': 'float64', 'TOV%': 'float64', 'USG%': 'float64', 'OWS': 'float64', 'DWS': 'float64', 'WS': 'float64', 'WS/48': 'float64', 'OBPM': 'float64', 'DBPM': 'float64',
       'BPM': 'float64', 'VORP': 'float64', 'Share': 'float64', 'W': 'int64', 'L': 'int64', 'TG': 'int64'})
final['GMissed%'] = round(1 - (final['G'] / final['TG']), 2)
final = final.drop(columns = 'TG')

# final.to_excel('final.xlsx')

print(final)
