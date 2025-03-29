from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))  # whyy


def encrypt_cfb(plaintext: bytes, key: bytes) -> bytes:
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = b""
    previous = iv
    block_size = 16

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i: i + block_size]
        encrypted = cipher.encrypt(previous)

        cipher_block = xor_bytes(encrypted[:len(block)], block)
        ciphertext += cipher_block
        previous = cipher_block
        return iv + ciphertext


def main():
    # Тест с ФИО
    message_name = "Aleksei Dmitriev dmitriev.av@edu.spbstu.ru"
    print("Initial message:", message_name)

    plaintext = message_name.encode('utf-8')

    # 192 битный ключ
    key = b'0123456789ABCDEF01234567'
    # проверка ключа
    assert len(key) == 24, "Ключ должен быть 192 бита"

    encrypted_data = encrypt_cfb(plaintext, key)


if __name__ == '__main__':
    main()
