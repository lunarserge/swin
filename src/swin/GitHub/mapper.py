'''
Map of known translations from affiliations into full entity names.
'''
_AFFILIATION_TO_FULL = [
    ('contextual', 'Contextual AI'),
    ('databricks', 'Databricks'),
    ('hit',        'Harbin Institute of Technology'),
    ('intel',      'Intel'),
    ('microsoft',  'Microsoft'),
    ('rutgers',    'Rutgers University'),
    ('tsinghua',   'Tsinghua University'),
    ('uci',        'University of California, Irvine'),
    ('ustc',       'University of Science and Technology of China')
]

def get_full_entity_name(affiliation):
    '''
    Get full entity name for a given affiliation.
    Return affiliation 'as is' if full name mapping is not found.
    '''
    for a,full in _AFFILIATION_TO_FULL:
        if a == affiliation:
            return full
    return affiliation
