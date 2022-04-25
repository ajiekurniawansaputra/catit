from flask import Flask
import json
from datetime import datetime

app = Flask(__name__)

@app.get("/api/sensor")
def get_sensor():
    processed_data = group_and_aggregate()
    return processed_data

def group_and_aggregate():
    """
    This function will read JSON file,
    The data will be grouped by room and then by date,
    grouped data will be aggregated.
    output: dictionary of processed data 
    """
    with open('sensor_data.json') as local_file:
        local_data_list = json.load(local_file)
    rooms = []
    dates = []
    temp_grouped = {}
    
    #group data and save it in temp_grouped dictionary, loop len(local_data_list) O(N)
    for item in local_data_list['array']:
        room = item['roomArea']
        date = _get_date(item['timestamp'])
        if room not in rooms:
            rooms.append(room)    
        if date not in dates:
            dates.append(date)
        if (room+date+'temperature') not in temp_grouped:
            temp_grouped[room+date+'temperature']=[]
        if (room+date+'humidity') not in temp_grouped:
            temp_grouped[room+date+'humidity']=[]  
        temp_grouped[room+date+'temperature'].append(item['temperature'])
        temp_grouped[room+date+'humidity'].append(item['humidity'])
    
    #create json structure and call aggregator function, loop len(rooms)*len(dates)*len(sensor) O(N)
    local_data_grouped_aggregated = {
        'array':{room:{date:{
            'temperature':aggregate(temp_grouped[room+date+'temperature']),
            'humidity':aggregate(temp_grouped[room+date+'humidity'])} for date in dates} for room in rooms}}
    '''
    print(local_data_grouped_aggregated.keys())
    print(local_data_grouped_aggregated['array'].keys())
    print(local_data_grouped_aggregated['array']['roomArea2'].keys())
    print(local_data_grouped_aggregated['array']['roomArea2']['2020-07-02'].keys())
    print(local_data_grouped_aggregated['array']['roomArea2']['2020-07-02']['temperature'])
    '''
    return local_data_grouped_aggregated

def aggregate(sensor_data_list):
    """
    This function aggregate list of data
    input: list of sensor data in a given time and room
    output: dictionary of min, max, median, and mean
    """
    sensor_data_list.sort()
    len_list = len(sensor_data_list) 
    mid_index = len_list // 2
    median_list = (sensor_data_list[mid_index]+sensor_data_list[~mid_index])/2
    mean_list = sum(sensor_data_list)/len_list
    aggregate_dict = {
        'min':min(sensor_data_list),
        'max':max(sensor_data_list),
        'median':median_list,
        'mean':mean_list
    }
    return aggregate_dict    
    
def _get_date(unix_time_ms):
    """convert unix ms to string"""
    timestamp = unix_time_ms/1000
    timestamp = datetime.utcfromtimestamp(timestamp)
    return timestamp.strftime('%Y-%m-%d')
    
if __name__ == '__main__':
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['JSON_SORT_KEYS'] = False
    app.run(host="0.0.0.0", port=5000, use_reloader=True)
    
    '''
    shape of aggregated data
    {
        'array':{
            room:{
                date:{
                    sensor:{
                        'min':value,
                        'max':value,
                        'median':value,
                        'mean':value
                    }
                }
            }
        }
    }
    '''