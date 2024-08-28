import enmscripting as enm

s = enm.open()
t = s.terminal()
r = t.execute('alarm get ENM')

alarm_key = ['Severity', 'Specific_Problem', 'Event_time', 'object_of_reference', 'Probable_cause', 'Alarm_count']
all_alarms = r._result_lines[1:-3]
alarm_attributes = [0, 2, 3, 4, 8, 10]
# array of dicts, each alarm is a dict
tenant_alarms = []


# Function to merge alarm key value
def merge_key_value(array1, array2):
    return dict(zip(array1, array2))


for alarm in all_alarms:
    x = map(str, alarm.split('\t'))
    alarm_value = [x[index] for index in alarm_attributes]
    # converting alarm count value to boolean
    if alarm_value[5] == "REPEATED_ALARM":
        alarm_value[5] = True
    else:
        alarm_value[5] = False
    tenant_alarms.append(merge_key_value(alarm_key, alarm_value))

print(tenant_alarms)
