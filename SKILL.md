---
name: personal-asset-allocation
description: Analyze personal cash flow, emergency reserves, fund and ETF holdings, asset concentration, target allocation, recurring investment plans, rebalancing, and investment decision records. Use when the user asks for a monthly financial review, portfolio diagnosis, fund allocation, contribution plan, risk check, rebalancing advice, compounding projection, or provides holdings screenshots, statements, CSV/XLSX files, or account values for personal wealth planning.
---

# Personal Asset Allocation

Build a repeatable personal wealth system. Optimize for survival, disciplined contributions, diversification, low friction, and decisions the user can actually hold through drawdowns. Do not predict short-term prices or promise returns.

## Workflow

1. Extract or request only decision-critical inputs:
   - monthly after-tax income;
   - essential and flexible expenses;
   - high-interest debt;
   - emergency cash;
   - holdings with current values;
   - money-use horizon, drawdown tolerance, and major goals.
2. Separate emergency money and money needed within three years from long-term investments.
3. Calculate savings rate, emergency-fund coverage, asset weights, concentration, target drift, and monthly investable amount. Use `scripts/analyze_portfolio.py` when structured values are available.
4. Classify the portfolio as defensive, balanced, growth, aggressive, or concentrated. Distinguish a diversified aggressive portfolio from a single-market bet.
5. Propose one primary target allocation. State assumptions and show a lower-risk alternative only when it materially helps the decision.
6. Prefer redirecting new contributions over immediate selling. Recommend selling only when concentration, product defects, fees, liquidity needs, or target drift justify it.
7. Produce an exact salary-day transfer plan and a rebalancing rule.
8. Record the decision conditions: expected holding period, acceptable drawdown, thesis, and conditions that would change the plan.

## Guardrails

- Pay high-interest debt before risk investing unless the user gives a compelling reason otherwise.
- Target 4–6 months of essential expenses as emergency reserves; use 6–12 months for unstable income or dependants.
- Keep emergency reserves in liquid, low-volatility instruments and outside portfolio return calculations.
- Treat equity, sector, country, currency, duration, credit, commodity, and product overlap as separate risks.
- Flag a single narrow index, sector, or theme above 30% as concentrated; above 40% as highly concentrated.
- Do not call a fund diversified merely because it holds many securities if one country, sector, or factor dominates.
- Explain plausible portfolio loss in yuan, not only percentages.
- Treat projected returns as scenarios, not forecasts. Show contributions separately from investment growth.
- Never recommend leverage, borrowing to invest, or frequent tactical trading as a default.
- Check current product rules, fees, taxes, trading restrictions, and regulations using authoritative sources when they affect the recommendation.

## Output

Lead with a verdict, then provide:

1. Financial foundation: surplus, savings rate, emergency coverage, debt priority.
2. Current portfolio: values, percentages, overlaps, and the two largest risks.
3. Target allocation: percentages and purpose of each sleeve.
4. Action plan: exact monthly amounts, what to pause, continue, or consolidate.
5. Rebalancing: review every six months or when an asset deviates by more than 5 percentage points; prefer new cash flows.
6. Stress test: estimated yuan loss at portfolio declines of 20%, 30%, and 40%, plus the behavior required to stay invested.
7. Missing information that could materially change the plan.

Keep fund counts low unless added complexity has a clear diversification benefit. Use plain Chinese when the user writes in Chinese.

## Resources

- Read `references/default-profile.md` when working for the current user; treat its values as editable defaults, not permanent facts.
- Read `references/methodology.md` for formulas, allocation checks, and decision rules.
- Use `references/example-input.json` as the structured-input schema for `scripts/analyze_portfolio.py`.

