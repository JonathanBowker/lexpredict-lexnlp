from typing import List, Tuple

from lexnlp.extract.common.special_characters import SpecialCharacters

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2019, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-lexnlp/blob/master/LICENSE"
__version__ = "0.2.7"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


class IntroductoryWordsDetector:
    # introductory words, detected by dictionary and POS
    # e.g. (so called "champerty' => "champerty')
    # should be removed
    INTRO_ADVERBS = {'so', 'also'}
    INTRO_VERBS = {'called', 'known', 'named'}

    INTRODUCTORY_POS = [
        [('RB', INTRO_ADVERBS), ('VBN', INTRO_VERBS)], # so called
        [('RB', INTRO_ADVERBS), ('JJ', INTRO_VERBS)], # so called, but "called" is adjective
        [('VBN', INTRO_VERBS)] # called
    ]

    # pylint:disable=unnecessary-lambda
    MAX_INTRO_LEN = len(max(INTRODUCTORY_POS, key=lambda i: len(i)))

    # punctuation POS that we have to skip while, e.g., removing introductory words
    PUNCTUATION_POS = {'``', '\t'}.union(SpecialCharacters.punctuation)

    @staticmethod
    def remove_term_introduction(term: str,
                                 term_pos: List[Tuple[str, str]]) -> str:
        """
        so called "champerty' => "champerty'
        """
        trim_pos = 0
        # index of significant word within the term (not punctuation)
        word_index = -1

        for word, pos, _, end in term_pos:
            # don't count punctuation
            if word in IntroductoryWordsDetector.PUNCTUATION_POS:
                continue

            word_index += 1
            if word_index == IntroductoryWordsDetector.MAX_INTRO_LEN:
                break
            word = word.lower()
            for intro in IntroductoryWordsDetector.INTRODUCTORY_POS:
                if word_index >= len(intro):
                    continue
                if pos != intro[word_index][0]:
                    continue
                if word not in intro[word_index][1]:
                    continue
                trim_pos = end + 1
            if trim_pos == 0:
                break

        if trim_pos == 0:
            return term
        term = term[trim_pos:]
        term = term.strip()
        return term
