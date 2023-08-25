#  ------------------------------------------------------------------------
#  File Name   : MagritekMonitorFiles.py
#  Description : Visualization of Monitoring Data of Magritek NMR Spectrometer
#  Developer   : Dr. Kosuke Ohgo
#  ULR         : https://github.com/ohgo1977/Magritek_NMR_Gadgets
#  Version     : 1.0.0
# 
#  ------------------------------------------------------------------------
# 
# MIT License
#
# Copyright (c) 2023 Kosuke Ohgo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Version 1.0.0 on 8/25/2023

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Log file for monitoring data
# C:\Users\UserName\AppData\Roaming\Magritek\EkoUi\monitor_15.sqlite
conn = sqlite3.connect('./monitor_15.sqlite')
DatabaseVersion = pd.read_sql_query('select * from DatabaseVersion', conn)
DataType = pd.read_sql_query('select * from DataType', conn)
sqlite_sequence = pd.read_sql_query('select * from sqlite_sequence', conn)
HardwareID = pd.read_sql_query('select * from HardwareID', conn)
DataTable = pd.read_sql_query('select * from DataTable', conn)

# Type of Data
# 1 LockFrequency
# 2 MagnetTemperature
# 3 BoxTemperature
# 4 RoomTemperature
# 5 MagnetControlVoltage
# 6 PeltierControlVoltage
data_id = 4

date_start = "2023-06-14" # Date to start a display.
date_finish = "2023-06-22"# Date to finish a display.

time_locator = 'day' # 'hour', 'day', 'month'
time_interval = 1 # interval of lables. Interval must be an integer greater than 0.


data_name = ['LockFrequency', 'MagnetTemperature', 'BoxTemperature', \
             'RoomTemperature', 'MagnetControlVoltage', 'PeltierControlVoltage']
y_unit = ['Hz', 'degC', 'degC', 'degC', 'V', 'V']

data_extract = DataTable[DataTable.Type == data_id]

time_tb = pd.to_datetime(data_extract.Time)
data_tb = data_extract.Data

span = pd.to_datetime([date_start, date_finish])

fig, ax = plt.subplots(figsize=(6, 2.5))
fig.autofmt_xdate()
ax.plot(time_tb, data_tb)

if time_locator == 'hour':
    locator = mdates.HourLocator(interval=time_interval)
elif time_locator == 'day':
    locator = mdates.DayLocator(interval=time_interval)
elif time_locator == 'month':
    locator = mdates.MonthLocator(interval=time_interval)

ax.xaxis.set_major_locator(locator)
ax.set_title(data_name[data_id - 1])
ax.set_ylabel(y_unit[data_id - 1])
ax.set_xlabel("Time")
ax.set_xlim(span)
plt.show()