from seed_common import OPTIMIZE_ENTRIES, SFT_ENTRIES, build_entry, cpp


SFT_CODE = {entry["problem"]["problem_id"]: entry["response"]["final_code"] for entry in SFT_ENTRIES}


OPTIMIZE_ENTRIES.extend(
    [
        build_entry(
            "azcp_p001",
            "OPTIMIZE",
            {
                "slow_code": {
                    "complexity": "O(sum query lengths)",
                    "code": cpp(
                        """
                        #include <bits/stdc++.h>
                        using namespace std;
                        int main() {
                            ios::sync_with_stdio(false);
                            cin.tie(nullptr);
                            int n, q;
                            cin >> n >> q;
                            vector<long long> a(n + 1);
                            for (int i = 1; i <= n; i++) cin >> a[i];
                            while (q--) {
                                int l, r;
                                cin >> l >> r;
                                long long ans = 0;
                                int sign = 1;
                                for (int i = l; i <= r; i++) {
                                    ans += sign * a[i];
                                    sign *= -1;
                                }
                                cout << ans << "\\n";
                            }
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "In the worst case every query scans O(n) elements, so q = n = 2e5 leads to O(nq) time.",
                "optimization_idea": "Precompute a globally alternating prefix sum anchored at index 1, then answer each query with one subtraction plus an optional negation based on the parity of l.",
                "new_complexity": {"time": "O(n + q)", "memory": "O(n)"},
                "optimized_code": SFT_CODE["azcp_p001"],
            },
            "gold",
            0.93,
        ),
        build_entry(
            "azcp_p003",
            "OPTIMIZE",
            {
                "slow_code": {
                    "complexity": "O(nq)",
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
                                int l, r;
                                long long x;
                                cin >> l >> r >> x;
                                for (int i = l; i <= r; i++) a[i] += x;
                            }
                            for (int i = 1; i <= n; i++) {
                                if (i > 1) cout << ' ';
                                cout << a[i];
                            }
                            cout << "\\n";
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "Touching every index of every updated segment is too expensive when both n and q are large.",
                "optimization_idea": "Convert every update into two difference-array boundary operations and reconstruct the final array with one prefix pass.",
                "new_complexity": {"time": "O(n + q)", "memory": "O(n)"},
                "optimized_code": SFT_CODE["azcp_p003"],
            },
            "gold",
            0.94,
        ),
        build_entry(
            "azcp_p004",
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
                            long long k;
                            cin >> n >> k;
                            vector<long long> a(n);
                            for (int i = 0; i < n; i++) cin >> a[i];
                            int ans = 0;
                            for (int l = 0; l < n; l++) {
                                long long sum = 0;
                                for (int r = l; r < n; r++) {
                                    sum += a[r];
                                    if (sum <= k) ans = max(ans, r - l + 1);
                                }
                            }
                            cout << ans << "\\n";
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "All O(n^2) subarrays are checked explicitly.",
                "optimization_idea": "Because all numbers are positive, two pointers maintain the longest feasible window without ever moving either pointer backward.",
                "new_complexity": {"time": "O(n)", "memory": "O(1) extra"},
                "optimized_code": SFT_CODE["azcp_p004"],
            },
            "gold",
            0.93,
        ),
        build_entry(
            "azcp_p006",
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
                            vector<long long> h(n + 1);
                            for (int i = 1; i <= n; i++) cin >> h[i];
                            for (int i = 1; i <= n; i++) {
                                int ans = 0;
                                for (int j = i - 1; j >= 1; j--) {
                                    if (h[j] > h[i]) {
                                        ans = j;
                                        break;
                                    }
                                }
                                if (i > 1) cout << ' ';
                                cout << ans;
                            }
                            cout << "\\n";
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "In decreasing or equal-height patterns, the inner backward scan is nearly O(n) for every i.",
                "optimization_idea": "Use a monotonic decreasing stack so every index is pushed once and popped once.",
                "new_complexity": {"time": "O(n)", "memory": "O(n)"},
                "optimized_code": SFT_CODE["azcp_p006"],
            },
            "gold",
            0.92,
        ),
        build_entry(
            "azcp_p007",
            "OPTIMIZE",
            {
                "slow_code": {
                    "complexity": "O(nk)",
                    "code": cpp(
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
                            for (int l = 0; l + k <= n; l++) {
                                long long best = a[l];
                                for (int i = l; i < l + k; i++) best = max(best, a[i]);
                                if (l) cout << ' ';
                                cout << best;
                            }
                            cout << "\\n";
                            return 0;
                        }
                        """
                    ),
                },
                "why_too_slow": "Each window recomputes its maximum from scratch.",
                "optimization_idea": "A monotonic deque stores only undominated indices of the current window, so the maximum is always at the front.",
                "new_complexity": {"time": "O(n)", "memory": "O(k)"},
                "optimized_code": SFT_CODE["azcp_p007"],
            },
            "gold",
            0.93,
        ),
    ]
)
