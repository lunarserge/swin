PROJECT = ''

import bisect
from collections import Counter
from datetime import date, timedelta
import pickle
import matplotlib.pyplot as plt
from swin.GitHub import mapper

with open(PROJECT+'.pickle', 'rb') as f:
    pulls, users = pickle.load(f)

with open(PROJECT+'-affiliations.pickle', 'rb') as f:
    affiliations = pickle.load(f)

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

def print_top(start_date, end_date):
    '''
    Print top contributors for a range of dates.
    '''
    relevant_PRs,relevant_affiliations = _get_relevant(start_date, end_date)

    # Get top contributors and combine all others into 'other' affiliation.
    # Looking at 5 top contributors and potentially more if several contributed on the same level.
    counter = Counter(relevant_affiliations)
    most_common = counter.most_common(6)
    last_player_i = len(most_common)-1
    if most_common[last_player_i] == 'unknown':
        last_player -=1
    threshold = most_common[last_player_i][1]
    relevant_affiliations = \
        [a if counter[a] >= threshold else 'other' for a in relevant_affiliations]

    '''
    unknowns = {}
    for i in range(len(relevant_affiliations)):
        if relevant_affiliations[i] == 'unknown':
            user = relevant_PRs[i].user.login
            if user in unknowns:
                unknowns[user] += 1
            else:
                unknowns[user] = 1
    print(Counter(unknowns))
    '''

    print(f'\nTop contributors for {start_date} - {end_date-timedelta(1)} (total {len(relevant_affiliations)} PRs):')
    for player,amount in Counter(relevant_affiliations).most_common():
        print(f'  - {mapper.get_full_entity_name(player)}: {amount}')

def _get_one_timestamp(pr):
    '''
    Get the closing year and month of a pull request.
    '''
    closed = pr.closed_at
    return date(closed.year,closed.month,1)

def draw_PRs(start_date, end_date, contributors):
    '''
    Draw a chart of contribution over time.
    '''
    relevant_PRs,relevant_affiliations = _get_relevant(start_date, end_date)
    min_stamp = max_stamp = _get_one_timestamp(relevant_PRs[0])

    # Determine range limits.
    for pr in relevant_PRs[1:]:
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
    axes.set_title('# contributed PRs / monthly: ' + PROJECT)

    for contributor in contributors:
        amount = [0] * len(timestamps)
        for i in range(len(relevant_PRs)):
            if relevant_affiliations[i] == contributor:
                amount[bisect.bisect(timestamps,relevant_PRs[i].closed_at.date())-1] += 1
        axes.plot(timestamps,amount)
    axes.legend([mapper.get_full_entity_name(c) for c in contributors])

    fig.savefig('contribution')

today = date.today()
this_month = date(today.year, today.month, 1)
last_month = date(this_month.year,this_month.month-1,1) if this_month.month > 1 \
    else date(this_month.year-1,12,1)
last_year  = date(this_month.year-1, this_month.month, 1)

print_top(last_year, this_month)
print_top(last_month, this_month)

draw_PRs(last_year, this_month, [])
