PROJECT = ''

import pickle

with open(PROJECT+'.pickle', 'rb') as f:
    pulls, users = pickle.load(f)

new_pulls = []
new_users = []
for i in range(len(pulls)):
    pr = pulls[i]

    # filter out contribution from bots
    if pr.user.login == 'dependabot[bot]':
        continue

    # only process contribution that is merged and closed
    if pr.merged_at and pr.closed_at:
        new_pulls.append(pr)
        new_users.append(users[i])

with open(PROJECT+'.pickle', 'wb') as f:
    pickle.dump((new_pulls,new_users), f)
