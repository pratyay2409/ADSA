import math

HEAP_TYPES = {
    1: "Binary Heap",
    2: "Binomial Heap",
    3: "Fibonacci Heap",
}


class BinaryHeap:
    """Array-based Min-Binary Heap with operation instrumentation."""

    def __init__(self):
        self.heap = []
        self.comparisons = 0
        self.structural_ops = 0
        self.insertions = 0
        self.extractions = 0
        self.decreases = 0

    def _sift_up(self, idx):
        ops = 0
        while idx > 0:
            parent = (idx - 1) // 2
            self.comparisons += 1
            ops += 1
            if self.heap[idx] < self.heap[parent]:
                self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
                self.structural_ops += 1
                idx = parent
            else:
                break
        return ops

    def _sift_down(self, idx):
        n = len(self.heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < n:
                self.comparisons += 1
                if self.heap[left] < self.heap[smallest]:
                    smallest = left
            if right < n:
                self.comparisons += 1
                if self.heap[right] < self.heap[smallest]:
                    smallest = right
            if smallest != idx:
                self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
                self.structural_ops += 1
                idx = smallest
            else:
                break

    def insert(self, key, report=True):
        if key in self.heap:
            if report:
                print("Duplicate key. Insertion skipped.")
            return False
        self.heap.append(key)
        self.structural_ops += 1
        self.insertions += 1
        before_c, before_s = self.comparisons, self.structural_ops
        self._sift_up(len(self.heap) - 1)
        steps = (self.comparisons - before_c) + (self.structural_ops - before_s) + 1
        if report:
            idx = self.heap.index(key)
            print(f"Key {key} inserted at index {idx}. Steps: {steps}")
        return True

    def get_min(self):
        return self.heap[0] if self.heap else None

    def extract_min(self, report=True):
        if not self.heap:
            if report:
                print("Heap is empty.")
            return None
        min_val = self.heap[0]
        last_val = self.heap.pop()
        self.extractions += 1
        before_c, before_s = self.comparisons, self.structural_ops
        if self.heap:
            self.heap[0] = last_val
            self.structural_ops += 1
            self._sift_down(0)
        steps = (self.comparisons - before_c) + (self.structural_ops - before_s)
        if report:
            print(f"Extracted minimum key: {min_val}. Heapify steps: {steps}")
        return min_val

    def decrease_key(self, old_key, new_key, report=True):
        if new_key >= old_key:
            if report:
                print("New key must be smaller than current key.")
            return False
        if new_key in self.heap:
            if report:
                print("New key already exists in the heap.")
            return False
        try:
            idx = self.heap.index(old_key)
        except ValueError:
            if report:
                print(f"Key {old_key} not found in heap.")
            return False
        self.heap[idx] = new_key
        self.decreases += 1
        before_c, before_s = self.comparisons, self.structural_ops
        self._sift_up(idx)
        steps = (self.comparisons - before_c) + (self.structural_ops - before_s)
        if report:
            print(f"Key {old_key} decreased to {new_key}. Sift-up steps: {steps}")
        return True

    def _print_tree(self, idx=0, prefix="", is_left=None):
        if idx >= len(self.heap):
            return
        if is_left is None:
            print(f"{prefix}[{self.heap[idx]}] (ROOT, index={idx})")
            new_prefix = prefix
        else:
            branch = "|-- L: " if is_left else "`-- R: "
            print(f"{prefix}{branch}[{self.heap[idx]}] (index={idx})")
            new_prefix = prefix + ("|      " if is_left else "       ")

        left = 2 * idx + 1
        right = 2 * idx + 2
        if left < len(self.heap) or right < len(self.heap):
            if left < len(self.heap):
                self._print_tree(left, new_prefix, True)
            if right < len(self.heap):
                self._print_tree(right, new_prefix, False)

    def display(self):
        print("\nHEAP STRUCTURE (Binary Heap)")
        print("=" * 55)
        if not self.heap:
            print("EMPTY")
            return
        print(f"Minimum Element (Root) : {self.heap[0]}")
        print(f"Total Elements         : {len(self.heap)}")
        print(f"Array Representation   : {self.heap}")
        print("\n1. Level-by-Level View:")
        height = int(math.log2(len(self.heap))) + 1
        for level in range(height):
            start = (2 ** level) - 1
            end = min((2 ** (level + 1)) - 1, len(self.heap))
            nodes = [f"[{self.heap[i]}]" for i in range(start, end)]
            print(f"   Level {level}: " + "  ".join(nodes))
        print("\n2. Tree Hierarchy (Parent -> Left/Right Child):")
        self._print_tree(0, "   ")
        print("=" * 55)

    def size(self):
        return len(self.heap)


class BinomialNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None


class BinomialHeap:
    """Binomial Heap supporting O(log n) worst-case merge and priority queue operations."""

    def __init__(self):
        self.head = None
        self.nodes = {}
        self.comparisons = 0
        self.structural_ops = 0
        self.insertions = 0
        self.extractions = 0
        self.decreases = 0

    def _link(self, y, z):
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1
        self.structural_ops += 1

    def _merge_roots(self, h1, h2):
        if not h1:
            return h2
        if not h2:
            return h1
        dummy = BinomialNode(0)
        tail = dummy
        while h1 and h2:
            if h1.degree <= h2.degree:
                tail.sibling = h1
                h1 = h1.sibling
            else:
                tail.sibling = h2
                h2 = h2.sibling
            tail = tail.sibling
        tail.sibling = h1 if h1 else h2
        return dummy.sibling

    def _union(self, h2_head):
        new_head = self._merge_roots(self.head, h2_head)
        if not new_head:
            return None
        prev_x = None
        x = new_head
        next_x = x.sibling
        while next_x is not None:
            if (x.degree != next_x.degree) or (
                next_x.sibling is not None and next_x.sibling.degree == x.degree
            ):
                prev_x = x
                x = next_x
            else:
                self.comparisons += 1
                if x.key <= next_x.key:
                    x.sibling = next_x.sibling
                    self._link(next_x, x)
                else:
                    if prev_x is None:
                        new_head = next_x
                    else:
                        prev_x.sibling = next_x
                    self._link(x, next_x)
                    x = next_x
            next_x = x.sibling
        return new_head

    def insert(self, key, report=True):
        if key in self.nodes:
            if report:
                print("Duplicate key. Insertion skipped.")
            return False
        node = BinomialNode(key)
        self.nodes[key] = node
        self.insertions += 1
        before_c, before_s = self.comparisons, self.structural_ops
        self.head = self._union(node)
        self.structural_ops += 1
        steps = (self.comparisons - before_c) + (self.structural_ops - before_s)
        if report:
            print(f"Key {key} inserted into Binomial Heap. Steps: {steps}")
        return True

    def get_min(self):
        if not self.head:
            return None
        y = self.head
        min_val = y.key
        curr = y.sibling
        while curr:
            self.comparisons += 1
            if curr.key < min_val:
                min_val = curr.key
            curr = curr.sibling
        return min_val

    def extract_min(self, report=True):
        if not self.head:
            if report:
                print("Heap is empty.")
            return None
        before_c, before_s = self.comparisons, self.structural_ops
        min_node = self.head
        min_prev = None
        prev = min_node
        curr = min_node.sibling
        while curr:
            self.comparisons += 1
            if curr.key < min_node.key:
                min_node = curr
                min_prev = prev
            prev = curr
            curr = curr.sibling

        if min_prev:
            min_prev.sibling = min_node.sibling
        else:
            self.head = min_node.sibling

        child_head = None
        c = min_node.child
        while c:
            next_c = c.sibling
            c.sibling = child_head
            c.parent = None
            child_head = c
            self.structural_ops += 1
            c = next_c

        self.head = self._union(child_head)
        del self.nodes[min_node.key]
        self.extractions += 1
        steps = (self.comparisons - before_c) + (self.structural_ops - before_s)
        if report:
            print(f"Extracted minimum key: {min_node.key}. Consolidation steps: {steps}")
        return min_node.key

    def decrease_key(self, old_key, new_key, report=True):
        if new_key >= old_key:
            if report:
                print("New key must be smaller than current key.")
            return False
        if new_key in self.nodes:
            if report:
                print("New key already exists in the heap.")
            return False
        if old_key not in self.nodes:
            if report:
                print(f"Key {old_key} not found in heap.")
            return False
        before_c, before_s = self.comparisons, self.structural_ops
        node = self.nodes.pop(old_key)
        node.key = new_key
        self.nodes[new_key] = node
        y = node
        z = y.parent
        while z is not None:
            self.comparisons += 1
            if y.key < z.key:
                y.key, z.key = z.key, y.key
                self.nodes[y.key] = y
                self.nodes[z.key] = z
                self.structural_ops += 1
                y = z
                z = y.parent
            else:
                break
        self.decreases += 1
        steps = (self.comparisons - before_c) + (self.structural_ops - before_s)
        if report:
            print(f"Key {old_key} decreased to {new_key}. Bubble-up steps: {steps}")
        return True

    def _print_binomial_subtree(self, node, prefix="", is_last=True):
        branch = "`-- " if is_last else "|-- "
        print(f"{prefix}{branch}[{node.key}] (deg={node.degree})")
        children = []
        c = node.child
        while c:
            children.append(c)
            c = c.sibling
        children.reverse()
        new_prefix = prefix + ("    " if is_last else "|   ")
        for i, child in enumerate(children):
            self._print_binomial_subtree(child, new_prefix, i == len(children) - 1)

    def display(self):
        print("\nHEAP STRUCTURE (Binomial Heap)")
        print("=" * 55)
        if not self.head:
            print("EMPTY")
            return
        roots = []
        curr = self.head
        min_key = curr.key
        while curr:
            roots.append(curr)
            if curr.key < min_key:
                min_key = curr.key
            curr = curr.sibling

        root_summary = " --> ".join([f"B{r.degree}(root={r.key})" for r in roots])
        print(f"Minimum Key   : {min_key}")
        print(f"Total Elements: {len(self.nodes)}")
        print(f"Root List     : {root_summary}")
        print("\nBinomial Trees in Forest:")
        for r in roots:
            print(f"\n   [Binomial Tree B{r.degree} | {2 ** r.degree} node(s)]")
            print(f"   [{r.key}] (ROOT, deg={r.degree})")
            children = []
            c = r.child
            while c:
                children.append(c)
                c = c.sibling
            children.reverse()
            for i, child in enumerate(children):
                self._print_binomial_subtree(child, "   ", i == len(children) - 1)
        print("=" * 55)

    def size(self):
        return len(self.nodes)


class FibNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.mark = False
        self.parent = None
        self.child = None
        self.left = self
        self.right = self


class FibonacciHeap:
    """Fibonacci Heap with O(1) amortized insert/decrease-key and cascading cuts."""

    def __init__(self):
        self.min_node = None
        self.nodes = {}
        self.comparisons = 0
        self.structural_ops = 0
        self.insertions = 0
        self.extractions = 0
        self.decreases = 0

    def _add_to_root_list(self, node):
        node.parent = None
        if self.min_node is None:
            node.left = node.right = node
            self.min_node = node
        else:
            node.left = self.min_node
            node.right = self.min_node.right
            self.min_node.right.left = node
            self.min_node.right = node

    def _remove_from_list(self, node):
        node.left.right = node.right
        node.right.left = node.left

    def insert(self, key, report=True):
        if key in self.nodes:
            if report:
                print("Duplicate key. Insertion skipped.")
            return False
        node = FibNode(key)
        self.nodes[key] = node
        self.insertions += 1
        before_c, before_s = self.comparisons, self.structural_ops
        self._add_to_root_list(node)
        self.structural_ops += 1
        if node != self.min_node:
            self.comparisons += 1
            if node.key < self.min_node.key:
                self.min_node = node
        steps = (self.comparisons - before_c) + (self.structural_ops - before_s)
        if report:
            print(f"Key {key} inserted into Fibonacci root list. Steps: {steps}")
        return True

    def get_min(self):
        return self.min_node.key if self.min_node else None

    def _fib_link(self, y, x):
        self._remove_from_list(y)
        y.parent = x
        if x.child is None:
            x.child = y
            y.left = y.right = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1
        y.mark = False
        self.structural_ops += 1

    def _consolidate(self):
        max_deg = int(math.log2(len(self.nodes))) + 3 if self.nodes else 1
        A = [None] * (max_deg + 2)
        roots = []
        if self.min_node:
            curr = self.min_node
            while True:
                roots.append(curr)
                curr = curr.right
                if curr == self.min_node:
                    break
        for w in roots:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                self.comparisons += 1
                if x.key > y.key:
                    x, y = y, x
                self._fib_link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        self.min_node = None
        for node in A:
            if node is not None:
                if self.min_node is None:
                    node.left = node.right = node
                    self.min_node = node
                else:
                    self._add_to_root_list(node)
                    self.comparisons += 1
                    if node.key < self.min_node.key:
                        self.min_node = node

    def extract_min(self, report=True):
        z = self.min_node
        if z is None:
            if report:
                print("Heap is empty.")
            return None
        before_c, before_s = self.comparisons, self.structural_ops
        if z.child is not None:
            children = []
            c = z.child
            while True:
                children.append(c)
                c = c.right
                if c == z.child:
                    break
            for c in children:
                self._add_to_root_list(c)
                self.structural_ops += 1
        self._remove_from_list(z)
        if z == z.right:
            self.min_node = None
        else:
            self.min_node = z.right
            self._consolidate()
        del self.nodes[z.key]
        self.extractions += 1
        steps = (self.comparisons - before_c) + (self.structural_ops - before_s)
        if report:
            print(f"Extracted minimum key: {z.key}. Consolidation steps: {steps}")
        return z.key

    def _cut(self, x, y):
        if x.right == x:
            y.child = None
        else:
            if y.child == x:
                y.child = x.right
            self._remove_from_list(x)
        y.degree -= 1
        self._add_to_root_list(x)
        x.mark = False
        self.structural_ops += 1

    def _cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

    def decrease_key(self, old_key, new_key, report=True):
        if new_key >= old_key:
            if report:
                print("New key must be smaller than current key.")
            return False
        if new_key in self.nodes:
            if report:
                print("New key already exists in the heap.")
            return False
        if old_key not in self.nodes:
            if report:
                print(f"Key {old_key} not found in heap.")
            return False
        before_c, before_s = self.comparisons, self.structural_ops
        x = self.nodes.pop(old_key)
        x.key = new_key
        self.nodes[new_key] = x
        y = x.parent
        if y is not None:
            self.comparisons += 1
            if x.key < y.key:
                self._cut(x, y)
                self._cascading_cut(y)
        self.comparisons += 1
        if x.key < self.min_node.key:
            self.min_node = x
        self.decreases += 1
        steps = (self.comparisons - before_c) + (self.structural_ops - before_s)
        if report:
            print(f"Key {old_key} decreased to {new_key}. Cut steps: {steps}")
        return True

    def _get_children(self, node):
        children = []
        if node.child is not None:
            c = node.child
            while True:
                children.append(c)
                c = c.right
                if c == node.child:
                    break
        return children

    def _print_fib_subtree(self, node, prefix="", is_last=True):
        branch = "`-- " if is_last else "|-- "
        mark_str = ", marked=True" if node.mark else ""
        print(f"{prefix}{branch}[{node.key}] (deg={node.degree}{mark_str})")
        children = self._get_children(node)
        new_prefix = prefix + ("    " if is_last else "|   ")
        for i, child in enumerate(children):
            self._print_fib_subtree(child, new_prefix, i == len(children) - 1)

    def display(self):
        print("\nHEAP STRUCTURE (Fibonacci Heap)")
        print("=" * 55)
        if not self.min_node:
            print("EMPTY")
            return
        roots = []
        curr = self.min_node
        while True:
            roots.append(curr)
            curr = curr.right
            if curr == self.min_node:
                break

        print(f"Minimum Pointer (min_node) : [{self.min_node.key}]")
        print(f"Total Elements             : {len(self.nodes)}")
        print(f"Number of Trees in Root List: {len(roots)}")
        root_chain = " <-> ".join([f"[{r.key}]" for r in roots])
        print(f"Circular Root List         : (circular) <-> {root_chain} <-> (back to [{roots[0].key}])")
        print("\nTrees in Root List:")
        for idx, r in enumerate(roots, start=1):
            min_tag = " <-- MIN ROOT" if r == self.min_node else ""
            print(f"   Tree {idx}: [{r.key}] (ROOT, deg={r.degree}){min_tag}")
            children = self._get_children(r)
            for i, child in enumerate(children):
                self._print_fib_subtree(child, "      ", i == len(children) - 1)
        if all(r.degree == 0 for r in roots) and len(roots) > 1:
            print("\n   (Note: Fibonacci Heap uses lazy insertion; trees consolidate into")
            print("    deeper hierarchies when Option 3 'Extract Minimum Key' is executed.)")
        print("=" * 55)

    def size(self):
        return len(self.nodes)


def create_heap_instance(heap_type):
    if heap_type == 1:
        return BinaryHeap()
    if heap_type == 2:
        return BinomialHeap()
    return FibonacciHeap()


def evaluate_performance(heap, heap_type):
    total_ops = heap.insertions + heap.extractions + heap.decreases
    avg_comp = heap.comparisons / total_ops if total_ops else 0
    avg_struct = heap.structural_ops / total_ops if total_ops else 0
    print(f"\nPERFORMANCE STATISTICS ({HEAP_TYPES.get(heap_type, 'Unknown')})")
    print("-" * 40)
    print("Current keys stored:", heap.size())
    print("Minimum key:", heap.get_min())
    print("Total operations executed:", total_ops)
    print("Total key comparisons:", heap.comparisons)
    print("Total structural operations:", heap.structural_ops)
    print(f"Average comparisons/op: {avg_comp:.2f}")
    print(f"Average structural steps/op: {avg_struct:.2f}")


def compare_heaps(keys):
    if not keys:
        print("Insert keys before comparing heap variants.")
        return

    print("\nHEAP PERFORMANCE COMPARISON (Insert + Decrease-Key + Extract-Min)")
    print("-" * 74)
    print(
        f"{'Heap Type':<18}{'Inserted':<10}{'Comparisons':<15}"
        f"{'Structural Ops':<16}{'Avg Steps/Op':<12}"
    )
    print("-" * 74)

    for htype, name in HEAP_TYPES.items():
        h = create_heap_instance(htype)
        for k in keys:
            h.insert(k, report=False)
        # Perform Decrease-Key on the largest 2 keys and 2 Extract-Min operations
        sorted_k = sorted(keys, reverse=True)
        for idx, target in enumerate(sorted_k[:2]):
            h.decrease_key(target, idx + 1, report=False)
        for _ in range(min(2, len(keys))):
            h.extract_min(report=False)

        total_ops = h.insertions + h.extractions + h.decreases
        avg = (h.comparisons + h.structural_ops) / total_ops if total_ops else 0
        print(
            f"{name:<18}{h.insertions:<10}{h.comparisons:<15}"
            f"{h.structural_ops:<16}{avg:<12.2f}"
        )

    print("-" * 74)


def main():
    heap_type, heap, keys = 0, None, []

    while True:
        print("\n========== HEAP OPERATIONS MENU ==========")
        print("1. Create Heap")
        print("2. Insert Key")
        print("3. Extract Minimum Key")
        print("4. Decrease Key")
        print("5. Display Heap")
        print("6. Evaluate Performance")
        print("7. Compare All Heaps")
        print("8. Exit")
        print("==========================================")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                print("\nSelect Heap Implementation")
                for number, name in HEAP_TYPES.items():
                    print(f"{number}. {name}")
                heap_type = int(input("Enter heap type: "))
                if heap_type not in HEAP_TYPES:
                    print("Invalid heap type.")
                    continue
                heap = create_heap_instance(heap_type)
                keys = []
                for value in input("Enter initial keys separated by spaces: ").split():
                    try:
                        k = int(value)
                        if k <= 0:
                            print("Only positive integer keys are supported.")
                        elif heap.insert(k):
                            keys.append(k)
                    except ValueError:
                        print(f"Invalid key skipped: {value}")
                print(f"{HEAP_TYPES[heap_type]} creation completed.")
            except ValueError:
                print("Enter a valid integer.")

        elif choice in ("2", "3", "4", "5", "6"):
            if heap is None:
                print("Create a heap first.")
                continue
            if choice == "2":
                try:
                    k = int(input("Enter key to insert: "))
                    if k <= 0:
                        print("Only positive integer keys are supported.")
                    elif heap.insert(k):
                        keys.append(k)
                except ValueError:
                    print("Enter a valid integer.")
            elif choice == "3":
                heap.extract_min()
            elif choice == "4":
                try:
                    old_k = int(input("Enter key to decrease: "))
                    new_k = int(input("Enter new smaller key value: "))
                    heap.decrease_key(old_k, new_k)
                except ValueError:
                    print("Enter valid integers.")
            elif choice == "5":
                heap.display()
            elif choice == "6":
                evaluate_performance(heap, heap_type)

        elif choice == "7":
            compare_heaps(keys)

        elif choice == "8":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Enter 1-8.")


if __name__ == "__main__":
    main()
