"""Re-checks every number in FINANCE_PLAN.md. Run: python3 tools/check_plan.py"""

OD_LIMIT = 600.00
start_balance = -600.00          # overdraft maxed
sept_pay = 983.00                # lands Wed 30 Sep 2026

# Debts
ls_a_due, ls_a_owed = 141.48, 143.06
ls_b_due, ls_b_owed = 316.20, 318.00
cc_balance, cc_min, cc_apr = 1179.29, 51.70, 0.30
friend = 66.00

# Monthly costs (October: 22 working days, November: 21)
def fixed(days, revolut=15.0):
    train = 7 * days
    lunch = round(5 * days * 3 / 5, 2)   # buy lunch 3 of 5 days
    return {"rent": 200, "train": train, "lunch": lunch, "gym": 30,
            "spotify": 12, "claude": 20, "revolut": revolut}

LIVING = 250.00  # food shop, phone, toiletries, going out - NOT in Steven's list, assumed

print("== Maths checks ==")
print(f"Total debt stated ~2,240 -> actual {143.06+318+1179.29+600:,.2f}")
print(f"Incl. friend -> {143.06+318+1179.29+600+friend:,.2f}")
print(f"Train 7x5x52/12 = {7*5*52/12:.2f}  Lunch 5x5x52/12 = {5*5*52/12:.2f}  Lunch 3 days = {5*3*52/12:.2f}")
tax = (27835 - 12570) * 0.20
ni = (27835 - 12570) * 0.08
pension = (27835 - 6240) * 0.05
print(f"Take-home no pension: {(27835-tax-ni)/12:,.2f}/mo | with 5% pension: {(27835-tax-ni-pension)/12:,.2f}/mo")
print(f"LendingStream leftovers after due payments: A {ls_a_owed-ls_a_due:.2f}, B {ls_b_owed-ls_b_due:.2f}")

def october(label, defer_friend, defer_ls_b, revolut, living):
    f = fixed(22, revolut)
    out = sum(f.values()) + cc_min + ls_a_due + living
    out += 0 if defer_friend else friend
    out += 0 if defer_ls_b else ls_b_due
    end = start_balance + sept_pay - out
    print(f"{label:<45} out {out:8.2f}  low point {end:8.2f}  headroom {end+OD_LIMIT:8.2f}"
          + ("  <-- BREAKS LIMIT" if end < -OD_LIMIT else ""))
    return end

print("\n== October (30 Sep -> 30 Oct) ==")
october("As listed, no living costs", False, False, 15, 0)
october("As listed + living costs", False, False, 15, LIVING)
october("Revolut free + friend waits", True, False, 0, 0)
end = october("Revolut free + friend waits + LS B moved", True, True, 0, 0)
print(f"  -> left for food/phone in October: {end+OD_LIMIT:.2f}")

print("\n== From 30 Oct payday ==")
for pay in (1963.40, 1873.42):
    bal, cc = end, cc_balance
    bal += pay - friend - ls_b_due
    month = 0
    names = ["Nov", "Dec", "Jan", "Feb", "Mar"]
    while cc > 0.005:
        f = fixed(21, 0)
        costs = sum(f.values()) + LIVING
        cc += cc * cc_apr / 12
        spare = bal - costs - 150      # keep a 150 buffer
        payment = min(cc, max(cc_min, spare))
        cc -= payment
        bal -= costs + payment
        print(f"  pay {pay:.0f}: {names[month]} card payment {payment:8.2f} card left {cc:8.2f} balance after {bal:8.2f}")
        bal += pay
        month += 1
