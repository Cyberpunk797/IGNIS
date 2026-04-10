from seed_common import REPAIR_ENTRIES, SFT_ENTRIES, build_entry, cpp


SFT_CODE = {entry["problem"]["problem_id"]: entry["response"]["final_code"] for entry in SFT_ENTRIES}


REPAIR_ENTRIES.extend(
    [
        build_entry(
            "azcp_p001",
            "REPAIR",
            {
                "buggy_code": cpp(
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
                            if (l % 2 == 1) ans = -ans;
                            cout << ans << "\\n";
                        }
                        return 0;
                    }
                    """
                ),
                "bug_type": "Parity sign error",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "5 1\n5 2 7 1 4\n2 4\n",
                    "expected_output": "-4\n",
                    "got_output": "4\n",
                },
                "diagnosis": [
                    "The raw prefix subtraction uses alternating signs anchored at index 1.",
                    "That raw value must be negated only when l is even, because then the query-defined sign pattern starts opposite to the global one.",
                ],
                "fix_explanation": "Change the parity check so the post-processing negation happens exactly for even l.",
                "fixed_code": SFT_CODE["azcp_p001"],
            },
            "gold",
            0.92,
        ),
        build_entry(
            "azcp_p003",
            "REPAIR",
            {
                "buggy_code": cpp(
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
                            diff[r] -= x;
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
                "bug_type": "Range boundary off-by-one",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "5 1\n2 4 3\n",
                    "expected_output": "0 3 3 3 0\n",
                    "got_output": "0 3 3 0 0\n",
                },
                "diagnosis": [
                    "In a difference array, an update on [l, r] adds at l and subtracts at r+1.",
                    "Subtracting at r removes the contribution one position too early.",
                ],
                "fix_explanation": "Write the negative boundary marker to diff[r+1] instead of diff[r].",
                "fixed_code": SFT_CODE["azcp_p003"],
            },
            "gold",
            0.91,
        ),
        build_entry(
            "azcp_p004",
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
                        long long k;
                        cin >> n >> k;
                        vector<long long> a(n);
                        for (int i = 0; i < n; i++) cin >> a[i];
                        long long sum = 0;
                        int l = 0, ans = 0;
                        for (int r = 0; r < n; r++) {
                            sum += a[r];
                            if (sum > k) {
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
                "bug_type": "Insufficient window shrink",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "4 5\n4 4 1 1\n",
                    "expected_output": "2\n",
                    "got_output": "3\n",
                },
                "diagnosis": [
                    "After adding a[r], the window may exceed k by more than one left element.",
                    "Using if instead of while can leave the window invalid and still count it.",
                ],
                "fix_explanation": "Shrink in a while loop until the current window sum is at most k.",
                "fixed_code": SFT_CODE["azcp_p004"],
            },
            "gold",
            0.92,
        ),
        build_entry(
            "azcp_p005",
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
                        long long k;
                        cin >> n >> k;
                        vector<long long> a(n);
                        for (int i = 0; i < n; i++) cin >> a[i];
                        sort(a.begin(), a.end());
                        int mid = n / 2;
                        long long low = a[mid], high = a[mid] + k + 1;
                        auto can = [&](long long x) {
                            int need = 0;
                            for (int i = mid; i < n; i++) if (a[i] < x) need += (int)(x - a[i]);
                            return need <= k;
                        };
                        while (low + 1 < high) {
                            long long m = (low + high) / 2;
                            if (can(m)) low = m;
                            else high = m;
                        }
                        cout << low << "\\n";
                        return 0;
                    }
                    """
                ),
                "bug_type": "32-bit overflow in feasibility check",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "5 3000000000\n0 0 0 0 0\n",
                    "expected_output": "1000000000\n",
                    "got_output": "overflowed value leads to an impossible larger answer\n",
                },
                "diagnosis": [
                    "The required increment total can exceed 2^31-1, so storing it in int overflows.",
                    "Once overflow occurs, the binary-search feasibility test becomes unreliable.",
                ],
                "fix_explanation": "Accumulate the required increment cost in long long and stop early if it exceeds k.",
                "fixed_code": SFT_CODE["azcp_p005"],
            },
            "gold",
            0.90,
        ),
        build_entry(
            "azcp_p006",
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
                        vector<long long> h(n + 1);
                        for (int i = 1; i <= n; i++) cin >> h[i];
                        vector<int> st, ans(n + 1, 0);
                        for (int i = 1; i <= n; i++) {
                            while (!st.empty() && h[st.back()] < h[i]) st.pop_back();
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
                "bug_type": "Comparator bug on equal values",
                "failure_description": {
                    "type": "Wrong Answer",
                    "failing_input": "3\n5 5 4\n",
                    "expected_output": "0 0 2\n",
                    "got_output": "0 1 2\n",
                },
                "diagnosis": [
                    "The task asks for the nearest strictly greater height.",
                    "Equal heights must not remain on the stack, because they are not valid answers.",
                ],
                "fix_explanation": "Pop while the stack top is less than or equal to the current height.",
                "fixed_code": SFT_CODE["azcp_p006"],
            },
            "gold",
            0.91,
        ),
    ]
)
