from collections import defaultdict
from search_engine.core.config import STOP_WORDS
from typing import DefaultDict, Set
from typing import Protocol


class AbstractPreprocesingService(Protocol):
    """
    Defines the contract for preprocesing services which have to return an inverted index
    """

    def process(self, doc_name: str, doc: str, dictionary: DefaultDict[str, DefaultDict[str, Set]]) -> DefaultDict[str, DefaultDict[str, Set]]:
        """
        :rparam doc_name: name of the document
        :rparam doc:   input string which will be tokenized 
        :rparam dictionary: represent a default map in case when we want to get new index for current document
                            or to update and existing index with this document 
            
            :rtype: dictionary of next format:
            {
                '<word>': {
                    '<document_name> : {(<start>,<end>),(<start>,<end>)},
                    '<document2_name> : {(<start>,<end>),(<start>,<end>)}
                }
                
            }
            indexes represent the begin and the end of the sentence where word had been found
        """
        pass


class RawPreprocesingService(AbstractPreprocesingService):
    """
    Implementation AbstractPreprocesingService which does't perform any special preprocesing steps 
    on corpus it just index each word 
    """

    def process(self, doc_name: str, doc: str, dictionary: DefaultDict[str, DefaultDict[str, Set]] = None) -> DefaultDict[str, DefaultDict[str, Set]]:
        """
        Parse the document remove stop words and return inverted index of document
        """
        dictionary = dictionary if dictionary else defaultdict(lambda: defaultdict(set))
        starting_index = 0

        for phrase in doc.split('.'):
            ending_index = starting_index + len(phrase)

            # phrase as a set without stop words
            _phrase = set(phrase.lower().split()).difference(STOP_WORDS)

            for word in _phrase:
                dictionary[word][doc_name].add((starting_index, ending_index))
            starting_index += len(phrase) + 1
        return dictionary
