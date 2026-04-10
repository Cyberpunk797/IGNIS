from seed_common import SFT_ENTRIES, build_entry, cpp, sft_response


SFT_ENTRIES.extend(
    [
        build_entry(
            "azcp_p016",
            "SFT_SOLVE",
            sft_response(
                "This is 0/1 knapsack. Use dp[c] = best value achievable with capacity c after processing some prefix of items.",
                [
                    "Initialize dp[0..W] = 0.",
                    "For each item (weight, value), iterate capacities from W down to weight.",
                    "Transition dp[c] = max(dp[c], dp[c-weight] + value).",
                ],
                ["vector<long long> dp"],
                [
                    "Before processing an item, dp[c] represents the best value using earlier items only.",
                    "Descending capacity order ensures the same item is not reused within one iteration.",
                ],
                ["no item fits", "multiple optimal subsets", "large values requiring long long"],
                "O(nW)",
                "O(W)",
                "The descending loop order is the crucial 0/1 detail. It preserves the one-use constraint while keeping memory one-dimensional.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n, W;
                        cin >> n >> W;
                        vector<long long> dp(W + 1, 0);
                        for (int i = 0; i < n; i++) {
                            int w;
                            long long v;
                            cin >> w >> v;
                            for (int c = W; c >= w; c--) {
                                dp[c] = max(dp[c], dp[c - w] + v);
                            }
                        }

                        cout << *max_element(dp.begin(), dp.end()) << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.93,
        ),
        build_entry(
            "azcp_p017",
            "SFT_SOLVE",
            sft_response(
                "Let dp[i][j] be the number of ways to reach cell (i, j). Open cells inherit paths from above and left.",
                [
                    "If the start cell is blocked, answer 0 immediately.",
                    "Iterate the grid row by row.",
                    "For each open cell, add the number of ways from the top and left neighbors modulo 1e9+7.",
                ],
                ["2D vector<int> dp", "vector<string> grid"],
                [
                    "Any valid path to an open cell must arrive from exactly one of the two allowed predecessor cells.",
                    "Blocked cells contribute zero paths and break transitions cleanly.",
                ],
                ["blocked start or finish", "single row", "single column"],
                "O(nm)",
                "O(nm)",
                "The move set is acyclic and local, so a simple forward DP is enough.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    static const int MOD = 1000000007;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n, m;
                        cin >> n >> m;
                        vector<string> g(n);
                        for (int i = 0; i < n; i++) cin >> g[i];

                        vector<vector<int>> dp(n, vector<int>(m, 0));
                        if (g[0][0] == '.') dp[0][0] = 1;

                        for (int i = 0; i < n; i++) {
                            for (int j = 0; j < m; j++) {
                                if (g[i][j] == '#') continue;
                                if (i == 0 && j == 0) continue;
                                long long ways = 0;
                                if (i > 0) ways += dp[i - 1][j];
                                if (j > 0) ways += dp[i][j - 1];
                                dp[i][j] = (int)(ways % MOD);
                            }
                        }

                        cout << dp[n - 1][m - 1] << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.93,
        ),
        build_entry(
            "azcp_p018",
            "SFT_SOLVE",
            sft_response(
                "Sort by width ascending and by height descending on equal widths. Then the answer is the LIS length on heights.",
                [
                    "Sort pairs by (width asc, height desc).",
                    "Scan the sorted list and maintain the LIS tails array on heights.",
                    "Use lower_bound for strict increasing LIS on the transformed sequence.",
                ],
                ["vector<pair<long long,long long>>", "vector<long long> tails"],
                [
                    "Descending heights on equal widths prevent choosing two towers with the same width in the LIS step.",
                    "The LIS tails invariant guarantees tails[len-1] is the minimum possible last height of an increasing chain of length len.",
                ],
                ["duplicate widths", "duplicate heights", "already increasing sequence"],
                "O(n log n)",
                "O(n)",
                "This is the standard 2D-chain reduction to LIS. The tie-breaking on equal widths is what makes the reduction correct.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n;
                        cin >> n;
                        vector<pair<long long, long long>> a(n);
                        for (int i = 0; i < n; i++) cin >> a[i].first >> a[i].second;

                        sort(a.begin(), a.end(), [](const auto& lhs, const auto& rhs) {
                            if (lhs.first != rhs.first) return lhs.first < rhs.first;
                            return lhs.second > rhs.second;
                        });

                        vector<long long> tails;
                        for (auto [w, h] : a) {
                            auto it = lower_bound(tails.begin(), tails.end(), h);
                            if (it == tails.end()) tails.push_back(h);
                            else *it = h;
                        }

                        cout << tails.size() << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.95,
        ),
        build_entry(
            "azcp_p019",
            "SFT_SOLVE",
            sft_response(
                "Represent the set of bulbs already turned on as a bitmask. DP over masks gives the minimum cost to reach every coverage state.",
                [
                    "Convert every switch's bulb list into a bitmask.",
                    "Initialize dp[0] = 0 and all other masks to INF.",
                    "For each switch, try taking it from every current mask and relax dp[mask | switch_mask].",
                ],
                ["vector<long long> dp", "bitmasks"],
                [
                    "dp[mask] is the minimum cost to achieve the covered-bulb set mask after processing some prefix of switches.",
                    "Using or skipping the next switch preserves optimal substructure because each switch can be used at most once.",
                ],
                ["impossible full coverage", "m = 1", "switches covering the same bulbs"],
                "O(n * 2^m)",
                "O(2^m)",
                "The state space is small enough because m <= 20. The bitmask DP is exact and easy to verify.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n, m;
                        cin >> n >> m;
                        int full = (1 << m) - 1;
                        const long long INF = (long long)4e18;
                        vector<long long> dp(1 << m, INF);
                        dp[0] = 0;

                        for (int i = 0; i < n; i++) {
                            long long cost;
                            int t;
                            cin >> cost >> t;
                            int mask = 0;
                            for (int j = 0; j < t; j++) {
                                int bulb;
                                cin >> bulb;
                                mask |= 1 << bulb;
                            }
                            vector<long long> ndp = dp;
                            for (int state = 0; state <= full; state++) {
                                if (dp[state] == INF) continue;
                                ndp[state | mask] = min(ndp[state | mask], dp[state] + cost);
                            }
                            dp.swap(ndp);
                        }

                        cout << (dp[full] == INF ? -1 : dp[full]) << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.94,
        ),
        build_entry(
            "azcp_p020",
            "SFT_SOLVE",
            sft_response(
                "Compute the prefix function pi. Starting from pi[n-1] and repeatedly jumping to pi[k-1] enumerates all borders.",
                [
                    "Build the prefix-function array for the string.",
                    "Start from the longest proper border length pi[n-1].",
                    "Repeatedly append the current border length and jump to pi[length-1] until the length becomes 0.",
                    "Reverse the collected lengths to print them in increasing order.",
                ],
                ["string", "vector<int> pi", "vector<int> borders"],
                [
                    "pi[i] is the length of the longest proper prefix that is also a suffix of s[0..i].",
                    "Every border of the whole string is a border of its longest border, so following pi links enumerates exactly all proper borders.",
                ],
                ["no borders", "all characters equal", "length 1 string"],
                "O(n)",
                "O(n)",
                "The prefix-function chain is the compact representation of border nesting. Following that chain is enough to recover every border length.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        string s;
                        cin >> s;
                        int n = (int)s.size();
                        vector<int> pi(n, 0);
                        for (int i = 1; i < n; i++) {
                            int j = pi[i - 1];
                            while (j > 0 && s[i] != s[j]) j = pi[j - 1];
                            if (s[i] == s[j]) j++;
                            pi[i] = j;
                        }

                        vector<int> borders;
                        for (int k = pi[n - 1]; k > 0; k = pi[k - 1]) borders.push_back(k);
                        reverse(borders.begin(), borders.end());

                        cout << borders.size() << "\\n";
                        for (int i = 0; i < (int)borders.size(); i++) {
                            if (i) cout << ' ';
                            cout << borders[i];
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
    ]
)
