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

    expected_mappings = {
        "H05243": "H00-H59 | Diseases of the eye and adnexa",
        "A0105": "A00-B99 | Certain infectious and parasitic diseases",
        "B658": "A00-B99 | Certain infectious and parasitic diseases",
        "C8333": "C00-D49 | Neoplasms",
        "D421": "C00-D49 | Neoplasms",
        "D4981": "C00-D49 | Neoplasms",
        "D528": "D50-D89 | Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism",
        "M84651K": "M00-M99 | Diseases of the musculoskeletal system and connective tissue",
        "L03114": "L00-L99 | Diseases of the skin and subcutaneous tissue",
        "Not a code": None,
        62719: None,
        "T25519D": "S00-T88 | Injury, poisoning and certain other consequences of external causes",
        # Test codes with dots - should work after dot stripping.
        "H05.243": "H00-H59 | Diseases of the eye and adnexa",
        "A01.05": "A00-B99 | Certain infectious and parasitic diseases",
    }

    for code, expected in expected_mappings.items():
        result = mapper.map(code)
        assert result == expected

    all_codes = list(expected_mappings.keys())
    expected_result = list(expected_mappings.values())

    result = mapper.map(all_codes)
    assert all([r == e for r, e in zip(result, expected_result)])


def test_mapper_alphanumeric_third_character_categories():
    from icdmappings.mappers import ICD10toChapters

    mapper = ICD10toChapters()

    expected_mappings = {
        "C7A022": "C00-D49 | Neoplasms",
        "C4A72": "C00-D49 | Neoplasms",
        "D3A090": "C00-D49 | Neoplasms",
        "M1A00X0": "M00-M99 | Diseases of the musculoskeletal system and connective tissue",
        "Z3A01": "Z00-Z99 | Factors influencing health status and contact with health services",
    }

    for code, expected in expected_mappings.items():
        assert mapper.map(code) == expected
