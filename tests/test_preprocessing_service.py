
from collections import defaultdict
from search_engine.services.preprocesing_service import PreprocesingService


def test_preprocessing():
    # given 
    service = PreprocesingService()
    input = 'Java is bad. Python is not better.'

    # when 
    output = service.process('file',input,defaultdict(set))

    #then
    assert 'java' in output.keys(), "word [java] is missing from dictionary of indexed word"
    assert 'bad' in output.keys(), "word [bad] is missing from dictionary of indexed word"
    assert len(output['java']) == 1, f"expected occurences of [java] in dict is [1] got [{len(output['java'])}]"
    assert len(output['bad']) == 1, f"expected occurences of [bad] in dict is [1] got [{len(output['bad'])}]"
    assert ('file',(0,11)) in output['java'],f'sentence is not indexed in the right way'
    assert ('file',(0,11)) in output['bad'],f'sentence is not indexed in the right way'
    
    assert 'python' in output.keys(), "word [python] is missing from dictionary of indexed word"
    assert 'better' in output.keys(), "word [better] is missing from dictionary of indexed word"
    assert len(output['python']) == 1, f"expected occurences of [java] in dict is [1] got [{len(output['python'])}]"
    assert len(output['better']) == 1, f"expected occurences of [bad] in dict is [1] got [{len(output['better'])}]"
    assert ('file',(12,33)) in output['python'],f'sentence is not indexed in the right way'
    assert ('file',(12,33)) in output['better'],f'sentence is not indexed in the right way'
  
    assert 'is' not in output.keys(), f"stop word [in] is in the dictionary of indexed word"
    assert 'not' not in output.keys(), f"stop word [not] is in the dictionary of indexed word"


def test_word_is_indexed_more_than_one_time():
    # given
    output = PreprocesingService().process('file','Java is bad. Python is not better than Java.',defaultdict(set))

    # then
    assert ('file',(0,11)) in output['java'], f'sentence is not indexed in the right way'
    assert ('file',(12,43)) in output['java'],f'sentence is not indexed in the right way'



def test_check_if_fun_is_updating_existing_dict():
    # given 
    service = PreprocesingService()
    
    # when
    output = service.process('file','Java is bad. Python is not better.',defaultdict(set))
    output = service.process('file2','Kotlin has some benefits',output)

    # then
    assert 'java' in output.keys(), "word [java] is missing from dictionary of indexed word"
    assert 'bad' in output.keys(), "word [bad] is missing from dictionary of indexed word"
    assert len(output['java']) == 1, f"expected occurences of [java] in dict is [1] got [{len(output['java'])}]"
    assert len(output['bad']) == 1, f"expected occurences of [bad] in dict is [1] got [{len(output['bad'])}]"
    assert ('file',(0,11)) in output['java'],f'sentence is not indexed in the right way'
    assert ('file',(0,11)) in output['bad'],f'sentence is not indexed in the right way'
    
    assert 'python' in output.keys(), "word [python] is missing from dictionary of indexed word"
    assert 'better' in output.keys(), "word [better] is missing from dictionary of indexed word"
    assert len(output['python']) == 1, f"expected occurences of [python] in dict is [1] got [{len(output['python'])}]"
    assert len(output['better']) == 1, f"expected occurences of [better] in dict is [1] got [{len(output['better'])}]"
    assert ('file',(12,33)) in output['python'],f'sentence is not indexed in the right way'
    assert ('file',(12,33)) in output['better'],f'sentence is not indexed in the right way'

    assert 'kotlin' in output.keys(), "word [kotlin] is missing from dictionary of indexed word"
    assert 'benefits' in output.keys(), "word [benefits] is missing from dictionary of indexed word"
    assert len(output['kotlin']) == 1, f"expected occurences of [kotlin] in dict is [1] got [{len(output['python'])}]"
    assert len(output['benefits']) == 1, f"expected occurences of [benefits] in dict is [1] got [{len(output['better'])}]"
    assert ('file2',(0,24)) in output['kotlin'],f'sentence is not indexed in the right way'
    assert ('file2',(0,24)) in output['benefits'],f'sentence is not indexed in the right way'

    assert 'is' not in output.keys(), f"stop word [in] is in the dictionary of indexed word"
    assert 'not' not in output.keys(), f"stop word [not] is in the dictionary of indexed word"
    assert 'has' not in output.keys(), f"stop word [has] is in the dictionary of indexed word"
    assert 'some' not in output.keys(), f"stop word [some] is in the dictionary of indexed word"

