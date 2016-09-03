"""https://en.wikipedia.org/wiki/String_metric"""
import string


def remove_punctuation(s):
    for x in string.punctuation:
        s = s.replace(x, '')
    return s


rp = remove_punctuation


def camelcase(s):
    """Converts each word to title case then removes whitespace.
     Punctuation is removed"""
    return string.capwords(rp(s)).replace(' ', '')


def char_case(s, sep=None):
    """Converts string to lower case then replaces whitespace with given character.
    Punctuation is removed"""
    return (sep or '').join(x.lower() for x in rp(s).split())


def snake_case(s):
    """Converts string to lower case then replaces whitespace with underscores.
    Punctuation is removed"""
    return char_case(rp(s), '_')


def hyphen_case(s):
    """Converts string to lower case then replaces whitespace with hyphen.
    Punctuation is removed"""
    return char_case(rp(s), '-')


def levenshtein_dist(s1, s2):
    """Measure of the difference between two sequences(strings)"""
    if len(s1) < len(s2):
        return levenshtein_dist(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer than s2
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]
