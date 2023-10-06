REPO = '' # in a form of 'lunarserge/swin'
GITHUB_TOKEN = ''

import sys
import os
import time
from datetime import datetime
import pickle
import github

RATE_LIMIT = 5000

g = github.Github(auth=github.Auth.Token(GITHUB_TOKEN))

if g.rate_limiting[1] != 5000:
    print(f'Unexpected GitHub API rate limit (should be {RATE_LIMIT}). Exiting.', file=sys.stderr)
    sys.exit(1)

def log(message):
    '''
    Log a message for user prefixed with the current time.
    '''
    print(f'{datetime.now().strftime("%y-%m-%d %H:%M:%S")}: {message}', file=sys.stderr)

def wait_rate_limiting_reset():
    '''
    Wait for GitHub API rate limit reset before collecting a new batch.
    '''
    remaining,limit = g.rate_limiting
    if remaining == limit:
        return

    reset_time = datetime.fromtimestamp(g.rate_limiting_resettime)
    wait = (reset_time-datetime.now()).total_seconds()
    log(f'Waiting till {reset_time} for GitHub API rate limit to reset')
    time.sleep(wait)

def get_batch_file_name(batch):
    '''
    Get the name of file for storing user data from the given batch number.
    '''
    return f'{project}-{batch}.pickle'

project = REPO[REPO.index('/')+1:]
pulls_file = project + '-pulls.pickle'

if os.path.exists(pulls_file):
    with open(pulls_file, 'rb') as f:
        pulls = pickle.load(f)
    log('Pull requests loaded from local disk')
else:
    if g.rate_limiting[0] == 0:
        wait_rate_limiting_reset()
    log('Started pull requests download from GitHub servers')
    pulls = list(g.get_repo(REPO).get_pulls(state='all', direction='asc'))
    with open(pulls_file, 'wb') as f:
        pickle.dump(pulls, f)
    log('Pull requests downloaded and stored to local disk')

start = 0
while os.path.exists(get_batch_file_name(start)):
    start += 1
finish = ((len(pulls)-1) // RATE_LIMIT) + 1

if finish > start:
    print(f'PR user data download will start from batch #{start}')
    print(f'Last batch is going to be #{finish-1}')

    for batch in range(start, finish):
        pr_from = batch * RATE_LIMIT
        pr_to = min(pr_from+RATE_LIMIT, len(pulls))
        users = []
        if g.rate_limiting[0] < pr_to-pr_from:
            wait_rate_limiting_reset()
        log(f'Started download for batch #{batch} (PRs {pr_from}-{pr_to})')
        for pr in pulls[pr_from:pr_to]:
            user = pr.user
            email = user.email # this will trigger user data download from GitHub
            users.append(user)
        with open(get_batch_file_name(batch), 'wb') as f:
            pickle.dump(users, f)
        log(f'Batch #{batch} downloaded and stored to local disk')

log(f'Combining the data into one file (# user data batches: {finish})')
users = []
for batch in range(0, finish):
    with open(get_batch_file_name(batch), 'rb') as f:
        users += pickle.load(f)

log(f'Storing the combined data into {project}.pickle')
with open(project+'.pickle', 'wb') as f:
    pickle.dump((pulls,users), f)
