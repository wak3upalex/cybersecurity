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


def decrypt_cfb(ciphertext: bytes, key: bytes) -> bytes:
    iv = ciphertext[:16]
    ciphertext_body = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = b""
    previous = iv
    block_size = 16
    for i in range(0, len(ciphertext_body), block_size):
        block = ciphertext_body[i: i + block_size]
        # Шифруем предыдущий блок
        encrypted = cipher.encrypt(previous)
        # Восстанавливаем блок открытого текста с помощью XOR
        plain_block = xor_bytes(encrypted[:len(block)], block)
        plaintext += plain_block
        # Обновляем previous для следующего шага
        previous = block
    return plaintext


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
    print("Зашифрованные данные (в hex):", encrypted_data.hex())


if __name__ == '__main__':
    main()
