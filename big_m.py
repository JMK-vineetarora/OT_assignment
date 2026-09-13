import numpy as np

M = 1000000

names = [
    "x1", "x2", "x3", "x4",
    "s1", "s2", "s3", "s4", "s5",
    "A1", "A2", "A3", "A4"
]

A = np.array([
    [44.974, 25.560, 20.874, 67.344,
     0, 0, 0, 0, 0,
     1, 0, 0, 0],

    [2.1583, 2.1780, 1.9454, 2.7968,
     -1, 0, 0, 0, 0,
     0, 1, 0, 0],

    [8.2716, 1.5240, 2.5418, 13.6528,
     0, -1, 0, 0, 0,
     0, 0, 1, 0],

    [8.2716, 1.5240, 2.5418, 13.6528,
     0, 0, 1, 0, 0,
     0, 0, 0, 0],

    [0.3503, 1.1940, 0.3266, 0.1288,
     0, 0, 0, -1, 0,
     0, 0, 0, 1],

    [0.3503, 1.1940, 0.3266, 0.1288,
     0, 0, 0, 0, 1,
     0, 0, 0, 0]
], dtype=float)

b = np.array([
    3035,
    84,
    341.4375,
    493.1875,
    67.4444,
    118.0278
], dtype=float)

c = np.array([
    -1, -1, -1, -1,
     0,  0,  0,  0,  0,
    -M, -M, -M, -M
], dtype=float)

basis = [9, 10, 11, 6, 12, 8]

for iteration in range(50):
    cb = c[basis]

    zj = cb @ A
    cj_zj = c - zj

    entering = np.argmax(cj_zj)

    if cj_zj[entering] <= 1e-9:
        break

    ratios = []

    for i in range(len(b)):
        if A[i, entering] > 0:
            ratios.append(b[i] / A[i, entering])
        else:
            ratios.append(np.inf)

    leaving = np.argmin(ratios)

    print(
        "Iteration", iteration + 1,
        "| Entering:", names[entering],
        "| Leaving:", names[basis[leaving]]
    )

    pivot = A[leaving, entering]

    A[leaving] = A[leaving] / pivot
    b[leaving] = b[leaving] / pivot

    for i in range(len(b)):
        if i != leaving:
            factor = A[i, entering]

            A[i] = A[i] - factor * A[leaving]
            b[i] = b[i] - factor * b[leaving]

    basis[leaving] = entering

solution = np.zeros(len(names))

for i in range(len(basis)):
    solution[basis[i]] = b[i]

x1 = solution[0]
x2 = solution[1]
x3 = solution[2]
x4 = solution[3]

Z = x1 + x2 + x3 + x4

print("\nOPTIMAL SOLUTION")
print("----------------")

print("Wheat   x1 =", round(x1, 4), "m^2")
print("Soybean x2 =", round(x2, 4), "m^2")
print("Lettuce x3 =", round(x3, 4), "m^2")
print("Potato  x4 =", round(x4, 4), "m^2")

print("\nMinimum total growing area =", round(Z, 4), "m^2")

print("\nArtificial Variables")
print("A1 =", round(solution[9], 6))
print("A2 =", round(solution[10], 6))
print("A3 =", round(solution[11], 6))
print("A4 =", round(solution[12], 6))
