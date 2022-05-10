from collections import defaultdict
from search_engine.services.corpus_service import CorpusService
from search_engine.services.preprocesing_service import PreprocesingService
from loguru import logger
from typing import DefaultDict, Set


class Engine:
    """
        core class of the project which load the corpus, preprocess it, and store in memory
        reversed index 
    """

    def __init__(self, corpus_service=CorpusService(), preprocessor=PreprocesingService()):
        self._corpus_service:CorpusService = corpus_service
        self._preprocessor:PreprocesingService = preprocessor
        self._index = defaultdict(set)

        logger.debug('indexing corpus')
        for name, doc in self._corpus_service.load_corpus():
            self._preprocessor.process(name, doc, self._index)
        logger.debug('indexing finished')

    def search(self, word: str) -> dict:
        _word = word.lower()
        if _word not in self._index.keys():
            return {}
        return self._colect_entries(_word)

    def _colect_entries(self, word: str) -> DefaultDict[str, Set]:
        """
            function which will extract the sentence from files based on key word,
            and will map everything into dictionary
        """
        collecting_dict = defaultdict(list)
        word_metadata = self._index[word]

        for file, phrase_range in word_metadata:

            try:
                doc = self._corpus_service.load_file(file)
            except IOError:
                logger.error(f'file {file} is missing from corpus')
                return {}

            starting_index, ending_index = phrase_range
            collecting_dict[file].append(doc[starting_index:ending_index].strip())

        return collecting_dict
