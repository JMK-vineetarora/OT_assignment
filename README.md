# Operations Techinques Assignment - Big-M, VAM and MODI

This repository contains my Python implementations for two Operations Research problems:

1. A crop allocation problem solved using the **Big-M Simplex Method**
2. A transportation problem solved using **Vogel's Approximation Method (VAM)** and **MODI**

The main purpose of the assignment was to implement the methods myself and understand how each algorithm reaches its solution, rather than using an optimization library to solve the problems directly.
 
---

## 1. Big-M Simplex Method

### NASA Crop Allocation Problem

For the first problem, I used a crop allocation model based on NASA research related to growing food for long-duration space missions.

The model considers four crops:

- Wheat
- Soybean
- Lettuce
- Potato

The goal is to find the minimum cultivation area required to meet a set of nutritional requirements.

### Decision Variables

```text
x1 = Area used for wheat
x2 = Area used for soybean
x3 = Area used for lettuce
x4 = Area used for potato
```

All areas are measured in square metres.

### Objective Function

The objective is:

```text
Minimize

Z = x1 + x2 + x3 + x4
```

The constraints represent requirements for:

- Energy
- Protein
- Carbohydrates
- Fat

Since the problem contains equality, `>=`, and `<=` constraints, the simplex setup requires slack, surplus, and artificial variables.

The artificial variables are handled using the **Big-M Method**. In the program, I used:

```python
M = 1000000
```

### Result

The final solution is:

```text
Wheat   = 0.0000 m²
Soybean = 53.8285 m²
Lettuce = 0.0000 m²
Potato  = 24.6369 m²
```

Minimum total cultivation area:

```text
78.4653 m²
```

All artificial variables are zero in the final solution, so the original linear programming problem is feasible.

For this model, soybean and potato are selected because they satisfy the nutritional constraints with the least total area.

This is still a simplified model. A real crop system for space missions would also need to consider things such as vitamins, minerals, water use, crop reliability, food variety, growth time, and other life-support requirements.

---

## 2. Transportation Problem

The second problem is a transportation problem involving three warehouses and four outlets.

### Warehouses

```text
G1
G2
G3
```

### Outlets

```text
O1
O2
O3
O4
```

The transportation cost table is:

| Warehouse | O1 | O2 | O3 | O4 | Supply |
|---|---:|---:|---:|---:|---:|
| G1 | 14 | 16 | 13 | 11 | 63 |
| G2 | 18 | 10 | 18 | 11 | 157 |
| G3 | 5 | 11 | 15 | 18 | 113 |
| **Demand** | **70** | **83** | **127** | **53** | |

The transportation costs are given in **thousand Indonesian Rupiah per unit**.

Total supply:

```text
63 + 157 + 113 = 333
```

Total demand:

```text
70 + 83 + 127 + 53 = 333
```

Since total supply is equal to total demand, the problem is balanced.

---

## Vogel's Approximation Method

The file `vam.py` uses **Vogel's Approximation Method** to find an Initial Basic Feasible Solution.

The method calculates penalties for the active rows and columns, chooses the largest penalty, and assigns as much as possible to the cheapest available cell.

The allocation obtained is:

```text
[[ 0  0 63  0]
 [ 0 40 64 53]
 [70 43  0  0]]
```

The transportation cost of this solution is:

```text
3777 thousand IDR
```

which is approximately:

```text
Rp 3,777,000
```

---

## MODI Method

The file `modi.py` starts from the VAM solution and uses the **Modified Distribution Method (MODI)** to check whether the allocation can be improved.

For every occupied cell, the row and column potentials satisfy:

```text
ui + vj = cij
```

For an unoccupied cell, the opportunity cost is calculated as:

```text
Δij = cij - ui - vj
```

If all opportunity costs are non-negative, the current solution is optimal.

In this case, the first MODI iteration finds a negative opportunity cost of:

```text
-4
```

for the `G3 -> O3` cell.

The corresponding loop is:

```text
G3-O3  (+)
G3-O2  (-)
G2-O2  (+)
G2-O3  (-)
```

with:

```text
theta = 43
```

After updating the allocations, the final transportation plan becomes:

```text
[[ 0  0 63  0]
 [ 0 83 21 53]
 [70  0 43  0]]
```

The minimum transportation cost is:

```text
3605 thousand IDR
```

or approximately:

```text
Rp 3,605,000
```

Compared with the initial VAM solution, MODI reduces the cost by:

```text
172 thousand IDR
```

---

## Results

| Problem | Method | Result |
|---|---|---|
| Crop Allocation | Big-M Simplex | Minimum area = **78.4653 m²** |
| Transportation | VAM | Initial cost = **3777 thousand IDR** |
| Transportation | MODI | Minimum cost = **3605 thousand IDR** |

---

## Repository Structure

```text
operations-research-assignment/
│
├── README.md
├── big_m.py
├── vam.py
├── modi.py
│
└── outputs/
    ├── big_m_output.png
    ├── vam_output.png
    └── modi_output.png
```

---

## Requirements

The programs use Python and NumPy.

Install NumPy with:

```bash
pip install numpy
```

---

## Running the Programs

Big-M Simplex:

```bash
python big_m.py
```

Vogel's Approximation Method:

```bash
python vam.py
```

MODI:

```bash
python modi.py
```

The MODI program uses the VAM allocation as its starting solution.

---

## References

### NASA Crop Allocation

NASA Biomass Production Chamber:

https://ntrs.nasa.gov/search.jsp?R=20040089951

Crop productivity research:

https://www.sciencedirect.com/science/article/pii/S0273117707007065

NASA crop composition research:

https://ntrs.nasa.gov/search.jsp?R=20040089944

NASA Human-System Standard — Food and Nutrition:

https://www.nasa.gov/reference/7-0-habit-ability-functions-vol-2/

### Transportation Problem

The transportation dataset is based on the following published case study:

**Minimize Shipping Costs from Multi-Warehouse to Multi-Outlet with VAM and MODI**

https://ejournal.isha.or.id/index.php/Mandiri/article/view/506

---

## Note

The algorithms in this repository were implemented directly in Python instead of using functions such as `scipy.optimize.linprog()`.

The purpose of the assignment was to understand how the methods work internally:

- Big-M handles artificial variables in simplex problems.
- VAM provides an initial transportation solution.
- MODI checks that solution and improves it when a lower-cost allocation is possible.
