import random
import math


# 素性测试函数
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# 随机生成一个范围内的素数
def generate_random_prime(lower, upper):
    while True:
        num = random.randint(lower, upper)
        if is_prime(num):
            return num


# 扩展欧几里得算法来求模逆
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


def invmod(e, et):
    g, x, _ = egcd(e, et)
    if g != 1:
        raise Exception('模逆不存在')
    return x % et


# RSA 关键生成
def generate_rsa_keys():
    # 使用自定义函数生成两个随机素数 p 和 q
    p = generate_random_prime(100, 1000)
    q = generate_random_prime(100, 1000)
    n = p * q
    et = (p - 1) * (q - 1)

    # 选择一个合适的 e，使得 gcd(e, et) == 1
    e = 3
    while math.gcd(e, et) != 1:
        e += 2  # 如果 gcd(e, et) != 1，尝试下一个奇数

    # 计算 d 的模逆
    d = invmod(e, et)  # 私钥指数

    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


# 加密函数
def rsa_encrypt(m, public_key):
    e, n = public_key
    c = pow(m, e, n)
    return c


# 解密函数
def rsa_decrypt(c, private_key):
    d, n = private_key
    m = pow(c, d, n)
    return m


# 测试数字加密和解密
public_key, private_key = generate_rsa_keys()
m = 42
print("原始信息:", m)

# 加密
c = rsa_encrypt(m, public_key)
print("加密信息:", c)

# 解密
decrypted_m = rsa_decrypt(c, private_key)
print("解密信息:", decrypted_m)
