from datetime import date, timedelta

# Total bill
total_bill = 11077.24

# Stay details
stay_info = [
    (1, 6, ['A', 'J']),
    (7, 8, ['A']),
    (9, 25, ['A', 'J', 'P']),
    (26, 29, ['A', 'P']),
    (30, 30, ['A', 'J', 'P'])
]

# Create a dict to hold daily share
daily_cost = total_bill / 30
contributions = {'A': 0.0, 'J': 0.0, 'P': 0.0}

# Calculate per-day contributions
for start, end, people in stay_info:
    days = end - start + 1
    for person in people:
        contributions[person] += (daily_cost * days) / len(people)

# Round to 2 decimal places for readability
contributions = {k: round(v, 2) for k, v in contributions.items()}

# Initial equal payment
initial_paid = round(total_bill / 3, 2)

# Net adjustment
adjustment = {k: round(contributions[k] - initial_paid, 2) for k in contributions}

# Output
print("Total Bill: ₹", total_bill)
print("Daily Cost: ₹", round(daily_cost, 2))
print("\nActual Share Based on Stay:")
for k in contributions:
    print(f"{k}: ₹{contributions[k]}")

print("\nEach Paid Initially: ₹", initial_paid)
print("\nAdjustment Needed (+ means pay more, - means get back):")
for k in adjustment:
    print(f"{k}: ₹{adjustment[k]}")
