def test_mapper_import():
    from icdmappings import Mapper
    return

def test_mapper_init():
    from icdmappings import Mapper
    mapper = Mapper()
    return

def test_mapper():
    from icdmappings import Mapper
    mapper = Mapper()

    mapper.show_mappers()

    icd9code = '5679'
    expected_icd10code = 'K659'
    expected_ccscode = '148'
    expected_chapter = '9'
    expected_icd9dxvalidity = True
    expected_icd9procvalidity = True
    expected_level_3 = '567'
    expected_cci = False

    assert expected_icd10code == mapper.map('icd9toicd10', icd9code)
    assert expected_ccscode == mapper.map('icd9toccs', icd9code)
    assert expected_chapter == mapper.map('icd9tochapter', icd9code)
    assert expected_icd9dxvalidity == mapper.validate_diagnostics('icd9', icd9code)
    assert expected_icd9procvalidity == mapper.validate_procedures('icd9', icd9code)
    assert expected_level_3 == mapper.map('icd9tolevel3', icd9code)
    assert expected_cci == mapper.map('icd9tocci', icd9code)

    icd9codes = ['5679', 235, '6010']
    expected_icd10codes = ['K659', None, 'N410']
    expected_ccscodes = ['148', None, '165']
    expected_chapters = ['9', None, '10']
    expected_icd9dxvalidity = [True, None, True]
    expected_icd9procvalidity = [True, None, False]
    expected_level_3 = ['567', None, '601']
    expected_cci = [False, None, False]

