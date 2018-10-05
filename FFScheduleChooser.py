from random import choice
import json

with open('schedules.json', 'r') as f:
    schedules_list = json.loads(f.read())
    schedule = choice(schedules_list)
    schedule_string = ''
    for week in schedule:
        schedule_string = schedule_string + 'Week %d' % schedule.index(week)
        for game in week:
            schedule_string = schedule_string + ' %s vs %s' % (game[0], game[1])
        schedule_string = schedule_string + '\n'
    print(schedule_string)