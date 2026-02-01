def test_import():
    from icdmappings.mappers import ICD10toCCIR
    return

def test_init():
    from icdmappings.mappers import ICD10toCCIR
    mapper = ICD10toCCIR()
    return 

def test_mapper():
    from icdmappings.mappers import ICD10toCCIR
    mapper = ICD10toCCIR()

    expected_mappings = {'H05243':True,
                         'A0105': False,
                         'B658': False,
                         'C8333': True,
                         'D421': True,
                         'D4981': False,
                         'D528': True,
                         'M84651K': False,
                         'L03114': False,
                         'Not a code':None,
                          62719: None,
                         'T25519D': False,
                         # Test codes with dots - should work after dot stripping
                         'H05.243': True,   # same as 'H05243'
                         'A01.05': False,   # same as 'A0105'
                        }
    for code, expected in expected_mappings.items():
        result = mapper.map(code)
        assert result == expected
    
    all_codes = list(expected_mappings.keys())
    expected_result = list(expected_mappings.values())

    result = mapper.map(all_codes)
    assert all([r == e for r, e in zip(result, expected_result)])