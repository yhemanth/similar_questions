import sys
from pathlib import Path

import pytest
from similar_questions import print_representative_questions

def test_print_representative_questions_mixed_formats(capsys):
    # Covers: plain "12. ..." and bolded "**7.** ..." formats, plus an unmatched line
    representatives = [
        (0, "12. How to foo?"),
        (1, "**7.** When bar?"),
        (2, "not numbered question"),
    ]

    print_representative_questions(representatives)
    output_lines = capsys.readouterr().out.splitlines()

    # Header printed
    assert output_lines[0] == "Representative questions from each cluster:"

    # Unmatched line reported
    assert "No match found." in output_lines

    # Extracted questions printed in ascending numeric order (7 before 12)
    assert "**7.** When bar?" in output_lines
    assert "12. How to foo?" in output_lines
    assert output_lines.index("**7.** When bar?") < output_lines.index("12. How to foo?")


def test_print_representative_questions_all_unmatched(capsys):
    # No lines match the pattern
    representatives = [
        (0, "Question A with no number"),
        (1, "Another question without numbering"),
    ]

    print_representative_questions(representatives)
    output_lines = capsys.readouterr().out.splitlines()

    # Header printed
    assert output_lines[0] == "Representative questions from each cluster:"

    # Each unmatched line prints "No match found."
    assert output_lines.count("No match found.") == 2

    # No extracted questions printed
    assert len(output_lines) == 3