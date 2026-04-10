from seed_common import make_problem, register_detailed, sample


register_detailed(
    make_problem(
        "azcp_p021",
        "Warehouse Lanes",
        """
        A lane has n containers with weights a_1 ... a_n.
        A segment is stable if the difference between its maximum and minimum weight is at most d.
        Find the maximum length of a stable contiguous segment.
        """,
        "First line: n d\nSecond line: n integers a_1 ... a_n",
        "Output one integer: the maximum stable segment length.",
        """
        1 <= n <= 2 * 10^5
        0 <= d <= 10^9
        0 <= a_i <= 10^9
        """,
        [sample("7 3\n4 2 5 6 3 3 8", "5")],
        ["sliding_window", "deque"],
        1400,
    ),
    ["PLAN_ONLY"],
    "Maintain window min and max with two monotonic deques.",
)

register_detailed(
    make_problem(
        "azcp_p022",
        "Shipment Split",
        """
        There are n package weights in fixed order. You must split them into at most k contiguous shipments.
        The load of a shipment is the sum of weights inside it.
        Minimize the maximum shipment load.
        """,
        "First line: n k\nSecond line: n positive integers",
        "Output one integer: the minimum possible maximum shipment load.",
        """
        1 <= n <= 2 * 10^5
        1 <= k <= n
        1 <= a_i <= 10^9
        """,
        [sample("5 2\n7 2 5 10 8", "18")],
        ["binary_search_answer", "greedy"],
        1500,
    ),
    ["PLAN_ONLY"],
    "Binary-search the answer and greedily count needed segments.",
)

register_detailed(
    make_problem(
        "azcp_p023",
        "Mirror Prefix Search",
        """
        Given a pattern p and a text t, output all starting positions where p occurs in t.
        Positions are 1-indexed.
        """,
        "First line: p\nSecond line: t",
        "First output c, then on the next line output all occurrence positions in increasing order.",
        """
        1 <= |p|, |t| <= 2 * 10^5
        Both strings consist of lowercase English letters.
        """,
        [sample("aba\nabacaba", "2\n1 5")],
        ["strings", "z_algorithm"],
        1300,
    ),
    ["PLAN_ONLY"],
    "Use Z on p + '#' + t and read off exact matches.",
)

register_detailed(
    make_problem(
        "azcp_p024",
        "Residue Triples",
        """
        You are given n integers and a modulus m.
        Count the number of triples (i, j, k) with i < j < k such that
        (a_i + a_j + a_k) mod m = 0.
        """,
        "First line: n m\nSecond line: n integers a_1 ... a_n",
        "Output one integer: the number of valid triples.",
        """
        3 <= n <= 2 * 10^5
        1 <= m <= 200
        -10^9 <= a_i <= 10^9
        """,
        [sample("6 5\n1 4 2 3 5 0", "4")],
        ["combinatorics", "modular_arithmetic"],
        1700,
    ),
    ["PLAN_ONLY"],
    "Compress by residues, then count valid residue triples with combinations.",
)

register_detailed(
    make_problem(
        "azcp_p025",
        "Fire Stations",
        """
        You are given an n x m city map with '.' empty roads, '#' blocked cells, and 'F' fire stations.
        For each non-blocked cell, compute the distance to the nearest fire station using 4-direction moves.
        Distances for blocked cells should remain -1.
        """,
        "First line: n m\nNext n lines: the grid",
        "Output an n x m matrix of integers.",
        """
        1 <= n, m <= 1000
        There is at least one fire station.
        """,
        [sample("3 4\nF..#\n....\n#..F", "0 1 2 -1\n1 2 2 1\n-1 2 1 0")],
        ["bfs", "graphs"],
        1100,
    ),
    ["PLAN_ONLY"],
    "Push all sources at distance 0 and run one multi-source BFS.",
)

register_detailed(
    make_problem(
        "azcp_p026",
        "Ancestor Budget",
        """
        The tree is rooted at node 1. Node i has a positive cost c_i.
        Choose a connected set of nodes that must contain the root.
        The total cost of chosen nodes must not exceed B.
        Maximize the number of chosen nodes.
        """,
        "First line: n B\nSecond line: c_1 ... c_n\nNext n-1 lines: u v",
        "Output one integer: the maximum number of chosen nodes.",
        """
        1 <= n <= 200
        1 <= B <= 5000
        1 <= c_i <= B
        """,
        [sample("5 7\n2 2 3 2 1\n1 2\n1 3\n3 4\n3 5", "3")],
        ["trees", "subtree_dp", "knapsack"],
        1900,
    ),
    ["PLAN_ONLY"],
    "Tree knapsack DP merges child tables while enforcing connectivity to the root.",
)

register_detailed(
    make_problem(
        "azcp_p027",
        "Broken Network",
        """
        There is an undirected graph with n vertices and m initial edges.
        Then q operations follow:
        - remove u v : delete that edge from the graph
        - ask u v : answer whether u and v are connected at that moment
        Every removed edge is guaranteed to exist when removed.
        """,
        "First line: n m q\nNext m lines: initial edges u v\nNext q lines: operations",
        "For every ask operation, output YES or NO.",
        """
        1 <= n, m, q <= 2 * 10^5
        1 <= u, v <= n
        """,
        [sample("4 3 4\n1 2\n2 3\n3 4\nask 1 4\nremove 2 3\nask 1 4\nask 3 4", "YES\nNO\nYES")],
        ["dsu", "graphs"],
        1900,
    ),
    ["PLAN_ONLY"],
    "Process deletions offline in reverse so DSU only ever adds edges.",
)

register_detailed(
    make_problem(
        "azcp_p028",
        "Festival Squares",
        """
        You are given an n x m grid of non-negative values and an integer K.
        Find the largest side length L such that there exists an L x L square whose sum is at most K.
        """,
        "First line: n m K\nNext n lines: m non-negative integers each",
        "Output one integer: the maximum valid side length.",
        """
        1 <= n, m <= 1000
        0 <= grid[i][j] <= 10^9
        0 <= K <= 10^18
        """,
        [sample("3 4 8\n1 2 1 3\n2 1 2 2\n1 1 1 1", "2")],
        ["prefix_sums", "binary_search_answer", "dp_2d"],
        1600,
    ),
    ["PLAN_ONLY"],
    "Use 2D prefix sums for O(1) square sums and binary-search the side length.",
)

register_detailed(
    make_problem(
        "azcp_p029",
        "Echo Equality",
        """
        You are given a string s and q queries.
        Each query contains l_1, r_1, l_2, r_2.
        Determine whether substring s[l_1..r_1] is equal to substring s[l_2..r_2].
        """,
        "First line: s\nSecond line: q\nNext q lines: l_1 r_1 l_2 r_2",
        "For every query, output YES or NO.",
        """
        1 <= |s|, q <= 2 * 10^5
        1 <= l_1 <= r_1 <= |s|
        1 <= l_2 <= r_2 <= |s|
        """,
        [sample("abacaba\n3\n1 3 5 7\n2 4 4 6\n1 4 1 4", "YES\nNO\nYES")],
        ["hashing", "strings"],
        1500,
    ),
    ["PLAN_ONLY"],
    "Polynomial rolling hashes answer substring-equality queries in O(1).",
)

register_detailed(
    make_problem(
        "azcp_p030",
        "Directed Routes",
        """
        You are given a directed acyclic graph with weighted edges.
        Find the maximum total weight of a path from vertex 1 to vertex n.
        If no path exists, output -1.
        """,
        "First line: n m\nNext m lines: u v w",
        "Output one integer: the maximum path weight from 1 to n, or -1.",
        """
        1 <= n, m <= 2 * 10^5
        1 <= u, v <= n
        -10^9 <= w <= 10^9
        The graph is guaranteed to be acyclic.
        """,
        [sample("5 5\n1 2 4\n1 3 1\n2 4 3\n3 4 5\n4 5 2", "8")],
        ["topo_sort", "graphs", "dp_1d"],
        1400,
    ),
    ["PLAN_ONLY"],
    "Topological order lets longest-path DP run in linear time on a DAG.",
)
