# Pattern Research Phase 1

Date: 2026-06-23

---

# Dataset

- Universe: 95 Stocks
- Total Signals: 2325
- Lookahead Period: 60 Days

---

# Pattern Counts

| Pattern | Signals |
|----------|---------:|
| DOUBLE_BOTTOM | 1344 |
| DOUBLE_BOTTOM_V2 | 75 |
| ROUNDING_BOTTOM | 353 |
| ROUNDING_BOTTOM_V2 | 388 |
| ROUNDING_BOTTOM_V3 | 165 |

---

# Average Returns

| Pattern | Avg Return (%) |
|----------|---------:|
| ROUNDING_BOTTOM_V3 | 4.61 |
| ROUNDING_BOTTOM_V2 | 4.51 |
| ROUNDING_BOTTOM | 4.00 |
| DOUBLE_BOTTOM | 3.99 |
| DOUBLE_BOTTOM_V2 | 1.68 |

---

# Outcomes

| Pattern | Wins | Losses | Time Exits |
|----------|------:|------:|------:|
| DOUBLE_BOTTOM | 332 | 104 | 908 |
| DOUBLE_BOTTOM_V2 | 21 | 8 | 46 |
| ROUNDING_BOTTOM | 63 | 10 | 280 |
| ROUNDING_BOTTOM_V2 | 87 | 19 | 279 |
| ROUNDING_BOTTOM_V3 | 32 | 4 | 129 |

---

# Average Winner / Loser

| Pattern | Avg Win (%) | Avg Loss (%) |
|----------|---------:|---------:|
| ROUNDING_BOTTOM_V3 | 22.77 | -20.66 |
| ROUNDING_BOTTOM | 22.47 | -20.90 |
| ROUNDING_BOTTOM_V2 | 19.26 | -15.66 |
| DOUBLE_BOTTOM | 18.97 | -17.29 |
| DOUBLE_BOTTOM_V2 | 16.39 | -19.59 |

---

# Average Holding Period

| Pattern | Avg Days |
|----------|---------:|
| DOUBLE_BOTTOM | 50.31 |
| ROUNDING_BOTTOM_V2 | 51.31 |
| ROUNDING_BOTTOM | 54.03 |

---

# Conclusions

## ROUNDING_BOTTOM_V3

Strengths:
- Highest average return
- Lowest number of losses
- Highest quality signals

Weaknesses:
- Lower signal count

Status:
- ACTIVE
- Current Champion

---

## ROUNDING_BOTTOM_V2

Strengths:
- Excellent balance between quality and quantity
- Strong average return
- Good win/loss profile

Status:
- ACTIVE

---

## ROUNDING_BOTTOM

Strengths:
- Strong average winner
- Reliable pattern

Status:
- ACTIVE

---

## DOUBLE_BOTTOM

Strengths:
- Largest number of signals
- Good diversification pattern
- Fastest pattern

Status:
- ACTIVE

---

## DOUBLE_BOTTOM_V2

Strengths:
- Higher filtering

Weaknesses:
- Average return collapsed
- Signal count reduced dramatically
- Worse risk/reward profile

Status:
- RETIRED

---

# Next Research Phase

Patterns to Add:

1. Cup & Handle
2. Ascending Triangle
3. Bull Flag
4. Falling Wedge
5. Inverse Head & Shoulders
6. VCP (Volatility Contraction Pattern)

---

# Future Research

- Expand universe from 95 stocks to Nifty 500
- Add Relative Strength filter
- Add Volume Breakout scoring
- Add Pattern Leaderboard table
- Train ML model on winning vs losing patterns