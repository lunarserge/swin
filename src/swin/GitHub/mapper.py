def _map(term, translation_map):
    '''
    Get term translation given a map.
    Return the term 'as is' if the translation is not found.
    '''
    for t,translation in translation_map:
        if t == term:
            return translation
    return term

'''
Map of known translations from affiliations into full entity names.
'''
_AFFILIATION_TO_FULL = [
    ('contextual', 'Contextual AI'),
    ('databricks', 'Databricks'),
    ('gatech',     'Georgia Institute of Technology'),
    ('healthdata', 'Institute For Health Metrics and Evaluation'),
    ('hit',        'Harbin Institute of Technology'),
    ('intel',      'Intel'),
    ('microsoft',  'Microsoft'),
    ('ponder',     'Ponder'),
    ('quansight',  'Quansight'),
    ('rutgers',    'Rutgers University'),
    ('tsinghua',   'Tsinghua University'),
    ('uci',        'University of California, Irvine'),
    ('ustc',       'University of Science and Technology of China'),
    ('yandex',     'Yandex')
]

def get_full_entity_name(affiliation):
    '''
    Get full entity name for a given affiliation.
    Return affiliation 'as is' if full name mapping is not found.
    '''
    return _map(affiliation, _AFFILIATION_TO_FULL)
