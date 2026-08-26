"""Tests that the dataset-builder language dropdown covers every valid code.

The dropdown previously hardcoded ten choices (en, zh, ja, ko, es, fr, de, pt,
ru, unknown), so languages the model accepts could not be selected when building
a training dataset. Samples were then labelled "unknown", which after the lyric
prompt parity fix ends up in the training header while inference sends the real
code.
"""

import unittest

try:
    from acestep.constants import VALID_LANGUAGES
    from acestep.ui.gradio.interfaces.training_dataset_tab_label_preview import (
        DATASET_LANGUAGE_CHOICES,
    )

    _IMPORT_ERROR = None
except ImportError as exc:  # pragma: no cover
    VALID_LANGUAGES = None
    DATASET_LANGUAGE_CHOICES = None
    _IMPORT_ERROR = exc


@unittest.skipIf(DATASET_LANGUAGE_CHOICES is None, f"import unavailable: {_IMPORT_ERROR}")
class DatasetLanguageChoicesTests(unittest.TestCase):
    """The dropdown must offer every model-supported language."""

    def test_every_valid_language_is_selectable(self):
        """No supported code is missing from the dropdown."""
        missing = [code for code in VALID_LANGUAGES if code not in DATASET_LANGUAGE_CHOICES]
        self.assertEqual(missing, [])

    def test_hindi_and_punjabi_are_selectable(self):
        """Regression: 'hi' and 'pa' were both absent from the hardcoded list."""
        self.assertIn("hi", DATASET_LANGUAGE_CHOICES)
        self.assertIn("pa", DATASET_LANGUAGE_CHOICES)

    def test_instrumental_marker_is_offered_first(self):
        """scan.py reads 'instrumental' as a marker, so it stays available."""
        self.assertEqual(DATASET_LANGUAGE_CHOICES[0], "instrumental")

    def test_choices_have_no_duplicates(self):
        """'instrumental' is not a VALID_LANGUAGES entry, so nothing repeats."""
        self.assertEqual(len(DATASET_LANGUAGE_CHOICES), len(set(DATASET_LANGUAGE_CHOICES)))


if __name__ == "__main__":
    unittest.main()
