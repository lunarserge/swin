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
    ('berkeley',    'University of California, Berkeley'),
    ('contextual',  'Contextual AI'),
    ('databricks',  'Databricks'),
    ('gatech',      'Georgia Institute of Technology'),
    ('healthdata',  'Institute For Health Metrics and Evaluation'),
    ('hit',         'Harbin Institute of Technology'),
    ('intel',       'Intel'),
    ('kumo',        'Kumo'),
    ('meta',        'Meta'),
    ('microsoft',   'Microsoft'),
    ('mit',         'Massachusetts Institute of Technology'),
    ('nvidia',      'Nvidia'),
    ('ponder',      'Ponder'),
    ('quansight',   'Quansight'),
    ('rutgers',     'Rutgers University'),
    ('sysu',        'Sun Yat-sen University'),
    ('tsinghua',    'Tsinghua University'),
    ('tu-dortmund', 'Dortmund University'),
    ('uci',         'University of California, Irvine'),
    ('ustc',        'University of Science and Technology of China'),
    ('yandex',      'Yandex')
]

def get_full_entity_name(affiliation):
    '''
    Get full entity name for a given affiliation.
    Return affiliation 'as is' if full name mapping is not found.
    '''
    return _map(affiliation, _AFFILIATION_TO_FULL)
