'''
This module manages global parameters.
'''

import os
from datetime import date, timedelta
import matplotlib.dates as mdates

CHART_FOLDER = 'charts'

if not os.path.exists(CHART_FOLDER):
    os.mkdir(CHART_FOLDER)

end_date = date.today() - timedelta(1)
start_date = end_date - timedelta(179)

# End date is not included in drange
ticks = mdates.drange(start_date, end_date+timedelta(1), timedelta(1))
dates = list(map(mdates.num2date, ticks))
