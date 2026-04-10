from seed_common import REPAIR_ENTRIES, SFT_ENTRIES, build_entry, cpp


SFT_CODE = {entry["problem"]["problem_id"]: entry["response"]["final_code"] for entry in SFT_ENTRIES}


REPAIR_ENTRIES.extend(
    [
        build_entry(
            "azcp_p007",
            "REPAIR",
            {
                "buggy_code": cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;
                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);
                        int n, k;
                        cin >> n >> k;
                        vector<long long> a(n);
                        for (int i = 0; i < n; i++) cin >> a[i];
                        deque<int> dq;
                        vector<long long> out;
                        for (int i = 0; i < n; i++) {
                            while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
                            dq.push_back(i);
                            while (!dq.empty() && dq.front() < i - k) dq.pop_front();
                            if (i + 1 >= k) out.push_back(a[dq.front()]);
                        }
                        for (int i = 0; i < (int)out.size(); i++) {
                            if (i) cout << ' ';
                            cout << out[i];
                        }
                        cout << "\\n";
                        return 0;
                    }
                    """
                ),
                "bug_type": "Stale window index handling",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "4 2\n9 1 2 3\n",
                    "expected_output": "9 2 3\n",
                    "got_output": "9 9 3\n",
                },
                "diagnosis": [
                    "At window ending i, any index <= i-k is already outside the window and must be removed.",
                    "Using < i-k leaves one stale index alive for one extra step.",
                ],
                "fix_explanation": "Remove front indices while dq.front() <= i-k before reading the maximum.",
                "fixed_code": SFT_CODE["azcp_p007"],
            },
            "gold",
            0.91,
        ),
        build_entry(
            "azcp_p008",
            "REPAIR",
            {
                "buggy_code": cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;
                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);
                        int n;
                        cin >> n;
                        vector<long long> starts(n), ends(n);
                        for (int i = 0; i < n; i++) cin >> starts[i] >> ends[i];
                        sort(starts.begin(), starts.end());
                        sort(ends.begin(), ends.end());
                        int active = 0, ans = 0, j = 0;
                        for (int i = 0; i < n; i++) {
                            while (j < n && ends[j] < starts[i]) {
                                active--;
                                j++;
                            }
                            active++;
                            ans = max(ans, active);
                        }
                        cout << ans << "\\n";
                        return 0;
                    }
                    """
                ),
                "bug_type": "Wrong interval boundary condition",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "2\n1 3\n3 5\n",
                    "expected_output": "1\n",
                    "got_output": "2\n",
                },
                "diagnosis": [
                    "The intervals are half-open [l, r), so a meeting ending at time t does not overlap one starting at t.",
                    "Releasing halls only for end < start incorrectly treats touching intervals as overlapping.",
                ],
                "fix_explanation": "Release every meeting with end <= current start before allocating the new hall.",
                "fixed_code": SFT_CODE["azcp_p008"],
            },
            "gold",
            0.92,
        ),
        build_entry(
            "azcp_p009",
            "REPAIR",
            {
                "buggy_code": cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;
                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);
                        int n, m;
                        cin >> n >> m;
                        vector<string> g(n);
                        for (int i = 0; i < n; i++) cin >> g[i];
                        pair<int, int> s = {-1, -1}, t = {-1, -1};
                        for (int i = 0; i < n; i++) {
                            for (int j = 0; j < m; j++) {
                                if (g[i][j] == 'S') s = {i, j};
                                if (g[i][j] == 'T') t = {i, j};
                            }
                        }
                        vector<vector<int>> dist(n, vector<int>(m, -1));
                        queue<pair<int, int>> q;
                        dist[s.first][s.second] = 0;
                        q.push(s);
                        const int dr[4] = {-1, 1, 0, 0};
                        const int dc[4] = {0, 0, -1, 1};
                        while (!q.empty()) {
                            auto [r, c] = q.front();
                            q.pop();
                            for (int dir = 0; dir < 4; dir++) {
                                int nr = r + dr[dir], nc = c + dc[dir];
                                if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
                                if (g[nr][nc] != '.') continue;
                                if (dist[nr][nc] != -1) continue;
                                dist[nr][nc] = dist[r][c] + 1;
                                q.push({nr, nc});
                            }
                        }
                        cout << dist[t.first][t.second] << "\\n";
                        return 0;
                    }
                    """
                ),
                "bug_type": "Incorrect traversable-cell test",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "1 2\nST\n",
                    "expected_output": "1\n",
                    "got_output": "-1\n",
                },
                "diagnosis": [
                    "The target cell T is not '.', but it is still traversable.",
                    "Filtering to '.' only makes the BFS unable to enter the target.",
                ],
                "fix_explanation": "Treat every non-wall cell as traversable, including both S and T.",
                "fixed_code": SFT_CODE["azcp_p009"],
            },
            "gold",
            0.91,
        ),
        build_entry(
            "azcp_p010",
            "REPAIR",
            {
                "buggy_code": cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;
                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);
                        int n, m;
                        cin >> n >> m;
                        vector<vector<int>> g(n + 1);
                        vector<int> indeg(n + 1, 0), dp(n + 1, 0);
                        for (int i = 0; i < m; i++) {
                            int u, v;
                            cin >> u >> v;
                            g[u].push_back(v);
                            indeg[v]++;
                        }
                        queue<int> q;
                        for (int i = 1; i <= n; i++) {
                            if (indeg[i] == 0) {
                                dp[i] = 1;
                                q.push(i);
                            }
                        }
                        int ans = 0;
                        while (!q.empty()) {
                            int u = q.front();
                            q.pop();
                            ans = max(ans, dp[u]);
                            for (int v : g[u]) {
                                dp[v] = max(dp[v], dp[u] + 1);
                                indeg[v]--;
                                if (indeg[v] == 0) q.push(v);
                            }
                        }
                        cout << ans << "\\n";
                        return 0;
                    }
                    """
                ),
                "bug_type": "Missing cycle detection",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "3 3\n1 2\n2 3\n3 1\n",
                    "expected_output": "-1\n",
                    "got_output": "0\n",
                },
                "diagnosis": [
                    "Kahn's algorithm only processes nodes reachable from the zero-indegree frontier.",
                    "If a cycle exists, some nodes never enter the queue, so printing the partial answer is invalid.",
                ],
                "fix_explanation": "Count processed nodes and output -1 whenever processed != n.",
                "fixed_code": SFT_CODE["azcp_p010"],
            },
            "gold",
            0.92,
        ),
        build_entry(
            "azcp_p013",
            "REPAIR",
            {
                "buggy_code": cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;
                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);
                        int n, m;
                        cin >> n >> m;
                        vector<vector<pair<int, int>>> g(n + 1);
                        for (int i = 0; i < m; i++) {
                            int u, v, w;
                            cin >> u >> v >> w;
                            g[u].push_back({v, w});
                            g[v].push_back({u, w});
                        }
                        const int INF = 2000000000;
                        vector<int> dist(n + 1, INF);
                        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
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
                "bug_type": "Distance overflow",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "3 2\n1 2 1500000000\n2 3 1500000000\n",
                    "expected_output": "3000000000\n",
                    "got_output": "negative or wrapped 32-bit value\n",
                },
                "diagnosis": [
                    "Shortest-path distances can exceed the 32-bit range when many large edges are added.",
                    "Both the graph weights and the distance array must use long long.",
                ],
                "fix_explanation": "Store weights and distances as long long and keep the priority queue keyed by long long distances.",
                "fixed_code": SFT_CODE["azcp_p013"],
            },
            "gold",
            0.91,
        ),
    ]
)
