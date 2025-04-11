from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def encrypt_cfb(plaintext: bytes, key: bytes) -> bytes:
    """
    Encryption in AES-CFB mode.

    1. Generating iv (16 bytes)
    2. Dividing initial text on blocks with 16 bytes
    3. For the first block
        - Encrypting `iv` via AES-ecb
        - Encrypting first block of text
        - Encrypted text block XOR with encrypted `iv`
    4. For following blocks:
        - Previous encrypted block of text will be used as `iv` in previous step
        - Encrypting new text block of text via AES in ECB mode
        - Encrypted text block XOR with encrypted previous block of text
    5. Returning initial iv with encrypted text.

    Args:
        plaintext (bytes): Data to be encrypted.
        key (bytes): key to be used for encryption.

    Returns:
        iv + ciphertext (bytes): IV and encrypted ciphertext.
    """
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
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
    """
        Decryption in AES-CFB mode.

        1. Extracting iv (16 bytes)
        2. Dividing initial text on blocks with 16 bytes in a loop
        3. To decrypt data into initial text:
            - encrypt `iv` via AES-ECB
            - encrypted `iv` XOR with encrypted earlier block of text
            - for next blocks we encrypt previous block of text to XOR it with encrypted block of text
        4. Returning final decrypted text.

        Args:
            ciphertext (bytes): Data to be decrypted.
            key (bytes): key to be used for decryption.

        Returns:
            iv + ciphertext (bytes): IV and encrypted ciphertext.
        """
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
        # Восстанавливаем блок открытого текста с помощью XOR и зашифрованного блока
        plain_block = xor_bytes(encrypted[:len(block)], block)
        plaintext += plain_block
        # Обновляем previous для следующего шага
        previous = block
    return plaintext


def write_to_file(filename: str, data: bytes):
    with open(filename, 'wb') as f:
        f.write(data)


def read_from_file(filename: str) -> bytes:
    with open(filename, 'rb') as f:
        return f.read()


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
    write_to_file("encrypted_message.bin", encrypted_data)
    write_to_file("original_message.txt", plaintext)

    # Чтение зашифрованного сообщения из файла и дешифрование
    encrypted_from_file = read_from_file("encrypted_message.bin")
    decrypted_plaintext = decrypt_cfb(encrypted_from_file, key)
    decrypted_message = decrypted_plaintext.decode('utf-8')
    print("Дешифрованное сообщение:", decrypted_message)

    # Проверка корректности шифрования/дешифрования
    assert decrypted_plaintext == plaintext, "Ошибка: дешифрованное сообщение не соответствует исходному!"
    print("Шифрование и дешифрование выполнены успешно.")


if __name__ == '__main__':
    main()
