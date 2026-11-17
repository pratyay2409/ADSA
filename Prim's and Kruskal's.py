import heapq


def kruskal_mst(V, edges):
  if V == -2 or any(u < 0 or v < 0 for u, v, w in edges):
    return None, [], -2
  if V <= 0 or len(edges) == 0:
    return None, [], -1

  parent = {}

  def find(i):
    parent.setdefault(i, i)
    if parent[i] != i:
      parent[i] = find(parent[i])
    return parent[i]

  mst = []
  total_weight = 0

  for u, v, w in sorted(edges, key=lambda x: x[2]):
    ru, rv = find(u), find(v)
    if ru != rv:
      parent[ru] = rv
      mst.append((u, v, w))
      total_weight += w
      if len(mst) == V - 1:
        break

  return total_weight, mst, 0


def prim_mst(V, edges):
  if V == -2 or any(u < 0 or v < 0 for u, v, w in edges):
    return None, [], -2
  if V <= 0 or len(edges) == 0:
    return None, [], -1

  adj = {}
  for u, v, w in edges:
    adj.setdefault(u, []).append((w, u, v))
    adj.setdefault(v, []).append((w, v, u))

  start = edges[0][0]
  visited = {start}
  pq = list(adj[start])
  heapq.heapify(pq)

  mst = []
  total_weight = 0

  while pq and len(visited) < V:
    w, u, v = heapq.heappop(pq)
    if v not in visited:
      visited.add(v)
      mst.append((u, v, w))
      total_weight += w
      for next_edge in adj[v]:
        if next_edge[2] not in visited:
          heapq.heappush(pq, next_edge)

  return total_weight, mst, 0


def display_result(name, V, weight, mst, err):
  if err == -1:
    print(f"\n[{name}] Error: -1 (Cannot form MST: Vertices or Edges are 0)")
    return
  if err == -2:
    print(f"\n[{name}] Error: Negative vertices or edge counts are not allowed!")
    return

  print(f"\n[{name}]")
  print(f"  Selected Edges : {mst}")
  if len(mst) < V - 1:
    print(
        f"  Status         : Disconnected Graph (Only {len(mst)}/{V - 1} edges"
        " formed)"
    )
    print(f"  Partial Weight : {weight} (Full MST not possible -> -1)")
  else:
    print(f"  Total MST Cost : {weight}")


def input_graph():
  try:
    V = int(input("\nEnter number of vertices (V): "))
    E = int(input("Enter number of edges (E): "))
  except ValueError:
    print("Error: Invalid input! Please enter integer values.")
    return 0, []

  if V < 0 or E < 0:
    print("Error: Number of vertices and edges cannot be negative!")
    return -2, []
  if V == 0 or E == 0:
    print("Error: -1 (Cannot form MST when vertices or edges are 0)")
    return 0, []

  edges = []
  print("Enter each edge as: u v weight (supports positive & negative weights)")
  for i in range(E):
    try:
      u, v, w = map(int, input(f"  Edge {i + 1}: ").split())
    except ValueError:
      print("Error: Invalid format! Enter three integers: u v weight.")
      return 0, []

    if u < 0 or v < 0:
      print("Error: Vertex numbers cannot be negative!")
      return -2, [(u, v, w)]

    edges.append((u, v, w))
  return V, edges


def main():
  V, edges = None, []

  while True:
    print("\n========= PRIM'S & KRUSKAL'S MST MENU =========")
    print("1. Enter Graph (Vertices & Edges)")
    print("2. Find MST using Kruskal's Algorithm")
    print("3. Find MST using Prim's Algorithm")
    print("4. Compare Both (Kruskal's vs Prim's)")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ").strip()

    if choice == "1":
      V, edges = input_graph()

    elif choice in ("2", "3", "4"):
      if V is None:
        V, edges = input_graph()

      k_weight, k_mst, k_err = (None, [], 0)
      p_weight, p_mst, p_err = (None, [], 0)

      if choice in ("2", "4"):
        k_weight, k_mst, k_err = kruskal_mst(V, edges)
        display_result("Kruskal's Algorithm", V, k_weight, k_mst, k_err)

      if choice in ("3", "4"):
        p_weight, p_mst, p_err = prim_mst(V, edges)
        display_result("Prim's Algorithm", V, p_weight, p_mst, p_err)

      if choice == "4" and k_err == 0 and p_err == 0:
        if k_weight != p_weight:
          print(
              f"\nNote: Different weights (Kruskal={k_weight} vs"
              f" Prim={p_weight}) because the graph is disconnected."
          )
          print(
              "      Kruskal spans all components (forest), while Prim only"
              " spans the starting component."
          )
        elif {tuple(sorted((u, v)) + [w]) for u, v, w in k_mst} != {
            tuple(sorted((u, v)) + [w]) for u, v, w in p_mst
        }:
          print(
              "\nNote: Both gave the same minimum cost, but picked different"
              " edges due to equal edge weights."
          )

    elif choice == "5":
      print("Exiting program.")
      break
    else:
      print("Invalid choice! Please select 1-5.")


if __name__ == "__main__":
  main()
