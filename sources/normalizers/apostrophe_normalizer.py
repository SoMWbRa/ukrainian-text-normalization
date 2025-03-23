from typing import Tuple, List
import re

from sources.normalizers.abstract_normalizer import AbstractNormalizer
from sources.normalizers.constants import Constants


class ApostropheNormalizer(AbstractNormalizer):

    @staticmethod
    def name() -> str:
        return "ApostropheNormalizer"

    @staticmethod
    def normalize(
        text: str,
        apostrophe=Constants.DEFAULT_APOSTROPHE,
        quote=Constants.DEFAULT_QUOTE
    ) -> Tuple[str, List[str], List[str]]:
        """
        Normalize apostrophes in the text. Handles possible use of apostrophes as quotation marks.

        Args:
            text: Input text for normalization
            apostrophe: Symbol to replace the apostrophe
            quote: Symbol to replace the quotation marks

        Returns:
            Tuple[str, List[str], List[str]]: Tuple with normalized text and a list of warnings and errors
        """

        warnings = []
        errors = []

        for symbol in Constants.APOSTROPHES:
            double_symbol_pattern = f"{re.escape(symbol)}{re.escape(symbol)}"
            text = re.sub(double_symbol_pattern, quote, text)

        text_list = list(text)
        text_list_without_space_quote = list(text)
        quote_count_before = text.count(quote)

        for symbol in Constants.APOSTROPHES:
            indices = [m.start() for m in re.finditer(symbol, text)]

            for index in indices:
                if index == 0 or index == len(text) - 1:
                    text_list[index] = quote
                    text_list_without_space_quote[index] = quote
                elif text[index - 1].isalpha() and text[index + 1].isalpha():
                    text_list[index] = apostrophe
                    text_list_without_space_quote[index] = apostrophe
                elif text[index - 1].isalpha() or text[index + 1].isalpha():
                    text_list[index] = quote
                    text_list_without_space_quote[index] = apostrophe
                elif text[index - 1] in Constants.PUNCTUATION:
                    text_list[index] = quote
                    text_list_without_space_quote[index] = quote
                elif text[index + 1] in Constants.PUNCTUATION:
                    text_list[index] = quote
                    text_list_without_space_quote[index] = quote
                else:
                    warnings.append(f"Warning: {symbol} at position {index}")

        quote_count_after = "".join(text_list).count(quote)

        quote_diff = quote_count_after - quote_count_before
        if quote_diff % 2 != 0 and quote_diff != 0:
            errors.append("Warning: odd number of quotes")
            return "".join(text_list_without_space_quote), warnings, errors

        return "".join(text_list), warnings, errors


if __name__ == "__main__":
    tests = [
        ("ʻжитиʼ", '"жити"'),
        ('"жити"', '"жити"'),
        ("‘жити’", '"жити"'),
        ("прем’єр", "премʼєр"),
        ("премʼєр", "премʼєр"),
        ("прем'єр-міністр", "премʼєр-міністр"),
        ("УДК 81'22:347.78.034", "УДК 81'22:347.78.034"),
        ("‘жити’, ", '"жити", '),
        ("'прем’єр' сім'я", '"премʼєр" сімʼя'),
        ("'прем'єр' сім'я", '"премʼєр" сімʼя'),
        ("oбʹєднання", "oбʼєднання"),
        ("''Дерево''", '"Дерево"'),
        ("''Дерево'', прем`єр", '"Дерево", премʼєр'),
        ("'Він!' - сказав він", '"Він!" - сказав він'),
        ("'Він!'- сказав він", '"Він!"- сказав він'),
        ("'Він!', - сказав він", '"Він!", - сказав він'),
        ("сказав:'Він!', - сказав він", 'сказав:"Він!", - сказав він'),
        ("сказав-'Він!', - сказав він", 'сказав-"Він!", - сказав він'),
        ("Сім ` я", "Сім ` я"),
    ]

    for input, expected_result in tests:
        output, _, _ = ApostropheNormalizer.normalize(input)
        assert output == expected_result, f"Input: {input}, expected: {expected_result}, result: {output}."

    print("All tests passed!")
#%%
