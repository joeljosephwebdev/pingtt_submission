from datetime import datetime, timedelta
import os
import json

#UTILS
def calculate_neighboring_dates(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    
    day_before = date - timedelta(days=1)
    day_after = date + timedelta(days=1)
    
    return [day_before.strftime('%Y-%m-%d'), date_str, day_after.strftime('%Y-%m-%d')]

def build_hash_table(arr, key):
    hash_table = {}
    for obj in arr:
        hash_table[obj[key]] = obj
    return hash_table

def sanitize_time(time_string):
   return int((datetime.strptime(time_string, '%H:%M:%S')).strftime('%H%M%S'))

def quick_find_object(arr, key, value):
    hash_table = build_hash_table(arr, key)
    return hash_table.get(value, None)

def check_common_elements(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    
    if set1.intersection(set2):
        return True
    else:
        return False

def combine_entries(json_data, time_data):
    combined_data = {}
    
    with open('employees.json', 'r') as employee_data:
      employees = json.load(employee_data)
      for entry in json_data:
          record_id = entry["employee_record_id"]
          employee = quick_find_object(employees,'record_id',record_id)
          if record_id not in combined_data and entry['country'] == employee['country']:
            combined_data[record_id] = {
                "record_id": employee['record_id'],
                "name": employee['name'],
                "work_id_number": employee['work_id_number'],
                "email_address": employee['email_address'],
                "country": employee['country'],
                "phone_number": employee['phone_number'],
                "average_hours_per_week": quick_find_object(time_data, 'employee_record_id', employee['record_id'])['total_hours'] / 52,
                "events": []
          }
          
          event = {
            "country" : entry['country'],
            "event_name" : entry['event_name'],
            "date" : entry['date']
          }
          
          if (event['country'] == employee['country']):
            try :
              if(event in combined_data[record_id]["events"]):
                continue
            except :
               pass
            
            combined_data[record_id]["events"].append(event)

    return list(combined_data.values())

def file_exists(filename):
    script_directory = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(script_directory, filename)
    return os.path.exists(filepath)

def calculate_time_difference(clock_in, clock_out):
  if (not clock_in or not clock_out):
     return datetime.timedelta()
  fmt = '%H:%M:%S'
  in_time = datetime.strptime(clock_in, fmt)
  out_time = datetime.strptime(clock_out, fmt)

  difference = out_time - in_time
  return difference.total_seconds() / 3600
