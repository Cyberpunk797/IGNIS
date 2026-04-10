from seed_common import make_problem, register_detailed, sample


register_detailed(
    make_problem(
        "azcp_p011",
        "Cut Value Tree",
        """
        You are given a tree with n vertices.
        If you remove one edge, the tree splits into two connected components of sizes x and n-x.
        The value of that cut is x * (n - x).
        Find the maximum possible cut value over all edges.
        """,
        "First line: n\nNext n-1 lines: u v",
        "Output one integer: the maximum cut value.",
        """
        2 <= n <= 2 * 10^5
        1 <= u, v <= n
        """,
        [sample("5\n1 2\n1 3\n3 4\n3 5", "6")],
        ["trees", "dfs", "subtree_dp"],
        1300,
    ),
    ["SFT_SOLVE", "OPTIMIZE"],
    "One subtree-size pass evaluates every edge cut in O(n).",
)

register_detailed(
    make_problem(
        "azcp_p012",
        "Alliance Desk",
        """
        There are n players, initially each in their own alliance.
        Process q operations:
        - union a b : merge the alliances containing a and b
        - size x : output the size of the alliance containing x
        """,
        'First line: n q\nNext q lines: either "union a b" or "size x"',
        "For every size query, output one integer.",
        """
        1 <= n, q <= 2 * 10^5
        1 <= a, b, x <= n
        """,
        [sample("5 6\nsize 1\nunion 1 2\nsize 2\nunion 2 3\nunion 4 5\nsize 1", "1\n2\n3")],
        ["dsu", "graphs"],
        1000,
    ),
    ["SFT_SOLVE"],
    "Classic DSU with union by size and path compression.",
)

register_detailed(
    make_problem(
        "azcp_p013",
        "Courier Paths",
        """
        You are given an undirected weighted graph with n vertices and m edges.
        Find the length of the shortest path from vertex 1 to vertex n.
        If there is no path, output -1.
        """,
        "First line: n m\nNext m lines: u v w",
        "Output one integer: the shortest path length from 1 to n, or -1.",
        """
        1 <= n, m <= 2 * 10^5
        1 <= u, v <= n
        1 <= w <= 10^9
        """,
        [sample("5 6\n1 2 4\n1 3 2\n3 2 1\n2 5 3\n3 4 7\n4 5 1", "6")],
        ["shortest_paths", "graphs"],
        1400,
    ),
    ["SFT_SOLVE", "REPAIR", "OPTIMIZE"],
    "Non-negative edges make Dijkstra the right shortest-path tool.",
)

register_detailed(
    make_problem(
        "azcp_p014",
        "Score Ledger",
        """
        An array of n scores is initially all zero.
        Process q operations:
        - add i x : add x to position i
        - sum l r : output the sum of positions l through r
        """,
        'First line: n q\nNext q lines: either "add i x" or "sum l r"',
        "For every sum query, output one integer.",
        """
        1 <= n, q <= 2 * 10^5
        1 <= i <= n
        1 <= l <= r <= n
        -10^9 <= x <= 10^9
        """,
        [sample("5 6\nadd 2 4\nadd 5 7\nsum 1 5\nadd 2 -1\nsum 2 4\nsum 5 5", "11\n3\n7")],
        ["fenwick", "prefix_sums"],
        1500,
    ),
    ["SFT_SOLVE", "OPTIMIZE"],
    "Fenwick tree supports point updates and prefix sums in O(log n).",
)

register_detailed(
    make_problem(
        "azcp_p015",
        "Peak Board",
        """
        An array of n integers is initially given.
        Process q operations:
        - set i x : assign a_i = x
        - max l r : output the maximum value on segment [l, r]
        """,
        'First line: n q\nSecond line: n integers\nNext q lines: either "set i x" or "max l r"',
        "For every max query, output one integer.",
        """
        1 <= n, q <= 2 * 10^5
        1 <= i <= n
        1 <= l <= r <= n
        -10^9 <= a_i, x <= 10^9
        """,
        [sample("5 4\n1 7 3 2 6\nmax 2 5\nset 4 9\nmax 1 4\nmax 4 4", "7\n9\n9")],
        ["segment_tree", "arrays"],
        1600,
    ),
    ["SFT_SOLVE"],
    "A point-update/range-max segment tree is the clean baseline.",
)

register_detailed(
    make_problem(
        "azcp_p016",
        "Parcel Budget",
        """
        There are n parcels. Parcel i has weight w_i and value v_i.
        You may take each parcel at most once.
        Find the maximum total value of chosen parcels whose total weight is at most W.
        """,
        "First line: n W\nNext n lines: w_i v_i",
        "Output one integer: the maximum achievable total value.",
        """
        1 <= n <= 2000
        1 <= W <= 2 * 10^5
        1 <= w_i <= W
        1 <= v_i <= 10^9
        """,
        [sample("4 7\n3 4\n4 5\n2 3\n3 7", "12")],
        ["dp_1d", "knapsack"],
        1400,
    ),
    ["SFT_SOLVE"],
    "Descending 1D knapsack DP prevents reusing the same parcel twice.",
)

register_detailed(
    make_problem(
        "azcp_p017",
        "Blocked Orchard",
        """
        You are given an n x m grid with open cells '.' and blocked cells '#'.
        Starting at (1, 1), you may move only right or down.
        Count the number of ways to reach (n, m) without entering blocked cells.
        Output the answer modulo 1,000,000,007.
        """,
        "First line: n m\nNext n lines: the grid",
        "Output one integer: the number of valid paths modulo 1,000,000,007.",
        """
        1 <= n, m <= 2000
        The cell (1, 1) and (n, m) may be blocked.
        """,
        [sample("3 4\n....\n.#..\n...#", "0")],
        ["dp_2d", "modular_arithmetic"],
        1300,
    ),
    ["SFT_SOLVE"],
    "DP over grid cells accumulates paths from top and left only.",
)

register_detailed(
    make_problem(
        "azcp_p018",
        "Tower Parade",
        """
        There are n towers. Tower i has width w_i and height h_i.
        You want the longest sequence of distinct towers such that both width and height
        are strictly increasing from one chosen tower to the next.
        Output the maximum possible length.
        """,
        "First line: n\nNext n lines: w_i h_i",
        "Output one integer: the maximum chain length.",
        """
        1 <= n <= 2 * 10^5
        1 <= w_i, h_i <= 10^9
        """,
        [sample("5\n2 3\n3 4\n3 5\n4 6\n5 5", "3")],
        ["lis", "sorting"],
        1700,
    ),
    ["SFT_SOLVE"],
    "Sort by width, reverse equal-width heights, then run LIS on heights.",
)

register_detailed(
    make_problem(
        "azcp_p019",
        "Panel Switches",
        """
        There are m bulbs labeled 0 to m-1, initially all off.
        There are n switches. Switch i has a cost c_i and turns on a fixed subset of bulbs.
        Each switch may be used at most once, and once a bulb is on it stays on.
        Find the minimum total cost needed to turn on all bulbs, or output -1 if impossible.
        """,
        "First line: n m\nNext n lines: c_i t_i b_1 ... b_t",
        "Output one integer: the minimum total cost, or -1.",
        """
        1 <= n <= 20
        1 <= m <= 20
        1 <= c_i <= 10^9
        0 <= b_j < m
        """,
        [sample("3 3\n4 2 0 1\n3 2 1 2\n5 2 0 2", "7")],
        ["bitmask", "dp_1d"],
        1700,
    ),
    ["SFT_SOLVE"],
    "Bitmask DP over covered bulb sets gives the exact minimum.",
)

register_detailed(
    make_problem(
        "azcp_p020",
        "Border Echoes",
        """
        A border of a string is a non-empty proper prefix that is also a suffix.
        Given a string s, output all border lengths of s in increasing order.
        """,
        "First line: s",
        "First output k, then on the next line output the k border lengths in increasing order.",
        """
        1 <= |s| <= 2 * 10^5
        s consists of lowercase English letters.
        """,
        [sample("ababa", "2\n1 3")],
        ["strings", "kmp"],
        1500,
    ),
    ["SFT_SOLVE", "OPTIMIZE"],
    "The prefix-function chain enumerates all borders in linear time.",
)
