import io
from os import path


class TextModerationBase:
    """Base Class for text moderation classes"""

    def __init__(self, wordlist_file: str):
        """Arguments:
        `wordlist_file` str - path to file containing flag words for
        filtering content"""
        self._wordlist = wordlist_file
        self._words = self.open_words(self._wordlist)

    def open_words(self, file_name: str) -> set:
        """function that opens a .csv file containing one column of flag words
        returns a set of words to use in comparison method
        self.check_word(word: str)
        Arguments:
        ---
        `file_name` str - name of file containing flag words for filtering
        **Note** - at this time the only type/format of file supported is .csv with one column of flag words.

        Returns:
        ---
        `set` - unique tokenized words contained in open(`file_name`)"""

        # open file
        word_file = open(file_name, "rt")
        # splits the csv format out of a data in file then strips header
        # and cast to a set
        data = set(word_file.read().split(",\n")[1:])
        # close file
        word_file.close()
        # return set of words
        return data

    def check_word(self, word: str) -> bool:
        """Function that checks membership of word in self._words set
        Arguments:
        ---
        `word` str - word in sample that is being checked for moderation

        Returns:
        ---
        bool: True if the word passed is a member of self._words set,
        otherwise False"""
        return word in self._words


class BadWordTextModerator(TextModerationBase):
    """Class that filters content with self.check_words(word: str) against a
    list of known inappropriate words
    for more information on specific methods see help(TextModerationBase)"""

    def __init__(self, wordlist_file: str):
        super().__init__(wordlist_file)

    def check_word(self, word: str) -> bool:
        return super().check_word(word)


class SensitiveContentTextModerator(TextModerationBase):
    """Class that filters content with self.check_word(word: str) against a
    list of known abuse flagged words
    for more information on specific methods see help(TextModerationBase)"""

    def __init__(self, wordlist_file: str):
        super().__init__(wordlist_file)

    def check_word(self, word: str) -> bool:
        return super().check_word(word)
