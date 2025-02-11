from difflib import SequenceMatcher


def comparar(a, b):
    res = SequenceMatcher(None, a, b).ratio()
    # print(res)
    if res >= 0.5:

        return True
    else:
        return False

# print(b and a)
