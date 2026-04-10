from seed_common import SFT_ENTRIES, build_entry, cpp, sft_response


SFT_ENTRIES.extend(
    [
        build_entry(
            "azcp_p001",
            "SFT_SOLVE",
            sft_response(
                "Store a globally alternating prefix sum. A query becomes one prefix subtraction, and parity of l decides whether to negate it.",
                [
                    "Build pref[i] = pref[i-1] + a_i if i is odd, otherwise pref[i-1] - a_i.",
                    "For query [l, r], compute raw = pref[r] - pref[l-1].",
                    "If l is even, negate raw because the query must start with plus at l.",
                ],
                ["vector<long long> pref"],
                [
                    "pref[i] equals a1-a2+a3-... with signs anchored at index 1.",
                    "Subtracting pref[l-1] removes the prefix before l, leaving the alternating sum on [l, r] under the global sign pattern.",
                    "When l is even, the global sign pattern is reversed relative to the query definition, so one negation fixes it.",
                ],
                ["l = r", "negative values", "large magnitudes requiring long long"],
                "O(n + q)",
                "O(n)",
                "A fixed signed prefix array is enough. The only subtle point is that query signs are anchored at l, not at 1, so even starting indices need one final negation.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n, q;
                        cin >> n >> q;
                        vector<long long> pref(n + 1, 0);
                        for (int i = 1; i <= n; i++) {
                            long long x;
                            cin >> x;
                            pref[i] = pref[i - 1] + (i % 2 == 1 ? x : -x);
                        }

                        while (q--) {
                            int l, r;
                            cin >> l >> r;
                            long long ans = pref[r] - pref[l - 1];
                            if (l % 2 == 0) ans = -ans;
                            cout << ans << "\\n";
                        }
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.96,
        ),
        build_entry(
            "azcp_p002",
            "SFT_SOLVE",
            sft_response(
                "After sorting the skills, pairing adjacent players minimizes the worst pair difference.",
                [
                    "Sort the skill array.",
                    "Pair positions (1,2), (3,4), ..., (n-1,n).",
                    "Take the maximum difference among these adjacent pairs.",
                ],
                ["vector<long long> skills"],
                [
                    "In sorted order, any crossing pairing can be uncrossed without increasing the larger involved gap.",
                    "Repeatedly uncrossing transforms an optimal solution into one with adjacent pairs only.",
                ],
                ["duplicate skills", "already sorted input", "very large values"],
                "O(n log n)",
                "O(1) extra beyond the array",
                "Sorting exposes the structure of the optimal matching. Once players are ordered, adjacent pairing is forced by the exchange argument.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n;
                        cin >> n;
                        vector<long long> a(n);
                        for (int i = 0; i < n; i++) cin >> a[i];
                        sort(a.begin(), a.end());

                        long long ans = 0;
                        for (int i = 0; i < n; i += 2) {
                            ans = max(ans, a[i + 1] - a[i]);
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
            "azcp_p003",
            "SFT_SOLVE",
            sft_response(
                "Mark where each range update starts and stops, then recover final values with one prefix pass.",
                [
                    "Create a difference array diff of size n+2 initialized to 0.",
                    "For each update (l, r, x), add x to diff[l] and subtract x from diff[r+1].",
                    "Prefix-sum diff to obtain the final water levels.",
                ],
                ["vector<long long> diff"],
                [
                    "Each update contributes x starting at l and contributes -x starting at r+1.",
                    "After prefixing, those contributions remain exactly on [l, r] and cancel elsewhere.",
                ],
                ["updates touching r = n", "large x values", "n = 1"],
                "O(n + q)",
                "O(n)",
                "Range updates are expensive only if applied cell by cell. The difference array stores update boundaries, and one prefix pass materializes the result.",
                cpp(
                    """
                    #include <bits/stdc++.h>
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(nullptr);

                        int n, q;
                        cin >> n >> q;
                        vector<long long> diff(n + 2, 0);
                        while (q--) {
                            int l, r;
                            long long x;
                            cin >> l >> r >> x;
                            diff[l] += x;
                            diff[r + 1] -= x;
                        }

                        long long cur = 0;
                        for (int i = 1; i <= n; i++) {
                            cur += diff[i];
                            if (i > 1) cout << ' ';
                            cout << cur;
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
            "azcp_p004",
            "SFT_SOLVE",
            sft_response(
                "Because all costs are positive, a window that is too expensive can only be fixed by moving its left end rightward.",
                [
                    "Maintain a window [l, r] and its sum.",
                    "Extend r one step at a time.",
                    "While the sum exceeds k, subtract a[l] and increment l.",
                    "Track the maximum window length seen.",
                ],
                ["vector<long long> a"],
                [
                    "With positive values, once a window exceeds k, any longer window with the same left endpoint also exceeds k.",
                    "Therefore shrinking the left endpoint until the sum fits is both necessary and sufficient.",
                ],
                ["no segment longer than 1 is valid", "k very large", "n = 1"],
                "O(n)",
                "O(1) extra",
                "Positivity is the key property. It makes two pointers exact rather than heuristic, because each pointer only moves forward.",
                cpp(
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

                        long long sum = 0;
                        int l = 0, ans = 0;
                        for (int r = 0; r < n; r++) {
                            sum += a[r];
                            while (sum > k) {
                                sum -= a[l];
                                l++;
                            }
                            ans = max(ans, r - l + 1);
                        }

                        cout << ans << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.95,
        ),
        build_entry(
            "azcp_p005",
            "SFT_SOLVE",
            sft_response(
                "Only the median and larger elements affect the final median. Binary-search the answer and check how many increments are needed to raise the upper half to that level.",
                [
                    "Sort the array and locate the median index mid = n/2.",
                    "Binary-search a candidate median x.",
                    "For each candidate x, sum max(0, x-a[i]) for i from mid to n-1 and test whether the cost is at most k.",
                ],
                ["vector<long long> a"],
                [
                    "Elements left of the median never need to be increased, because they do not reduce the sorted median.",
                    "A candidate x is feasible exactly when the sorted upper half can all be made at least x within budget.",
                    "Feasibility is monotone in x, so binary search is valid.",
                ],
                ["k = 0", "already large median", "large k needing long long"],
                "O(n log n + n log k)",
                "O(1) extra beyond sorting",
                "The feasibility test is monotone, which makes binary search natural. Sorting isolates the part of the array that can block the median from rising.",
                cpp(
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
                        sort(a.begin(), a.end());

                        int mid = n / 2;
                        long long low = a[mid];
                        long long high = a[mid] + k + 1;

                        auto can = [&](long long x) {
                            long long need = 0;
                            for (int i = mid; i < n; i++) {
                                if (a[i] < x) {
                                    need += x - a[i];
                                    if (need > k) return false;
                                }
                            }
                            return true;
                        };

                        while (low + 1 < high) {
                            long long m = low + (high - low) / 2;
                            if (can(m)) low = m;
                            else high = m;
                        }

                        cout << low << "\\n";
                        return 0;
                    }
                    """
                ),
            ),
            "gold",
            0.96,
        ),
    ]
)
