"""Simple substitution cipher stuff."""


def frequency_count(cipher):
    """Get a basic frequency count.

    Args:
        cipher (str): ciphertext string

    Returns:
        dict[str, int]: character -> count
    """
    freqs = {}
    for char in cipher:
        freqs[char] = freqs.get(char, 0) + 1
    return freqs


def substitute(cipher, key, filler='_'):
    """Use the given mapping to substitute characters in the ciphertext.

    Args:
        cipher (str): ciphertext string
        key (dict[str, str]): map of cipher character to plain character
        filler (str): filler character to use for chars not defined in mapping
            use filler=None to keep original ciphertext

    Returns:
        str: substituted string
    """
    plaintext = ''
    for char in cipher:
        if char == ' ':
            plaintext += ' '
        else:
            if char in key:
                plaintext += key[char]
            elif filler is None:
                plaintext += char
            else:
                plaintext += filler
    return plaintext


def guess_word(cipher, word):
    """Guess a word in the plaintext, and see if and where it could be.

    Returns a list of possibilities, in order of the location of the word.
    For example, if the word fits starting at position 0, or at position 10,
    the first item in the list will correspond to the word substituted at 0,
    and the second at 10.

    Args:
        cipher (str): ciphertext string
        word (str): word to guess. Longer is better.

    Returns:
        list[(str, dict[str, str])]: list of possibilities. First item is the
            guessed plaintext, with the substitutions defined by the word.
            Second is the substitution key.
    """
    poss = []
    for i in range(len(cipher)):
        key = place_word(cipher, word, i)
        if not key:
            continue
        poss.append((substitute(cipher, key), key))
    return poss


def place_word(cipher, word, i):
    """Attempt to place the given word at the given position in the cipher.

    Args:
        cipher (str): ciphertext string
        word (str): word to guess
        i (int): position

    Returns:
        dict[str, str]: substitution key resulting from this word placement,
            or empty dict {} if it cannot be placed here.
    """
    key = {}
    for j in range(len(word)):
        plain_char = word[j]
        cipher_char = cipher[i+j]
        if cipher_char in key:
            if key[cipher_char] != plain_char:
                # we fail because this cipher character is already required
                # to be another plain character
                return {}
            elif plain_char in key.values():
                # we fail because this plain character is already required to
                #  be represented by another cipher character
                return {}
        else:
            key[cipher_char] = plain_char
    return key

if __name__ == '__main__':
    pass
