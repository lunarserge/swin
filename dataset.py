PROJECT = ''

import pickle

with open(PROJECT+'.pickle', 'rb') as f:
    pulls,users = pickle.load(f)
with open(PROJECT+'-affiliations.pickle', 'rb') as f:
    affiliations = pickle.load(f)

with open(PROJECT+'-dataset.pickle', 'wb') as f:
    pickle.dump(([p.closed_at.date() for p in pulls],
                 [p.title.lower() for p in pulls], affiliations), f)
