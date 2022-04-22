import json
import logging
import pandas as pd
import matplotlib.pyplot as plt
import time 

def main(debug=False):
    if debug == True:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    processed_dataframe = aggregate()
    plot_data(processed_dataframe)

def plot_data(data):
    sensors = ["temperature","humidity"]
    logger.info(f"get room")
    rooms = []
    for indexroom, indextime in data.index:
        if indexroom in rooms:
            pass
        else:
            rooms.append(indexroom)
    logger.info(f"create layout")
    fig, axs = plt.subplots(len(rooms), 2, figsize=(15,15))
    logger.info(f"plotting")
    for j, sensor in enumerate(sensors):
        for i, room in enumerate(rooms):
            sensor_data = data.loc[room, sensor]
            sensor_data_min = sensor_data["min"]
            axs[i, j].plot(sensor_data_min.index, sensor_data_min)
            axs[i, j].set_title(room)
            sensor_data_max = sensor_data["max"]
            axs[i, j].plot(sensor_data_max.index, sensor_data_max)
            axs[i, j].set_title(room)
            sensor_data_median = sensor_data["median"]
            axs[i, j].plot(sensor_data_median.index, sensor_data_median)
            axs[i, j].set_title(room)
            sensor_data_mean = sensor_data["mean"]
            axs[i, j].plot(sensor_data_mean.index, sensor_data_mean)
            axs[i, j].set_title(room)
    plt.show()

def aggregate():
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
    logger.info(local_df_group.head(30))
    return local_df_group

def _conv_date(row):
    """Convert unix from milisecond to second and put it in dataframe"""
    row = row/1000
    return pd.Timestamp(row, unit='s')

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    main(debug=False)