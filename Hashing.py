def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


def find_R(size):
    for r in range(size - 1, 1, -1):
        if is_prime(r):
            return r
    return 2


class HashTable:
    def __init__(self, size, method):
        self.size = size
        self.method = method
        self.table = [[] for _ in range(size)] if method == 1 else [None] * size
        self.count = 0
        self.collisions = 0
        self.total_probes = 0
        self.keys_inserted = []
        self.R = find_R(size) if method == 4 else None

    def hash_function(self, key):
        return key % self.size

    def probe(self, key, i):
        index = self.hash_function(key)

        if self.method == 2:
            return (index + i) % self.size

        elif self.method == 3:
            return (index + i * i) % self.size

        elif self.method == 4:
            step = self.R + (key % self.R)

            # Avoid a zero step after modulo reduction.
            step %= self.size
            if step == 0:
                step = 1

            return (index + i * step) % self.size

    def insert(self, key, silent=False):
        if key < 0:
            if not silent:
                print("Only non-negative keys are allowed.")
            return False

        index = self.hash_function(key)

        if self.method == 1:
            if key in self.table[index]:
                if not silent:
                    print("Duplicate key. Insertion rejected.")
                return False

            if self.table[index]:
                self.collisions += 1

            self.table[index].append(key)
            self.count += 1
            self.keys_inserted.append(key)

            if not silent:
                print(f"Key {key} inserted successfully at index {index}.")
            return True

        for i in range(self.size):
            pos = self.probe(key, i)

            if self.table[pos] == key:
                if not silent:
                    print("Duplicate key. Insertion rejected.")
                return False

            if self.table[pos] is None:
                self.table[pos] = key
                self.count += 1
                self.total_probes += i + 1
                self.keys_inserted.append(key)

                if not silent:
                    print(f"Key {key} inserted successfully at index {pos}.")
                return True

            self.collisions += 1

        if not silent:
            print(f"Unable to insert key {key}. No available slot in probe sequence.")
        return False

    def search(self, key):
        index = self.hash_function(key)

        if self.method == 1:
            if key in self.table[index]:
                print(f"Key {key} found at index {index}.")
            else:
                print(f"Key {key} not found.")
            return

        for i in range(self.size):
            pos = self.probe(key, i)

            if self.table[pos] is None:
                break

            if self.table[pos] == key:
                print(f"Key {key} found at index {pos}.")
                return

        print(f"Key {key} not found.")

    def display(self):
        print("\nHash Table:")
        print("Index\tValue")
        print("----------------")

        for i in range(self.size):
            if self.method == 1:
                value = (
                    " -> ".join(map(str, self.table[i])) if self.table[i] else "EMPTY"
                )
            else:
                value = self.table[i] if self.table[i] is not None else "EMPTY"

            print(f"{i}\t{value}")

    def evaluate_performance(self):
        load_factor = self.count / self.size

        print("\nPerformance Evaluation")
        print("---------------------")
        print(f"Number of keys  : {self.count}")
        print(f"Table size      : {self.size}")
        print(f"Load factor     : {load_factor:.2f}")
        print(f"Collisions      : {self.collisions}")

        if self.method != 1 and self.count > 0:
            print(f"Average probes  : {self.total_probes / self.count:.2f}")

        if self.method == 4:
            print(f"Selected R      : {self.R}")


def compare_performance(keys, size):
    methods = {
        1: "Separate Chaining",
        2: "Linear Probing",
        3: "Quadratic Probing",
        4: "Double Hashing",
    }

    print("\nComparison of Collision Resolution Methods")
    print("=" * 76)
    print(
        f"{'Method':<23}{'Inserted':<12}{'Collisions':<14}{'Load Factor':<12}{'Avg Probes':<12}"
    )
    print("-" * 76)

    for method, name in methods.items():
        temp = HashTable(size, method)

        for key in keys:
            temp.insert(key, silent=True)

        load_factor = temp.count / size
        avg_probes = temp.total_probes / temp.count if temp.count else 0

        print(
            f"{name:<23}"
            f"{temp.count:<12}"
            f"{temp.collisions:<14}"
            f"{load_factor:<12.2f}"
            f"{avg_probes:<12.2f}"
        )

    print("=" * 76)


def main():
    ht = None

    while True:
        print("\n========== HASHING MENU ==========")
        print("1. Create Hash Table")
        print("2. Insert Key")
        print("3. Search Key")
        print("4. Display Hash Table")
        print("5. Evaluate Performance")
        print("6. Compare All Methods")
        print("7. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                size = int(input("Enter the size of the hash table: "))

                if size < 3:
                    print("Table size must be at least 3.")
                    continue

                print("\nSelect Collision Resolution Technique:")
                print("1. Open Hashing (Separate Chaining)")
                print("2. Closed Hashing (Linear Probing)")
                print("3. Closed Hashing (Quadratic Probing)")
                print("4. Closed Hashing (Double Hashing)")

                method = int(input("Enter your choice: "))

                if method not in (1, 2, 3, 4):
                    print("Invalid method choice.")
                    continue

                ht = HashTable(size, method)

                if method == 4:
                    print(f"Selected R: {ht.R}")

                keys_input = input(
                    "Enter the keys to insert (space-separated): "
                ).split()

                for key in keys_input:
                    ht.insert(int(key))

            elif choice == 2:
                if ht is None:
                    print("Create a hash table first.")
                    continue

                ht.insert(int(input("Enter key to insert: ")))

            elif choice == 3:
                if ht is None:
                    print("Create a hash table first.")
                    continue

                ht.search(int(input("Enter key to search: ")))

            elif choice == 4:
                if ht is None:
                    print("Create a hash table first.")
                    continue

                ht.display()

            elif choice == 5:
                if ht is None:
                    print("Create a hash table first.")
                    continue

                ht.evaluate_performance()

            elif choice == 6:
                if ht is None:
                    print("Create a hash table first.")
                    continue

                if not ht.keys_inserted:
                    print("The hash table is empty.")
                    continue

                compare_performance(ht.keys_inserted, ht.size)

            elif choice == 7:
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Try again.")

        except ValueError:
            print("Please enter valid integer values.")


if __name__ == "__main__":
    main()
