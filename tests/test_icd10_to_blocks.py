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
        'H05243'     : 'H00-H06 | Disorders of eyelid, lacrimal system and orbit',
        'A0105'      : 'A00-A09 | Intestinal infectious diseases',
        'B658'       : 'B65-B83 | Helminthiases',
        'C8333'      : 'C81-C96 | Malignant neoplasms, stated or presumed to be primary, of lymphoid, haematopoietic and related tissue',
        'D421'       : 'D37-D48 | Neoplasms of uncertain or unknown behaviour',
        'D4981'      : None,       # valid code but there's no mapping for it
        'D528'       : 'D50-D53 | Nutritional anaemias',
        'M84651K'    : 'M80-M94 | Osteopathies and chondropathies',
        'L03114'     : 'L00-L08 | Infections of the skin and subcutaneous tissue',
        'Not a code' : None,
        62719        : None,
        'T25519D'    : 'T20-T32 | Burns and corrosions',
        # Test codes with dots - should work after dot stripping
        'H05.243'    : 'H00-H06 | Disorders of eyelid, lacrimal system and orbit',  # same as 'H05243'
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

    # Source ranges: block_lookup.json
    # C00-C75, D10-D36, M00-M25, Z30-Z39 should cover these categories.
    expected_mappings = {
        "C7A022": "C00-C75 | Malignant neoplasms, stated or presumed to be primary, of specified sites, except of lymphoid, haematopoietic and related tissue",
        "C4A72": "C00-C75 | Malignant neoplasms, stated or presumed to be primary, of specified sites, except of lymphoid, haematopoietic and related tissue",
        "D3A090": "D10-D36 | Benign neoplasms",
        "M1A00X0": "M00-M25 | Arthropathies",
        "Z3A01": "Z30-Z39 | Persons encountering health services in circumstances related to reproduction",
    }

    for code, expected in expected_mappings.items():
        assert mapper.map(code) == expected
