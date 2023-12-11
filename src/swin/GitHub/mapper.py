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
    ('amazon',        'Amazon'),
    ('amd',           'AMD'),
    ('apple',         'Apple'),
    ('berkeley',      'University of California, Berkeley'),
    ('cam',           'University of Cambridge'),
    ('contextual',    'Contextual AI'),
    ('cornell',       'Cornell University'),
    ('databricks',    'Databricks'),
    ('gatech',        'Georgia Institute of Technology'),
    ('graphcore',     'Graphcore'),
    ('healthdata',    'Institute For Health Metrics and Evaluation'),
    ('hit',           'Harbin Institute of Technology'),
    ('hiwhy',         'HIWHY'),
    ('huawei',        'Huawei'),
    ('huggingface',   'Hugging Face'),
    ('ibm',           'IBM'),
    ('ideas2it',      'Ideas2IT'),
    ('intel',         'Intel'),
    ('isi',           'Information Sciences Institute'),
    ('jpmorganchase', 'JPMorgan Chase'),
    ('kaizan',        'Kaizan'),
    ('kumo',          'Kumo'),
    ('meta',          'Meta'),
    ('microsoft',     'Microsoft'),
    ('mit',           'Massachusetts Institute of Technology'),
    ('ntu',           'Nanyang Technological University'),
    ('nvidia',        'Nvidia'),
    ('openai',        'OpenAI'),
    ('ponder',        'Ponder'),
    ('quansight',     'Quansight'),
    ('rutgers',       'Rutgers University'),
    ('speechmatics',  'Speechmatics'),
    ('stonybrook',    'Stony Brook University'),
    ('striveworks',   'Striveworks'),
    ('sysu',          'Sun Yat-sen University'),
    ('tsinghua',      'Tsinghua University'),
    ('tu-dortmund',   'Dortmund University'),
    ('uci',           'University of California, Irvine'),
    ('uem',           'University of Engineering & Management, Kolkata'),
    ('ufrj',          'Federal University of Rio de Janeiro'),
    ('umich',         'University of Michigan'),
    ('umn',           'University of Minnesota'),
    ('ustc',          'University of Science and Technology of China'),
    ('yandex',        'Yandex'),
    ('zju',           'Zhejiang University')
]

def get_full_entity_name(affiliation):
    '''
    Get full entity name for a given affiliation.
    Return affiliation 'as is' if full name mapping is not found.
    '''
    return _map(affiliation, _AFFILIATION_TO_FULL)
