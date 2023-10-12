PROJECT = ''

import pickle
from swin.GitHub import mapper

'''
List of generic email domains that can't help with determining user affiliation.
'''
GENERIC_DOMAINS = [
    'gmail',
    'mail',
    'outlook',
    'me'
]

def guess_affiliation_from_email(user):
    '''
    Guess user affiliation based on email.
    'user' is PyGithub user descriptor.
    '''
    email = user.email
    if not email:
        return None

    index = last_dot = email.rfind('.')
    while True:
        index -= 1
        if email[index] in '@.':
            res = email[index+1:last_dot]
            return None if res in GENERIC_DOMAINS else res

'''
Map of known translations from company info into affiliation.
'''
COMPANY_TO_AFFILIATION = [
    ('advanced micro devices inc.',                 'amd'),
    ('stasosphere online inc. / contextual.ai',     'contextual'),
    ('institute for health metrics and evaluation', 'healthdata'),
    ('harbin institute of technology',              'hit'),
    ('information sciences institute',              'isi'),
    ('usc information sciences institute',          'isi'),
    ('facebook',                                    'meta'),
    ('https://github.com/microsoft',                'microsoft'),
    ('the ohio state university',                   'osu'),
    ('ponder-org',                                  'ponder'),
    ('ponder.io',                                   'ponder'),
    ('rutgers university',                          'rutgers'),
    ('nisl, tsinghua university',                   'tsinghua')
]

def guess_affiliation_from_company(user):
    '''
    Guess user affiliation based on associated company info.
    'user' is PyGithub user descriptor.
    '''
    company = user.company
    if not company:
        return None

    # users often put '@' before their company info
    if company[0] == '@':
        company = company[1:]
    # for whatever reasons users sometimes put ' ' after their company info
    if company[-1] == ' ':
        company = company[:-1]
    # work in low case to match email-based affiliations
    company = company.lower()

    if company.endswith(' corporation'):
        company = company[:-12]

    # check if we can translate into a known affiliation
    for s,affiliation in COMPANY_TO_AFFILIATION:
        if s == company:
            return affiliation

    return company

def guess_affiliation(user):
    '''
    Guess user affiliation.
    'user' is PyGithub user descriptor.
    '''
    email = guess_affiliation_from_email(user)

    # prefer email if it is specified
    if email:
        return email

    company = guess_affiliation_from_company(user)
    return company if company else 'unknown'

with open(PROJECT+'.pickle', 'rb') as f:
    pulls, users = pickle.load(f)

affiliations = [guess_affiliation(user) for user in users]

with open(PROJECT+'-affiliations.pickle', 'wb') as f:
    pickle.dump(affiliations, f)
