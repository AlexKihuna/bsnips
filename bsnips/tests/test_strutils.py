from unittest import TestCase

from bsnips.utils.strutils import (
    snake_case, camelcase, char_case, hyphen_case, levenshtein_dist, remove_punctuation
)


class TestStrUtils(TestCase):
    def setUp(self):
        self.st = "The quick    brown    !$*     fox is Lazy."

    def test_remove_punctuation(self):
        self.assertEquals(
            remove_punctuation(self.st),
            'The quick    brown         fox is Lazy'
        )

    def test_camelcase(self):
        self.assertEquals(camelcase(self.st), 'TheQuickBrownFoxIsLazy')

    def test_char_case(self):
        self.assertEquals(char_case(self.st, '.'), 'the.quick.brown.fox.is.lazy')

    def test_snake_case(self):
        self.assertEquals(snake_case(self.st), 'the_quick_brown_fox_is_lazy')

    def test_hyphen_case(self):
        self.assertEquals(hyphen_case(self.st), 'the-quick-brown-fox-is-lazy')

    def test_levenshtein_dist(self):
        self.assertEquals(levenshtein_dist('brown', 'brawn'), 1)
