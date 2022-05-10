import glob
from typing import Tuple,Generator
from search_engine.core.exceptions import EmptyCorpusException
from search_engine.core.config import CORPUS_PATH
from loguru import logger
import abc


class AbstractCorpusService:
    """
        defines contract for corpus services
    """

    @abc.abstractclassmethod
    def load_corpus(self)-> Generator[Tuple[str, str], None, None]:
        raise NotImplementedError("Call on abstraction method of AbstractCorpusService")



class TextCorpusService(AbstractCorpusService):
    """
        implementation of AbstractCorpusService which load files/corpus from a folder 
    """

    def __init__(self, corpus_path: str = CORPUS_PATH):
        self._corpus_path = corpus_path
   

    def load_corpus(self) -> Tuple[str, str]:
        """
            creates a generetor for files inside the corpus folder
            
            :param root_folder: path to corpus folder
            :rtype Iterator for file name and file content
        """
        root_len = len(self._corpus_path)
        files_path = glob.glob(f'{self._corpus_path}*.txt')
        

        if len(files_path) == 0:
            raise EmptyCorpusException(f"empty corpus at {self._corpus_path}")
            
       
        for path in files_path:
            file_name = path[root_len:-4]
            yield file_name, self.load_file(file_name)

    
    def load_file(self, name: str) -> str:
        with open(f'{self._corpus_path}{name}.txt') as file:
            return file.read().replace('\n', '')
            
