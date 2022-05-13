from search_engine.core.exceptions import EmptyCorpusException
from search_engine.services.corpus_service import TextCorpusService
import pytest
from .config import TEST_CORPUS_1,TEST_CORPUS_2,TEST_CORPUS_3

def test_load_document():
    # given
    service = TextCorpusService(corpus_path=TEST_CORPUS_1)
    expected_output = "test corpus1. second random phrase."
    
    # when
    loaded_file = service.load_document('file1')
    
    # then
    assert expected_output == loaded_file, "content of file don't match with expected output"

def test_load_corpus():
    # given
    service = TextCorpusService(corpus_path=TEST_CORPUS_2)
    expected_corpus = [('file1','test corpus1. second random phrase.'),('file2','test corpus2. random phrase of second corpus.')]
    
    # when
    loaded_corpus = {file:doc for file,doc in service.load_corpus()}
    
    # then
    assert 'file1' in loaded_corpus.keys(), "file is missing from loaded corpus"
    assert expected_corpus[0][1] == loaded_corpus['file1'], "content of documents don't match"
    assert 'file2' in loaded_corpus.keys(), "file is missing from loaded corpus"
    assert expected_corpus[1][1] == loaded_corpus['file2'], "content of documents don't match"

def test_load_corpus_root_dir_is_empty():
    # given
    service = TextCorpusService(corpus_path=TEST_CORPUS_3)
    
    # when
    with pytest.raises(EmptyCorpusException) as ctx:
        [x for x in service.load_corpus()]
   
    # then 
    assert "Empty corpus at" in str(ctx.value)