from search_engine.engine import Engine
from search_engine.services.corpus_service import TextCorpusService
from search_engine.services.preprocesing_service import RawPreprocesingService
from unittest.mock import MagicMock



def test_search_of_word_which_exist_in_corpus():
    
    # given
    f1_name,f1_doc = 'Java and python','Java is bad. Python is not better.'
    f2_name,f2_doc = 'Introducing Kotlin', 'Kotlin has some benefits'
    
    corpus_service = MagicMock()
    preprocesing_service = RawPreprocesingService()
    corpus_service.load_corpus.return_value =  iter([(f1_name,f1_doc),(f2_name,f2_doc)])
    corpus_service.load_document.side_effect = ['Java is bad. Python is not better.','Kotlin has some benefits']

    engine = Engine(corpus_service = corpus_service, preprocessor = preprocesing_service)
    
    # when & then
    r1 = engine.search('java')

    assert len(r1) ==1 , f"engine found [{len(r1)}] more occurences of [java] than expected [1]"
    assert f1_name in r1.keys(), "Name of file is missing from search"
    assert len(r1[f1_name]) == 1, f"engine found [{len(r1[f1_name])}] matches of [java] expected [1]"
    assert 'Java is bad' == r1[f1_name][0], "expected sentence don't match with output of eninge"

    r2 = engine.search('kotlin')

    assert len(r2) ==1 , f"engine found [{len(r2)}] more occurences of [kotlin] than expected [1]"
    assert f2_name in r2.keys(), "Name of file is missing from search"
    assert len(r2[f2_name]) == 1, f"engine found [{len(r2[f2_name])}] matches of [koltin] expected [1]"
    assert 'Kotlin has some benefits' == r2[f2_name][0], "expected sentence don't match with output of eninge"
    

def test_earch_of_missing_word():
    # given
    f1_name,f1_doc = 'Java and python','Java is bad. Python is not better.'
    f2_name,f2_doc = 'Introducing Kotlin', 'Kotlin has some benefits'
    
    corpus_service = MagicMock()
    preprocesing_service = RawPreprocesingService()
    corpus_service.load_corpus.return_value =  iter([(f1_name,f1_doc),(f2_name,f2_doc)])
    
    # when 
    engine = Engine(corpus_service = corpus_service, preprocessor = preprocesing_service)
    
    # then
    r1 = engine.search('rust')
    assert len(r1) == 0