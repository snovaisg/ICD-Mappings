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
        'H05243'     : 'H00-H05 | Disorders of eyelid, lacrimal system and orbit',
        'A0105'      : 'A00-A09 | Intestinal infectious diseases',
        'B658'       : 'B65-B83 | Helminthiases',
        'C8333'      : 'C00-C96 | Malignant neoplasms',
        'D421'       : 'D37-D48 | Neoplasms of uncertain behavior, polycythemia vera and myelodysplastic syndromes',
        'D4981'      : 'D49-D49.9 | Neoplasms of unspecified behavior',
        'D528'       : 'D50-D53 | Nutritional anemias',
        'M84651K'    : 'M80-M94 | Osteopathies and chondropathies',
        'L03114'     : 'L00-L08 | Infections of the skin and subcutaneous tissue',
        'Not a code' : None,
        62719        : None,
        'T25519D'    : 'T07-T88 | Injury, poisoning and certain other consequences of external causes',
        # Test codes with dots - should work after dot stripping
        'H05.243'    : 'H00-H05 | Disorders of eyelid, lacrimal system and orbit',  # same as 'H05243'
        'A01.05'     : 'A00-A09 | Intestinal infectious diseases',  # same as 'A0105'
    } 
    
    for code, expected in expected_mappings.items():
        assert mapper.map(code) == expected
    
    all_codes = list(expected_mappings.keys())
    expected_result = list(expected_mappings.values())

    assert mapper.map(all_codes) == expected_result

    return None


def test_mapper_alphanumeric_third_character_categories():
    from icdmappings.mappers import ICD10toBlocks
    mapper = ICD10toBlocks()

    # Source ranges: icd10cmblocks.json
    # C00-C96, D10-D36, M00-M25, Z30-Z3A should cover these categories.
    expected_mappings = {
        "C7A022": "C00-C96 | Malignant neoplasms",
        "C4A72": "C00-C96 | Malignant neoplasms",
        "D3A090": "D10-D36 | Benign neoplasms, except benign neuroendocrine tumors",
        "M1A00X0": "M00-M25 | Arthropathies",
        "Z3A01": "Z30-Z3A | Persons encountering health services in circumstances related to reproduction",
    }

    for code, expected in expected_mappings.items():
        assert mapper.map(code) == expected
