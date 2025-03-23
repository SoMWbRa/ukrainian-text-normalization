

def format_phone_number(text: str) -> str:
    """
    Нормалізує формат номера телефону у стандартний формат +380XXXXXXXXX
    Працює з номерами телефонів, що починаються з коду +380 або 0
    :param text:
    :return:
    """
    output = ""
    digits_seen = 0
    expect_digit = None  # Очікувана наступна цифра в послідовності +380 або 380

    for char in text:
        if char.isdigit():
            digits_seen += 1

            # Якщо це перша цифра і вона 3 або 0
            if digits_seen == 1:
                if char == '3':
                    output += char
                    expect_digit = '8'  # Далі очікуємо 8
                elif char == '0':
                    output += char
                    expect_digit = None  # Більше не очікуємо особливих цифр
                else:
                    output += 'X'
            # Якщо це друга цифра і ми очікуємо 8
            elif expect_digit == '8' and char == '8':
                output += char
                expect_digit = '0'  # Після 38 очікуємо 0
            # Якщо це третя цифра і ми очікуємо 0
            elif expect_digit == '0' and char == '0':
                output += char
                expect_digit = None  # Більше не очікуємо особливих цифр
            else:
                output += 'X'
        else:
            # Не цифра, просто додаємо символ
            output += char
            # Якщо це +, скидаємо лічильник цифр
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

