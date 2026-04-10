from seed_common import SFT_ENTRIES, build_entry, cpp, sft_response


SFT_ENTRIES.extend(
    [
        build_entry(
            "azcp_p011",
            "SFT_SOLVE",
            sft_response(
                "For an edge connecting a node's subtree to its parent, the cut sizes are exactly subtree_size and n-subtree_size.",
                [
                    "Root the tree at 1 and build a parent array plus traversal order.",
                    "Process nodes in reverse order to compute subtree sizes.",
                    "For every non-root node u, removing the edge to its parent creates parts of sizes sub[u] and n-sub[u].",
                    "Track the maximum product.",
                ],
                ["adjacency list", "parent array", "order array", "subtree size array"],
                [
                    "Every edge corresponds to exactly one child subtree in the rooted tree.",
                    "The subtree size of that child is one component size, and the rest of the tree is the other component.",
                ],
                ["n = 2", "star tree", "path tree"],
                "O(n)",
                "O(n)",
                "The problem only asks about component sizes after one cut, so subtree sizes are sufficient. No per-edge recomputation is needed.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n;
                        cin >> n;
                        vector<vector<int>> g(n + 1);
                        for (int i = 0; i < n - 1; i++) {
                            int u, v;
                            cin >> u >> v;
                            g[u].push_back(v);
                            g[v].push_back(u);
                        }

                        vector<int> parent(n + 1, 0), order;
                        stack<int> st;
                        st.push(1);
                        parent[1] = -1;
                        while (!st.empty()) {
                            int u = st.top();
                            st.pop();
                            order.push_back(u);
                            for (int v : g[u]) {
                                if (v == parent[u]) continue;
                                parent[v] = u;
                                st.push(v);
                            }
                        }

                        vector<long long> sub(n + 1, 1);
                        long long ans = 0;
                        for (int i = n - 1; i >= 0; i--) {
                            int u = order[i];
                            if (parent[u] > 0) {
                                ans = max(ans, sub[u] * (n - sub[u]));
                                sub[parent[u]] += sub[u];
                            }
                        }

                        cout << ans << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.94,
        ),
        build_entry(
            "azcp_p012",
            "SFT_SOLVE",
            sft_response(
                "Use a disjoint-set union structure with union by size and path compression.",
                [
                    "Initialize each node as its own parent with component size 1.",
                    "For union a b, merge the two roots if distinct.",
                    "For size x, find the root of x and print its component size.",
                ],
                ["DSU parent array", "DSU size array"],
                [
                    "Each set is represented by one root; size[root] stores the component size.",
                    "Path compression preserves correctness while making future finds faster.",
                ],
                ["repeated unions on same pair", "size query on isolated node", "deep merge chains"],
                "O(q * alpha(n))",
                "O(n)",
                "This is the standard DSU use case. The only dynamic information needed is component membership and root size.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    struct DSU {
                        vector<int> parent, sz;
                        explicit DSU(int n) : parent(n + 1), sz(n + 1, 1) {
                            iota(parent.begin(), parent.end(), 0);
                        }
                        int find(int x) {
                            if (parent[x] == x) return x;
                            return parent[x] = find(parent[x]);
                        }
                        void unite(int a, int b) {
                            a = find(a);
                            b = find(b);
                            if (a == b) return;
                            if (sz[a] < sz[b]) swap(a, b);
                            parent[b] = a;
                            sz[a] += sz[b];
                        }
                        int size_of(int x) {
                            return sz[find(x)];
                        }
                    };

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n, q;
                        cin >> n >> q;
                        DSU dsu(n);

                        while (q--) {
                            string op;
                            cin >> op;
                            if (op == "union") {
                                int a, b;
                                cin >> a >> b;
                                dsu.unite(a, b);
                            } else {
                                int x;
                                cin >> x;
                                cout << dsu.size_of(x) << "\\n";
                            }
                        }
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.93,
        ),
        build_entry(
            "azcp_p013",
            "SFT_SOLVE",
            sft_response(
                "All edge weights are non-negative, so Dijkstra from node 1 gives the shortest distances.",
                [
                    "Build the weighted adjacency list.",
                    "Initialize dist[1] = 0 and all others to INF.",
                    "Run Dijkstra with a min-priority queue.",
                    "Output dist[n], or -1 if it was never improved.",
                ],
                ["adjacency list", "priority_queue", "vector<long long> dist"],
                [
                    "Whenever a node is popped with its current best distance, that distance is final under non-negative weights.",
                    "Relaxing outgoing edges preserves shortest-known upper bounds on all nodes.",
                ],
                ["disconnected graph", "multiple edges", "large distance sums requiring long long"],
                "O((n + m) log n)",
                "O(n + m)",
                "The graph is sparse and weights are non-negative, so Dijkstra is the standard scalable choice.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n, m;
                        cin >> n >> m;
                        vector<vector<pair<int, long long>>> g(n + 1);
                        for (int i = 0; i < m; i++) {
                            int u, v;
                            long long w;
                            cin >> u >> v >> w;
                            g[u].push_back({v, w});
                            g[v].push_back({u, w});
                        }

                        const long long INF = (long long)4e18;
                        vector<long long> dist(n + 1, INF);
                        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
                        dist[1] = 0;
                        pq.push({0, 1});

                        while (!pq.empty()) {
                            auto [d, u] = pq.top();
                            pq.pop();
                            if (d != dist[u]) continue;
                            for (auto [v, w] : g[u]) {
                                if (dist[v] > d + w) {
                                    dist[v] = d + w;
                                    pq.push({dist[v], v});
                                }
                            }
                        }

                        cout << (dist[n] == INF ? -1 : dist[n]) << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.95,
        ),
        build_entry(
            "azcp_p014",
            "SFT_SOLVE",
            sft_response(
                "A Fenwick tree supports point additions and prefix sums, so a range sum is prefix(r) - prefix(l-1).",
                [
                    "Store the array implicitly inside a Fenwick tree.",
                    "For add i x, update Fenwick index i by x.",
                    "For sum l r, return prefix(r) - prefix(l-1).",
                ],
                ["Fenwick tree array"],
                [
                    "Fenwick nodes store disjoint suffixes of prefixes, so prefix sums decompose exactly into O(log n) nodes.",
                    "Point updates touch exactly the Fenwick nodes whose covered ranges include the updated index.",
                ],
                ["negative updates", "single-index range", "many operations"],
                "O(q log n)",
                "O(n)",
                "Fenwick is the minimal data structure here: easier than a segment tree and fast enough for large online updates plus queries.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    struct Fenwick {
                        int n;
                        vector<long long> bit;
                        explicit Fenwick(int n) : n(n), bit(n + 1, 0) {}
                        void add(int idx, long long delta) {
                            for (; idx <= n; idx += idx & -idx) bit[idx] += delta;
                        }
                        long long prefix(int idx) const {
                            long long res = 0;
                            for (; idx > 0; idx -= idx & -idx) res += bit[idx];
                            return res;
                        }
                    };

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n, q;
                        cin >> n >> q;
                        Fenwick fw(n);
                        while (q--) {
                            string op;
                            cin >> op;
                            if (op == "add") {
                                int idx;
                                long long x;
                                cin >> idx >> x;
                                fw.add(idx, x);
                            } else {
                                int l, r;
                                cin >> l >> r;
                                cout << fw.prefix(r) - fw.prefix(l - 1) << "\\n";
                            }
                        }
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.94,
        ),
        build_entry(
            "azcp_p015",
            "SFT_SOLVE",
            sft_response(
                "Use a segment tree that stores the maximum on each segment. Point assignments update one leaf and all its ancestors.",
                [
                    "Build an iterative segment tree over the initial array.",
                    "For set i x, update the corresponding leaf and rebuild parent maxima upward.",
                    "For max l r, perform a standard iterative range query.",
                ],
                ["iterative segment tree array"],
                [
                    "Each tree node stores the maximum of its covered segment.",
                    "A point update changes exactly the nodes whose segments contain that point.",
                ],
                ["query on one element", "negative values", "repeated updates"],
                "O((n + q) log n)",
                "O(n)",
                "This is the basic segment-tree pattern: associative merge function, logarithmic updates, logarithmic range queries.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    struct SegTree {
                        int size = 1;
                        vector<long long> tree;
                        explicit SegTree(int n) {
                            while (size < n) size <<= 1;
                            tree.assign(2 * size, LLONG_MIN);
                        }
                        void build(const vector<long long>& a) {
                            for (int i = 0; i < (int)a.size(); i++) tree[size + i] = a[i];
                            for (int i = size - 1; i >= 1; i--) tree[i] = max(tree[2 * i], tree[2 * i + 1]);
                        }
                        void set_value(int idx, long long value) {
                            int p = size + idx;
                            tree[p] = value;
                            for (p >>= 1; p >= 1; p >>= 1) {
                                tree[p] = max(tree[2 * p], tree[2 * p + 1]);
                                if (p == 1) break;
                            }
                        }
                        long long range_max(int l, int r) const {
                            long long left_res = LLONG_MIN, right_res = LLONG_MIN;
                            for (l += size, r += size; l <= r; l >>= 1, r >>= 1) {
                                if (l & 1) left_res = max(left_res, tree[l++]);
                                if (!(r & 1)) right_res = max(tree[r--], right_res);
                            }
                            return max(left_res, right_res);
                        }
                    };

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n, q;
                        cin >> n >> q;
                        vector<long long> a(n);
                        for (int i = 0; i < n; i++) cin >> a[i];
                        SegTree st(n);
                        st.build(a);

                        while (q--) {
                            string op;
                            cin >> op;
                            if (op == "set") {
                                int idx;
                                long long x;
                                cin >> idx >> x;
                                st.set_value(idx - 1, x);
                            } else {
                                int l, r;
                                cin >> l >> r;
                                cout << st.range_max(l - 1, r - 1) << "\\n";
                            }
                        }
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.93,
        ),
    ]
)
