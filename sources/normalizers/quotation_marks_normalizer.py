from typing import Tuple, List
import re

from sources.normalizers.abstract_normalizer import AbstractNormalizer
from sources.normalizers.constants import Constants

# https://slovnyk.ua/pravopys.php?prav_par=164
# fill_quotation_marks(input, divider="|", outer_open="[", outer_close="]", inner_open="(", inner_close=")")
FILL_QUOTATION_MARKS_EXPECTED_BEHAVIOUR = [
    "a [b] c",  # Word in quotation marks
    "[a b c]",  # Sentence in quotation marks
    "[a] b [c]",  # Multiple quotations in a sentence

    "[a (b) c]",  # Nested quotations for a single word
    "[a (b) (c)]",  # Nested quotations for multiple words

    "а [є]! в [г (ґ) (ї), - к]",  # Supports Ukrainian language
    "а [1]! b [c (5), - d]",  # Supports numbers
    # "a [!], b [?] c [;], - d",  # Supports punctuation marks
    "a b [c d.]. e",  # Supports periods within quotation marks, e.g., for abbreviations
    "a [b].\n[c]\nd e f",  # Supports line breaks
    "[a b c.]- d",  # Supports hyphens
    "[a b c ], - d",  # Supports commas
    "[a (b)?], – b",

    "[(a b [c], - d), - e]", "[a (b [c]) d]",  # Quotation marks alternate with deep nesting

    "a [b?] c d [b] e",  # Handles quotation marks after punctuation with space

    # Handles quotation marks after punctuation without spaces
    "a [b?], - c d [b] e",
    "a [b?]; c d [b] e",
    "a [b c d, e f?]; j k, a b [c d!]?",

    # Handles quotation marks before punctuation with space for numbers
    "a [b 5]? c d [b] e",
    "a [b 5]! c d [b] e",

    "[([a b] [c] d)]", "[([(a + b) - (c)])]", "[([(a)])]",  # Handles adjacent quotation marks

    # Odd number of quotation marks are also normalized, but without nesting
    "[a b",
    "a b]",
    "[a [b]",
    "[a [b [c] c]",
    "a [a a, - a a a. a a. [a a. a a, - a.",
    "a [a] a], - [a] a a. a a. [a a. a a, - a.",
]


class QuotationMarksNormalizer(AbstractNormalizer):
    """
    Quotation marks normalizer.

    Performs three main functions:
    1. Unification of different quotation mark types into a standard delimiter
    2. Replacement of unified delimiters with paired quotation marks based on context
    3. Implementation of alternating styles for nested quotations
    """

    @staticmethod
    def name() -> str:
        return "QuotationMarksNormalizer"

    @staticmethod
    def normalize(
        text: str,
        divider=Constants.DEFAULT_QUOTE,
        spacer=Constants.SPACE,
        outer_open=Constants.QUOTE_OUTER_OPEN,
        outer_close=Constants.QUOTE_OUTER_CLOSE,
        inner_open=Constants.QUOTE_INNER_OPEN,
        inner_close=Constants.QUOTE_INNER_CLOSE,
    ) -> Tuple[str, List[str], List[str]]:
        """
        Main text normalization method.

        Args:
            text: Input text for normalization
            divider: Delimiter symbol that will be replaced with quotation marks
            spacer: Space character
            outer_open: Opening outer quotation mark symbol
            outer_close: Closing outer quotation mark symbol
            inner_open: Opening inner quotation mark symbol
            inner_close: Closing inner quotation mark symbol

        Returns:
            Tuple[str, List[str], List[str]]: Normalized text, warnings, and errors
        """

        # Step 1: Symbol unification
        unified_text = QuotationMarksNormalizer.unify_quotes(text)

        # Step 2: Contextual replacement
        processed_text, errors = QuotationMarksNormalizer.replace_quotation_marks(
            unified_text, divider, spacer, outer_open, outer_close, inner_open, inner_close
        )

        if errors:
            return processed_text, [], errors

        # Step 3: Nested quotation handling
        processed_text, warnings = QuotationMarksNormalizer.process_nested_quotations(
            processed_text, outer_open, outer_close, inner_open, inner_close
        )

        return processed_text, warnings, []

    @staticmethod
    def unify_quotes(text: str) -> str:
        """
        Replaces various quotation mark symbols with a standard delimiter.

        Args:
            text: Input text for normalization

        Returns:
            str: Text with unified quotation marks
        """
        marks = Constants.QUOTATION_MARKS.copy()

        marks.remove(Constants.DEFAULT_QUOTE)
        marks.remove(Constants.QUOTE_OUTER_OPEN)
        marks.remove(Constants.QUOTE_OUTER_CLOSE)

        for mark in marks:
            text = text.replace(mark, Constants.DEFAULT_QUOTE)

        return text

    @staticmethod
    def replace_quotation_marks(
        text: str,
        divider=Constants.DEFAULT_QUOTE,
        spacer=Constants.SPACE,
        outer_open=Constants.QUOTE_OUTER_OPEN,
        outer_close=Constants.QUOTE_OUTER_CLOSE,
        inner_open=Constants.QUOTE_INNER_OPEN,
        inner_close=Constants.QUOTE_INNER_CLOSE
    ) -> Tuple[str, List[str]]:
        """
        Replaces delimiters with contextually appropriate quotation marks.

        Args:
            text: Input text for processing
            divider: Delimiter symbol that will be replaced with quotation marks
            spacer: Space character
            outer_open: Opening outer quotation mark symbol
            outer_close: Closing outer quotation mark symbol
            inner_open: Opening inner quotation mark symbol
            inner_close: Closing inner quotation mark symbol

        Returns:
            Tuple[str, List[str]]: Processed text and list of errors
        """

        initial_value = text
        output = text

        # Replace divider next to alphabet: "a|" -> "a]", "|b" -> "[b"
        escaped_divider = re.escape(divider)
        output = re.sub(escaped_divider + r'(\w)', outer_open + r'\1', output)
        output = re.sub(r'(\w)' + escaped_divider, r'\1' + outer_close, output)

        # Replace divider on string edges: "|a b c|" -> "[a b c]"
        if output.startswith(divider):
            output = outer_open + output[1:]
        if output.endswith(divider):
            output = output[:-1] + outer_close

        punctuation = Constants.PUNCTUATION
        for punct in punctuation:
            if punct in [outer_open, outer_close, inner_open, inner_close, spacer, divider]:
                continue
            # Replace divider next to punctuation: "|," -> "],"
            output = output.replace(f"{divider}{punct}", f"{outer_close}{punct}")
            # Add support for abbreviations, e.g. "a [b.|. " -> "a [b.] "
            output = output.replace(f".{divider}{punct}{spacer}", f".{outer_close}{punct}{spacer}")

        # Replace divider next to hyphen: "|-" -> "]-"
        for hyphen in Constants.HYPHENS:
            output = output.replace(f"{divider}{hyphen}", f"{outer_close}{hyphen}")

        # Replace divider next to spacer: "| " -> "] " and " |" -> " ["
        output = output.replace(f"{divider}{spacer}", f"{outer_close}{spacer}")
        output = output.replace(f"{spacer}{divider}", f"{spacer}{outer_open}")

        # Replace on divider duplications
        patterns = [
            # |] -> ]]
            (f"{divider}{outer_close}", f"{outer_close}{outer_close}"),

            # [| -> [[
            (f"{outer_open}{divider}", f"{outer_open}{outer_open}"),

            # ]| -> ]]
            (f"{outer_close}{divider}", f"{outer_close}{outer_close}"),

            # |[ -> [[
            (f"{divider}{outer_open}", f"{outer_open}{outer_open}"),
        ]
        for pattern in patterns:
            while pattern[0] in output:
                output = output.replace(pattern[0], pattern[1])

        # Check if there are any delimiters left
        if output.count(divider) != 0:
            return initial_value, ["There are delimiters left in the text!"]

        return output, []

    @staticmethod
    def process_nested_quotations(
            text: str,
            outer_open=Constants.QUOTE_OUTER_OPEN,
            outer_close=Constants.QUOTE_OUTER_CLOSE,
            inner_open=Constants.QUOTE_INNER_OPEN,
            inner_close=Constants.QUOTE_INNER_CLOSE
    ) -> Tuple[str, List[str]]:
        """
        Processes nested quotations to implement alternating styles.

        Args:
            text: Input text containing quotation marks
            outer_open: Opening outer quotation mark symbol
            outer_close: Closing outer quotation mark symbol
            inner_open: Opening inner quotation mark symbol
            inner_close: Closing inner quotation mark symbol

        Returns:
            Tuple[str, List[str]]: Processed text with proper nested quotations and list of warnings
        """
        # Find all quotation mark indices
        quote_indices = []
        open_count = 0
        close_count = 0

        for i, char in enumerate(text):
            if char == outer_open:
                quote_indices.append((i, char))
                open_count += 1
            elif char == outer_close:
                quote_indices.append((i, char))
                close_count += 1

        if not quote_indices:
            return text, []  # If no quotation marks, return original text

        if open_count != close_count:
            return text, ["The number of open and close quotation marks is not equal!"]

        result = list(text)
        stack = []

        for idx, char in quote_indices:
            if char == outer_open:
                if stack and stack[-1] == outer_open:
                    result[idx] = inner_open
                    stack.append(inner_open)
                else:
                    stack.append(outer_open)
            elif char == outer_close:
                if stack:
                    last_open = stack.pop()
                    if last_open == inner_open:
                        result[idx] = inner_close

        return ''.join(result), []


if __name__ == "__main__":
    for expected_result in FILL_QUOTATION_MARKS_EXPECTED_BEHAVIOUR:
        input = expected_result.replace("[", "|").replace("]", "|").replace("(", "|").replace(")", "|")
        result, _, _ = QuotationMarksNormalizer.normalize(input, divider="|", outer_open="[", outer_close="]", inner_open="(", inner_close=")")
        assert result == expected_result, f"Input: {input}, expected: {expected_result}, result: {result}"

    print("All tests passed!")
#%%
