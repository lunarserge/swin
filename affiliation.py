PROJECT = ''

import pickle
from swin.GitHub import mapper

'''
List of known translations from user login into affiliation.
'''
LOGIN_TO_AFFILIATION = [
    ('SherlockNoMad', 'meta'), # linkedin (Sherlock Huang)
    ('ZainRizvi',     'meta'), # github.com/ZainRizvi
    ('anijain2305',   'meta'), # github.com/anijain2305
    ('desertfire',    'meta'), # linkedin (Bin Bao)
    ('malfet',        'meta'), # linkedin (Nikita Shulga)
    ('weiwangmeta',   'meta')
]

def guess_affiliation_from_login(user):
    '''
    Guess user affiliation based on login.
    'user' is PyGithub user descriptor.
    '''
    for l,affiliation in LOGIN_TO_AFFILIATION:
        if l == user.login:
            return affiliation
    return None

'''
List of known translations from user GitHub organizations into affiliation.
'''
ORG_TO_AFFILIATION = [
    ('facebookresearch', 'meta')
]

def guess_affiliation_from_orgs(user):
    '''
    Guess user affiliation based on GitHub organizations.
    'user' is PyGithub user descriptor.
    '''
    for org in user.get_orgs():
        login = org.login
        for l,affiliation in ORG_TO_AFFILIATION:
            if l == login:
                return affiliation
    return None

'''
List of email domains that can't help with determining user affiliation.
These are either generic domains (like gmail) or private domains
that belong to a person, not a company.
'''
NOT_TELLING_DOMAINS = [
    'gmail',         # generic
    'jezng',         # private (jezng.com)
    'karetnikov',    # private (karetnikov.org)
    'mail',          # generic
    'outlook',       # generic
    'me',            # generic
    'thiagocrepaldi' # private (thiagocrepaldi.com)
]

def guess_affiliation_from_email(user):
    '''
    Guess user affiliation based on email.
    'user' is PyGithub user descriptor.
    '''
    email = user.email
    if not email:
        return None

    index = dot = email.rfind('.')
    while True:
        index -= 1
        if email[index] in '@.':
            res = email[index+1:dot]

            # Keeping moving left for 'edu' under country domains.
            if res == 'edu':
                dot = index
                while True:
                    index -= 1
                    if email[index] in '@.':
                        res = email[index+1:dot]
                        break

            return None if res in NOT_TELLING_DOMAINS else res

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
    ('kumo.ai',                                     'kumo'),
    ('facebook',                                    'meta'),
    ('meta/facebook',                               'meta'),
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
    # prefer login-based affiliation if known
    login_affiliation = guess_affiliation_from_login(user)
    if login_affiliation:
        return login_affiliation

    '''
    # then prefer GitHub organizations
    org_affiliation = guess_affiliation_from_orgs(user)
    if org_affiliation:
        return org_affiliation
    '''

    # then prefer email if it is specified
    email = guess_affiliation_from_email(user)
    if email:
        return email

    company = guess_affiliation_from_company(user)
    return company if company else 'unknown'

with open(PROJECT+'.pickle', 'rb') as f:
    pulls, users = pickle.load(f)

affiliations = [guess_affiliation(user) for user in users]

with open(PROJECT+'-affiliations.pickle', 'wb') as f:
    pickle.dump(affiliations, f)
