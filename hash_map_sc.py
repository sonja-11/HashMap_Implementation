# Name: Sonja Hanemann
# OSU Email: hanemans@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/07/2023
# Description: HashMap Implementation using a dynamic array to store the hash table and implementing chaining for
#              collision resolution using a singly linked list.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a new key/value pair must be added.
        For this hash map implementation, the table must be resized to double its current
        capacity when this method is called and the current load factor of the table is
        greater than or equal to 1.0.
        """
        if self.table_load() >= 1.0:
            self.resize_table(self.get_capacity() * 2)

        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        bucket = self._buckets[index]
        for i in bucket:
            if i.key == key:
                i.value = value
                return

        bucket.insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs
        must remain in the new hash map, and all hash table links must be rehashed. (Consider
        calling another HashMap method for this part).
        First check that new_capacity is not less than 1; if so, the method does nothing.
        If new_capacity is 1 or more, make sure it is a prime number. If not, change it to the next
        highest prime number. You may use the methods _is_prime() and _next_prime() from the
        skeleton code.
        """
        if new_capacity < 1:
            return
        else:
            if not (self._is_prime(new_capacity)):
                new_capacity = self._next_prime(new_capacity)

        new_table = DynamicArray()
        for i in range(new_capacity):
            new_table.append(LinkedList())

        for i in range(self.get_capacity()):
            bucket = self._buckets[i]
            for j in bucket:
                index = self._hash_function(j.key) % new_capacity
                new_table[index].insert(j.key, j.value)

        self._buckets = new_table
        self._capacity = new_capacity

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return float(self.get_size() / self.get_capacity())

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        count = 0
        for i in range(self.get_capacity()):
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def get(self, key: str):
        """
        Returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        bucket = self._buckets[index]

        if bucket.contains(key) is not None:
            return bucket.contains(key).value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        bucket = self._buckets[index]

        for i in bucket:
            if i.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).
        """
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        bucket = self._buckets[index]

        if bucket.remove(key) is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map. The order of the keys in the dynamic array does not matter.
        """
        list = DynamicArray()
        for i in range(self.get_capacity()):
            bucket = self._buckets.get_at_index(i)
            if bucket is not None:
                for j in bucket:
                    list.append((j.key, j.value))
        return list

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        for i in range(self.get_capacity()):
            self._buckets[i] = LinkedList()
        self._size = 0

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Standalone function outside of the HashMap class that receives a dynamic array,
    which is not guaranteed to be sorted. This function will return a tuple containing, in this
    order, a dynamic array comprising the mode (most occurring) value(s) of the given array,
    and an integer representing the highest frequency of occurrence for the mode value(s).
    If there is more than one value with the highest frequency, all values at that frequency
    should be included in the array being returned (the order does not matter). If there is only
    one mode, the dynamic array will only contain that value.
    You may assume that the input array will contain at least one element, and that all values
    stored in the array will be strings. You do not need to write checks for these conditions.
    For full credit, the function must be implemented with O(N) time complexity. For best
    results, we recommend using the separate chaining hash map instance provided for you in
    the function’s skeleton code.
    """
    map = HashMap()
    # Populate data to the map
    for i in range(da.length()):
        element = da.get_at_index(i)
        if map.contains_key(element):
            map.put(element, map.get(element) + 1)
        else:
            map.put(element, 1)

    # Find the max count in pairs
    max_freq = 0
    kv_list = map.get_keys_and_values()
    for i in range(kv_list.length()):
        key, value = kv_list[i]
        if value > max_freq:
            max_freq = value
    max_element = DynamicArray()

    # Return result
    for i in range(kv_list.length()):
        key, value = kv_list[i]
        if value == max_freq:
            max_element.append(key)

    return max_element, max_freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
