import hashlib
import time


class Block:
    def __init__(self, data, previous_hash, difficulty):
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.mine()

    def get_hash(self):
        sha = hashlib.sha256()
        hash_str = str(self.previous_hash) + str(self.timestamp) + str(self.data) + str(self.nonce)
        sha.update(hash_str.encode('utf-8'))
        return sha.hexdigest()

    def mine(self):
        target = '0' * self.difficulty
        while True:
            hash_mined = self.get_hash()
            if hash_mined.startswith(target):
                return hash_mined
            else:
                self.nonce += 1

class Blockchain:
    def __init__(self, difficulty):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("Genesis Block", "0", self.difficulty)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_hash = self.get_last_block().hash
        new_block = Block(data, previous_hash, self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for x in range(1, len(self.chain)):
            current = self.chain[x]
            previous = self.chain[x - 1]
            # Проверяем, не изменились ли данные блока
            if current.hash != current.get_hash():
                return False
            # Проверяем соответствие previous_hash
            if current.previous_hash != previous.hash:
                return False
        return True


if __name__ == '__main__':
    difficulty = 5 # кол-во нулей
    my_blockchain = Blockchain(difficulty)

    print("Генезис-блок создан:")
    print(f"Data: {my_blockchain.chain[0].data}")
    print(f"Timestamp: {my_blockchain.chain[0].timestamp}")
    print(f"Nonce: {my_blockchain.chain[0].nonce}")
    print(f"Hash: {my_blockchain.chain[0].hash}")
    print(f"PrevHash: {my_blockchain.chain[0].previous_hash}")

    # Добавляем несколько блоков
    print("\nДобавление новых блоков...")
    my_blockchain.add_block("Block 1 Data")
    my_blockchain.add_block("Block 2 Data")
    my_blockchain.add_block("Block 3 Data")

    # Выводим информацию по всем блокам
    for i, block in enumerate(my_blockchain.chain):
        print(f"\nBlock {i}:")
        print(f"Data: {block.data}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Nonce: {block.nonce}")
        print(f"Hash: {block.hash}")
        print(f"PrevHash: {block.previous_hash}")

    is_valid = my_blockchain.is_chain_valid()
    print("\nПроверка цепочки:", "Valid" if is_valid else "Invalid")

    with open("blockchain.txt", "w") as f:
        for i, block in enumerate(my_blockchain.chain):
            f.write(f"Block {i}:\n")
            f.write(f"Data: {block.data}\n")
            f.write(f"Timestamp: {block.timestamp}\n")
            f.write(f"Nonce: {block.nonce}\n")
            f.write(f"Hash: {block.hash}\n")
            f.write(f"PrevHash: {block.previous_hash}\n\n")
    print("\nРезультаты записаны в файл 'blockchain.txt'")
