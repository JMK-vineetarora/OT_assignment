import numpy as np

cost = np.array([
    [14, 16, 13, 11],
    [18, 10, 18, 11],
    [5, 11, 15, 18]
], dtype=float)

supply = np.array([63, 157, 113], dtype=float)

demand = np.array([70, 83, 127, 53], dtype=float)

warehouses = ["G1", "G2", "G3"]
outlets = ["O1", "O2", "O3", "O4"]


def penalty(values):
    values = sorted(values)

    if len(values) == 1:
        return values[0]

    return values[1] - values[0]


allocation = np.zeros_like(cost)

step = 1

while supply.sum() > 0:
    rows = [i for i in range(3) if supply[i] > 0]
    cols = [j for j in range(4) if demand[j] > 0]

    row_penalty = {}

    for i in rows:
        values = [cost[i, j] for j in cols]
        row_penalty[i] = penalty(values)

    col_penalty = {}

    for j in cols:
        values = [cost[i, j] for i in rows]
        col_penalty[j] = penalty(values)

    max_row = max(row_penalty, key=row_penalty.get)
    max_col = max(col_penalty, key=col_penalty.get)

    if row_penalty[max_row] >= col_penalty[max_col]:
        i = max_row
        j = min(cols, key=lambda j: cost[i, j])
    else:
        j = max_col
        i = min(rows, key=lambda i: cost[i, j])

    quantity = min(supply[i], demand[j])

    allocation[i, j] += quantity

    supply[i] -= quantity
    demand[j] -= quantity

    print(
        "Step", step,
        ":",
        warehouses[i], "->", outlets[j],
        "=", int(quantity)
    )

    step += 1

total_cost = np.sum(allocation * cost)

print("\nVAM ALLOCATION")
print(allocation.astype(int))

print(
    "\nInitial transportation cost =",
    int(total_cost),
    "thousand IDR"
)
