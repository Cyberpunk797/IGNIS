from seed_common import SFT_ENTRIES, build_entry, cpp, sft_response


SFT_ENTRIES.extend(
    [
        build_entry(
            "azcp_p006",
            "SFT_SOLVE",
            sft_response(
                "Keep a stack of indices with strictly decreasing heights. After removing all heights not greater than h_i, the top is the nearest previous higher tower.",
                [
                    "Process towers from left to right.",
                    "While the stack top has height <= current height, pop it.",
                    "The remaining top, if any, is the nearest previous greater index.",
                    "Push the current index onto the stack.",
                ],
                ["stack of indices", "vector<long long> h"],
                [
                    "The stack always stores heights in strictly decreasing order.",
                    "Any popped index is dominated by the current tower and can never answer a future query.",
                ],
                ["equal heights", "strictly increasing heights", "strictly decreasing heights"],
                "O(n)",
                "O(n)",
                "The monotonic stack deletes only dominated candidates. Each index is pushed and popped at most once.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n;
                        cin >> n;
                        vector<long long> h(n + 1);
                        for (int i = 1; i <= n; i++) cin >> h[i];

                        vector<int> st, ans(n + 1, 0);
                        for (int i = 1; i <= n; i++) {
                            while (!st.empty() && h[st.back()] <= h[i]) st.pop_back();
                            ans[i] = st.empty() ? 0 : st.back();
                            st.push_back(i);
                        }

                        for (int i = 1; i <= n; i++) {
                            if (i > 1) cout << ' ';
                            cout << ans[i];
                        }
                        cout << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.94,
        ),
        build_entry(
            "azcp_p007",
            "SFT_SOLVE",
            sft_response(
                "A deque of indices in decreasing value order stores exactly the candidates that can still become the maximum of the current or future windows.",
                [
                    "Process indices from left to right.",
                    "Before inserting i, drop deque back indices with value <= a[i].",
                    "Push i, then remove the front index if it left the current window.",
                    "Once the first full window is formed, the deque front is the window maximum.",
                ],
                ["deque<int>", "vector<long long> a"],
                [
                    "Deque values are kept in decreasing order, so the front is always the maximum candidate.",
                    "An index removed from the back is dominated by a later index with greater or equal value.",
                ],
                ["k = 1", "all equal values", "negative values"],
                "O(n)",
                "O(k)",
                "The deque only stores undominated indices inside the current window. That preserves exact maxima while keeping total work linear.",
                cpp(
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
                            while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
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
            ),
            "gold",
            0.95,
        ),
        build_entry(
            "azcp_p008",
            "SFT_SOLVE",
            sft_response(
                "Sort all start times and end times separately. Sweep through starts while releasing every hall whose meeting has already ended.",
                [
                    "Store all starts in one array and all ends in another.",
                    "Sort both arrays.",
                    "For each next start time, first advance the end pointer while end <= start.",
                    "After releasing finished meetings, occupy one hall for the new meeting and update the maximum active count.",
                ],
                ["vector<long long> starts", "vector<long long> ends"],
                [
                    "active equals the number of meetings that have started but not yet ended.",
                    "Because intervals are half-open [l, r), meetings ending at time t do not overlap meetings starting at t.",
                ],
                ["multiple equal start times", "meetings touching at endpoints", "n = 1"],
                "O(n log n)",
                "O(n)",
                "The answer is the peak overlap count. Separating starts and ends makes that overlap easy to maintain with one sweep.",
                cpp(
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
                            while (j < n && ends[j] <= starts[i]) {
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
            ),
            "gold",
            0.94,
        ),
        build_entry(
            "azcp_p009",
            "SFT_SOLVE",
            sft_response(
                "The grid is an unweighted graph, so BFS from S visits cells in increasing distance order.",
                [
                    "Locate S and T, and initialize all distances to -1.",
                    "Run BFS from S over the four directions, ignoring walls and already visited cells.",
                    "The first distance assigned to T is the shortest path length.",
                ],
                ["vector<string> grid", "queue<pair<int,int>>", "2D distance array"],
                [
                    "BFS expands cells layer by layer by move count.",
                    "When a cell is first reached, that path uses the minimum possible number of moves.",
                ],
                ["T unreachable", "S adjacent to T", "n or m equal to 1"],
                "O(nm)",
                "O(nm)",
                "All moves cost one, so standard BFS already guarantees shortest paths in this grid.",
                cpp(
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
                                if (g[nr][nc] == '#') continue;
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
            ),
            "gold",
            0.95,
        ),
        build_entry(
            "azcp_p010",
            "SFT_SOLVE",
            sft_response(
                "Perform Kahn's topological sort. Along that order, dp[v] is the earliest semester in which v can be taken.",
                [
                    "Build indegrees and adjacency lists.",
                    "Initialize zero-indegree courses with dp = 1 and push them into the queue.",
                    "Pop u, relax each edge u -> v with dp[v] = max(dp[v], dp[u] + 1), and push v when its indegree becomes zero.",
                    "If not all nodes are processed, a cycle exists.",
                ],
                ["vector<vector<int>> g", "queue<int>", "vector<int> indeg", "vector<int> dp"],
                [
                    "A course can only be taken after all predecessors are processed, which is exactly what zero indegree means in Kahn's algorithm.",
                    "dp[v] tracks the longest prerequisite chain ending at v, so it equals the earliest feasible semester for v.",
                ],
                ["isolated courses", "cycle in the graph", "multiple prerequisite chains merging"],
                "O(n + m)",
                "O(n + m)",
                "This is longest path on a DAG plus cycle detection. Kahn's algorithm handles both in one pass.",
                cpp(
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

                        int processed = 0, ans = 0;
                        while (!q.empty()) {
                            int u = q.front();
                            q.pop();
                            processed++;
                            ans = max(ans, dp[u]);
                            for (int v : g[u]) {
                                dp[v] = max(dp[v], dp[u] + 1);
                                indeg[v]--;
                                if (indeg[v] == 0) q.push(v);
                            }
                        }

                        cout << (processed == n ? ans : -1) << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.95,
        ),
    ]
)
