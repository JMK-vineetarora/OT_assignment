import numpy as np

cost = np.array([
    [14, 16, 13, 11],
    [18, 10, 18, 11],
    [5, 11, 15, 18]
], dtype=float)

allocation = np.array([
    [0, 0, 63, 0],
    [0, 40, 64, 53],
    [70, 43, 0, 0]
], dtype=float)


def get_potentials(cost, allocation):
    rows, cols = cost.shape

    basic = [
        (i, j)
        for i in range(rows)
        for j in range(cols)
        if allocation[i, j] > 0
    ]

    u = [None] * rows
    v = [None] * cols

    u[0] = 0

    while None in u or None in v:
        changed = False

        for i, j in basic:
            if u[i] is not None and v[j] is None:
                v[j] = cost[i, j] - u[i]
                changed = True

            elif v[j] is not None and u[i] is None:
                u[i] = cost[i, j] - v[j]
                changed = True

        if not changed:
            break

    return u, v, basic


def find_loop(basic, start):
    cells = set(basic)
    cells.add(start)

    def search(path, move_in_row):
        current = path[-1]

        if move_in_row:
            candidates = [
                cell for cell in cells
                if cell[0] == current[0]
                and cell != current
            ]
        else:
            candidates = [
                cell for cell in cells
                if cell[1] == current[1]
                and cell != current
            ]

        for next_cell in candidates:
            if next_cell == start:
                if len(path) >= 4 and len(path) % 2 == 0:
                    return path

                continue

            if next_cell in path:
                continue

            path.append(next_cell)

            result = search(path, not move_in_row)

            if result is not None:
                return result

            path.pop()

        return None

    loop = search([start], True)

    if loop is None:
        loop = search([start], False)

    return loop


iteration = 1

while True:
    u, v, basic = get_potentials(cost, allocation)

    opportunity = np.full(cost.shape, np.nan)

    for i in range(cost.shape[0]):
        for j in range(cost.shape[1]):
            if (i, j) not in basic:
                opportunity[i, j] = (
                    cost[i, j]
                    - u[i]
                    - v[j]
                )

    print("\nMODI Iteration", iteration)

    print("u =", u)
    print("v =", v)

    print("\nOpportunity Costs")
    print(opportunity)

    minimum = 0
    entering = None

    for i in range(cost.shape[0]):
        for j in range(cost.shape[1]):
            if not np.isnan(opportunity[i, j]):
                if opportunity[i, j] < minimum:
                    minimum = opportunity[i, j]
                    entering = (i, j)

    if entering is None:
        print("\nAll opportunity costs are non-negative.")
        print("Optimal solution reached.")
        break

    print("\nEntering cell =", entering)

    loop = find_loop(basic, entering)

    print("Closed loop =", loop)

    theta = min(
        allocation[i, j]
        for k, (i, j) in enumerate(loop)
        if k % 2 == 1
    )

    print("Theta =", theta)

    for k, (i, j) in enumerate(loop):
        if k % 2 == 0:
            allocation[i, j] += theta
        else:
            allocation[i, j] -= theta

    iteration += 1

total_cost = np.sum(allocation * cost)

print("\nOPTIMAL ALLOCATION")
print(allocation.astype(int))

print(
    "\nMinimum transportation cost =",
    int(total_cost),
    "thousand IDR"
)
