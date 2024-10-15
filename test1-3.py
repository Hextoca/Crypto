# （1）
import base64

s = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

b64 = base64.b64encode(bytes.fromhex(s)).decode()

print(b64)

# （2）
def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    return bytes([_a ^ _b for _a, _b in zip(b1, b2)])


if __name__ == '__main__':
    src = bytes.fromhex('1c0111001f010100061a024b53535009181c')
    mask = bytes.fromhex('686974207468652062756c6c277320657965')
    result = xor_bytes(src, mask)
    result_hex = result.hex()
    print(result_hex)

# （3）
import math

FREQ = {'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
        'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
        'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
        'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}


def xor_bytes_const(b: bytes, const: int) -> bytes:
    return bytes([const ^ _b for _b in b])


def bhattacharyya_distance(dist1: dict, dist2: dict) -> float:
    bc_coeff = 0
    for letter in FREQ.keys():
        bc_coeff += math.sqrt(dist1[letter] * dist2[letter])

    return -math.log(bc_coeff)


def score_string(word: bytes) -> float:
    curr_freq = {letter: 0 for letter in FREQ.keys()}

    # calc letter dist for current word
    num_letters = 0
    for i in word:
        if chr(i).lower() in FREQ.keys():
            curr_freq[chr(i).lower()] += 1
            num_letters += 1

    if num_letters != 0:
        curr_freq = {letter: val / num_letters for letter, val in curr_freq.items()}
    else:
        return 0

    # evaluate dist using the Bhattacharyya distance
    distance = bhattacharyya_distance(FREQ, curr_freq)
    return 1 / distance


if __name__ == '__main__':
    src = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

    max_score = 0
    best_res = b''
    for i in range(2 ** 8):
        tmp = xor_bytes_const(src, i)
        score = score_string(tmp)

        if score > max_score:
            max_score = score
            best_res = tmp

    print(best_res)
    print(f'{max_score=}')

# （4）
import math

FREQ = {'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
        'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
        'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
        'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}


def xor_bytes_const(b: bytes, const: int) -> bytes:
    return bytes([const ^ _b for _b in b])


def bhattacharyya_distance(dist1: dict, dist2: dict) -> float:
    bc_coeff = 0
    for letter in FREQ.keys():
        bc_coeff += math.sqrt(dist1[letter] * dist2[letter])

    return -math.log(bc_coeff)


def score_string(word: bytes) -> float:
    curr_freq = {letter: 0 for letter in FREQ.keys()}

    # calc letter dist for current word
    num_letters = 0
    for i in word:
        if chr(i).lower() in FREQ.keys():
            curr_freq[chr(i).lower()] += 1
            num_letters += 1

    if num_letters != 0:
        curr_freq = {letter: val / num_letters for letter, val in curr_freq.items()}
    else:
        return 0

    # evaluate dist using the Bhattacharyya distance
    distance = bhattacharyya_distance(FREQ, curr_freq)
    return 1 / distance


def decode_single_byte_xor_cypher(word: str) -> (bytes, int):
    src = bytes.fromhex(word)

    max_score = 0
    best_res = b''
    for i in range(2 ** 8):
        tmp = xor_bytes_const(src, i)
        score = score_string(tmp)

        if score > max_score:
            max_score = score
            best_res = tmp

    return best_res, max_score


if __name__ == '__main__':
    # read given file
    with open('1.txt', 'r') as fh:
        Lines = fh.readlines()

    # evaluate each line and find best word
    max_score = 0
    best_word = b''
    for line in Lines:
        tmp_word, tmp_score = decode_single_byte_xor_cypher(line)

        if tmp_score > max_score:
            max_score = tmp_score
            best_word = tmp_word

    print(best_word)
    print(f'{max_score=}')

    # (5)
def Repeating_key_XOR(_message,_key) :
    cipher = b''
    length = len(_key)
    for i in range(0,len(_message)) :
        cipher = cipher + bytes([_message[i]^_key[i % length]])
        # print(cipher.hex())
    return cipher

if __name__ == '__main__' :
    message = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = b"ICE"
    ciphertext = Repeating_key_XOR(message,key)
    print(ciphertext.hex())

    # （6）
