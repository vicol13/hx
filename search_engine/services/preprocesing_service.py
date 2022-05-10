from collections import defaultdict
from search_engine.core.config import STOP_WORDS
from typing import DefaultDict, Set
import abc


class AbstractPreprocesingService:
    """
        defines the contract for preprocesing services which have to return an inverted index
    """

    @abc.abstractmethod
    def process(self, doc_name: str, doc: str, dictionary: DefaultDict[str, Set])->DefaultDict[str, Set]:
        """
        :rparam doc_name: name of the document
        :rparam doc:   input string which will be tokenized 
        :rparam dictionary: represent a default map in case when we want to get new index for current document
                            or to update and existing index with this document 
            
            :rtype: dictionary of next format:
            {
                '<word>':[(<name_of_file>,(<starting_index>,<ending_index>)),...]
                
            }
            indexes represent the begin and the end of the sentence where word had been found
        """
        raise NotImplementedError("Call on abstraction method of AbstractPreprocesingService")


class RawPreprocesingService:
    """
        implementation AbstractPreprocesingService which does't perform any special preprocesing steps 
        on corpus it just index each word 
    """

    def process(self, doc_name: str, doc: str, dictionary: DefaultDict[str, Set] = defaultdict(set)) -> DefaultDict[str, Set]:
        """
            parse the document remove stop words and return inverted index of document
        """
        starting_index = 0

        for phrase in doc.split('.'):
            ending_index = starting_index + len(phrase)

            # phrase as a set without stop words
            _phrase = set(phrase.lower().split()).difference(STOP_WORDS)

            for word in _phrase:
                dictionary[word].add((doc_name, (starting_index, ending_index)))
            starting_index += len(phrase) + 1
        return dictionary
