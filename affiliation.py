PROJECT = ''

import pickle
from swin.GitHub import mapper

'''
List of known translations from user login into affiliation.
'''
LOGIN_TO_AFFILIATION = [
    ('SherlockNoMad',    'meta'),        # linkedin.com/in/sherlock-baihan-huang-07787a59
    ('ZainRizvi',        'meta'),        # github.com/ZainRizvi
    ('amyeroberts',      'huggingface'), # linkedin.com/in/amy-roberts-70903a6a
    ('anijain2305',      'meta'),        # github.com/anijain2305
    ('angelayi',         'meta'),        # linkedin.com/in/yiangela
    ('awgu',             'meta'),        # linkedin.com/in/~andrew
    ('bdhirsh',          'meta'),        # linkedin.com/in/hirshbrian
    ('dagitses',         'meta'),        # linkedin.com/in/michaeldagitses
    ('desertfire',       'meta'),        # linkedin.com/in/bin-bao-9b095812
    ('eellison',         'meta'),        # web search (Elias Ellison)
    ('fegin',            'meta'),        # linkedin.com/in/cchuangtw
    ('hi-sushanta',      'hiwhy'),       # linkedin.com/in/sushanta-das-
    ('huydhn',           'meta'),        # linkedin.com/in/huy-do
    ('janeyx99',         'meta'),        # linkedin.com/in/jane-yuan-xu
    ('jansel',           'meta'),        # linkedin.com/in/jansel
    ('jcaip',            'meta'),        # linkedin.com/in/jcaip
    ('kshitij12345',     'quansight'),   # linkedin.com/in/kshiteejkalambarkar
    ('kumpera',          'meta'),        # linkedin.com/in/rodrigokumpera
    ('malfet',           'meta'),        # linkedin.com/in/nikita-shulga-2875828
    ('msaroufim',        'meta'),        # linkedin.com/in/marksaroufim
    ('namannandan',      'amazon'),      # linkedin.com/in/namannandan
    ('ngimel',           'meta'),        # linkedin.com/in/natalia-gimelshein-8347a480
    ('patrickvonplaten', 'huggingface'), # linkedin.com/in/patrick-von-platen-343401123
    ('sekyondaMeta',     'meta'),
    ('sgugger',          'huggingface'), # linkedin.com/in/sylvain-gugger-74218b144
    ('soulitzer',        'meta'),        # linkedin.com/in/jeffrey-wan
    ('susnato',          'uem'),         # linkedin.com/in/susnato-dhar-922239211
    ('wanchaol',         'meta'),        # linkedin.com/in/wanchaol
    ('wconstab',         'meta'),        # linkedin.com/in/will-constable-969a53b
    ('weiwangmeta',      'meta'),
    ('williamwen42',     'meta'),        # linkedin.com/in/william-wen-1373b8156
    ('wz337',            'meta'),        # linkedin.com/in/weseeweisi
    ('ydshieh',          'huggingface'), # linkedin.com/in/yih-dar-shieh
    ('ydwu4',            'meta'),        # web search (Yidi Wu)
    ('zou3519',          'meta')         # linkedin.com/in/richard-zou-bb3558a6
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
    'gmail',          # generic
    'jezng',          # private (jezng.com)
    'karetnikov',     # private (karetnikov.org)
    'lysand',         # private (lysand.re)
    'mail',           # generic
    'me',             # generic
    'outlook',        # generic
    'thiagocrepaldi', # private (thiagocrepaldi.com)
    'yahoo'           # generic
]

'''
Map of known translations into primary email domains.
'''
TO_PRIMARY_DOMAINS = [
    ('fb', 'meta')
]

def guess_affiliation_from_email(user):
    '''
    Guess user affiliation based on email.
    'user' is PyGithub user descriptor.
    '''
    email = user.email
    if not email or '.' not in email:
        return None

    email = email.lower()
    index = dot = email.rfind('.')
    while True:
        index -= 1
        if email[index] in '@.':
            res = email[index+1:dot]

            # Keeping moving left for 'edu' under country domains.
            if res in ['ac', 'edu']:
                dot = index
                while True:
                    index -= 1
                    if email[index] in '@.':
                        res = email[index+1:dot]
                        break
            break

    if res in NOT_TELLING_DOMAINS:
        return None

    # Check if we can translate into a primary domain.
    for e,primary in TO_PRIMARY_DOMAINS:
        if e == res:
            return primary

    return res

'''
Map of known translations from company info into affiliation.
'''
COMPANY_TO_AFFILIATION = [
    ('advanced micro devices inc.',                 'amd'),
    ('university of cambridge',                     'cam'),
    ('stasosphere online inc. / contextual.ai',     'contextual'),
    ('institute for health metrics and evaluation', 'healthdata'),
    ('harbin institute of technology',              'hit'),
    ('hugging face',                                'huggingface'),
    ('information sciences institute',              'isi'),
    ('usc information sciences institute',          'isi'),
    ('kaizan & bbk',                                'kaizan'),
    ('kumo.ai',                                     'kumo'),
    ('facebook',                                    'meta'),
    ('facebook ai',                                 'meta'),
    ('facebookresearch',                            'meta'),
    ('meta/facebook',                               'meta'),
    ('https://github.com/microsoft',                'microsoft'),
    ('nanyang technological university',            'ntu'),
    ('the ohio state university',                   'osu'),
    ('ponder-org',                                  'ponder'),
    ('ponder.io',                                   'ponder'),
    ('rutgers university',                          'rutgers'),
    ('nisl, tsinghua university',                   'tsinghua'),
    ('uc irvine',                                   'uci'),
    ('federal university of rio de janeiro',        'ufrj'),
    ('zhejiang university',                         'zju')
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

    if company.endswith(' inc'):
        company = company[:-4]
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
