# Macro Tactical Allocation Engine (India ETF Rotation Strategy)

A systematic **cross-asset tactical allocation strategy** that rotates capital weekly between:

* NIFTY
* BANK NIFTY
* MIDCAP
* GOLD
* CASH (USD proxy)

using **momentum + macro regime logic**.

Designed for:

* low turnover execution (~6 switches/year)
* ETF-based implementation via Zerodha
* automated weekly signals
* Telegram delivery
* GitHub scheduled execution
* pilot capital deployment readiness
* future broker automation integration

---

# Strategy Objective

Generate **risk-adjusted alpha vs NIFTY benchmark** using disciplined ETF rotation.

Primary goals:

```
maximize long-term CAGR
reduce drawdowns
avoid prolonged equity bear phases
rotate into defensive assets during stress
maintain execution simplicity
```

Execution time required:

```
< 2 minutes per week
```

---

# Asset Universe

Strategy rotates across these assets:

| Asset     | Index Source | Zerodha ETF     |
| --------- | ------------ | --------------- |
| NIFTY     | ^NSEI        | NIFTYBEES       |
| BANK      | ^NSEBANK     | BANKBEES        |
| MIDCAP    | ^NSEMDCP50   | MID150CASE      |
| GOLD      | GC=F         | GOLDBEES        |
| USD proxy | INR=X        | Cash (no trade) |

---

# Strategy Logic

Allocator selects asset using hierarchical filtering:

```
Step 1: Detect macro regime
Step 2: Evaluate 6M + 12M momentum
Step 3: Rank equity leadership
Step 4: Apply crash override logic
Step 5: Apply minimum holding constraint
Step 6: Allocate capital to strongest asset
```

Fallback structure:

```
Equity → Gold → Cash
```

---

# Data Sources

Market data retrieved using:

```
yfinance
```

Tickers:

```
^NSEI
^NSEBANK
^NSEMDCP50
GC=F
INR=X
```

---

# Execution Schedule

Signal generation:

```
Friday after market close
```

Trade execution:

```
Monday market open
```

Execution frequency:

```
weekly evaluation
low turnover (~6 switches/year)
```

---

# Backtest Performance Snapshot

Example validated run:

```
Initial Capital: ₹100,000
Final Capital: ₹317,445
CAGR: ~13%
Max Drawdown: ~32%
Alpha vs NIFTY: positive
Beta vs NIFTY: ~0.64
Transitions: ~60 over 9.5 years
```

Strategy emphasizes:

```
consistency
discipline
drawdown control
```

over aggressive return maximization.

---

# Automation Pipeline

Weekly signal pipeline:

```
GitHub Actions scheduler
    ↓
daily_signal.py
    ↓
Telegram alert
    ↓
signal_logger.py
    ↓
signal_history.csv
```

Runs automatically every Friday.

---

# Telegram Signal Output Example

```
Switch Required: YES

SELL: GOLDBEES
BUY: MID150CASE
```

Message includes:

```
current signal
previous signal
switch decision
suggested ETF
portfolio NAV
allocator return
benchmark return
alpha vs NIFTY
active allocation
```

Execution-ready format for manual or future automated trading.

---

# Portfolio NAV Engine

NAV calculated using:

```
transition-cost-aware rotation model
```

Assumptions:

```
transition cost = 0.2%
full portfolio rotation
weekly evaluation
ETF proxy execution
```

NAV matches backtest execution logic.

---

# Signal History Tracking

Signals stored automatically inside:

```
signal_history.csv
```

Fields tracked:

```
timestamp
current signal
previous signal
switch required
ETF allocation
allocator return %
NIFTY return %
alpha %
```

Used for:

```
shadow deployment monitoring
Excel dashboard tracking
performance verification
execution audit trail
```

---

# Excel Dashboard Tracking

Performance tracked via:

```
signal_history.csv
```

inside:

```
Allocator_Dashboard.xlsx
```

Displays:

```
allocator NAV
benchmark NAV
alpha vs NIFTY
signal history
switch frequency
weekly performance trend
```

Auto-updates after each weekly signal run.

---

# Zerodha Execution Mapping

Production ETF mapping:

```
NIFTY → NIFTYBEES
BANK → BANKBEES
MIDCAP → MID150CASE
GOLD → GOLDBEES
USDINR → stay in cash
```

Execution method during pilot phase:

```
market orders
full capital rotation
Monday open execution
```

---

# Weekly Execution Workflow

Every Friday:

```
receive Telegram signal
```

If:

```
Switch Required = YES
```

Execute:

```
Sell previous ETF
Buy suggested ETF
```

Else:

```
Hold position
```

Execution time:

```
< 2 minutes/week
```

---

# Pilot Deployment Plan

Recommended pilot capital:

```
₹25,000 allocator portfolio
```

Benchmark tracked virtually via script.

Pilot goals:

```
validate signal stability
observe ETF liquidity behaviour
confirm NAV alignment with backtest
verify alpha persistence
test execution discipline
```

Pilot duration:

```
4–8 weeks
```

No parameter tuning allowed during pilot phase.

---

# Current System Capabilities

Strategy engine:

```
dual momentum allocator
macro regime filter
equity leadership ranking
crash protection logic
cash hedge fallback
minimum holding filter
```

Infrastructure:

```
weekly signal automation
Telegram execution alerts
ETF mapping for Zerodha
transition-cost NAV engine
benchmark comparison module
signal history logging
walk-forward testing module
rolling performance analytics
optimizer support module
monthly reporting module
```

Deployment status:

```
shadow deployment complete
pilot capital deployment ready
```

---

# Repository Structure

Core modules:

```
strategy.py
backtest.py
daily_signal.py
portfolio_nav.py
data_loader.py
config.py
```

Analytics modules:

```
performance_metrics.py
rolling_performance.py
benchmark_comparison.py
trade_frequency.py
monthly_report.py
walk_forward.py
optimizer.py
```

Execution & automation:

```
telegram_alert.py
signal_logger.py
portfolio_tracker.py
```

Environment:

```
pyproject.toml
requirements.txt
uv.lock
```

---

# Strategy Philosophy

Allocator principles:

```
slow signals
low turnover
full capital rotation
ETF-only execution
benchmark-relative alpha generation
weekly discipline
automation-ready architecture
```

Designed for:

```
long-term capital growth
drawdown protection
simple execution workflow
future broker automation
```

---

# Roadmap

## v1.1 (Current)

```
pilot deployment ready
Zerodha ETF mapping complete
Telegram execution alerts active
signal history logging enabled
NAV engine validated
```

---

## v1.2 (Next)

Pilot execution validation phase

```
₹25k allocator deployment
weekly NAV monitoring
ETF spread observation
signal stability verification
```

---

## v1.3

Execution monitoring layer

```
drawdown alert module
rolling alpha monitor
regime warning signals
switch-frequency anomaly detection
```

---

## v1.4

Broker automation integration

Planned:

```
Zerodha Kite Connect API
```

Pipeline becomes:

```
GitHub signal
→ Telegram confirmation
→ automatic ETF execution
```

---

## v2.0

Allocator desk upgrade

Planned features:

```
global equity overlay
volatility targeting module
risk budgeting engine
ETF tracking error monitor
execution slippage monitor
multi-asset expansion
```

---

# Execution Rules

Always:

```
rotate full portfolio value
```

Never:

```
partially rebalance
```

Signal timing:

```
evaluate Friday
execute Monday
```

Pilot rule:

```
no parameter changes during validation phase
```

Monitoring rule:

```
track alpha vs NIFTY weekly
```

---

# Version

Current version:

```
Macro Tactical Allocation v1.1
```

Status:

```
Pilot Deployment Ready
```
