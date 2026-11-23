"""Complete normalized matches preserve original source slices and ambiguity."""
import unittest
from unittest.mock import patch

import quote_lookup


class QuoteLookupTest(unittest.TestCase):
    def find(self, source, quote):
        return quote_lookup.find_quote(quote, source, quote_lookup.build_index(source))

    def test_repeated_identical_source_values_do_not_choose_a_position(self):
        source = 'Shipments began in May . Shipments began in May .'
        self.assertEqual(self.find(source, 'Shipments began in May.'), 'Shipments began in May .')

    def test_distinct_original_values_are_not_silently_chosen(self):
        source = 'Shipments began in May . SHIPMENTS began in May .'
        self.assertIsNone(self.find(source, 'Shipments began in May.'))

    def test_casefold_search_does_not_accept_a_partial_expansion(self):
        self.assertIsNone(self.find('ß', 'ss'))
        self.assertEqual(self.find('İ i', 'i'), 'i')

    def test_greek_word_boundary_is_checked_as_an_original_slice(self):
        self.assertEqual(self.find('ΟΣ,', 'σ ,'), 'Σ,')
        self.assertEqual(self.find('ΟΣΑ', 'ος'), 'ΟΣ')

    def test_possessive_spacing_locates_original_source(self):
        self.assertEqual(self.find("Amazon 's next chip", "Amazon's next chip"), "Amazon 's next chip")

    def test_mapping_failure_is_explicit_even_when_assertions_are_disabled(self):
        with patch.object(quote_lookup, 'normalise', return_value='different'):
            with self.assertRaises(ValueError):
                quote_lookup.build_index('Source text')


if __name__ == '__main__':
    unittest.main()
