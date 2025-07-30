from collections import defaultdict
from datetime import datetime, timedelta

# Total bill for June
total_bill = 11077.24
total_days = 30
per_day_cost = total_bill / total_days

# Define stay data for each date
date_ranges = {
    (1, 6): ['A', 'J'],
    (7, 8): ['A'],
    (9, 25): ['A', 'J', 'P'],
    (26, 29): ['A', 'P'],
    (30, 30): ['A', 'J', 'P'],
}

# Create a mapping of each day to people present
daily_share = defaultdict(list)

for date_range, people in date_ranges.items():
    start, end = date_range
    for day in range(start, end + 1):
        daily_share[day] = people

# Initialize cost per person
person_cost = defaultdict(float)

# Distribute cost per day based on presence
print("Daily cost distribution:")
for day in range(1, 31):
    people = daily_share[day]
    share_per_person = per_day_cost / len(people)
    for person in people:
        person_cost[person] += share_per_person
    print(f"Day {day:2d}: {people} => {per_day_cost:.2f} split into {share_per_person:.2f} each")

# Calculate originally paid amount (equal split)
equal_split = total_bill / 3

print("\nFinal cost per person based on actual stay:")
for person in ['A', 'J', 'P']:
    print(f"{person}: {person_cost[person]:.2f}")

print("\nEqual split amount per person: {:.2f}".format(equal_split))

print("\nAdjustment needed (positive means the person should receive money, negative means they should pay):")
for person in ['A', 'J', 'P']:
    adjustment = equal_split - person_cost[person]
    print(f"{person}: {adjustment:+.2f}")
