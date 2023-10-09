def test_import():
    from icdmappings.mappers import ICD9Level3toCCI
    return

def test_init():
    from icdmappings.mappers import ICD9Level3toCCI
    mapper = ICD9Level3toCCI()
    return 

def test_mapper():
    from icdmappings.mappers import ICD9Level3toCCI
    mapper = ICD9Level3toCCI()

    code = ""
    expected = None
    result = mapper.map(code)
    assert result is expected

    code = "999"
    expected = False 
    result = mapper.map(code)
    assert result == expected

    code = '567'
    expected = False
    result = mapper.map(code)
    assert result == expected

    code = "V45"
    expected = False
    result = mapper.map(code)
    assert result == expected

    code = 2.45
    expected = None
    result = mapper.map(code)
    assert result is expected

    code = ["201", 123, "461"]
    expected = [True, None, False]
    result = mapper.map(code)
    assert result == expected