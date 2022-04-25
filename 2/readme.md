# Documentation
To run this file simply 
* install all dependencies required using pip install on your environtment.
* run main.py in your console
* to access api open the endpoint at _your-ip:5000/api/sensor_
* to see the graph open the endpoint at _your-ip:5000/<string:sensor>/<string:room_area>_, sensor ['temperature', 'humidity'], room_area example ['roomArea1', 'roomArea2', 'roomArea3']
* ie  _your-ip:5000/temperature/roomArea2_,  _<yourip>:5000/humidity/roomArea3>_

shape of aggregated data
```
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
```