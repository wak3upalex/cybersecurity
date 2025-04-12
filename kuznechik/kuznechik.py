# 5. Полином - | **0x171** | x⁸ + x⁶ + x⁵ + x⁴ + 1|, размер блока 8 байт
import random


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


def L_inv(state):
    for _ in range(8):
        state = R_inv(state)
    return state


# Generating keys
def generate_s_boxes(key):
    seed_val = sum(key)  # sum all bytes of our key for getting determined value of our key
    random.seed(seed_val)  # setting initial state for generating numbers
    # generating S box/block π0
    s_box = list(range(256))
    random.shuffle(s_box)
    # making invet s box π1
    inv_s_box = [0] * 256
    # for i position val value we are turning on val position i value
    for i, val in enumerate(s_box):
        inv_s_box[val] = i
    return s_box, inv_s_box


def sub_bytes(data, s_box):
    """
    Функция подстановки байтов (S-блок)

    Args:
        data: каждый байт из входного списка `data` на соответствующее значение из S-блока `s_box`.
        s_box: S-блок

    Returns:
        Каждое значение из входного списка обрабатывается по таблице, формируя новый список заменённых байтов.

    """
    return [s_box[x] for x in data]


def key_schedule(main_key, s_box):
    """
    генерация ключей
    Args:
        main_key:
        s_box:

    Returns:

    """
    # main key of 16 bytes will be divided on 8 and 8 bytes
    K1 = main_key[:8]
    K2 = main_key[8:]

    round_keys = []
    for i in range(1, 11):
        # создаем значение на раунд. Первый байт по номеру раунда, второй просто нули
        RC = [i] + [0] * 7
        temp = xor_bytes(K1, RC)
        temp = sub_bytes(temp, s_box)
        temp = L(temp)
        # формируем новый ключ
        new_key = xor_bytes(temp, K2)
        round_keys.append(new_key)
        # после каждого раунда значение K1 присваивается новому ключу, а K2 получает предыдущий K1
        K1, K2 = new_key, K1
    return round_keys


def encrypt_block(block, round_keys, s_box):
    """
    Шифрование блока текста
    Args:
        block:
        round_keys:
        s_box:

    Returns:

    """
    state = block[:]  # копия блока
    for i in range(9):
        # с раундовым ключом
        state = xor_bytes(state, round_keys[i])

        state = sub_bytes(state, s_box)
        state = L(state)
    state = xor_bytes(state, round_keys[9])
    return state


def decrypt_block(block, round_keys, inv_s_box):
    """
    Дешифрование блока
    Args:
        block:
        round_keys:
        inv_s_box:

    Returns:

    """
    state = block[:]  # копия блока
    state = xor_bytes(state, round_keys[9])
    for i in reversed(range(9)):
        state = L_inv(state)
        state = sub_bytes(state, inv_s_box)
        state = xor_bytes(state, round_keys[i])
    return state


def pad(data, block_size=8):
    """
    Функция дополнения данных
    Args:
        data:
        block_size:

    Returns:

    """
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)  # дополняем данные нужным количеством


def unpad(data):
    """
    Удаление доп байтов после дешифрования
    Args:
        data:

    Returns:

    """
    pad_len = data[
        -1]  # Последний байт данных указывает, сколько байтов было добавлено при padding
    return data[:-pad_len]
