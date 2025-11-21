import numpy as np

# СПІЛЬНІ ДАНІ
PROFIT_X, PROFIT_Y = 4, 3   # Цільові коефіцієнти
LIMIT_A = 10                # 2x + y <= 10
LIMIT_B = 8                 # x + 2y <= 8

print(f"ЗАДАЧА: Максимізувати {PROFIT_X}x + {PROFIT_Y}y при обмеженнях")
print(f"         2x + y <= {LIMIT_A}")
print(f"         x + 2y <= {LIMIT_B}")

# ==========================================
# 1. SciPy
# ==========================================
import scipy.optimize as sco 
def scipy_solution():
    objective = lambda v: -(PROFIT_X*v[0] + PROFIT_Y*v[1]) 
    cons = (
        {'type': 'ineq', 'fun': lambda v: LIMIT_A - (2*v[0] + 1*v[1])},
        {'type': 'ineq', 'fun': lambda v: LIMIT_B - (1*v[0] + 2*v[1])}
    )
    bnds = ((0, None), (0, None))
    res = sco.minimize(objective, [0, 0], method='SLSQP', bounds=bnds, constraints=cons)
    print(f"[SciPy]   X={res.x[0]:.2f}, Y={res.x[1]:.2f} -> Прибуток: {-res.fun:.2f}")

# ==========================================
# 2. CVXPY
# ==========================================
import cvxpy as cp
def cvxpy_solution():
    x = cp.Variable()
    y = cp.Variable()
    objective = cp.Maximize(PROFIT_X*x + PROFIT_Y*y)
    constraints = [
        2*x + y <= LIMIT_A,
        x + 2*y <= LIMIT_B,
        x >= 0, y >= 0
    ]
    prob = cp.Problem(objective, constraints)
    prob.solve()
    print(f"[CVXPY]   X={x.value:.2f}, Y={y.value:.2f} -> Прибуток: {prob.value:.2f}")

# ==========================================
# 3. Pyomo
# ==========================================
from pyomo.environ import *
def pyomo_solution():
    model = ConcreteModel()
    model.x = Var(domain=NonNegativeReals)
    model.y = Var(domain=NonNegativeReals)
    # Чітке розділення на цілі та правила
    model.obj = Objective(expr=PROFIT_X*model.x + PROFIT_Y*model.y, sense=maximize)
    model.con1 = Constraint(expr=2*model.x + model.y <= LIMIT_A)
    model.con2 = Constraint(expr=model.x + 2*model.y <= LIMIT_B)
    print(f"[Pyomo]   (Код моделі готовий. Потребує зовнішнього солвера)")

# ==========================================
# 4. GEKKO 
# ==========================================
from gekko import GEKKO
def gekko_solution():
    m = GEKKO(remote=False)
    x, y = m.Var(lb=0), m.Var(lb=0)
    m.Maximize(PROFIT_X*x + PROFIT_Y*y)
    m.Equation(2*x + y <= LIMIT_A)
    m.Equation(x + 2*y <= LIMIT_B)
    m.solve(disp=False)
    print(f"[GEKKO]   X={x.value[0]:.2f}, Y={y.value[0]:.2f} -> Прибуток: {m.options.OBJFCNVAL*-1:.2f}")

# ==========================================
# 5. Optuna (Метод "Чорної скриньки" / ML)
# ==========================================
import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)
def optuna_solution():
    def objective(trial):
        x = trial.suggest_float('x', 0, 10)
        y = trial.suggest_float('y', 0, 10)
        if (2*x + y > LIMIT_A) or (x + 2*y > LIMIT_B):
            return -1000
        return PROFIT_X*x + PROFIT_Y*y
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=1000)
    best = study.best_params
    val = study.best_value
    print(f"[Optuna]  X={best['x']:.2f}, Y={best['y']:.2f} -> Прибуток: {val:.2f} (Приблизно)")

# ЗАПУСК 
if __name__ == "__main__":
    scipy_solution()
    cvxpy_solution()
    gekko_solution()
    optuna_solution()
    optuna_solution()
    optuna_solution()
    optuna_solution()
    #pyomo_solution() # солвер не встановлено