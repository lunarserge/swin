PROJECT = ''

import pickle

'''
Known bot accounts.
'''
BOTS = [
    'dependabot[bot]',
    'pytorchmergebot',
    'pytorchupdatebot'
]

with open(PROJECT+'.pickle', 'rb') as f:
    pulls, users = pickle.load(f)

new_pulls = []
new_users = []
for i in range(len(pulls)):
    pr = pulls[i]

    # filter out contribution from bots
    if pr.user.login in BOTS:
        continue

    # only process contribution that is merged and closed
    if pr.closed_at:
        if not pr.merged_at:
            for label in pr.labels:
                if label.name.lower() == 'merged':
                    break
            else:
                continue

        new_pulls.append(pr)
        new_users.append(users[i])

with open(PROJECT+'.pickle', 'wb') as f:
    pickle.dump((new_pulls,new_users), f)
