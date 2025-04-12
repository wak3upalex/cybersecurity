# 5. Полином - | **0x171** | x⁸ + x⁶ + x⁵ + x⁴ + 1|, размер блока 8 байт

# (gf_mul) Функция умножения в поле Галуа GF(2⁸) с редукцией по полиному (0x171)
def gf_mul(a, b, poly=0x171):
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:  # если a >= 256, производится редукция по модулю poly
            a ^= poly
        b >>= 1
    return result & 0xFF

# (xor_bytes) Функция поразрядного XOR для байтовых последовательностей:
def xor_bytes(a, b):
    return [x ^ y for x, y in zip(a, b)]