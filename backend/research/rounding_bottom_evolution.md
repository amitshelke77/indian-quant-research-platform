# Rounding Bottom Research Evolution

## Objective

Improve the quality of rounding bottom breakout signals using data-driven filters rather than adding complexity blindly.

---

## V1 - ROUNDING_BOTTOM

Signals: 353

Average Return: 4.00%

Notes:

* Basic rounding bottom detection.
* Large number of mediocre signals.

---

## V2 - ROUNDING_BOTTOM_V2

Signals: 388

Average Return: 4.51%

Improvement:

* Better breakout detection.
* Slight increase in average return.

---

## V3 - ROUNDING_BOTTOM_V3

Signals: 165

Average Return: 4.61%

Enhancements:

* EMA50 > EMA200 trend filter.
* Volume breakout filter.
* Cooldown logic.

Result:

* Fewer signals.
* Better signal quality.

---

## V4 - ROUNDING_BOTTOM_V4

Additional Filter:

* RSI >= 70

Signals: 123

Average Return: 5.74%

Improvement:

* Removed many low-quality trades.
* Average return improved by approximately 25%.

---

## V5 - ROUNDING_BOTTOM_V5

Additional Filter:

* RSI >= 70
* Volume Ratio >= 1.5
* Volume Ratio < 2.0

Signals: 53

Average Return: 8.10%

Outcome Distribution:

* WIN: 13
* TIME_EXIT: 40
* LOSS: 0

Observations:

* Best performing detector so far.
* Signals span 2022-2026.
* TIME_EXIT trades remain profitable on average.
* Strong evidence that moderate volume expansion performs better than extreme volume spikes.

---

## Key Findings

RSI Analysis:

* RSI < 70 → 1.69%
* RSI >= 70 → 6.15%

Volume Analysis:

* Volume Ratio < 2 → 8.81%
* Volume Ratio >= 2 → 4.45%

Conclusion:

Signal filtering generated significantly more improvement than adding new patterns.

Future work:

* V6 trend-strength filter
* Maximum excursion analysis
* Dynamic targets
* ATR exits
* Portfolio-level backtesting
