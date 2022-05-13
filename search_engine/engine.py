from collections import defaultdict
from typing import DefaultDict
from search_engine.services.corpus_service import TextCorpusService, AbstractCorpusService
from search_engine.services.preprocesing_service import RawPreprocesingService, AbstractPreprocesingService
from loguru import logger
from typing import DefaultDict, Set, List

class Engine:
    """
    Core class of the project which load the corpus, preprocess it, 
    and store in memory inverted index 
    """

    def __init__(self, corpus_service: AbstractCorpusService, preprocessor: AbstractPreprocesingService):
        self.__corpus_service = corpus_service
        self.__preprocessor = preprocessor
        self.__indicies: DefaultDict[str, DefaultDict[str, Set]] = defaultdict(lambda: defaultdict(set))

        logger.debug('indexing corpus')
        for name, doc in self.__corpus_service.load_corpus():
           self.__indicies = self.__preprocessor.process(name, doc, dictionary=self.__indicies)
        logger.debug('indexing finished')

    def search(self, word: str) -> dict:
        word = word.lower()
        if word not in self.__indicies:
            return {}
        return self.__collect_entries(word)

    def __collect_entries(self, word: str) -> DefaultDict[str, List[str]]:
        """
        Function which will extract the sentence from files based on key word,
        and will map everything into dictionary
        """
        collecting_dict = defaultdict(list)
        word_metadata = self.__indicies[word]

        for file in word_metadata:
            try:
                doc = self.__corpus_service.load_document(file)
            except FileNotFoundError:
                logger.error(f'file {file} is missing from corpus')
                return {}

            for phrase_range in word_metadata[file]:
                start, end = phrase_range
                collecting_dict[file].append(doc[start:end].strip())

        return collecting_dict
