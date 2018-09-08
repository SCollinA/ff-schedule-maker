"""This is an app to create randomized divisions and a random schedule for a fantasy football league. The app takes number of teams, number of divisions, and number of playoff teams as input. All teams must play everyone in their division twice. Non-division opponents are random."""

from random import choice
from time import sleep

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

while True:
    number_of_playoff_teams = int(input("Enter number of playoff teams: ")) # no greater than number of teams, no less than 2 # will be used to determine number of weeks of play # must also be less than twice the number of teams in division. max playoff rounds is 4 for 16 teams, so 16 team division needs 4 divisions. 14 team league can have 2 weeks playoffs
    if number_of_playoff_teams > number_of_teams or number_of_playoff_teams < 2 or number_of_playoff_teams > (16 - minimum_weeks_of_regular_season) * 2:
        print("Playoff teams must be at least 2 and less than total number of teams.")
    else:
        break

def playoff_rounds(number_of_playoff_teams):
    num_teams = number_of_playoff_teams
    rounds_of_playoffs = 0
    while num_teams > 1:
        if num_teams % 2 == 0:
            rounds_of_playoffs += 1
        else:
            rounds_of_playoffs += 1
        num_teams /= 2
    return rounds_of_playoffs

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

# randomly assign teams to divisions
teams = all_teams.copy()
for division in league:
    for i in range(0, teams_per_division):#number_of_teams / number_of_divisions):
        team = choice(teams)
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
divisional_games = []
for division in league:
    divisional_games += [[home_team, away_team] for home_team in league[division] for away_team in league[division] if home_team is not away_team]
possible_games = [[home_team, away_team] for home_team in all_teams for away_team in all_teams if home_team is not away_team]
all_games = [] # record of all teams that have played each other outside of division. should contain no duplicates
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



# use recursion
# choose random game from possible games
# add as first game of first week
# choose random game as from possible games
# add as second game of first week
# continue until week is full
# continue with subsequent weeks
# if no games are possible to add, remove previous game and add different game.
# make copy of possible games at each recursion and remove game once selected
# return true if schedule complete to end recursion

def add_next_game():
    for week in schedule: # check each week of schedule
        # if week is complete, clear checked games for next week
        for this_week in schedule:
            if len(schedule[this_week]) == 0: # if the week is empty (because this is the first game added to it, clear it's checked games)
                checked_games[this_week].clear()
                break
        games =  [game for game in possible_games if game not in all_games]# possible games haven't been played, haven't been checked, and don't have teams playing that week
        while len(schedule[week]) < len(all_teams) / 2: # if the week is not full yet
            games = [game for game in games if game not in checked_games[week] if game not in all_games]
            if len(schedule[week]) > 0: # if a game has been added to week
                for each_game in schedule[week]: # don't add other games with those teams to week
                    games = [game for game in games if each_game[0] not in game if each_game[1] not in game]
            #print("Possible choices = " + str(len(games)))
            #print(games)
            if len(games) == 0: # checked all possible games
                return False
            #print("Choosing game...")
            game = choice(games) # pick a random game from the pool of possible games
            checked_games[week].append(game)
            if check_game(game, week): # check to see if its a good game
                #checked_games[week].remove(game) # good game, do not keep on checked list
                add_game(game, week) # add the game to the schedule
                if not add_next_game(): # if you can not find the next game to add, using the remaining games
                    checked_games[week].append(game) #add that game back to checked list
                    remove_game(game, week) # take the last game that was just added off the schedule
    return True # made it to end of schedule. gg
    
def check_game(game, week):
    #print("Checking game..." + str(game))
    if divisional_game(game):
        #print("Good game.")
        return True
    elif non_division_games_per_team[game[0]] < max_non_division_games and non_division_games_per_team[game[1]] < max_non_division_games:
        if home_games_per_team[game[0]] < max_home_games and away_games_per_team[game[1]] < max_away_games:
            if [game[1], game[0]] in all_games:
            # they have played all other division games
                if played_all_non_div_teams(game[0]) and played_all_non_div_teams(game[1]):
                    #print("Good game.")
                    return True
            else:
                #print("Good game.")
                return True
    #print("Bad game.")
    return False
                        
def add_game(game, week):
    #print("Adding game..." + str(game))
    schedule[week].append(game)
    all_games.append(game)
    if not divisional_game(game):
        non_division_games_per_team[game[0]] += 1
        non_division_games_per_team[game[1]] += 1
    home_games_per_team[game[0]] += 1
    away_games_per_team[game[1]] += 1

    for week in schedule:
        if len(schedule[week]) > 0:
            print(week)
            print(schedule[week])
            #print("Choices checked = " + str(len(checked_games[week])))
            #print(checked_games[week])

def divisional_game(game):
    #print("Checking divisional...")
    for division in league:
        if game[0] in league[division]:
            if game[1] in league[division]:
                return True
            else:
                return False

def remove_game(game, week):
    #print("Removing game..." + str(game))
    schedule[week].remove(game)
    all_games.remove(game)
    if not divisional_game(game):
        non_division_games_per_team[game[0]] -= 1
        non_division_games_per_team[game[1]] -= 1
    else:
        divisional_games.append(game)
    home_games_per_team[game[0]] -= 1
    away_games_per_team[game[1]] -= 1

    for week in schedule:
        print(week)
        print(schedule[week])

def played_all_non_div_teams(team):
    non_div_games = 0
    for game in all_games:
        if not divisional_game(game) and team in game:
            non_div_games += 1
    if non_div_games >= len(all_teams) - teams_per_division:
        return True
    else:
        return False


while not add_next_game():
    continue

for division in league:
    print(league[division])
for week in schedule:
    print(week)
    print(schedule[week])





# set weeks of regular season in dictionary with each week holding list of games that week
# add games randomly to week, being sure not to add same team twice
# add games to next week, being sure not to add same game to next week
# teams must play each other twice, and home field matters
# teams can only play non-division teams once maximum
""" 
def schedule_maker(league, weeks_of_regular_season, weeks_of_playoffs):
    add_divisional_games()
    print("Done adding divisional games.")
    sleep(3)
    while not check_schedule(schedule):
        game = choose_game()
        for week in schedule:
            if check_game(game, week):
                add_game(game, week)
                break
        else:
            checked_games.append(game)
    return schedule

def check_schedule(schedule):
    print("Checking schedule...")
    for week in schedule:
        if len(schedule[week]) < len(all_teams) / 2:
            return False
    return True

def choose_game():
    print("Choosing game...")
    while True:
        game_choices = [game for game in possible_games if game not in checked_games]
        if len(game_choices) > 0:
            break
        choose_game_to_remove()
    game = choice(game_choices)
    return game

def check_game(game, week):
    print("Checking game...")
    checked_games.append(game)
    if game not in all_games:
        print("Not already scheduled.")
        if not playing_that_week(game, week):
            if divisional_game(game):
                print("Good game.")
                return True
            elif non_division_games_per_team[game[0]] < max_non_division_games and non_division_games_per_team[game[1]] < max_non_division_games:
                if home_games_per_team[game[0]] < max_home_games and away_games_per_team[game[1]] < max_away_games:
                    print("Good game.")
                    return True
    print("Bad game.")
    return False
                        
def add_game(game, week):
    print("Adding game..." + str(game))
    schedule[week].append(game)
    all_games.append(game)
    possible_games.remove(game)
    checked_games.clear()
    if not divisional_game(game):
        non_division_games_per_team[game[0]] += 1
        non_division_games_per_team[game[1]] += 1
    else:
        divisional_games.remove(game)
    home_games_per_team[game[0]] += 1
    away_games_per_team[game[1]] += 1

    for week in schedule:
        print(week)
        print(schedule[week])
        if len(schedule[week]) == (len(all_teams) / 2) - 1: # one game remaining in week
            add_remaining_game(week)
            break

def add_remaining_game(week):
    print("Finishing week...")
    teams = all_teams.copy()
    for team in all_teams:
        for game in schedule[week]:
            if team in game:
                teams.remove(team)
                break
    if check_game([teams[0], teams[1]], week):
        add_game([teams[0], teams[1]], week)
    elif check_game([teams[1], teams[0]], week):
        add_game([teams[1], teams[0]], week)
    else: 
        games = schedule[week].copy()
        while len(games) > 0:
            game = choice(games)
            games.remove(game)
            if not divisional_game(game):
                remove_game(game, week)# remove random game from that week
                break
        else: # all games are divisional, so move the one you need from another week
            for this_week in schedule:
                for game in schedule[this_week]:
                    if teams[0] in game and teams[1] in game:
                        remove_game(game, this_week)
                        if check_game([teams[0], teams[1]], week):
                            add_game([teams[0], teams[1]], week)
                            return
                        elif check_game([teams[1], teams[0]], week):
                            add_game([teams[1], teams[0]], week)
                            return
            
            print("Oh no!!!!!")
            sleep(60)


def choose_game_to_remove(): # has to be non-division game
    week = choice(list(schedule.keys()))
    games = schedule[week].copy()
    while len(games) > 0:
        game = choice(games)
        games.remove(game)
        if not divisional_game(game):
            remove_game(game, week)# remove random game from that week
            break
    else:
        choose_game_to_remove() # try again, you'll get a week with a non-divisional game eventually

def remove_game(game, week):
    print("Removing game..." + str(game))
    schedule[week].remove(game)
    all_games.remove(game)
    possible_games.append(game)
    checked_games.clear()
    if not divisional_game(game):
        non_division_games_per_team[game[0]] -= 1
        non_division_games_per_team[game[1]] -= 1
    else:
        divisional_games.append(game)
    home_games_per_team[game[0]] -= 1
    away_games_per_team[game[1]] -= 1

def playing_that_week(game, week):
    print("Checking if playing...")
    if len(schedule[week]) > 0:
        for match in schedule[week]:
            if game[0] in match or game[1] in match:
                return True
    return False

def divisional_game(game):
    print("Checking divisional...")
    for division in league:
        if game[0] in league[division]:
            if game[1] in league[division]:
                return True
            else:
                return False

def add_divisional_games():
    while len(divisional_games) > 0:
        week = choice(list(schedule.keys()))
        add_count = 0
        game_choices = [game for game in divisional_games if game not in checked_games]
        while add_count < 2:
            game = choice(game_choices)
            game_choices.remove(game)
            if check_game(game, week): # games must be added two at a time
                add_game(game, week)
                add_count += 1     
            if len(game_choices) == 0: # and removed two at a time if no options remain
                while True:
                    new_week = choice(list(schedule.keys()))
                    if len(schedule[new_week]) > 1:
                        break
                game1 = choice(schedule[new_week])
                remove_game(game1, new_week)
                game2 = choice(schedule[new_week])
                remove_game(game2, new_week)
                break
        
 """
"""def schedule_maker(league, weeks_of_regular_season, weeks_of_playoffs):
    add_divisional_games()
    # while schedule is not complete, continue trying to make schedule
    while not check_schedule(schedule):
        # add random non-divisional games to remaining spots
        while len(checked_games) < len(possible_games): 
            while True:
                game = choose_teams() # choose a game until you find a non divisional
                if game not in checked_games and not divisional_game(game):
                    break
            weeks = list(schedule.keys()).copy()
            for week in weeks:
                if len(schedule[week]) == 6:
                    weeks.remove(week)
            while len(weeks) > 0: # try to add chosen game to each week that's not full
                week = choice(weeks)
                weeks.remove(week)
                if check_game(game, week):
                    add_game(game, week)
                    break
        else: # unable to add game
            # remove game
            choose_game_to_remove()
    return schedule

def check_schedule(schedule):
    print("Checking schedule...")
    for week in schedule:
        print(week)
        print(schedule[week])
    for week in schedule:
        if len(schedule[week]) < 6:
            return False
    return True # all weeks have 6 games. Done!

def choose_teams():
    print("Choosing teams...")
    teams = all_teams.copy()
    # choose home team
    home_team = choice(teams)
    teams.remove(home_team)
    # choose away team
    away_team = choice(teams)
    # return teams         
    game = choice(possible_games)
    return game

def check_game(game, week):
    print("Checking game...")
    # simply returns true or false depending on whether game can be added
    checked_games.append(game)
    # sleep(.25)
    if not already_playing_this_week(game, week):
        print("Not playing...")
        # sleep(.25)
        if game not in all_games:
            print("Not scheduled...")
            # sleep(.25)
            if divisional_game(game):
                print("Good game.")
                return True
            elif non_division_games_per_team[game[0]] < max_non_division_games and non_division_games_per_team[game[1]] < max_non_division_games:
                if home_games_per_team[game[0]] < max_home_games and away_games_per_team[game[1]] < max_away_games:
                    print("Good game.")
                    return True
    print("Bad game.")
    return False

def already_playing_this_week(game, week):
    print("Checking if playing...")
    if len(schedule[week]) > 0:
        for match in schedule[week]:
            if game[0] in match or game[1] in match:
                return True
    return False

def add_game(game, week):
    print("Adding game... " + game[0] + ", " + game[1])
    # sleep(.25)
    schedule[week].append(game)
    all_games.append(game)
    possible_games.remove(game)
    checked_games.clear() # resets upon successful add
    home_games_per_team[game[0]] += 1
    away_games_per_team[game[1]] += 1
    if not divisional_game(game):
        non_division_games_per_team[game[0]] += 1
        non_division_games_per_team[game[1]] += 1
    if len(schedule[week]) == 5:
        add_remaining_game(week)

def add_remaining_game(week):
    print("Finishing week...")
    # sleep(.25)
    # add remaining game to finish week
    remaining_game = []
    for team in all_teams: # find remaining game
        for game in schedule[week]:
            if team not in game:
                remaining_game.append(team)
                break
    # check game, if not possible, game must be removed somewhere
    if check_game(remaining_game, week):
        add_game(remaining_game, week)
    else:
        choose_game_to_remove()

def choose_game_to_remove():
    print("Choosing removal...")
    # remove only non-divisional games if necessary
    all_games_copy = all_games.copy()
    while True:
        game = choice(all_games_copy) # choose a random game
        all_games_copy.remove(game)
        if not divisional_game(game):
            # find week that game is in
            for week in schedule:
                if game in schedule[week]:
                    remove_game(game, week)
                    return

def remove_game(game, week):
    print("Removing game... " + game[0] + ", " + game[1])
    # sleep(1)
    schedule[week].remove(game)
    all_games.remove(game)
    possible_games.append(game)
    home_games_per_team[game[0]] -= 1
    away_games_per_team[game[1]] -= 1
    if not divisional_game(game):
        non_division_games_per_team[game[0]] -= 1
        non_division_games_per_team[game[1]] -= 1
    checked_games.clear()

def add_divisional_games():
    # find all divisional games
    print("Adding divisional games...")
    # sleep(.25)
    divisional_games = []
    for division in league:
        divisional_games += [[home_team, away_team] for home_team in league[division] for away_team in league[division] if home_team is not away_team]
    # add divisional games to random weeks in schedule
    while len(divisional_games) > 0: # while there are still divisional games to assign
        print("Remaining games " + str(len(divisional_games)))
        week = choice(list(schedule.keys())) # choose random week
        print(week)
        if len(schedule[week]) < 6: # if week is not full
            game = choice(divisional_games) # choose a random divisional game
            print(game)
            if check_game(game, week): # if the game fits in the week
                add_game(game, week) # add the game to the week
                divisional_games.remove(game) # remove the game from remaining divisional games

def divisional_game(game):
    print("Checking if divisional...")
    home_division = ""
    for division in league:
        if game[0] in league[division]:
            home_division = division
            break
    if game[1] in league[home_division]:
        return True
    return False

"""

""" def schedule_maker(league, weeks_of_regular_season, weeks_of_playoffs):
    while check_schedule(schedule):
        matchup = choose_teams() # pick a good matchup that can be played
        try_matchup(matchup)
    return schedule          

def check_schedule(schedule): # helper function returns true if schedule is complete
    print("Checking schedule...")

    for week in schedule:
        if len(schedule[week]) < 6:
            if len(schedule[week]) == 5: # if there are already five games, the last game is determined
                teams = all_teams.copy()
                for team in teams:  # find teams not playing yet that week
                    for game in schedule[week]:
                        if team in game:
                            teams.remove(team)
                game = [teams[0], teams[1]]
                if game not in all_games:
                    if divisional_game(game):
                        try_matchup(game)
                    elif non_division_games_per_team[game[0]] < max_non_division_games and non_division_games_per_team[game[1]] < max_non_division_games: # this is a non-div game
                        # if neither team has played too many non divisional games
                        # check if either has played too many home or away games
                        # if so, try swapping and check again
                        if home_games_per_team[game[0]] < max_home_games and away_games_per_team[game[1]] < max_away_games:
                            try_matchup(game)
                        elif home_games_per_team[game[1]] < max_home_games and away_games_per_team[game[0]] < max_away_games:# either team has played too many home or away games
                            try_matchup([game[1], game[0]])
                elif divisional_game(game) and [game[1], game[0]] not in all_games: # if divisional game that hasn't been played away yet
                    try_matchup(game)
                else:
                    remove_game(game)
            return True
    return False

def try_matchup(matchup):
    for week in schedule:
        if not playing_already_this_week(matchup, schedule[week]):
            schedule[week].append(matchup) # if you found a matchup that was not already scheduled, add it to schedule
            add_matchup(matchup)
            return True
    else:
        remove_game(matchup) # there is a case where matchup is legit but does not fit, need to remove matchup to reconfigure
        return False

def playing_already_this_week(matchup, week):
    print("Checking if playing...")
    home_team = matchup[0]
    away_team = matchup[1]
    for game in week:
        if home_team in game or away_team in game:
            return True
    return False

def add_matchup(matchup):
    print("Adding..." + matchup[0] + ", " + matchup[1])
    
    for week in schedule:
        print(week)
        print(schedule[week])

    all_games.append(matchup)
    home_games_per_team[matchup[0]] += 1
    away_games_per_team[matchup[1]] += 1
    if not divisional_game(matchup):
        non_division_games_per_team[matchup[0]] += 1
        non_division_games_per_team[matchup[1]] += 1

def choose_teams(): # chooses two teams at random, making sure home team hasn't played too many home games and vice versa for away team
    print("Choosing...")
    
    while True:
        teams = all_teams.copy()
        matchup = ["", ""] # matchup is nobody yet, if it's nobody later we'll have to remove a game to fix the schedule
        home_teams = teams.copy()
        while len(home_teams) > 0: # go through possible home teams
            home_team = choice(home_teams) 
            home_teams.remove(home_team)
            if home_games_per_team[home_team] < max_home_games: # if home team hasn't played too many home games
                matchup[0] = home_team # team can be home team
                teams.remove(home_team) # they should not be chosen as away team also
                # if we found a suitable home team, let's also find an away team
                away_teams = teams.copy()
                while len(away_teams) > 0:
                    away_team = choice(away_teams)
                    away_teams.remove(away_team)
                    matchup[1] = away_team # make them away team for now
                    if away_games_per_team[away_team] > max_away_games: # they have played too many away games
                        continue
                    elif matchup not in all_games: # if matchup not already played
                        if divisional_game(matchup): # if divisional matchup
                            return matchup # must play divisional matchups
                        # if both teams haven't played too many non-division games
                        elif non_division_games_per_team[home_team] < max_non_division_games and non_division_games_per_team[away_team] < max_non_division_games:
                            return matchup #schedule this matchup
                    elif divisional_game(matchup) and (matchup[1], matchup[0]) not in all_games: # if divisional game but haven't played away
                        return [matchup[1], matchup[0]]
                else:
                    matchup[1] = ""
        else:
            matchup = ["", ""]
        if matchup[0] == "" or matchup[1] == "": # if we haven't found teams we need to remove a game from the schedule
            sleep(5)
            remove_game(matchup)

def divisional_game(matchup): # checks if matchup is divisional game
    print("Checking Divisional...")
    for division in league:
        if matchup[0] in league[division] and matchup[1] in league[division]:
            return True
        else:
            return False

def remove_game(matchup):
    # if matchup has both values, it was a legit game that we couldn't find room for
    # if it's missing away team value, we could find home team, but either non div games or away games were limited
    # if it's missing home team, home games were limited
    # using this information, delete one matchup from schedule
    if matchup[0] == "": # missing home team, remove team with most home games, unlikely case
        # find team with most home games, remove one of its home games
        home_team = all_teams[0]
        for team in home_games_per_team: # find team with most home games
            if home_games_per_team[team] > home_games_per_team[home_team]:
                home_team = team
        for match in all_games: # find game where home team is home
            if home_team == match[0]: 
                game = match
    elif matchup[1] == "": # missing away team, either too many away games or too many non-div games
        # find team with most away games
        away_team = all_teams[0]
        for team in away_games_per_team: # find team with most away games
            if away_games_per_team[team] > away_games_per_team[away_team]:
                away_team = team
        # find team with too many non-div games
        non_div_team = all_teams[0]
        for team in non_division_games_per_team:
            if non_division_games_per_team[team] > non_division_games_per_team[non_div_team]:
                non_div_team = team
        # whichever value is closest to max, remove one of that team's games
        if non_div_team == away_team or (max_non_division_games - non_division_games_per_team[non_div_team]) > (max_away_games - away_games_per_team[away_team]): # same team
            # or away team is closer to max, either way remove game where team is away
            for match in all_games:
                if away_team == match[1]:
                    game = match
        else: # non-div team is closer to max
            for match in all_games:
                if non_div_team in match and not divisional_game(match):
                    game = match        
    else: # if both teams are there, find a non_div game to remove
        all_matches = all_games.copy()
        while len(all_matches) > 0:
            match = choice(all_matches) # choose match at random
            all_matches.remove(match)
            if not divisional_game(match) and (match[0] in match or match[1] in match): # if one of the teams is playing in non divisional match
                game = match # this will be the game to remove
                break
        else: # no non div games found, remove div game
            all_matches = all_games.copy()
            while len(all_matches) > 0:
                match = choice(all_matches) # choose match at random
                all_matches.remove(match)
                if divisional_game(match) and (match[0] in match or match[1] in match): # if one of the teams is playing in non divisional match
                    game = match # this will be the game to remove
                    break
    # remove game from schedule and decrement appropriate counts
    print("Removing..." + game[0] + ", " + game[1])
    for week in schedule:
        print(week)
        print(schedule[week])
    for week in schedule:
        if game in schedule[week]:
            schedule[week].remove(game)
            break
    all_games.remove(game)
    home_team = game[0]
    away_team = game[1]
    home_games_per_team[home_team] -= 1
    away_games_per_team[away_team] -= 1
    if not divisional_game(game): # if it's a non-divisional matchup, decrement those counts as well
        non_division_games_per_team[home_team] -= 1
        non_division_games_per_team[away_team] -= 1

    # if legit matchup, try it again
    if matchup[0] != "" or matchup[1] != "":
        if not try_matchup(matchup) and [matchup[1], matchup[0]] not in all_games: # try the same matchup again because that is the one we just made room for 
            try_matchup([matchup[1], matchup[0]])
        # otherwise the program will automatically try to choose another matchup and try it on the next iteration of the while loop in schedule_maker
 """

#print(schedule_maker(league, weeks_of_regular_season, weeks_of_playoffs))
