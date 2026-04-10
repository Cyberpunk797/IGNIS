from seed_common import PLAN_ONLY_ENTRIES, build_entry, plan_only_response


PLAN_ONLY_ENTRIES.extend(
    [
        build_entry(
            "azcp_p021",
            "PLAN_ONLY",
            plan_only_response(
                "Maintain the current window's minimum and maximum with two deques while expanding the right pointer.",
                [
                    "Use one deque increasing by value for minima and one decreasing for maxima.",
                    "Extend the right endpoint and update both deques.",
                    "While max-min > d, move the left endpoint right and discard expired indices.",
                    "Track the best window length.",
                ],
                ["two monotonic deques", "two pointers"],
                [
                    "The min deque front is always the minimum in the window; the max deque front is always the maximum.",
                    "A window is stable exactly when those two front values differ by at most d.",
                ],
                ["d = 0", "all values equal", "strictly increasing array"],
                "O(n)",
                "O(n)",
            ),
            "gold",
            0.92,
        ),
        build_entry(
            "azcp_p022",
            "PLAN_ONLY",
            plan_only_response(
                "Binary-search the answer M = allowed maximum shipment load, and greedily count how many contiguous groups are needed if no group may exceed M.",
                [
                    "Search M between max(a_i) and sum(a_i).",
                    "For a fixed M, scan left to right, starting a new shipment whenever adding the next package would exceed M.",
                    "If the greedy scan uses at most k groups, M is feasible.",
                ],
                ["array", "binary search"],
                [
                    "For a fixed maximum load M, the greedy grouping uses the minimum possible number of segments because it delays every cut as much as possible.",
                    "Feasibility is monotone: if M works, any larger value also works.",
                ],
                ["k = 1", "k = n", "one very heavy package"],
                "O(n log(sum a_i))",
                "O(1) extra",
            ),
            "gold",
            0.91,
        ),
        build_entry(
            "azcp_p023",
            "PLAN_ONLY",
            plan_only_response(
                "Form the string p + '#' + t and compute its Z-array. A match starts wherever the Z-value reaches |p| inside the text part.",
                [
                    "Concatenate pattern, separator, and text.",
                    "Compute the Z-array in linear time.",
                    "For each text position, if Z there is at least |p|, record the corresponding 1-indexed start.",
                ],
                ["string", "vector<int> z"],
                [
                    "Z[i] is the longest prefix length matching the suffix starting at i.",
                    "Therefore Z[i] >= |p| exactly when the pattern matches at that shifted text position.",
                ],
                ["no occurrences", "pattern longer than text", "overlapping occurrences"],
                "O(|p| + |t|)",
                "O(|p| + |t|)",
            ),
            "gold",
            0.90,
        ),
        build_entry(
            "azcp_p024",
            "PLAN_ONLY",
            plan_only_response(
                "Count how many numbers fall into each residue class modulo m, then enumerate residue triples whose sum is 0 mod m and multiply by the corresponding combination counts.",
                [
                    "Normalize every value to a residue in [0, m-1] and build freq[r].",
                    "Enumerate residue choices r1 <= r2 <= r3 with (r1+r2+r3) mod m = 0.",
                    "For each pattern, add the right combinatorial term based on how many residues are equal.",
                ],
                ["frequency array of size m"],
                [
                    "Only residue classes matter for divisibility by m.",
                    "Once the residue multiset is fixed, the number of index triples depends only on how many residues are equal.",
                ],
                ["negative input values", "m = 1", "some residue classes empty"],
                "O(m^3 + n)",
                "O(m)",
            ),
            "gold",
            0.92,
        ),
        build_entry(
            "azcp_p025",
            "PLAN_ONLY",
            plan_only_response(
                "Treat every fire station as a BFS source with distance 0 and propagate outward once.",
                [
                    "Initialize the answer matrix with -1 for blocked cells and INF for open cells.",
                    "Push all fire-station cells into the queue with distance 0.",
                    "Run BFS in four directions and relax neighbors the first time they are seen.",
                ],
                ["queue", "2D distance array"],
                [
                    "Multi-source BFS processes all cells in order of distance from the nearest source.",
                    "The first assigned distance to a cell is therefore its minimum distance to any station.",
                ],
                ["multiple stations adjacent to the same cell", "blocked cells", "single station"],
                "O(nm)",
                "O(nm)",
            ),
            "gold",
            0.90,
        ),
        build_entry(
            "azcp_p026",
            "PLAN_ONLY",
            plan_only_response(
                "Use subtree knapsack DP. For each node, dp_u[c] stores the maximum number of chosen nodes in u's subtree with total cost c, under the condition that the chosen set is connected and contains u.",
                [
                    "Root the tree at 1.",
                    "Initialize dp_u[c_u] = 1 for each node u, and impossible elsewhere.",
                    "Merge each child v into u with a knapsack convolution over budgets.",
                    "The final answer is max dp_root[c] for c <= B.",
                ],
                ["tree adjacency list", "DP tables by subtree and budget"],
                [
                    "Connectivity is preserved because child states are only merged into a parent state that already includes the parent.",
                    "Every feasible connected rooted selection appears in exactly one merge outcome.",
                ],
                ["budget smaller than c_1", "leaf nodes", "many children competing for the same budget"],
                "O(n * B^2) in the straightforward implementation",
                "O(n * B)",
            ),
            "gold",
            0.92,
        ),
        build_entry(
            "azcp_p027",
            "PLAN_ONLY",
            plan_only_response(
                "Dynamic deletions are hard online for DSU, so process operations in reverse where removals become insertions.",
                [
                    "Mark every edge that will eventually be removed.",
                    "Build a DSU with only the edges that survive all forward operations.",
                    "Process operations backward: reverse ask as ask, reverse remove as add edge.",
                    "Record answers in reverse order and reverse them at the end.",
                ],
                ["DSU", "hash set of removed edges", "operation list"],
                [
                    "When running backward, the DSU state matches exactly the graph state after the corresponding prefix of reversed operations.",
                    "Because DSU supports insertions but not deletions, reversing time makes the data structure compatible with the operation sequence.",
                ],
                ["same edge removed only once", "queries before any removal", "disconnected initial graph"],
                "O((n + m + q) * alpha(n))",
                "O(n + m + q)",
            ),
            "gold",
            0.93,
        ),
        build_entry(
            "azcp_p028",
            "PLAN_ONLY",
            plan_only_response(
                "Use a 2D prefix sum to query any square sum in O(1), then binary-search the side length.",
                [
                    "Build the 2D prefix-sum matrix.",
                    "Binary-search a candidate side length L.",
                    "For each top-left corner, query the L x L sum in O(1); if any is <= K, L is feasible.",
                ],
                ["2D prefix sums", "binary search"],
                [
                    "2D prefix sums return the exact sum of any axis-aligned square by inclusion-exclusion.",
                    "If a side length L is feasible, every smaller side length is also feasible because all grid values are non-negative.",
                ],
                ["K = 0", "L = 1 only", "entire grid feasible"],
                "O(nm log(min(n, m)))",
                "O(nm)",
            ),
            "gold",
            0.91,
        ),
        build_entry(
            "azcp_p029",
            "PLAN_ONLY",
            plan_only_response(
                "Precompute polynomial rolling hashes and powers. Then every substring hash is O(1), so substring-equality queries become hash comparisons.",
                [
                    "Build prefix hashes and base powers for the string.",
                    "Define a function that returns the normalized hash of any substring.",
                    "For each query, if the substring lengths differ answer NO; otherwise compare their hashes.",
                ],
                ["prefix hash arrays", "power array"],
                [
                    "Prefix hashes allow any substring hash to be isolated by subtraction and scaling.",
                    "Equal-length substrings with equal normalized hashes are treated as equal under the chosen hash scheme.",
                ],
                ["different substring lengths", "many repeated characters", "very large q"],
                "O(|s| + q)",
                "O(|s|)",
            ),
            "gold",
            0.90,
        ),
        build_entry(
            "azcp_p030",
            "PLAN_ONLY",
            plan_only_response(
                "Since the graph is a DAG, process vertices in topological order and do longest-path DP from node 1.",
                [
                    "Compute a topological ordering of the DAG.",
                    "Initialize dp[1] = 0 and all other states to negative infinity.",
                    "Traverse vertices in topological order and relax outgoing edges.",
                    "If dp[n] stays unreachable, answer -1.",
                ],
                ["topological order array", "DP array"],
                [
                    "Every edge goes from an earlier topological position to a later one, so when processing u, dp[u] is already final.",
                    "Relaxing outgoing edges considers every directed path exactly in dependency order.",
                ],
                ["negative edge weights", "node n unreachable", "multiple optimal paths"],
                "O(n + m)",
                "O(n + m)",
            ),
            "gold",
            0.91,
        ),
    ]
)
