def test_import():
    from icdmappings.mappers import ICD10toChapters
    return

def test_init():
    from icdmappings.mappers import ICD10toChapters
    mapper = ICD10toChapters()
    return 

def test_mapper():
    from icdmappings.mappers import ICD10toChapters
    mapper = ICD10toChapters()

    expected_mappings = {'H05243':'7', 
                         'A0105': '1', 
                         'B658': '1', 
                         'C8333': '2', 
                         'D421': '2',
                         'D4981': None, # valid code but there's no mapping for it
                         'D528': '3', 
                         'M84651K': '13',
                         'L03114': '12', 
                         'Not a code':None,
                          62719: None,
                         'T25519D': '19'
                        } 
    
    for code, expected in expected_mappings.items():
        result = mapper.map(code)
        assert result == expected
    
    all_codes = list(expected_mappings.keys())
    expected_result = list(expected_mappings.values())

    result = mapper.map(all_codes)
    assert all([r == e for r, e in zip(result, expected_result)])