"""This is an app to create randomized divisions and a random schedule for a fantasy football league. The app takes number of teams, number of divisions, and number of playoff teams as input. All teams must play everyone in their division twice. Non-division opponents are random."""
"""Turns out 8 teams must have at least 4 people in playoffs in 16 week season to avoid playing someone three times.
Also, a 16 team league cannot have more than 2 rounds of playoffs if only 2 divisions in order to allow playing divisionals twice."
"""

'''make program run through every possible schedule, saving each good one until all checked'''
from random import choice
from time import sleep
import json
from os import path

while True:
    number_of_teams = int(input("Enter an even number of teams between 8 and 16: ")) # 8 - 16
    if number_of_teams < 8 or number_of_teams > 16 or number_of_teams % 2 != 0:
        print("You have entered an invalid number of teams.")
    else:
        break

while True:
    number_of_divisions = int(input("Enter number of divisions: ")) # make sure number of teams goes into number of divisions evenly, use drop down to provide appropriate choices # also must be at least 2. 8 teams cannot play each other twice and have playoffs in 16 week season. playoffs is at least 1 week. 14 teams has 2 divisions can only play each other twice with 1 round of playoffs
    if number_of_divisions == 0 or number_of_teams % number_of_divisions != 0 or number_of_teams / number_of_divisions < 2:
        print("Divisions must have an equal number of teams and at least 2 teams each.") # divisions must have at least 2 teams
    else:
        break

teams_per_division = int(number_of_teams / number_of_divisions)
minimum_weeks_of_regular_season = (teams_per_division - 1) * 2 if number_of_divisions > 1 else number_of_teams - 1
maximum_weeks_of_regular_season = (number_of_teams - 1) * 2
def playoff_rounds(number_of_playoff_teams):
    num_teams = number_of_playoff_teams
    rounds_of_playoffs = 0
    while num_teams > 1:
        rounds_of_playoffs += 1
        num_teams /= 2
    return rounds_of_playoffs

while True:
    number_of_playoff_teams = int(input("Enter number of playoff teams: ")) # no greater than number of teams # will be used to determine number of weeks of play # must also be less than twice the number of teams in division. max playoff rounds is 4 for 16 teams, so 16 team division needs 4 divisions. 14 team league can have 2 weeks playoffs
    if number_of_playoff_teams > number_of_teams or 16 - playoff_rounds(number_of_playoff_teams) < minimum_weeks_of_regular_season or maximum_weeks_of_regular_season + playoff_rounds(number_of_playoff_teams) < 16:# or number_of_playoff_teams > (16 - minimum_weeks_of_regular_season) * 2:
        print("Playoff teams must be less than total number of teams, allow for minimal regular season, and use entire season.")
    else:
        break

weeks_of_playoffs = playoff_rounds(number_of_playoff_teams)
weeks_of_regular_season = 16 - weeks_of_playoffs 

# assign number of teams indicated to the league
all_teams = []
for i in range(1, number_of_teams + 1):
    all_teams.append("Team" + str(i))

# assign number of divisions to the league
league = []
for i in range(1, number_of_divisions + 1):
    league.append([])

# assign teams to divisions
teams = all_teams.copy()
for division in league:
    for i in range(0, teams_per_division):#number_of_teams / number_of_divisions):
        team = teams[0]
        division.append(team)
        teams.remove(team)

print(league)
print(weeks_of_regular_season)
print(weeks_of_playoffs)
sleep(3)

max_division_games = (teams_per_division - 1) * 2
max_non_division_games = weeks_of_regular_season - max_division_games
max_home_games = (weeks_of_regular_season / 2) if (weeks_of_regular_season % 2 == 0) else ((weeks_of_regular_season / 2) + 1)
max_away_games= max_home_games # if odd number of games, some teams may have one more home game or away game

schedule = []
scheduled_games = [] # record of all teams that have played each other outside of division. should contain no duplicates
checked_games = []
non_division_games_per_team = {}
home_games_per_team = {}
away_games_per_team = {}

all_games = [[home_team, away_team] for home_team in all_teams for away_team in all_teams if home_team is not away_team]
for i in range(1, weeks_of_regular_season + 1):
    schedule.append([]) # schedule is dictionary of weekly keys with lists of games as lists of two teams that week
    checked_games.append([])

schedules_list = [] # empty list to hold completed schedules
if not path.exists('schedules.json'):
    with open('schedules.json', 'w') as f:
        f.write(json.dumps(schedules_list))
with open('schedules.json', 'r') as f:
    schedules_list = json.loads(f.read())

if len(schedules_list) > 0: # if there are schedules on file
    print("schedule loaded")
    sleep(1)
    schedule = schedules_list[-1] # get the last schedule
    for week in schedule:
        for game in week: # and add all the games to scheduled games
            scheduled_games.append(game)
    # then if any game is in all the schedules, add to checked games
    maybe_games = []
    i = 0
    j = 0
    while i < len(schedule): # for each week of schedule
        while j < len(schedule[0]): # for each game
            # put each game from each schedule in a list
            for a_schedule in schedules_list:
                a_game = a_schedule[i][j]
                maybe_games.append(a_game)
            else:
                # for first game in that list
                for game in maybe_games:
                    for other_game in maybe_games:
                        if game is other_game:
                            continue
                        elif game is not other_game and game == other_game: # if same as other games
                            continue
                        else:
                            maybe_games.clear()
                            break
                    else: # reach this statement
                        checked_games[i].append(game)
                        break            
            j += 1
        i += 1
    print("Games checked")
    print(checked_games)
    sleep(5)


for team in all_teams:
    non_division_games_per_team[team] = 0
    home_games_per_team[team] = 0 # max is number of total games / 2 or (num of games / 2) + 1 if odd num of games
    away_games_per_team[team] = 0


# for new recursive schedule maker
# choose first game from possible games, remove
# create fresh possible games only missing first game
# choose next game from possible games, remove
# if game doesn't work, go back one game and try next game from possible games
# again create fresh possible games with last bad game added back, but not existing games


def add_next_game():
    for week in schedule: # go through weeks of schedule one by one
        week_index = schedule.index(week)
        if len(week) == 0: # new week beginning, clear checked games
            checked_games[week_index].clear()
        while len(week) < len(all_teams) / 2: # while the week is not full, continue choosing, checking, adding games
            possible_games = find_games(all_games, week_index, checked_games[week_index])
            if len(possible_games) == 0: # if no games are possible
                return False
            game = possible_games[0] # choose game for this week          
            checked_games[week_index].append(game) # add game to checked_games for this week
            if check_game(game, week_index): # if game fits scheduling rules
                add_game(game, week_index) # add game to schedule for that week
                if not add_next_game(): # try to add next game, passing current path, and if it returns bad path    
                    remove_game(game, week_index) # remove just that game
    # check to make sure schedule has not been made yet
    for a_schedule in schedules_list:
        if a_schedule == schedule:
            print("schedule exists")
            return False
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

    print("Game added")
    print("week %d" % week)
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

    print("Game removed.")
    print("week %d" % week)
    print(schedule[week])

def divisional_game(game): # checks if a matchup is a divisional game
    for division in league:
        if game[0] in division:
            if game[1] in division:
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


while True:
    if add_next_game(): # continue adding games to the schedule until it is complete
        # print("Bad schedule") # if schedule makes it all the way back to empty, which it won't, try again
        # sleep(5)
        # continue
    # else:
        # if you find a good schedule, write it to file
        # if schedule is not in schedules file already
        # create file if it doesn't exist, only first run
        print("Good schedule")
        print(len(schedules_list))
        sleep(1)
        # read file then truncate then append then write file
        with open('schedules.json', 'r+') as f:
            schedules_list = json.loads(f.read())
            f.seek(0)
            f.truncate()
            # append copy of schedule to avoid having pointer to working
            # schedule existing in schedules_list
            schedules_list.append(schedule.copy())
            f.write(json.dumps(schedules_list))
        # remove the last game added from successful schedule
        remove_game(schedule[-1][-1], -1)
        # and try adding games again
    else: # add next game failed, probably from half-made schedule
         # remove the last game from the last week
        i = len(schedule) - 1 # i equals last index of schedule
        while i >= 0:
            if len(schedule[i]) > 0:
                remove_game(schedule[i][-1], i)
                break
            i -= 1
        else: # schedule is empty so no game removed
            break # all schedules found
    
            
for division in league:
    print(division)
for week in schedule:
    print(week)

