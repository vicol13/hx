import glob
from typing import Tuple
from search_engine.core.exceptions import EmptyCorpusException
from search_engine.core.config import CORPUS_PATH
from loguru import logger
class CorpusService:
    """
        class which responsability is to interact with files/corpus

        note:   ideally this class should have an interface contract but is not
                needed for python implementation
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
            
