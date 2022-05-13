from typing import Tuple, Generator,Protocol
from pathlib import Path
from loguru import logger
from search_engine.core.exceptions import EmptyCorpusException
from search_engine.core.config import CORPUS_PATH





class AbstractCorpusService(Protocol):
    """
    Defines contract for corpus services which should load the data into memory.
    """

    def load_corpus(self) -> Generator[Tuple[str, str], None, None]:
        """
        Creates a generetor for files/sql-row/no-sql corpus
        :rtype Generator for file name and file content
        """

    def load_document(self, doc_name: str) -> str:
        """
        Should return the document by name
        """


class TextCorpusService(AbstractCorpusService):
    """
    Implementation of AbstractCorpusService which load files/corpus from a folder
    """

    def __init__(self, corpus_path: str = CORPUS_PATH):
        self.__corpus_path: Path = Path(corpus_path)

    def load_corpus(self) -> Generator[Tuple[str, str], None, None]:
        """
        List files from folder and return name of the file with content of the file
        """
        files_list = list(self.__corpus_path.glob('*.txt'))

        if not files_list:
            logger.error('Corpus is missing')
            raise EmptyCorpusException(str(self.__corpus_path.absolute()))

        for path in files_list:
            yield path.stem, self.load_document(path.stem)

    def load_document(self, doc_name: str) -> str:
        with self.__corpus_path.joinpath(f'{doc_name}.txt').open('r') as file:
            return file.read().replace('\n', '')
