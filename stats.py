PROJECT = ''

from collections import Counter
from datetime import date, timedelta
import pickle
from swin.GitHub import mapper

with open(PROJECT+'.pickle', 'rb') as f:
    pulls, users = pickle.load(f)

with open(PROJECT+'-affiliations.pickle', 'rb') as f:
    affiliations = pickle.load(f)

def print_top(start_date, end_date):
    '''
    Print top contributors for a range of dates.
    '''

    # Get affiliations that contributed within the specified range of dates.
    relevant_affiliations = []
    for i in range(len(pulls)):
        pr = pulls[i]
        if start_date <= pr.closed_at.date() < end_date:
            relevant_affiliations.append(affiliations[i])

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

    print(f'\nTop contributors for {start_date} - {end_date-timedelta(1)}:')
    for player,amount in Counter(relevant_affiliations).most_common():
        print(f'  - {mapper.get_full_entity_name(player)}: {amount}')

today = date.today()
this_month = date(today.year, today.month, 1)
last_month = date(this_month.year,this_month.month-1,1) if this_month.month > 1 \
    else date(this_month.year-1,12,1)
last_year  = date(this_month.year-1, this_month.month, 1)

print_top(last_year, this_month)
print_top(last_month, this_month)
