from seed_common import make_problem, register_detailed, sample


register_detailed(
    make_problem(
        "azcp_p001",
        "Alternating Toll",
        """
        A road has n toll sensors numbered from 1 to n. Sensor i contributes value a_i.
        For a query [l, r], define the toll balance as:
        a_l - a_{l+1} + a_{l+2} - a_{l+3} + ...
        where the sign always starts with plus at position l.
        Answer q independent queries.
        """,
        """
        First line: n q
        Second line: n integers a_1 ... a_n
        Next q lines: l r
        """,
        "For each query, output the toll balance of segment [l, r].",
        """
        1 <= n, q <= 2 * 10^5
        -10^9 <= a_i <= 10^9
        1 <= l <= r <= n
        """,
        [sample("5 3\n5 2 7 1 4\n1 5\n2 4\n3 3", "13\n-4\n7")],
        ["arrays", "prefix_sums"],
        900,
    ),
    ["SFT_SOLVE", "REPAIR", "OPTIMIZE"],
    "Prefix-transform alternating range sums into O(1) queries.",
)

register_detailed(
    make_problem(
        "azcp_p002",
        "Balanced Pairing",
        """
        There are n players with skill values s_1 ... s_n, and n is even.
        You must split them into n/2 pairs.
        The cost of a pair is the absolute difference of the two skills.
        Minimize the maximum pair cost over all chosen pairs.
        """,
        "First line: n\nSecond line: n integers s_1 ... s_n",
        "Output one integer: the minimum possible value of the maximum pair cost.",
        """
        2 <= n <= 2 * 10^5
        n is even
        0 <= s_i <= 10^9
        """,
        [sample("6\n9 1 3 8 12 13", "2")],
        ["sorting", "greedy"],
        1000,
    ),
    ["SFT_SOLVE", "OPTIMIZE"],
    "Sort and pair adjacent values to minimize the worst gap.",
)

register_detailed(
    make_problem(
        "azcp_p003",
        "Rain Schedule",
        """
        There are n dry fields arranged in a line, initially all with water level 0.
        You are given q rain operations. Operation (l, r, x) adds x units of water
        to every field from l to r inclusive.
        Output the final water level of every field.
        """,
        "First line: n q\nNext q lines: l r x",
        "Output n integers: the final water levels of fields 1..n.",
        """
        1 <= n, q <= 2 * 10^5
        1 <= l <= r <= n
        1 <= x <= 10^9
        """,
        [sample("5 3\n1 3 2\n2 5 1\n4 4 7", "2 3 3 8 1")],
        ["difference_array", "prefix_sums"],
        900,
    ),
    ["SFT_SOLVE", "REPAIR", "OPTIMIZE"],
    "Range updates collapse to boundary markers plus one prefix pass.",
)

register_detailed(
    make_problem(
        "azcp_p004",
        "Budgeted Sprint",
        """
        A runner has energy costs a_1 ... a_n for consecutive track segments.
        All costs are positive.
        The runner wants a contiguous segment whose total cost is at most k.
        Find the maximum possible length of such a segment.
        """,
        "First line: n k\nSecond line: n positive integers a_1 ... a_n",
        "Output one integer: the maximum valid segment length.",
        """
        1 <= n <= 2 * 10^5
        1 <= k <= 10^18
        1 <= a_i <= 10^9
        """,
        [sample("7 8\n2 1 3 2 4 1 1", "4")],
        ["two_pointers", "sliding_window"],
        1100,
    ),
    ["SFT_SOLVE", "REPAIR", "OPTIMIZE"],
    "Positive costs let a two-pointer window move monotonically.",
)

register_detailed(
    make_problem(
        "azcp_p005",
        "Median Upgrade",
        """
        You are given an array of odd length n and an integer k.
        In one move you may increase any array element by 1.
        You may use at most k moves in total.
        Maximize the median of the array after all moves.
        """,
        "First line: n k\nSecond line: n integers a_1 ... a_n",
        "Output one integer: the maximum possible median.",
        """
        1 <= n <= 2 * 10^5
        n is odd
        0 <= k <= 10^18
        0 <= a_i <= 10^9
        """,
        [sample("5 7\n1 2 5 6 6", "8")],
        ["sorting", "binary_search_answer"],
        1600,
    ),
    ["SFT_SOLVE", "REPAIR"],
    "Only the upper half matters; binary-search the achievable median.",
)

register_detailed(
    make_problem(
        "azcp_p006",
        "Previous Higher Beacon",
        """
        A sequence of towers has heights h_1 ... h_n.
        For every position i, output the nearest index j < i such that h_j > h_i.
        If no such index exists, output 0.
        """,
        "First line: n\nSecond line: n integers h_1 ... h_n",
        "Output n integers. The i-th integer is the answer for position i.",
        """
        1 <= n <= 2 * 10^5
        0 <= h_i <= 10^9
        """,
        [sample("7\n6 2 5 4 5 1 7", "0 1 1 3 1 5 0")],
        ["monotonic_stack", "arrays"],
        1100,
    ),
    ["SFT_SOLVE", "REPAIR", "OPTIMIZE"],
    "Maintain a decreasing stack of candidate previous-greater positions.",
)

register_detailed(
    make_problem(
        "azcp_p007",
        "Window Champion",
        """
        Given an array a_1 ... a_n and an integer k, output the maximum value
        in every contiguous window of length k.
        """,
        "First line: n k\nSecond line: n integers a_1 ... a_n",
        "Output n-k+1 integers: the maximum in each window from left to right.",
        """
        1 <= k <= n <= 2 * 10^5
        -10^9 <= a_i <= 10^9
        """,
        [sample("8 3\n1 3 -1 -3 5 3 6 7", "3 3 5 5 6 7")],
        ["deque", "sliding_window"],
        1300,
    ),
    ["SFT_SOLVE", "REPAIR", "OPTIMIZE"],
    "A monotonic deque keeps the maximum candidate for each window in O(n).",
)

register_detailed(
    make_problem(
        "azcp_p008",
        "Hall Reservations",
        """
        There are n meetings. Meeting i occupies the half-open interval [l_i, r_i),
        so a hall used by one meeting becomes available exactly at time r_i.
        Find the minimum number of halls required to host all meetings.
        """,
        "First line: n\nNext n lines: l_i r_i",
        "Output one integer: the minimum number of halls.",
        """
        1 <= n <= 2 * 10^5
        0 <= l_i < r_i <= 10^9
        """,
        [sample("4\n1 4\n2 3\n4 6\n5 7", "2")],
        ["intervals", "greedy", "sorting"],
        1200,
    ),
    ["SFT_SOLVE", "REPAIR", "OPTIMIZE"],
    "Sort starts and ends separately, and sweep current overlap count.",
)

register_detailed(
    make_problem(
        "azcp_p009",
        "Signal Maze",
        """
        You are given an n x m grid containing:
        '.' for an open cell, '#' for a wall, 'S' for the start, and 'T' for the target.
        In one move you may go up, down, left, or right to another open cell.
        Find the minimum number of moves from S to T, or output -1 if impossible.
        """,
        "First line: n m\nNext n lines: the grid",
        "Output one integer: the shortest path length, or -1.",
        """
        1 <= n, m <= 1000
        There is exactly one S and exactly one T.
        """,
        [sample("4 5\nS..#.\n.#.#.\n.#..T\n.....", "7")],
        ["bfs", "graphs"],
        1200,
    ),
    ["SFT_SOLVE", "REPAIR"],
    "Unweighted grid shortest path is plain BFS.",
)

register_detailed(
    make_problem(
        "azcp_p010",
        "Semester Signals",
        """
        There are n courses and m prerequisite relations u -> v, meaning course u
        must be completed before course v.
        In one semester you may take any number of courses whose prerequisites are already completed.
        Find the minimum number of semesters needed to finish all courses.
        If the prerequisite graph contains a cycle, output -1.
        """,
        "First line: n m\nNext m lines: u v",
        "Output one integer: the minimum number of semesters, or -1 if impossible.",
        """
        1 <= n, m <= 2 * 10^5
        1 <= u, v <= n
        """,
        [sample("5 4\n1 3\n2 3\n3 4\n3 5", "3")],
        ["topo_sort", "graphs"],
        1500,
    ),
    ["SFT_SOLVE", "REPAIR"],
    "Topological order plus longest-path depth in a DAG gives semester count.",
)
