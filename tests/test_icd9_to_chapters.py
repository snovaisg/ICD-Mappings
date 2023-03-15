def test_import():
    from icdmappings.mappers import ICD9toChapters
    return

def test_init():
    from icdmappings.mappers import ICD9toChapters
    mapper = ICD9toChapters()
    return 

def test_mapper():
    from icdmappings.mappers import ICD9toChapters
    mapper = ICD9toChapters()


    code = "999"
    expected = "17" 
    result = mapper.map(code)
    assert result == expected

    code = "5352"
    expected = "9"
    result = mapper.map(code)
    assert result == expected

    code = 2.45
    try:
        result = mapper.map(code)
    except TypeError:
        pass

    code = ["20104",123, "4339"]
    expected = ["2", None, "7"]
    result = mapper.map(code)
    assert result == expected
    
    # edge cases
    code = "15268176283765123123"
    expected = None
    will_get = mapper.map("152")
    result = mapper.map(code)
    assert will_get == result