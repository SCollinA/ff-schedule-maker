"""This is an app to create randomized divisions and a random schedule for a fantasy football league. The app takes number of teams, number of divisions, and number of playoff teams as input. All teams must play everyone in their division twice. Non-division opponents are random."""

from random import choice
from time import sleep
import sys
import copy

while True:
    number_of_teams = int(input("Enter an even number of teams between 8 and 16: ")) # 8 - 16
    if number_of_teams < 8 or number_of_teams > 16 or number_of_teams % 2 != 0:
        print("You have entered an invalid number of teams.")
    else:
        break

while True:
    number_of_divisions = int(input("Enter number of divisions: ")) # make sure number of teams goes into number of divisions evenly, use drop down to provide appropriate choices # also must be at least 2. 8 teams cannot play each other twice and have playoffs in 16 week season. playoffs is at least 1 week. 14 teams has 2 divisions can only play each other twice with 1 round of playoffs
    if number_of_teams % number_of_divisions != 0 or number_of_divisions < 2 or number_of_divisions > number_of_teams / 2:
        print("League must have at least 2 divisions, each with an equal number of teams and at least 2 teams each.") # divisions must have at least 4 teams
    else:
        break

teams_per_division = int(number_of_teams / number_of_divisions)
minimum_weeks_of_regular_season = (teams_per_division - 1) * 2
def playoff_rounds(number_of_playoff_teams):
    num_teams = number_of_playoff_teams
    rounds_of_playoffs = 0
    while num_teams > 1:
        rounds_of_playoffs += 1
        num_teams /= 2
    return rounds_of_playoffs

while True:
    number_of_playoff_teams = int(input("Enter number of playoff teams: ")) # no greater than number of teams, no less than 2 # will be used to determine number of weeks of play # must also be less than twice the number of teams in division. max playoff rounds is 4 for 16 teams, so 16 team division needs 4 divisions. 14 team league can have 2 weeks playoffs
    if number_of_playoff_teams > number_of_teams or number_of_playoff_teams < 2 or 16 - minimum_weeks_of_regular_season < playoff_rounds(number_of_playoff_teams):# or number_of_playoff_teams > (16 - minimum_weeks_of_regular_season) * 2:
        print("Playoff teams must be at least 2 and less than total number of teams.")
    else:
        break

weeks_of_playoffs = playoff_rounds(number_of_playoff_teams)
weeks_of_regular_season = 16 - weeks_of_playoffs 

# assign number of teams indicated to the league
all_teams = []
for i in range(1, number_of_teams + 1):
    all_teams.append("Team" + str(i))

# assign number of divisions to the league
league = {}
for i in range(1, number_of_divisions + 1):
    league["Division" + str(i)] = []

# assign teams to divisions
teams = all_teams.copy()
for division in league:
    for i in range(0, teams_per_division):#number_of_teams / number_of_divisions):
        team = teams[0]
        league[division].append(team)
        teams.remove(team)

print(league)
print(weeks_of_regular_season)
print(weeks_of_playoffs)
sleep(3)

schedule = {}
non_division_games_per_team = {}
home_games_per_team = {}
away_games_per_team = {}

all_games = [[home_team, away_team] for home_team in all_teams for away_team in all_teams if home_team is not away_team]
scheduled_games = [] # record of all teams that have played each other outside of division. should contain no duplicates
checked_games = {}

max_division_games = (teams_per_division - 1) * 2
max_non_division_games = weeks_of_regular_season - max_division_games
max_home_games = (weeks_of_regular_season / 2) if (weeks_of_regular_season % 2 == 0) else ((weeks_of_regular_season / 2) + 1)
max_away_games= max_home_games # if odd number of games, some teams may have one more home game or away game

for team in all_teams:
    non_division_games_per_team[team] = 0
    home_games_per_team[team] = 0 # max is number of total games / 2 or (num of games / 2) + 1 if odd num of games
    away_games_per_team[team] = 0

for i in range(1, weeks_of_regular_season + 1):
    schedule["Week" + str(i)] = [] # schedule is dictionary of weekly keys with lists of games as lists of two teams that week
    checked_games["Week" + str(i)] = []

def add_next_game():
    current_week = 0
    for week in schedule: # go through weeks of schedule one by one
        current_week += 1
        if len(schedule[week]) == 0: # new week beginning, clear checked games
            checked_games[week].clear()
        while len(schedule[week]) < len(all_teams) / 2: # while the week is not full, continue choosing, checking, adding games
            possible_games = find_games(all_games, week, checked_games[week])
            if len(possible_games) == 0: # if no games are possible
                return False
            game = choice(possible_games) # choose game for this week
            checked_games[week].append(game) # add game to checked_games for this week
            if check_game(game, week): # if game fits scheduling rules
                add_game(game, week) # add game to schedule for that week
                if not add_next_game(): # try to add next game, passing current path, and if it returns bad path    
                    remove_game(game, week) # remove just that game
    return True

def find_games(possible_games, week, checked_games): # determines which games are allowable
    scheduled_teams = []
    for game in schedule[week]:
        scheduled_teams.append(game[0])
        scheduled_teams.append(game[1])
    possible_games = [game for game in possible_games if game not in scheduled_games] # games not scheduled this season
    possible_games = [game for game in possible_games if game not in checked_games] # games not checked this week
    possible_games = [game for game in possible_games if game[0] not in scheduled_teams and game[1] not in scheduled_teams] # games without teams scheduled this week
    return possible_games

def check_game(game, week): # checks to see if a game fits rules of scheduling
    #print("Checking game... " + str(game))
    if divisional_game(game):
        return True
    elif non_division_games_per_team[game[0]] < max_non_division_games and non_division_games_per_team[game[1]] < max_non_division_games:
        if home_games_per_team[game[0]] < max_home_games and away_games_per_team[game[1]] < max_away_games:
            if [game[1], game[0]] in scheduled_games:
            # they have played all other non division games
                if played_all_non_div_teams(game[0]) and played_all_non_div_teams(game[1]):
                    return True
            else:
                return True
    return False
                        
def add_game(game, week): # adds a new game to the schedule
    #print("Adding game... " + str(game))
    schedule[week].append(game)
    scheduled_games.append(game)
    if not divisional_game(game):
        non_division_games_per_team[game[0]] += 1
        non_division_games_per_team[game[1]] += 1
    home_games_per_team[game[0]] += 1
    away_games_per_team[game[1]] += 1

    print(week)
    print(schedule[week])

def remove_game(game, week): # removes the first game added to all_games
    #print("Removing game... " + str(game))
    schedule[week].remove(game)
    scheduled_games.remove(game)
    if not divisional_game(game):
        non_division_games_per_team[game[0]] -= 1
        non_division_games_per_team[game[1]] -= 1
    home_games_per_team[game[0]] -= 1
    away_games_per_team[game[1]] -= 1

def clear_week(week): # clears entire week of games
    print("Clearing week")
    while len(schedule[week]) > 0: # while schedule contains games that week
        remove_game(schedule[week][0], week) # remove the first game from the week

def divisional_game(game): # checks if a matchup is a divisional game
    for division in league:
        if game[0] in league[division]:
            if game[1] in league[division]:
                return True
            else:
                return False

def played_all_non_div_teams(team): # checks if team has played all non-divisional teams yet
    non_div_games = 0
    for game in scheduled_games:
        if not divisional_game(game) and team in game:
            non_div_games += 1
    if non_div_games >= len(all_teams) - teams_per_division:
        return True
    else:
        return False


while not add_next_game(): # continue adding games to the schedule until it is complete
    print("Bad schedule")
    continue

for division in league:
    print(league[division])
for week in schedule:
    print(week)
    print(len(checked_games[week]))
    print(checked_games[week])
    print(schedule[week])
