from datetime import datetime, timedelta
from collections import defaultdict

# Input bills
april_bill = 5018
may_bill = 9684

# Generate per-day cost
april_days = (30 - 16 + 1)  # 16 to 30 inclusive
may_days = 31

april_per_day = april_bill / april_days
may_per_day = may_bill / may_days

# Helper function to generate date ranges
def daterange(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

# Create a dictionary with each date and who was present
stay_map = {}

# Date ranges with residents
date_ranges = [
    ("2024-04-16", "2024-04-16", ["A", "J", "P"]),
    ("2024-04-17", "2024-04-20", ["A", "J"]),
    ("2024-04-21", "2024-04-24", ["A", "J", "P"]),
    ("2024-04-25", "2024-04-30", ["A", "P"]),
    ("2024-05-01", "2024-05-02", ["A", "P"]),
    ("2024-05-03", "2024-05-05", ["P"]),
    ("2024-05-05", "2024-05-16", ["A", "P"]),
    ("2024-05-16", "2024-05-19", ["P"]),
    ("2024-05-19", "2024-05-24", ["J", "P"]),
    ("2024-05-25", "2024-05-28", ["A", "J", "P"]),
    ("2024-05-29", "2024-05-31", ["A", "J"]),
]

# Populate stay_map
for start_str, end_str, people in date_ranges:
    start = datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.strptime(end_str, "%Y-%m-%d")
    for d in daterange(start, end):
        stay_map[d] = people

# Initialize individual cost trackers
person_costs = defaultdict(float)

# Compute individual shares
for date, people in stay_map.items():
    cost = april_per_day if date.month == 4 else may_per_day
    split_cost = cost / len(people)
    for person in people:
        person_costs[person] += split_cost

# Total bill and equal share
total_bill = april_bill + may_bill
equal_share = total_bill / 3

# Calculate adjustments
adjustments = {p: person_costs[p] - equal_share for p in ["A", "J", "P"]}

print(person_costs)
print(equal_share)
print(adjustments)
