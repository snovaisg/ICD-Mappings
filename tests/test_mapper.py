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
    expected_cci = False

    assert expected_icd10code == mapper.map(icd9code, source='icd9', target='icd10')
    assert expected_ccscode == mapper.map(icd9code, source='icd9', target='ccs')
    assert expected_cci == mapper.map(icd9code, source='icd9', target='cci')
    assert expected_chapter == mapper.map(icd9code, source='icd9', target='chapter')
    assert expected_icd9dxvalidity == mapper.validate_diagnostics(icd9code, 'icd9')
    assert expected_icd9procvalidity == mapper.validate_procedures(icd9code, 'icd9')

    icd9codes = ['5679', 235, '6010']
    expected_icd10codes = ['K659', None, 'N410']
    expected_ccscodes = ['148', None, '165']
    expected_chapters = ['9', None, '10']
    expected_icd9dxvalidity = [True, False, True]
    expected_icd9procvalidity = [True, False, False]
    expected_cci = [False, None, False]

    assert expected_icd10codes == mapper.map(icd9codes, source='icd9', target='icd10')
    assert expected_ccscodes == mapper.map(icd9codes, source='icd9', target='ccs')
    assert expected_cci == mapper.map(icd9codes, source='icd9', target='cci')
    assert expected_chapters == mapper.map(icd9codes, source='icd9', target='chapter')
    assert expected_icd9dxvalidity == mapper.validate_diagnostics(icd9codes, 'icd9')
    assert expected_icd9procvalidity == mapper.validate_procedures(icd9codes, 'icd9')

    # test icd10 mappings to chapter

    expected_mappings = {'H05243':'7', 
                         'A0105': '1', 
                         'B658': '1', 
                         'C8333': '2', 
                         'D421': '2',
                         'D4981': None, # valid code but there's no mapping for it
                         'D528': '3', 
                         'M84651K': '13',
                         'L03114': '12', 
                         'Not a code':None,
                          62719: None,
                         'T25519D': '19'
                        }
    
    for code, expected in expected_mappings.items():
        result = mapper.map(code, source='icd10', target='chapter')
        assert result == expected

    # test icd10 mappings to ccsr

    expected_mappings = {'H05243':'EYE008', 
                         'A0105': 'INF003', 
                         'B658': 'INF009', 
                         'C8333': 'NEO058', 
                         'D421': 'NEO072',
                         'D4981': 'NEO072',
                         'D528': 'BLD001', 
                         'M84651K': 'MUS015',
                         'L03114': 'SKN001', 
                         'Not a code':None,
                          62719: None,
                         'T25519D': 'INJ056'
                        }
    
    for code, expected in expected_mappings.items():
        result = mapper.map(code, source='icd10', target='ccsr')
        assert result == expected
    

