from dataclass_models import Task
from dataclasses import asdict
import math
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Any

data_predictors = ["days_until_due",
            "duration_in_minutes",
            "priority_level",
            "energy_required",
            "available_time_minutes"]


def fit_beta_success(tasks: List[Task]) -> np.ndarray:
    """Returns a 6-element beta vector (of the intercept  + the 5 predictors betas) against succcess."""

    df = pd.DataFrame([asdict(t) for t in tasks])

    # get x values in matrix format
    x = df[data_predictors].astype(float)
    x.insert(0, "intercept", 1.0)       # beta 0 column
    X = x.values                        # (n, 6) n rows with 6 columns of values
    y = df["success"].to_numpy(float)   # (n,) n rows of y values

    # matrix multiplication to find relevant matrices for formulas.
    Xt = X.T
    XtX = np.matmul(Xt, X)
    Xty = np.matmul(Xt, y)

    # calculate vector of coefficients for individual variables when comparing predictors to success
    beta = np.matmul(np.linalg.inv(XtX), Xty)

    return beta


def fit_beta_grade(tasks: List[Task]) -> np.ndarray:
    """Returns a 6-element beta vector (intercept + 5 predictor betas) against grade."""
    df = pd.DataFrame([asdict(t) for t in tasks])

    # get x values in matrix format
    x = df[data_predictors].astype(float)
    x.insert(0, "intercept", 1.0)  # beta 0 column
    X = x.values  # (n, 6) n rows with 6 columns of values
    y = df["grade"].to_numpy(float)

    # matrix multiplication to find relevant matrices for formulas
    Xt = X.T
    XtX = np.matmul(Xt, X)
    Xty = np.matmul(Xt, y)

    # calculate vector of coefficients for individual variables when comparing predictors to grade
    beta = np.matmul(np.linalg.inv(XtX), Xty)

    return beta


def predict_prob(beta_success: np.ndarray, beta_grade, predicted_task: Task | Dict[str, Any]) -> Tuple[float, float, float]:
    """ takes input of beta vector calculated from fit_beta and a predicted task. Calculates logarithmic odd by finding the
    matrix multiplication of the beta vector (which is a vector with the coefficients of the individual predictors) and
    the x_vector which is the user input of their new information. We output a tuple of the probability and log-odd."""
    if isinstance(predicted_task, Task):
        d = asdict(predicted_task)
    else:
        d = predicted_task

    x_vector = np.array([1.0] + [d[k] for k in data_predictors], dtype=float)

    z = float(np.matmul(beta_success, x_vector))  # logarithmic-odds (odds as in probability)
    p = 1.0 / (1.0 + math.exp(-z))        # sigmoid probability calculation

    g = np.matmul(beta_grade, x_vector)
    return p, z, g


