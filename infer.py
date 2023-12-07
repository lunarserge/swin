PROJECT = ''
CONTRIBUTORS = []

import sys
import bisect
from collections import Counter
from datetime import date
import pickle
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

dates,titles,affiliations = pd.read_pickle(PROJECT+'-dataset.pickle')
df = pd.DataFrame(data=[(d,t,a) for d,t,a in zip(dates,titles,affiliations)],
                  columns=['Date','Title','Affiliation'])

# filter out PRs from Intel and Nvidia that were used for training
training = []
for i,d,t,a in df.itertuples():
    if a in ['intel','nvidia']:
        training.append(i)
df = df.drop(training)

with open(PROJECT+'-model.pickle', 'rb') as f:
    text_clf = pickle.load(f)

df['Favors'] = text_clf.predict(df['Title'])
print(df.head(100))
print('All PRs:', Counter(df['Favors']))

# create a chart for the previous 12 months:
# filter out PRs that were closed earlier than Dec'22 or later than Nov'23
out_of_chart = []
d_from, d_to = date(2022,12,1), date(2023,12,1)
for i,d,t,a,f in df.itertuples():
    if d < d_from or d >= d_to:
        out_of_chart.append(i)
df = df.drop(out_of_chart)

# consolidate 'other' contributors into one category
df['Affiliation'] = df['Affiliation'].apply(lambda x: x if x in CONTRIBUTORS else 'other')

timestamps = [date(2022,12,1)] + [date(2023,month,1) for month in range(1,12)]

fig, axes = plt.subplots()
axes.set_title('ecosystem favor towards Intel: ' + PROJECT)

for contributor in CONTRIBUTORS:
    intel = [0] * len(timestamps)
    nvidia = [0] * len(timestamps)
    for i,d,t,a,f in df.itertuples():
        if a == contributor:
            index = bisect.bisect(timestamps,d)-1
            if f == 'intel':
                intel[index] += 1
            elif f == 'nvidia':
                nvidia[index] += 1
            else:
                print('ERROR')
                sys.exit(1)
    
    axes.plot(timestamps,[i/(i+n)*100 if i+n>0 else 50 for i,n in zip(intel,nvidia)])

axes.legend(CONTRIBUTORS)
axes.yaxis.set_major_formatter(mtick.PercentFormatter())

fig.savefig('favor')
