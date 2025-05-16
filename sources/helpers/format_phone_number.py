

def format_phone_number(text: str) -> str:
    """
    Normalizes the phone number to the standard format +380XXXXXXXXX.
    Works with phone numbers starting with the code +380 or 0.
    :param text: Input text containing a phone number
    :return: Normalized phone number with digits replaced by 'X'
    """
    output = ""
    digits_seen = 0
    expect_digit = None  # Expected next digit in the +380 or 380 sequence

    for char in text:
        if char.isdigit():
            digits_seen += 1

            # If this is the first digit, and it is 3 or 0
            if digits_seen == 1:
                if char == '3':
                    output += char
                    expect_digit = '8'  # Next we expect 8
                elif char == '0':
                    output += char
                    expect_digit = None  # No specific digit expected next
                else:
                    output += 'X'
            # If this is the second digit and we expect 8
            elif expect_digit == '8' and char == '8':
                output += char
                expect_digit = '0'  # After 38, expect 0
            # If this is the third digit and we expect 0
            elif expect_digit == '0' and char == '0':
                output += char
                expect_digit = None  # No specific digit expected next
            else:
                output += 'X'
        else:
            # Not a digit, just add the character
            output += char
            # If it's a '+', reset the digit counter
            if char == '+':
                digits_seen = 0

    return output


if __name__ == "__main__":
    tests = [
        ("+380991234567", "+380XXXXXXXXX"),
        ("380991234567", "380XXXXXXXXX"),
        ("0991234567", "0XXXXXXXXX"),
        ("+380 99 123 45 67", "+380 XX XXX XX XX"),
        ("+380 (99) 123 45 67", "+380 (XX) XXX XX XX"),
        ("+38 099 123 45 67", "+38 0XX XXX XX XX"),
        ("+38 099 123 4567", "+38 0XX XXX XXXX"),

        ("+380 99 123-45-67", "+380 XX XXX-XX-XX"),
        ("+380 (99) 123-45-67", "+380 (XX) XXX-XX-XX"),

    ]

    for test, expected in tests:
        result = format_phone_number(test)
        assert result == expected, f"For {test} expected {expected} but got {result}"

    print("All tests passed!")

