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


coefficients = [1, 2, 3, 4, 5, 6, 7, 8]


def R(state):
    """
    Функция R

    Каждый байт списка умножается на один из коэффициентов `coefficients`. Затем результаты суммируются по XOR, где к `new_val` прибавляется через XOR значение результата умножения Галуа
    Args:
        state: список из 8 байтов

    Returns:
        циклический сдвиг влево. Через срез байтов `state` берет срез с первого элемента до конца, а [new_val] добавляется в конец.


    """
    new_val = 0
    for i in range(8):
        new_val ^= gf_mul(state[i], coefficients[i])
    return state[1:] + [new_val]


def L(state):
    for _ in range(8):
        state = R(state)
    return state


def R_inv(state):
    x0 = state[7]  # last byte of state
    # for each state multiplying on coef and XOR with
    for i in range(7):
        x0 ^= gf_mul(state[i], coefficients[i + 1])
    return [x0] + state[
                  :7]  # new list with beginning of x0 and leftover is initial state of 7 elements
