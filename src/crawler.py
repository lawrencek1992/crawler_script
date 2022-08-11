import re
from collections import Counter, OrderedDict

import requests
from bs4 import BeautifulSoup


def get_history_words(request):
    """
    Take the request from the Microsoft Wiki url and return only the text in the 'History' section of the Microsoft Wiki. 

    :param request: Request returned from the Microsoft Wiki page.

    :returns:  ["word1", "word2", "word3", ...]

    :rtype: list
    """
    # BeautifulSoup.get_text() returns all of the text on given web page. 
    # Strip white spaces at beginning and end of wiki_text. 
    # Convert to lower case. 
    wiki_text = BeautifulSoup(request.text, "html.parser").get_text(" ").strip().lower()

    # Replace unicode characters and new line charactes with " ". 
    # Remove all forward slashes.
    # Remove all remaining characters which are not letters or spaces.
    chars_to_replace = [
        ("\\n", " "),
        ("\\xa0", " "),
        ("\\u200a", " "),
        ("\\u202f", " "),
        ("\/", ""),
        ("[^a-z\s]", ""),
    ]
    for replacement in chars_to_replace:
        wiki_text = re.sub(replacement[0], replacement[1], wiki_text)

    # Search for the "History" section of the text with the substrings which begin and end that section.
    # Split the "History" string into a list so that it can be passed to Counter.
    # Return the list of "History" words. 
    return re.search("(?:history   further information).+(?:us federal trade commission)", wiki_text).group(0).split()


def process_words(history_words, num_words_to_return, words_to_exclude):
    """
    Count the number of times each word appears.
    Remove any words_to_exclude. 
    Return the first n words and their counts, where n=num_words_to_return.

    :param list history_words: A list of all the words which appear in the "History" section of the Microsoft Wiki. 

    :param int num_words_to_return: How many words should be returned.

    :param list words_to_exclude: Words which should not be returned, even if they are among the most common words.

    :returns:  {
        word_1: 100,
        word_2: 99,
        ...
    }

    :rtype: dict

    """
    counter = Counter(history_words)

    if words_to_exclude:
        for word in words_to_exclude:
            del counter[word.lower()]

    most_common_words = OrderedDict(counter.most_common(num_words_to_return))
    print("Most Common Words: ", most_common_words)
    return most_common_words


def main(
    num_words_to_return=None, 
    words_to_exclude=None,
):
    """Find the number of occurences of the most common words on the history section of the Microsoft Wikipedia page.

    :param int num_words_to_return: How many words should be returned. Defaults to 10.

    :param list words_to_exclude: Words which should not be returned, even if they are among the most common words. Defaults to None

    :returns:  {
        word_1: 100,
        word_2: 99,
        ...
    }

    :rtype: dict
    """

    if not num_words_to_return:
        num_words_to_return=10
    print(f"Returning the {num_words_to_return} most common words")

    if not words_to_exclude:
        print("No words are excluded")
    else:
        print(f"Return value will not include: {words_to_exclude}")

    request = requests.get("https://en.wikipedia.org/wiki/Microsoft")
    history_words = get_history_words(request)
    return process_words(
        history_words,
        num_words_to_return,
        words_to_exclude
    )


if __name__ == "__main__":
    main()
