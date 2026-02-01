def test_import():
    from icdmappings.mappers import ICD9toCCCCategory
    return

def test_init():
    from icdmappings.mappers import ICD9toCCCCategory
    mapper = ICD9toCCCCategory()
    return

def test_mapper():
    from icdmappings.mappers import ICD9toCCCCategory
    mapper = ICD9toCCCCategory()

    # Empty code test
    code = ""
    expected = None
    result = mapper.map(code)
    assert result is expected

    # Invalid code test
    code = "invalid123"
    expected = None
    result = mapper.map(code)
    assert result is expected

    # Non-string type test
    code = 2.45
    expected = None
    result = mapper.map(code)
    assert result is expected

    # Valid single codes
    code = "135"
    expected = "hemato_immu"
    result = mapper.map(code)
    assert result == expected

    code = "179"
    expected = "malignancy"
    result = mapper.map(code)
    assert result == expected

    code = "243"
    expected = "metabolic"
    result = mapper.map(code)
    assert result == expected

    # Test codes with dots - should work after dot stripping
    code = "1.35"
    expected = "hemato_immu"  # same as "135"
    result = mapper.map(code)
    assert result == expected

    code = "1.79"
    expected = "malignancy"  # same as "179"
    result = mapper.map(code)
    assert result == expected

    # Batch processing
    code = ["135", 123, "179", "", "1.35"]
    expected = ["hemato_immu", None, "malignancy", None, "hemato_immu"]
    result = mapper.map(code)
    assert result == expected
