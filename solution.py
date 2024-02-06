from requests import get
import json
import time
from utils import calculate_neighboring_dates, sanitize_time, combine_entries, file_exists, check_common_elements, quick_find_object, calculate_time_difference

#CONSTANTS
NORMAL_WEATHER = [
  'sunny',
  'rainy',
  'cloudy',
  'clear'
]

ATTENDANCE_DB = 'attendance.json'
EMPLOYEES_DB = 'employees.json'
WEATHER_API = "https://www.pingtt.com/exam/weather/"
EVENT_API = "https://www.pingtt.com/exam/events"
CHECK_IN_CUTOFF = 81500
CHECK_OUT_CUTOFF = 160000

def main():
  start = time.time()
  # get api data
  weather_data = get(WEATHER_API).json()
  events_data = get(EVENT_API).json()

  instances = []
  disaster_days = []
  valid_event_dates = []
  valid_events = []
  employee_times = {}

  for item in weather_data:
    if ('2023' in item['date'] and (item['condition'] not in NORMAL_WEATHER or item['max_temp'] >= 40)) :
      disaster_days.append(item['date'])

  for event in events_data:
    if('2023' in event['event_date'] and event['event_date'] not in disaster_days):
      valid_event_dates.append(event['event_date'])
      event = {
        'event_id' : event['id'],
        'country' : event['country'],
        'event_name' : event['event_name'],
        'event_date' : event['event_date']
      }
      valid_events.append(event)

  with open("attendance.json", "r") as attendance_data:
    data = json.load(attendance_data)
  for record in data:
    if '2023' not in record['date'] : continue
    if (record['clock_in']) : daily_hours = calculate_time_difference(record['clock_in'], record['clock_out'])
    if record['employee_record_id'] not in employee_times:
      employee_times[record['employee_record_id']] = {
        'employee_record_id' : record['employee_record_id'],
        'total_hours' : daily_hours,
      }
    else : 
      employee_times[record['employee_record_id']]['total_hours'] += daily_hours

    event_matches = []
    dates_to_check = calculate_neighboring_dates(record['date'])
    if(not check_common_elements(dates_to_check,valid_event_dates)):
        continue
    else:
      for date in dates_to_check:
        event = quick_find_object(valid_events,'event_date',date)
        if (event) : event_matches.append(event)
    if (not event_matches) : 
      continue
    if (not record['clock_in'] or (sanitize_time(record['clock_in']) > CHECK_IN_CUTOFF or sanitize_time(record['clock_out']) < CHECK_OUT_CUTOFF)):
      if (len(event_matches) > 1):
        with open('employees.json', 'r') as employee_data:
          employees = json.load(employee_data)
          for match in event_matches :
            if (match['country'] == quick_find_object(employees,'record_id',record['employee_record_id'])['country']):
              event = match
      else : 
        event = event_matches[0]

      if(event):
        new_record = {
          'id' : len(instances)+1,
          'date' : event['event_date'],
          'employee_record_id' : record['employee_record_id'],
          'event_name' : event['event_name'],
          'country' : event['country']
        }

        instances.append(new_record)

  slackers = combine_entries(instances, list(employee_times.values()))

  with open('solution.json', 'w') as f:
    json.dump(slackers, f, indent=4)

  end = time.time()
  time_elapsed = end - start
  print(f"""
    Complete!
    Identified {len(slackers)} employees.
    And it only took {time_elapsed} seconds
  """)

if __name__ == "__main__":
  main()