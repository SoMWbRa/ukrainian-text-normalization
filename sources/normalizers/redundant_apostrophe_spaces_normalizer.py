from typing import Tuple, List
import re

from sources.normalizers.abstract_normalizer import AbstractNormalizer
from sources.normalizers.constants import Constants


class RedundantApostropheSpacesNormalizer(AbstractNormalizer):
    """
    During experimentation, we identified errors related to apostrophes surrounded by spaces,
    such as «сім ʼ я» (family). To address this issue, we introduced a preprocessing step to remove redundant
    spacing before apostrophes when the next letter after the spacing is one of the iotated vowels «я», «ю», «є», or «ї».
    """

    @staticmethod
    def name() -> str:
        return "RedundantApostropheSpacesNormalizer"

    @staticmethod
    def normalize(text: str) -> Tuple[str, List[str], List[str]]:
        for apostrophe in Constants.APOSTROPHES:
            text = re.sub(rf" {apostrophe} (?=[яюєї])", f"{apostrophe}", text)

        return text, [], []


if __name__ == "__main__":
    tests = [
        ("Сім ` я", "Сім`я"),
        ("Сім` я", "Сім` я"),  # no change
        ("Сім `я", "Сім `я"),  # no change
    ]

    for input, expected_result in tests:
        output, _, _ = RedundantApostropheSpacesNormalizer.normalize(input)
        assert output == expected_result, f"Input: {input}, expected: {expected_result}, result: {output}."

    print("All tests passed!")
# %%
