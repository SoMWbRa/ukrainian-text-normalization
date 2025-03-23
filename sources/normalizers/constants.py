import re


class Constants:
    """Class with constants for normalizers."""

    QUOTATION_MARKS = [
        '\u0022',  # QUOTATION MARK - "
        '\u00AB',  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK - «
        '\u00BB',  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK - »
        "\u201C",  # LEFT DOUBLE QUOTATION MARK - “
        "\u201D",  # RIGHT DOUBLE QUOTATION MARK - ”
        "\u201F",  # DOUBLE HIGH-REVERSED-9 QUOTATION MARK - ‟
        "\u201E",  # DOUBLE LOW-9 QUOTATION MARK - „
        "\u275D",   # HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT - ❝
        "\u275E",   # HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT - ❞
    ]

    HYPHENS = [
        "\u002D",  # HYPHEN-MINUS - -
        "\u2010",  # HYPHEN - ‐
        "\u2011",  # NON-BREAKING HYPHEN - ‑
        "\u2012",  # FIGURE DASH - ‒
        "\u2013",  # EN DASH - –
        "\u2014",  # EM DASH - —
        "\u2015",  # HORIZONTAL BAR - ―
        "\u2212",  # MINUS SIGN - −
    ]

    APOSTROPHES = [
        "\u0027",  # APOSTROPHE - '
        "\u02B9",  # MODIFIER LETTER PRIME - ʹ
        "\u02BB",  # MODIFIER LETTER TURNED COMMA - ʻ
        "\u02BC",  # MODIFIER LETTER APOSTROPHE - ʼ
        "\u2018",  # LEFT SINGLE QUOTATION MARK - ‘
        "\u2019",  # RIGHT SINGLE QUOTATION MARK - ’
        "\u0060",  # GRAVE ACCENT - `
    ]

    DEFAULT_APOSTROPHE = "\u02BC"  # MODIFIER LETTER APOSTROPHE - ʼ

    # Denote as delimiter for context-based quotation marks replacement
    DEFAULT_QUOTE = '\u0022'  # QUOTATION MARK - "

    QUOTE_OUTER_OPEN = '\u00AB'  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK - «
    QUOTE_OUTER_CLOSE = '\u00BB'  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK - »
    QUOTE_INNER_OPEN = '\u201C'  # LEFT DOUBLE QUOTATION MARK - “
    QUOTE_INNER_CLOSE = '\u201D'  # RIGHT DOUBLE QUOTATION MARK - ”

    PUNCTUATION = re.split(r'\s+', r"… …… , . : ; ! ? ¿ ؟ ¡ ( ) [ ] { } < > _ # * & 。 ？ ！ ， 、 ； ： ～ · । ، ۔ ؛ ٪")

    SPACE = "\u0020"
