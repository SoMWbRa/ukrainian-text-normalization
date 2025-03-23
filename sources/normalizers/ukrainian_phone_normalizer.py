import re
from typing import Tuple, List

from sources.normalizers.abstract_normalizer import AbstractNormalizer


class UkrainianPhoneNormalizer(AbstractNormalizer):
    """
    Normalizes Ukrainian phone numbers to the format: +380 (XX) XXX-XX-XX or +380 (XXX) XX-XX-XX.
    Skips numbers that are part of another number series, for example: 0 800 33 92 91 56 12.
    Operator codes taken from https://www.vodafone.ua/support/faq/jak-diznatysj-kod-operatora
    """

    UKRAINE_OPERATOR_CODES = r"3[1-7]|4[1-8]|5[1-7]|6[1-4]|50|66|67|68|73|75|9[1-9]|89"
    UKRAINE_SPECIAL_CODES = r"800|900"

    REGULAR_PHONE_PATTERNS = [
        # AA_XXX_XX_XX
        # +380_(99)_123_45_67
        r"\+?380\s?\(?(\d{2})\)?[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # +38_(099)_123_45_67
        r"\+?38\s?\(?0(\d{2})\)?[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",

        # 0_(99)_123_45_67
        r"0[\s-]?(\d{2})[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # (099)_123_45_67
        r"\(0(\d{2})\)[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # 0 (99)_123_45_67
        r"0[\s-]?\((\d{2})\)[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",


        # АА_XX_XX_XXX
        # +380_(99)_12_34_567
        r"\+?380\s?\(?(\d{2})\)?[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})",
        # +38_(099)_12_34_567
        r"\+?38\s?\(?0(\d{2})\)?[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})",
        # 0_(99)_12_34_567
        r"0[\s-]?(\d{2})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})",
        # (099)_12_34_567
        r"\(0(\d{2})\)[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})",
        # 0 (99)_12_34_567
        r"0[\s-]?\((\d{2})\)[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})",

        # АА_XX_XXX_XX
        # +380_(99)_12_345_67
        r"\+?380\s?\(?(\d{2})\)?[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # +38_(099)_12_345_67
        r"\+?38\s?\(?0(\d{2})\)?[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # 0_(99)_12_345_67
        r"0[\s-]?(\d{2})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # (099)_12_345_67
        r"\(0(\d{2})\)[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # 0 (99)_12_345_67
        r"0[\s-]?\((\d{2})\)[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",

        # AAX_XX_XX_XX
        # +38_(0991)_23_45_67
        r"\+38[\s-]?\(0(\d{2})(\d{1})\)[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # (0991)_23_45_67
        r"\(0(\d{2})(\d{1})\)[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",

        # AAXX_X_XX_XX
        # +38 (09912)_3_45_67
        r"\+?38[\s-]?\(0(\d{2})(\d{1})(\d{1})\)[\s-]?(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # (09912)_3_45_67
        r"\(0(\d{2})(\d{1})(\d{1})\)[\s-]?(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
    ]

    SPECIAL_PHONE_PATTERNS = [
        # AAA_XXX_XXX
        # +380_(800)_123_456
        r"\+380[\s-]?(800|900)[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})",
        # 0_800_123_456
        r"0[\s-]?(800|900)[\s-]?(\d{1})(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})(\d{1})",

        # AAX_XX_XX_XX
        # +380_(800)_12_34_56
        r"\+?380[\s-]?\(?(800|900)\)?[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # +38_(0800)_12_34_56
        r"\+?38[\s-]?\(?0(800|900)\)?[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
        # 0_800_12_34_56
        r"0[\s-]?(800|900)[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})[\s-]?(\d{1})(\d{1})",
    ]

    @staticmethod
    def name() -> str:
        return "UkrainianPhoneNormalizer"

    @staticmethod
    def normalize(text: str) -> Tuple[str, List[str], List[str]]:
        warnings = []
        errors = []

        output = UkrainianPhoneNormalizer.normalize_special_phone_numbers(text)

        output = UkrainianPhoneNormalizer.normalize_regular_phone_numbers(output)

        return output, warnings, errors

    @staticmethod
    def normalize_special_phone_numbers(text: str) -> str:
        """
        Normalizes phone numbers with a three-part code.
        """
        output = text
        for pattern in UkrainianPhoneNormalizer.SPECIAL_PHONE_PATTERNS:
            def replace(match):
                if UkrainianPhoneNormalizer.should_not_match(output, match):
                    return match.group(0)

                return UkrainianPhoneNormalizer.format_special_phone_number(match)

            output = re.sub(pattern, replace, output)

        return output

    @staticmethod
    def normalize_regular_phone_numbers(text: str) -> str:
        """
        Normalizes phone numbers with a two-part code.
        """
        output = text
        for pattern in UkrainianPhoneNormalizer.REGULAR_PHONE_PATTERNS:
            def replace(match):
                if UkrainianPhoneNormalizer.should_not_match(output, match):
                    return match.group(0)

                return UkrainianPhoneNormalizer.format_regular_phone_number(match)

            output = re.sub(pattern, replace, output)

        return output

    @staticmethod
    def format_regular_phone_number(match) -> str:
        """
        Formats a phone number with a two-part code into a standard format.
        """
        code, d1, d2, d3, d4, d5, d6, d7 = match.groups()

        return f"+380 ({code}) {d1}{d2}{d3}-{d4}{d5}-{d6}{d7}"

    @staticmethod
    def format_special_phone_number(match) -> str:
        """
        Formats a phone number with a three-part code into a standard format.
        """
        code, d1, d2, d3, d4, d5, d6 = match.groups()

        return f"+380 ({code}) {d1}{d2}-{d3}{d4}-{d5}{d6}"

    @staticmethod
    def should_not_match(text: str, match) -> bool:
        """
        Checks if the matched phone number should not be normalized.
        """

        previous_two_symbols = text[max(0, match.start() - 2):match.start()]
        if re.match(r"\d[ -]|\d|-", previous_two_symbols):
            return True

        next_two_symbols = text[match.end():min(len(text), match.end() + 2)]
        if re.match(r"[ -]\d|\d|-", next_two_symbols):
            return True

        code = match.group(1)

        is_ukraine_operator_code = re.fullmatch(UkrainianPhoneNormalizer.UKRAINE_OPERATOR_CODES, code)
        is_ukraine_special_code = re.fullmatch(UkrainianPhoneNormalizer.UKRAINE_SPECIAL_CODES, code)

        if is_ukraine_operator_code or is_ukraine_special_code:
            return False

        return True


if __name__ == "__main__":
    three_part_code = [
        "0991234567",
        "099 123 45 67",
        "099 123-45-67",
        "099 1234 567",
        "099 12 34 567",

        "0 99 123 45 67",
        "0-99-123-45-67",
        "099-12-345-67",
        "0-99-12-345-67",
        "+380 (99) 12-345-67",

        "+380991234567",
        "+380 99 123 45 67",
        "+380 99 123-45-67",
        "+380 (99) 123 45 67",
        "+380 (99) 123-45-67",

        "380991234567",
        "380 99 123 45 67",
        "380 99 123-45-67",
        "380 (99) 123 45 67",
        "380 (99) 123-45-67",

        "+38 099 123 45 67",
        "+38 099 123-45-67",
        "+38 (099) 123 45 67",
        "+38 (099) 123-45-67",

        "38 099 123 45 67",
        "38 099 123-45-67",
        "38 (099) 123 45 67",
        "38 (099) 123-45-67",

        "+380 99 123 4567",
        "+380 99 123-4567",
        "+380 99 1234-567",

        "099 1234-567",
        "+38 099 1234-567",
        "+380 99 1234-567",
        "+38 099 1234-567",
        "+38 099 1234 567",
        "+380 (99) 1234-567",
        "+380 (99) 1234567",
        "+380 (99) 1234 567",
        "+380 99 1234 567",

        "099 1234-567",
        "+38 099 12-34-567",
        "+380 99 12-34-567",
        "+38 099 12 34 567",
        "+380 (99) 12 34 567",
        "+380 (99) 12 34 567",

        "(099) 123-45-67",
        "(099) 12-34-567",
        "(099) 12 34 567",
        "(0991)23-45-67",

        "0 (99) 123 45 67",
        "0 (99) 12 34 567",
        "+38 (0991) 23-45-67",
        "+38(0991) 234567",
        "(09912) 3-45-67",
    ]

    two_part_code = [
        "0800123456",
        "0 800 12 34 56",
        "0 800 12 3456",
        "0-800-12-34-56",
        "+380 800 12 34 56",
        "+380 800 12-34-56",
        "0 800 123 456",
        "0-800-123-456",
        "+380 800 123 456",
        "+380 800 123-456",
    ]

    test_cases = [
        ("+380 (99) 123-45-67", three_part_code),
        ("+380 (800) 12-34-56", two_part_code),
    ]

    for expected_output, test_cases in test_cases:
        for input_text in test_cases:
            result, _, _ = UkrainianPhoneNormalizer.normalize(input_text)
            assert result == expected_output, f'\nInput: "{input_text}",\nexpected: "{expected_output}",\nresult: "{result}"'

    should_not_match = [
        "100 500 100",
        "1 500",
        "0 800 33 92 91 56 12",
        "45 67 0 800 33 92 91",
        "0 800 33 92 9156 12",
        "45 670 800 33 92 91",
        "45 67 0 800 33 92 91",
        "0 99 233 32 95-",
        "011 123 45 67"
    ]

    for string in should_not_match:
        result, _, _ = UkrainianPhoneNormalizer.normalize(string)
        assert result == string, f"Should not match: {string}, result: {result}"

    print("\nPassed!\n")

#%%
