"""Simple substitution cipher stuff."""


alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def sorted_frequency_count(cipher):
    """Return a sorted list of letter counts.

    Args:
        cipher (str): ciphertext string

    Returns:
        list[(str, int)]: list of (character, count)
    """
    freqs = frequency_count(cipher)
    l = freqs.keys()
    l.sort(key=lambda c: -freqs[c])
    return [(char, freqs[char]) for char in l]


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


def key_caesar(shift, letters=alphabet):
    """Generate a key for a Caesar cipher.

    Args:
        shift (int): the amount to shift by. Negative is OK.
        letters (iterable[str]): list of letters to use. default: the alphabet.

    Returns:
        dic[str, str]: the key
    """
    key = {}
    for i, l in enumerate(letters):
        key[l] = letters[(i + shift) % len(letters)]
    return key


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
    for i in range(len(cipher) - len(word) + 1):
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
        if cipher_char in key and key[cipher_char] != plain_char:
            # we fail because this cipher character is already required
            # to be another plain character
            return {}
        elif cipher_char not in key and plain_char in key.values():
            # we fail because this plain character is already required to
            # be represented by another cipher character
            return {}
        else:
            key[cipher_char] = plain_char
    return key

if __name__ == '__main__':
    # let's work through a cipher as an example.
    # The original ciphertext:
    text_full = 'VJ AM LAP AS PCX IS WSAQMM OV JAS PHI V LIV JAM GVAQV JUD JT' \
                ' AV JAH SPUD JT VIV LAV JET JMF'
    # The solitary V must be either A or I (or possibly O) in standard English.
    # However, VIV rules out those possibilities. Therefore, the spaces are
    # probably a red herring. Let's remove them.
    text = text_full.replace(' ', '')
    print sorted_frequency_count(text)
    # We can guess a couple of words, but they don't really help
    print
    print '\n'.join(x[0] for x in guess_word(text, 'THE'))
    print
    # What if we treat the vowels as spaces?
    text_spaced = text.replace('A', ' ').replace('I', ' ').replace('E', ' ')
    text_spaced = text_spaced.replace('O', ' ').replace('U', ' ')
    print text_spaced
    # Similarly, let's guess the words now have the vowels stripped.
    # Turns out the first one is pretty good
    print guess_word(text_spaced, 'TH')[0]
    # Maybe we have a Ceasar cipher?
    print substitute(text_spaced, key_caesar(-2))
    # What if it's only a Caesar on the consonants?
    consonants = alphabet.replace('A', '').replace('E', '').replace('I', '')
    consonants = consonants.replace('O', '').replace('U', '')
    print substitute(text_spaced, key_caesar(-1, consonants))
    # Bingo!
    print "THE LAKE IN RAINBOW RIVER PULL THE RING TAKE THE LEFT PATH CHOOSE " \
          "THE GREEN CHEST TAKE THE SHIELD"

