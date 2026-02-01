def test_import():
    from icdmappings.mappers import ICD10toCCSR
    return

def test_init():
    from icdmappings.mappers import ICD10toCCSR
    mapper = ICD10toCCSR()
    return 

def test_mapper():
    from icdmappings.mappers import ICD10toCCSR
    mapper = ICD10toCCSR()

    expected_mappings = {'H05243':'EYE008',
                         'A0105': 'INF003',
                         'B658': 'INF009',
                         'C8333': 'NEO058',
                         'D421': 'NEO072',
                         'D4981': 'NEO072',
                         'D528': 'BLD001',
                         'M84651K': 'MUS015',
                         'L03114': 'SKN001',
                         'Not a code':None,
                          62719: None,
                         'T25519D': 'INJ056',
                         # Test codes with dots - should work after dot stripping
                         'H05.243': 'EYE008',  # same as 'H05243'
                         'A01.05': 'INF003',   # same as 'A0105'
                        } 
    
    for code, expected in expected_mappings.items():
        result = mapper.map(code)
        assert result == expected
    
    all_codes = list(expected_mappings.keys())
    expected_result = list(expected_mappings.values())

    result = mapper.map(all_codes)
    assert all([r == e for r, e in zip(result, expected_result)])