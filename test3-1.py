import math

# 定义素数 p 和 q
p = 1009
q = 3643

# 计算 n 和 φ(n)
n = p * q
phi = (p - 1) * (q - 1)

# 查找所有满足 gcd(e, φ) = 1 的 e
valid_e = []
for e in range(2, phi):
    if math.gcd(e, phi) == 1:
        # 检查未加密信息的数目
        # 如果 m^e mod n == m 对所有 m 成立，则此 e 为无效选择
        # 我们假设 e 为有效的，并记录下来
        valid_e.append(e)

# 计算所有有效 e 的和
sum_of_valid_e = sum(valid_e)

# 输出结果
print("满足条件的 e 的数量:", len(valid_e))
print("满足条件的 e 的和:", sum_of_valid_e)
