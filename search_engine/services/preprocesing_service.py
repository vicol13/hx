from collections import defaultdict
from search_engine.core.config import STOP_WORDS


class PreprocesingService:
    """
        class which is responsible for tokenization of documents and then mapping to reversed index map

        note:   ideally this class should have an interface contract but is not
                needed for python implementation
    """

    def process(self, doc_name: str, doc: str, dictionary: defaultdict = defaultdict(set)) -> str:
        """
            parse the document remove stop words and return reversed index of document
            :rparam doc:   input string which will be tokenized 
            :rparam dictionary: represent a default map in case when we want to get new index for current document
                                or to update and existing index with this document 
            
            :rtype: dictionary of next format:
            {
                '<word>':[(<name_of_file>,(<starting_index>,<ending_index>)),...]
                ...
            }
            indexes represent the begin and the end of the sentence where word had been found
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
