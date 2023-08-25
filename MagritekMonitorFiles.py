import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# https://dskevin.hatenablog.com/entry/2022/03/06/120000

conn = sqlite3.connect('./monitor_15.sqlite')
DatabaseVersion = pd.read_sql_query('select * from DatabaseVersion', conn)
DataType = pd.read_sql_query('select * from DataType', conn)
sqlite_sequence = pd.read_sql_query('select * from sqlite_sequence', conn)
HardwareID = pd.read_sql_query('select * from HardwareID', conn)
DataTable = pd.read_sql_query('select * from DataTable', conn)

# 1 LockFrequency
# 2 MagnetTemperature
# 3 BoxTemperature
# 4 RoomTemperature
# 5 MagnetControlVoltage
# 6 PeltierControlVoltage
data_name = ['LockFrequency', 'MagnetTemperature', 'BoxTemperature', \
             'RoomTemperature', 'MagnetControlVoltage', 'PeltierControlVoltage']
y_unit = ['Hz', 'degC', 'degC', 'degC', 'V', 'V']

data_id = 4
data_extract = DataTable[DataTable.Type == data_id]

time_tb = pd.to_datetime(data_extract.Time)
data_tb = data_extract.Data

span = pd.to_datetime(["2023-06-14", "2023-06-22"])

fig, ax = plt.subplots(figsize=(6, 2.5))
fig.autofmt_xdate()
ax.plot(time_tb, data_tb)
# locator = mdates.DayLocator(interval=1)
locator = mdates.HourLocator(interval=12)
# locator = mdates.MonthLocator(interval=1)
ax.xaxis.set_major_locator(locator)
ax.set_title(data_name[data_id - 1])
ax.set_ylabel(y_unit[data_id - 1])
ax.set_xlabel("Time")
ax.set_xlim(span)
plt.show()


# https://www.yutaka-note.com/entry/pandas_datetime
# https://www.yutaka-note.com/entry/matplotlib_time_axis#%E6%99%82%E7%B3%BB%E5%88%97%E7%9B%AE%E7%9B%9B%E3%82%8A%E3%81%AE%E8%87%AA%E5%8B%95%E8%AA%BF%E6%95%B4%E6%A9%9F%E8%83%BD

# https://note.com/dngri/n/nae5c558ea318
# conn = sqlite3.connect('./monitor_15.sqlite')
# c = conn.cursor()
# c.execute("select * from sqlite_master where type='table'")
# for x in c.fetchall():
#    print(x)
# conn.close()
