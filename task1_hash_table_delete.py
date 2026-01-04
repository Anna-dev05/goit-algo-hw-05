class HashTable:
    def __init__(self, size: int = 10):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key) -> int:
        return hash(key) % self.size

    def insert(self, key, value) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  
                return

        bucket.append((key, value))  

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key) -> bool:
        """
        Видаляє пару key-value.
        Повертає True, якщо видалили, і False, якщо ключ не знайдено.
        """
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True

        return False


if __name__ == "__main__":
    ht = HashTable()
    ht.insert("apple", 10)
    ht.insert("banana", 20)

    print("apple =", ht.get("apple"))      
    print("delete apple:", ht.delete("apple"))  
    print("apple =", ht.get("apple"))      
    print("delete apple again:", ht.delete("apple"))  
