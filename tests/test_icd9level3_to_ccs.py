def test_import():
    from icdmappings.mappers import ICD9Level3toCCS
    return

def test_init():
    from icdmappings.mappers import ICD9Level3toCCS
    mapper = ICD9Level3toCCS()
    return 

def test_mapper():
    from icdmappings.mappers import ICD9Level3toCCS
    mapper = ICD9Level3toCCS()

    code = "123.45"
    expected = None
    result = mapper.map(code)
    assert result == expected

    code = "5352"
    expected = None
    result = mapper.map(code)
    assert result == expected

    code = "535" # 535 can map to either 140 or 660
    expected1 = '140' 
    expected2 = '660'
    result = mapper.map(code)
    assert result in [expected1,expected2]

    code = 2.45
    try:
        result = mapper.map(code)
    except TypeError:
        pass

    code = ["201","20123", "433"]
    expected = ["37", None, "110"]
    result = mapper.map(code)
    assert result == expected