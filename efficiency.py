PROJECT = ''
CONTRIBUTORS = ['other']

import bisect
from datetime import date,timedelta
import pickle
import matplotlib.pyplot as plt
from swin.GitHub import mapper

def _get_relevant(start_date, end_date):
    '''
    Get PRs and affiliations for contributions within the specified range of dates.
    '''
    relevant_PRs = []
    relevant_affiliations = []
    for i in range(len(pulls)):
        pr = pulls[i]
        if start_date <= pr.closed_at.date() < end_date:
            relevant_PRs.append(pulls[i])
            relevant_affiliations.append(affiliations[i])
    return relevant_PRs, relevant_affiliations

today = date.today()
this_month = date(today.year, today.month, 1)
last_month = date(this_month.year,this_month.month-1,1) if this_month.month > 1 \
    else date(this_month.year-1,12,1)
last_year  = date(this_month.year-1, this_month.month, 1)

def _get_one_timestamp(pr):
    '''
    Get the closing year and month of a pull request.
    '''
    closed = pr.closed_at
    return date(closed.year,closed.month,1)

def draw_PRs():
    '''
    Draw a chart of contribution over time.
    '''
    min_stamp = max_stamp = _get_one_timestamp(pulls[0])

    # Determine range limits.
    for pr in pulls[1:]:
        stamp = _get_one_timestamp(pr)
        if stamp > max_stamp:
            max_stamp = stamp
        elif stamp < min_stamp:
            min_stamp = stamp

    # Create a range of dates based on the limits.
    stamp = min_stamp
    timestamps = [stamp]
    while stamp != max_stamp:
        stamp = date(stamp.year,stamp.month+1,1) if stamp.month < 12 else date(stamp.year+1,1,1)
        timestamps.append(stamp)

    fig, axes = plt.subplots()
    axes.set_title('# PR days to close / monthly: ' + PROJECT)

    for contributor in CONTRIBUTORS:
        q = [0] * len(timestamps)
        t = [timedelta() for t in timestamps]
        for i in range(len(pulls)):
            if affiliations[i] == contributor:
                pr = pulls[i]
                index = bisect.bisect(timestamps,pr.closed_at.date())-1
                q[index] += 1
                t[index] += pr.closed_at - pr.created_at
        axes.plot(timestamps,
                  [(t[i]/q[i]).days if q[i] > 0 else 0 for i in range(len(timestamps))])
    axes.legend([mapper.get_full_entity_name(c) for c in CONTRIBUTORS])

    fig.savefig('PR-days-to-close')

with open(PROJECT+'.pickle', 'rb') as f:
    pulls, users = pickle.load(f)

with open(PROJECT+'-affiliations.pickle', 'rb') as f:
    affiliations = pickle.load(f)

pulls, affiliations = _get_relevant(last_year, this_month)

for i in range(len(affiliations)):
    if affiliations[i] not in CONTRIBUTORS:
        affiliations[i] = 'other'

quantity = {c:0 for c in CONTRIBUTORS}
total = {c:timedelta() for c in CONTRIBUTORS}

for i in range(len(pulls)):
    pr = pulls[i]
    a = affiliations[i]
    quantity[a] += 1
    total[a] += pr.closed_at - pr.created_at

for c in CONTRIBUTORS:
    print(c + ':', total[c]/quantity[c])

draw_PRs()
