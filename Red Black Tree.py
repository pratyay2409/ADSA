# Menu-Driven Program to Implement a Red-Black Tree
import sys

# Ensure UTF-8 output encoding for tree drawing characters on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class Node:
    def __init__(self, key=None, color="BLACK"):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        # NIL represents every missing child
        self.NIL = Node()
        self.NIL.color = "BLACK"
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL

        self.root = self.NIL

    # ---------------- CREATION ----------------

    def clear(self):
        self.root = self.NIL
        self.NIL.parent = self.NIL

    # ---------------- SEARCH ----------------

    def search(self, key):
        current = self.root

        while current != self.NIL:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return self.NIL

    # ---------------- LEFT ROTATION ----------------

    def left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    # ---------------- RIGHT ROTATION ----------------

    def right_rotate(self, x):
        y = x.left
        x.left = y.right

        if y.right != self.NIL:
            y.right.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    # ---------------- INSERTION ----------------

    def insert(self, key):
        parent = self.NIL
        current = self.root

        # Find the correct insertion position
        while current != self.NIL:
            parent = current

            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return False  # Duplicate keys are not allowed

        # Insert the new node as RED
        node = Node(key, "RED")
        node.left = self.NIL
        node.right = self.NIL
        node.parent = parent

        if parent == self.NIL:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node

        self.insert_fixup(node)
        return True

    def insert_fixup(self, z):
        while z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right

                # Case 1: Uncle is RED
                if uncle.color == "RED":
                    z.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent

                else:
                    # Case 2: Triangle configuration
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)

                    # Case 3: Line configuration
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.right_rotate(z.parent.parent)

            else:
                # Mirror cases when parent is a right child
                uncle = z.parent.parent.left

                # Case 1: Uncle is RED
                if uncle.color == "RED":
                    z.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent

                else:
                    # Case 2: Triangle configuration
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)

                    # Case 3: Line configuration
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.left_rotate(z.parent.parent)

        # The root must always be BLACK
        self.root.color = "BLACK"

    # ---------------- DELETION ----------------

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def delete(self, key):
        z = self.search(key)

        if z == self.NIL:
            return False

        y = z
        original_color = y.color

        # Case 1: Node has no left child
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)

        # Case 2: Node has no right child
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)

        # Case 3: Node has two children
        else:
            y = self.minimum(z.right)
            original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        # Fix the Red-Black Tree if a BLACK node was removed
        if original_color == "BLACK":
            self.delete_fixup(x)

        return True

    def delete_fixup(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                sibling = x.parent.right

                # Case 1: Sibling is RED
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    sibling = x.parent.right

                # Case 2: Sibling and both children are BLACK
                if sibling.left.color == "BLACK" and sibling.right.color == "BLACK":
                    if sibling != self.NIL:
                        sibling.color = "RED"

                    x = x.parent

                else:
                    # Case 3: Far child is BLACK
                    if sibling.right.color == "BLACK":
                        sibling.left.color = "BLACK"
                        sibling.color = "RED"
                        self.right_rotate(sibling)
                        sibling = x.parent.right

                    # Case 4: Far child is RED
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"
                    sibling.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root

            else:
                # Mirror cases when x is a right child
                sibling = x.parent.left

                # Case 1: Sibling is RED
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    sibling = x.parent.left

                # Case 2: Sibling and both children are BLACK
                if sibling.right.color == "BLACK" and sibling.left.color == "BLACK":
                    if sibling != self.NIL:
                        sibling.color = "RED"

                    x = x.parent

                else:
                    # Case 3: Far child is BLACK
                    if sibling.left.color == "BLACK":
                        sibling.right.color = "BLACK"
                        sibling.color = "RED"
                        self.left_rotate(sibling)
                        sibling = x.parent.left

                    # Case 4: Far child is RED
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"
                    sibling.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = "BLACK"

    # ---------------- TRAVERSALS ----------------

    def preorder(self, node, result):
        if node != self.NIL:
            result.append(f"{node.key}({node.color})")
            self.preorder(node.left, result)
            self.preorder(node.right, result)

    def inorder(self, node, result):
        if node != self.NIL:
            self.inorder(node.left, result)
            result.append(f"{node.key}({node.color})")
            self.inorder(node.right, result)

    def postorder(self, node, result):
        if node != self.NIL:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(f"{node.key}({node.color})")

    # ---------------- DISPLAY ----------------

    def display_tree(self, node, label="ROOT", prefix="", is_last=True):
        if node == self.NIL:
            return

        # Display the root
        if label == "ROOT":
            print(f"ROOT: {node.key} ({node.color})")
            child_prefix = ""
        else:
            connector = "└── " if is_last else "├── "

            print(f"{prefix}{connector}{label}: {node.key} ({node.color})")

            child_prefix = prefix + ("    " if is_last else "│   ")

        # Collect existing left and right children
        children = []

        if node.left != self.NIL:
            children.append(("LEFT", node.left))

        if node.right != self.NIL:
            children.append(("RIGHT", node.right))

        # Display left and right subtrees
        for index, (child_label, child_node) in enumerate(children):
            last_child = index == len(children) - 1

            self.display_tree(child_node, child_label, child_prefix, last_child)

    def display(self, title="RED-BLACK TREE", show_traversals=False):
        if self.root == self.NIL:
            print(f"\n[{title}] Tree is empty.")
            return

        print(f"\n========== {title} ==========")
        print("ROOT / LEFT / RIGHT with node colors")
        print("====================================")

        self.display_tree(self.root)

        # Show Preorder, Inorder, and Postorder traversals only when requested (e.g., Option 4)
        if show_traversals:
            pre_result = []
            self.preorder(self.root, pre_result)
            print("\nPreorder Traversal:")
            print(" -> ".join(pre_result))

            in_result = []
            self.inorder(self.root, in_result)
            print("\nInorder Traversal:")
            print(" -> ".join(in_result))

            post_result = []
            self.postorder(self.root, post_result)
            print("\nPostorder Traversal:")
            print(" -> ".join(post_result))


# ---------------- MENU-DRIVEN PROGRAM ----------------


def read_integer_list(prompt="Enter elements separated by spaces or commas: "):
    while True:
        values = input(prompt).strip()

        if not values:
            return []

        try:
            return [int(value) for value in values.replace(",", " ").split()]
        except ValueError:
            print("Invalid input! Please enter integers only.")


def main():
    tree = RedBlackTree()

    while True:
        print("\n========== RED-BLACK TREE MENU ==========")
        print("1. Creation")
        print("2. Insertion")
        print("3. Deletion")
        print("4. Display")
        print("5. Exit")
        print("=========================================")

        choice = input("Enter your choice: ").strip()

        # 1. Creation
        if choice == "1":
            tree.clear()
            values = read_integer_list(
                "Enter initial elements separated by spaces or commas: "
            )

            if not values:
                print("No elements provided. Tree is empty.")
            else:
                for value in values:
                    print(f"\n--- Inserting Node: {value} ---")
                    if tree.insert(value):
                        print(f"Node {value} inserted successfully.")
                        tree.display(f"TREE AFTER INSERTING {value}")
                    else:
                        print(f"Duplicate value {value} skipped.")

                print("\nRed-Black Tree creation complete.")

        # 2. Insertion
        elif choice == "2":
            values = read_integer_list(
                "Enter value(s) to insert separated by spaces or commas: "
            )

            if not values:
                print("No values entered.")
                continue

            for key in values:
                print(f"\n--- Inserting Node: {key} ---")
                if tree.insert(key):
                    print(f"Node {key} inserted successfully.")
                    tree.display(f"TREE AFTER INSERTING {key}")
                else:
                    print(f"Duplicate value {key}! Insertion not allowed.")

        # 3. Deletion
        elif choice == "3":
            if tree.root == tree.NIL:
                print("\nTree is empty! Cannot perform deletion.")
                continue

            values = read_integer_list(
                "Enter value(s) to delete separated by spaces or commas: "
            )

            if not values:
                print("No values entered.")
                continue

            for key in values:
                print(f"\n--- Deleting Node: {key} ---")
                if tree.delete(key):
                    print(f"Node {key} deleted successfully.")
                    print("Red-Black Tree properties restored.")
                    tree.display(f"TREE AFTER DELETING {key}")
                else:
                    print(f"Node {key} not found in the tree.")

        # 4. Display
        elif choice == "4":
            tree.display(show_traversals=True)

        # 5. Exit
        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid choice! Please select 1 to 5.")


if __name__ == "__main__":
    main()
