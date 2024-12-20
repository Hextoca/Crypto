import math
import base64
import statistics
from itertools import combinations

# Globals
COUNTS = [bin(x).count("1") for x in range(256)]
FREQ = {'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
        'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
        'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
        'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}


def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    return bytes([_a ^ _b for _a, _b in zip(b1, b2)])


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


def repeating_key_xor(stream: bytes, key: bytes) -> bytes:
    return bytes([letter ^ key[idx % len(key)] for idx, letter in enumerate(stream)])


def hamming_dist(b1: bytes, b2: bytes) -> int:
    """ Number of different bits """
    diff = xor_bytes(b1, b2)
    count = sum(map(lambda x: COUNTS[x], diff))
    return count


def eval_key_size(stream: bytes, max_key_size: int) -> int:
    # default values
    min_dist = max_key_size * 8
    best_key_size = 2

    # find best key size
    for key_size in range(2, max_key_size):
        # calc dist between close chunks
        idx_list = combinations(range(5), 2)
        dist_list = []
        for idx in idx_list:
            block1 = stream[idx[0] * key_size:(idx[0]+1) * key_size]
            block2 = stream[idx[1] * key_size:(idx[1]+1) * key_size]
            dist_list.append(hamming_dist(block1, block2))

        # calc and update best result
        total_dist = statistics.mean(dist_list) / key_size
        if total_dist < min_dist:
            min_dist = total_dist
            best_key_size = key_size

    return best_key_size


def transpose_blocks(stream: bytes, key_size: int) -> list[bytes]:
    block_list = [stream[shift::key_size] for shift in range(key_size)]
    return block_list


def decode_single_byte_xor_cypher(src: bytes) -> int:
    max_score = 0
    best_key = 0
    for i in range(2 ** 8):
        tmp = xor_bytes_const(src, i)
        score = score_string(tmp)

        if score > max_score:
            max_score = score
            best_key = i

    return best_key


def main():
    # key size range
    KEYSIZE = 40

    # load cipher and decode base64 to bytes
    with open('6.txt', 'r') as fh:
        cipher = base64.b64decode(fh.read())

    # estimate key size
    key_size = eval_key_size(cipher, KEYSIZE)

    # divide and transpose blocks
    block_list = transpose_blocks(cipher, key_size)

    # reconstruct key
    key = []
    for block in block_list:
        key.append(decode_single_byte_xor_cypher(block))

    key = bytes(key)
    print(f'{key=}')  # b'Terminator X: Bring the noise'

    # decode the stream
    word = repeating_key_xor(cipher, key)
    print(f'{word=}')
    #  b"I'm back and I'm ringin' the bell \nA rockin' on the mike while the fly girls yell \nIn ecstasy in the back of me \nWell that's my DJ Deshay cuttin' all them Z's \nHittin' hard and the girlies goin' crazy \nVanilla's on the mike, man I'm not lazy. \n\nI'm lettin' my drug kick in \nIt controls my mouth and I begin \nTo just let it flow, let my concepts go \nMy posse's to the side yellin', Go Vanilla Go! \n\nSmooth 'cause that's the way I will be \nAnd if you don't give a damn, then \nWhy you starin' at me \nSo get off 'cause I control the stage \nThere's no dissin' allowed \nI'm in my own phase \nThe girlies sa y they love me and that is ok \nAnd I can dance better than any kid n' play \n\nStage 2 -- Yea the one ya' wanna listen to \nIt's off my head so let the beat play through \nSo I can funk it up and make it sound good \n1-2-3 Yo -- Knock on some wood \nFor good luck, I like my rhymes atrocious \nSupercalafragilisticexpialidocious \nI'm an effect and that you can bet \nI can take a fly girl and make her wet. \n\nI'm like Samson -- Samson to Delilah \nThere's no denyin', You can try to hang \nBut you'll keep tryin' to get my style \nOver and over, practice makes perfect \nBut not if you're a loafer. \n\nYou'll get nowhere, no place, no time, no girls \nSoon -- Oh my God, homebody, you probably eat \nSpaghetti with a spoon! Come on and say it! \n\nVIP. Vanilla Ice yep, yep, I'm comin' hard like a rhino \nIntoxicating so you stagger like a wino \nSo punks stop trying and girl stop cryin' \nVanilla Ice is sellin' and you people are buyin' \n'Cause why the freaks are jockin' like Crazy Glue \nMovin' and groovin' trying to sing along \nAll through the ghetto groovin' this here song \nNow you're amazed by the VIP posse. \n\nSteppin' so hard like a German Nazi \nStartled by the bases hittin' ground \nThere's no trippin' on mine, I'm just gettin' down \nSparkamatic, I'm hangin' tight like a fanatic \nYou trapped me once and I thought that \nYou might have it \nSo step down and lend me your ear \n'89 in my time! You, '90 is my year. \n\nYou're weakenin' fast, YO! and I can tell it \nYour body's gettin' hot, so, so I can smell it \nSo don't be mad and don't be sad \n'Cause the lyrics belong to ICE, You can call me Dad \nYou're pitchin' a fit, so step back and endure \nLet the witch doctor, Ice, do the dance to cure \nSo come up close and don't be square \nYou wanna battle me -- Anytime, anywhere \n\nYou thought that I was weak, Boy, you're dead wrong \nSo come on, everybody and sing this song \n\nSay -- Play that funky music Say, go white boy, go white boy go \nplay that funky music Go white boy, go white boy, go \nLay down and boogie and play that funky music till you die. \n\nPlay that funky music Come on, Come on, let me hear \nPlay that funky music white boy you say it, say it \nPlay that funky music A little louder now \nPlay that funky music, white boy Come on, Come on, Come on \nPlay that funky music \n"


if __name__ == '__main__':
    main()