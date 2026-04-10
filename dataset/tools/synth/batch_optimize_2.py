from seed_common import OPTIMIZE_ENTRIES, SFT_ENTRIES, build_entry, cpp


SFT_CODE = {entry["problem"]["problem_id"]: entry["response"]["final_code"] for entry in SFT_ENTRIES}


OPTIMIZE_ENTRIES.extend(
    [
        build_entry(
            "azcp_p008",
            "OPTIMIZE",
            {
                "slow_code": {
                    "complexity": "O(n^2)",
                    "code": cpp(
                        """
                        #include <bits/stdc++.h>
                        using namespace std;
                        int main() {
                            ios::sync_with_stdio(false);
                            cin.tie(nullptr);
                            int n;
                            cin >> n;
                            vector<pair<long long, long long>> meetings(n);
                            for (int i = 0; i < n; i++) cin >> meetings[i].first >> meetings[i].second;
                            vector<long long> room_end;
                            for (auto [l, r] : meetings) {
                                bool placed = false;
                                for (long long& e : room_end) {
                                    if (e <= l) {
                                        e = r;
                                        placed = true;
                                        break;
                                    }
                                }
                                if (!placed) room_end.push_back(r);
                            }
                            cout << room_end.size() << "\\n";
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "Scanning all rooms for every meeting can take O(n^2), and the code also depends on input order rather than event order.",
                "optimization_idea": "Sort starts and ends separately and sweep overlap count, releasing all meetings whose end time is <= the next start time.",
                "new_complexity": {"time": "O(n log n)", "memory": "O(n)"},
                "optimized_code": SFT_CODE["azcp_p008"],
            },
            "gold",
            0.92,
        ),
        build_entry(
            "azcp_p011",
            "OPTIMIZE",
            {
                "slow_code": {
                    "complexity": "O(n^2)",
                    "code": cpp(
                        """
                        #include <bits/stdc++.h>
                        using namespace std;
                        int main() {
                            ios::sync_with_stdio(false);
                            cin.tie(nullptr);
                            int n;
                            cin >> n;
                            vector<pair<int, int>> edges;
                            vector<vector<int>> g(n + 1);
                            for (int i = 0; i < n - 1; i++) {
                                int u, v;
                                cin >> u >> v;
                                edges.push_back({u, v});
                                g[u].push_back(v);
                                g[v].push_back(u);
                            }
                            long long ans = 0;
                            for (auto [ban_u, ban_v] : edges) {
                                vector<int> vis(n + 1, 0);
                                queue<int> q;
                                q.push(ban_u);
                                vis[ban_u] = 1;
                                long long cnt = 0;
                                while (!q.empty()) {
                                    int u = q.front();
                                    q.pop();
                                    cnt++;
                                    for (int v : g[u]) {
                                        if ((u == ban_u && v == ban_v) || (u == ban_v && v == ban_u)) continue;
                                        if (!vis[v]) {
                                            vis[v] = 1;
                                            q.push(v);
                                        }
                                    }
                                }
                                ans = max(ans, cnt * (n - cnt));
                            }
                            cout << ans << "\\n";
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "It recomputes a graph traversal for every edge, which is quadratic on a tree.",
                "optimization_idea": "Root the tree once, compute subtree sizes once, and evaluate every cut using sub[u] * (n-sub[u]).",
                "new_complexity": {"time": "O(n)", "memory": "O(n)"},
                "optimized_code": SFT_CODE["azcp_p011"],
            },
            "gold",
            0.93,
        ),
        build_entry(
            "azcp_p013",
            "OPTIMIZE",
            {
                "slow_code": {
                    "complexity": "O(nm)",
                    "code": cpp(
                        """
                        #include <bits/stdc++.h>
                        using namespace std;
                        struct Edge {
                            int u, v;
                            long long w;
                        };
                        int main() {
                            ios::sync_with_stdio(false);
                            cin.tie(nullptr);
                            int n, m;
                            cin >> n >> m;
                            vector<Edge> edges;
                            for (int i = 0; i < m; i++) {
                                int u, v;
                                long long w;
                                cin >> u >> v >> w;
                                edges.push_back({u, v, w});
                                edges.push_back({v, u, w});
                            }
                            const long long INF = (long long)4e18;
                            vector<long long> dist(n + 1, INF);
                            dist[1] = 0;
                            for (int iter = 1; iter <= n - 1; iter++) {
                                bool changed = false;
                                for (auto e : edges) {
                                    if (dist[e.u] == INF) continue;
                                    if (dist[e.v] > dist[e.u] + e.w) {
                                        dist[e.v] = dist[e.u] + e.w;
                                        changed = true;
                                    }
                                }
                                if (!changed) break;
                            }
                            cout << (dist[n] == INF ? -1 : dist[n]) << "\\n";
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "Bellman-Ford is correct but far too slow for sparse non-negative graphs with up to 2e5 edges.",
                "optimization_idea": "Use Dijkstra with a min-priority queue because all weights are non-negative.",
                "new_complexity": {"time": "O((n + m) log n)", "memory": "O(n + m)"},
                "optimized_code": SFT_CODE["azcp_p013"],
            },
            "gold",
            0.94,
        ),
        build_entry(
            "azcp_p014",
            "OPTIMIZE",
            {
                "slow_code": {
                    "complexity": "O(n) per operation",
                    "code": cpp(
                        """
                        #include <bits/stdc++.h>
                        using namespace std;
                        int main() {
                            ios::sync_with_stdio(false);
                            cin.tie(nullptr);
                            int n, q;
                            cin >> n >> q;
                            vector<long long> a(n + 1, 0);
                            while (q--) {
                                string op;
                                cin >> op;
                                if (op == "add") {
                                    int idx;
                                    long long x;
                                    cin >> idx >> x;
                                    a[idx] += x;
                                } else {
                                    int l, r;
                                    cin >> l >> r;
                                    long long ans = 0;
                                    for (int i = l; i <= r; i++) ans += a[i];
                                    cout << ans << "\\n";
                                }
                            }
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "Range sums linearly scan the interval, so many large queries are too expensive.",
                "optimization_idea": "Fenwick tree gives both point additions and prefix sums in O(log n), so each range sum is two prefix queries.",
                "new_complexity": {"time": "O(q log n)", "memory": "O(n)"},
                "optimized_code": SFT_CODE["azcp_p014"],
            },
            "gold",
            0.93,
        ),
        build_entry(
            "azcp_p020",
            "OPTIMIZE",
            {
                "slow_code": {
                    "complexity": "O(n^2)",
                    "code": cpp(
                        """
                        #include <bits/stdc++.h>
                        using namespace std;
                        int main() {
                            ios::sync_with_stdio(false);
                            cin.tie(nullptr);
                            string s;
                            cin >> s;
                            int n = (int)s.size();
                            vector<int> ans;
                            for (int len = 1; len < n; len++) {
                                bool ok = true;
                                for (int i = 0; i < len; i++) {
                                    if (s[i] != s[n - len + i]) {
                                        ok = false;
                                        break;
                                    }
                                }
                                if (ok) ans.push_back(len);
                            }
                            cout << ans.size() << "\\n";
                            for (int i = 0; i < (int)ans.size(); i++) {
                                if (i) cout << ' ';
                                cout << ans[i];
                            }
                            cout << "\\n";
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "Checking every candidate border length by character comparison is quadratic in the worst case.",
                "optimization_idea": "Build the prefix function once and follow the border chain from pi[n-1] to enumerate all borders in linear total time.",
                "new_complexity": {"time": "O(n)", "memory": "O(n)"},
                "optimized_code": SFT_CODE["azcp_p020"],
            },
            "gold",
            0.93,
        ),
    ]
)
