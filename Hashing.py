import matplotlib.pyplot as plt

METHODS = {
    1: "Separate Chaining",
    2: "Linear Probing",
    3: "Quadratic Probing",
    4: "Double Hashing",
}


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def find_R(size):
    for n in range(size - 1, 1, -1):
        if is_prime(n):
            return n
    return 2  # Fallback for a table size of 3


class HashTable:
    def __init__(self, size, method):
        self.size, self.method = size, method
        self.R = find_R(size)
        self.table = [[] for _ in range(size)] if method == 1 else [None] * size
        self.count = self.collisions = self.total_probes = 0

    def hash_function(self, key):
        return key % self.size

    def probe(self, key, i):
        index = self.hash_function(key)
        if self.method == 2:
            return (index + i) % self.size
        if self.method == 3:
            return (index + i * i) % self.size
        step = self.R - key % self.R
        return (index + i * step) % self.size

    def insert(self, key, report=True):
        index, probes = self.hash_function(key), 0

        if self.method == 1:
            bucket = self.table[index]
            if key in bucket:
                if report:
                    print("Duplicate key. Insertion skipped.")
                return False
            probes = len(bucket) + 1
            self.collisions += bool(bucket)
            bucket.insert(0, key)
            pos = index
        else:
            for i in range(self.size):
                pos = self.probe(key, i)
                probes += 1
                if self.table[pos] == key:
                    if report:
                        print("Duplicate key. Insertion skipped.")
                    return False
                if self.table[pos] is None:
                    self.table[pos] = key
                    break
                self.collisions += 1
            else:
                if report:
                    print("No available slot found.")
                return False

        self.count += 1
        self.total_probes += probes
        if report:
            if self.method == 1:
                print(f"Key {key} inserted in bucket {index}.")
            else:
                print(f"Key {key} inserted at index {pos}.")
            print("Probes:", probes)
        return True

    def search(self, key):
        index, probes = self.hash_function(key), 0
        if self.method == 1:
            positions = [(index, value) for value in self.table[index]]
        else:
            positions = [(self.probe(key, i), None) for i in range(self.size)]

        for pos, value in positions:
            probes += 1
            current = value if self.method == 1 else self.table[pos]
            if self.method != 1 and current is None:
                break
            if current == key:
                if self.method == 1:
                    print(f"Key {key} found in bucket {index}.")
                else:
                    print(f"Key {key} found at index {pos}.")
                print("Probes:", probes)
                return True

        print(f"Key {key} not found. Probes: {probes}")
        return False

    def display(self):
        print(f"\nHASH TABLE ({METHODS.get(self.method, 'Unknown')})")
        print("-" * 35)
        for i, item in enumerate(self.table):
            value = "EMPTY" if item is None or (self.method == 1 and not item) else item
            print(f"{i:<8}{value}")

    def performance(self):
        average = self.total_probes / self.count if self.count else 0
        print("\nPERFORMANCE STATISTICS")
        print("-" * 30)
        print("Table size:", self.size)
        print("Keys stored:", self.count)
        print("Collisions:", self.collisions)
        print("Total insertion probes:", self.total_probes)
        print(f"Average probes: {average:.2f}")
        print(f"Load factor: {self.count / self.size:.2f}")


def compare_performance(keys, size):
    if not keys:
        print("Insert keys before comparing performance.")
        return

    names, collisions, average_probes = [], [], []
    print("\nPERFORMANCE COMPARISON")
    print("-" * 65)
    print(f"{'Method':<23}{'Inserted':<12}{'Collisions':<13}{'Avg Probes':<12}")
    print("-" * 65)

    for method, name in METHODS.items():
        ht = HashTable(size, method)
        for key in keys:
            ht.insert(key, report=False)
        average = ht.total_probes / ht.count if ht.count else 0
        names.append(name)
        collisions.append(ht.collisions)
        average_probes.append(average)
        print(f"{name:<23}{ht.count:<12}{ht.collisions:<13}{average:.2f}")

    print("-" * 65)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    charts = [
        (collisions, "Collision Comparison", "Number of Collisions", True),
        (average_probes, "Average Insertion Probes", "Average Number of Probes", False),
    ]

    for ax, (values, title, ylabel, whole_numbers) in zip(axes, charts):
        bars = ax.bar(names, values)
        ax.set_title(title)
        ax.set_xlabel("Hashing Method")
        ax.set_ylabel(ylabel)
        ax.tick_params(axis="x", rotation=25)
        for bar, value in zip(bars, values):
            label = str(value) if whole_numbers else f"{value:.2f}"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                label,
                ha="center",
                va="bottom",
            )

    fig.suptitle("Hashing Performance Comparison")
    plt.tight_layout()
    plt.show()


def main():
    size, hash_table, keys = 0, None, []

    while True:
        print("\n========== HASHING MENU ==========")
        print("1. Create Hash Table")
        print("2. Insert Key")
        print("3. Search Key")
        print("4. Display Hash Table")
        print("5. Evaluate Performance")
        print("6. Compare All Methods and Generate Graphs")
        print("7. Exit")
        print("==================================")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                new_size = int(input("Enter table size (minimum 3): "))
                if new_size < 3:
                    print("Table size must be at least 3.")
                    continue
                print("\nSelect Hashing Method")
                for number, name in METHODS.items():
                    print(f"{number}. {name}")
                method = int(input("Enter method: "))
                if method not in METHODS:
                    print("Invalid method.")
                    continue

                size, hash_table, keys = new_size, HashTable(new_size, method), []
                for value in input("Enter initial keys separated by spaces: ").split():
                    try:
                        key = int(value)
                        if key < 0:
                            print("Negative keys are not supported.")
                        elif hash_table.insert(key):
                            keys.append(key)
                    except ValueError:
                        print(f"Invalid key skipped: {value}")
                print("Hash table creation completed.")
            except ValueError:
                print("Enter a valid integer.")

        elif choice in ("2", "3"):
            if hash_table is None:
                print("Create a hash table first.")
                continue
            try:
                prompt = (
                    "Enter key to insert: "
                    if choice == "2"
                    else "Enter key to search: "
                )
                key = int(input(prompt))
                if key < 0:
                    print("Negative keys are not supported.")
                elif choice == "2":
                    if hash_table.insert(key):
                        keys.append(key)
                else:
                    hash_table.search(key)
            except ValueError:
                print("Enter a valid integer.")

        elif choice in ("4", "5", "6"):
            if hash_table is None:
                print("Create a hash table first.")
            elif choice == "4":
                hash_table.display()
            elif choice == "5":
                hash_table.performance()
            else:
                compare_performance(keys, size)

        elif choice == "7":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Enter 1-7.")


if __name__ == "__main__":
    main()
