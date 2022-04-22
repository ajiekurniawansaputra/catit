from flask import Flask
import json
import logging
import pandas as pd

app = Flask(__name__)

def main(debug=False):
    if debug == True:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['JSON_SORT_KEYS'] = False
    
@app.get("/api/sensor")
def get_sensor():
    processed_dataframe = _aggregate()
    processed_json = json.loads(processed_dataframe.to_json(orient="index"))
    print(processed_dataframe.head(30))
    return processed_json

def _aggregate():
    logger.info(f"Opening json file")
    with open('sensor_data.json') as local_file:
        local_data_list = json.load(local_file)["array"]
    logger.info(f"Put json data into dataframe")
    local_df = pd.DataFrame(local_data_list)
    logger.info(f"Convert timestamp into dataframe-enabled grouping")
    local_df['timestamp'] = local_df["timestamp"].apply(lambda row: _conv_date(row))
    logger.info(f"Group by room area and timestamp date")
    local_df_group = local_df.groupby(["roomArea", pd.Grouper(key='timestamp', axis=0, freq='D')])
    logger.info(f"Aggregate the data")
    local_df_group = local_df_group.agg({'temperature':['min','max','median','mean'],'humidity':['min','max','median','mean']})
    logger.info(f"Done")
    return local_df_group

def _conv_date(row):
    """Convert unix from milisecond to second and put it in dataframe"""
    row = row/1000
    return pd.Timestamp(row, unit='s')

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    main(debug=False)
    app.run(host="0.0.0.0", port=5000, use_reloader=True)