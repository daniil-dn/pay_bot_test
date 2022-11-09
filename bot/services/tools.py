from cleantext import clean as clean_text


def check_userID(input: str) -> int | bool:
    if input.isdigit():
        return int(input)
    else:
        return False


def check_username(input: str) -> str | bool:
    input = input.split(' ')[0]
    if 5 <= len(input) <= 32:
        return input
    else:
        return False



