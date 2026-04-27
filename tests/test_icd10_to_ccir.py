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


def test_parent_inference_enabled_by_default():
    from icdmappings.mappers import ICD10toCCIR

    mapper = ICD10toCCIR()
    assert mapper.map("H81.0") is True
    assert mapper.map("H81.0", allow_parent_inference=False) is None


def test_parent_inference_enabled_for_consistent_children():
    from icdmappings.mappers import ICD10toCCIR

    mapper = ICD10toCCIR()
    assert mapper.map("H81.0", allow_parent_inference=True) is True
    assert mapper.map("M75.1", allow_parent_inference=True) is False


def test_parent_inference_does_not_map_ambiguous_or_missing_prefixes():
    from icdmappings.mappers import ICD10toCCIR

    mapper = ICD10toCCIR()
    assert mapper.map("N90.8", allow_parent_inference=True) is None
    assert mapper.map("K35.9", allow_parent_inference=True) is None


def test_parent_inference_supports_multi_level_prefix_fallback():
    from icdmappings.mappers import ICD10toCCIR

    mapper = ICD10toCCIR()
    assert mapper.map("M75", allow_parent_inference=True) is False
    assert mapper.map("M751", allow_parent_inference=True) is False
    assert mapper.map("M7510", allow_parent_inference=True) is False


def test_exact_none_mapping_takes_precedence_over_inference():
    from icdmappings.mappers import ICD10toCCIR

    mapper = ICD10toCCIR()
    # Z283 is an exact CCIR code with value None even though descendants are consistently False.
    assert mapper.map("Z283") is None
    assert mapper.map("Z283", allow_parent_inference=True) is None


def test_parent_inference_handles_iterable_inputs():
    from icdmappings.mappers import ICD10toCCIR

    mapper = ICD10toCCIR()
    result = mapper.map(["H81.0", "N90.8", "M75"], allow_parent_inference=True)
    assert result == [True, None, False]
