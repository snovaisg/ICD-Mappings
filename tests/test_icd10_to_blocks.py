def test_import():
    from icdmappings.mappers import ICD10toBlocks

    return None

def test_init():
    from icdmappings.mappers import ICD10toBlocks
    ICD10toBlocks()

    return None


def test_mapper():
    from icdmappings.mappers import ICD10toBlocks
    mapper = ICD10toBlocks()

    expected_mappings = {
        'H05243'     : 'H00-H06', 
        'A0105'      : 'A00-A09', 
        'B658'       : 'B65-B83', 
        'C8333'      : 'C81-C96', 
        'D421'       : 'D37-D48',
        'D4981'      : None,       # valid code but there's no mapping for it
        'D528'       : 'D50-D53', 
        'M84651K'    : 'M80-M94',
        'L03114'     : 'L00-L08', 
        'Not a code' : None,
        62719        : None,
        'T25519D'    : 'T20-T32',
    } 
    
    for code, expected in expected_mappings.items():
        assert mapper.map(code) == expected
    
    all_codes = list(expected_mappings.keys())
    expected_result = list(expected_mappings.values())

    assert mapper.map(all_codes) == expected_result

    return None