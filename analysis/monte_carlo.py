import numpy as np

def monte_carlo_simulation(slope, intercept, std_dev, data_length, n_simulations=1000):
    simulated_projections = slope * (data_length + 1) + intercept + np.random.normal(0, std_dev, n_simulations)
    return simulated_projections
