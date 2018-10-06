from random import choice
import json
from os import system

def schedule_to_string(schedule):
    schedule_string = ''
    for week in schedule:
        schedule_string = schedule_string + 'Week %d' % schedule.index(week)
        for game in week:
            schedule_string = schedule_string + ' %s vs %s' % (game[0], game[1])
        schedule_string = schedule_string + '\n'
    return schedule_string

def team_schedule(schedule, team):
    schedule_string = ''
    for week in schedule:
        schedule_string = schedule_string + 'Week %d ' % schedule.index(week)
        for game in week:
            if team in game:
                schedule_string = schedule_string + '%s vs %s \n' % (game[0], game[1])
                break
    return schedule_string

with open('schedules.json', 'r') as f:
    schedules_list = json.loads(f.read())
    i = 1000
    while i > 0:
        schedule = choice(schedules_list)
       # print(schedule_to_string(schedule))
        print(team_schedule(schedule, schedule[0][0][0]))
        system('clear')
        i -= 1
    schedule = choice(schedules_list)
    # print(schedule_to_string(schedule))
    print(team_schedule(schedule, schedule[0][0][0]))

