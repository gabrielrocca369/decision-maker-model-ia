# -*- coding: utf-8 -*-

import numpy as np
import logging

def monte_carlo_simulation(slope, intercept, std_dev, data_length, n_simulations=1000):
    try:
        # Verificar se std_dev é positivo
        if std_dev <= 0:
            raise ValueError("O desvio padrao deve ser positivo para a simulacao de Monte Carlo.")

        # Verificar se data_length é um inteiro positivo
        if data_length <= 0 or not isinstance(data_length, int):
            raise ValueError("O comprimento dos dados deve ser um inteiro positivo.")

        # Gerar as projecoes simuladas
        simulated_projections = slope * (data_length + 1) + intercept + np.random.normal(0, std_dev, n_simulations)

        return simulated_projections

    except Exception as e:
        logging.error(f"Erro na simulacao de Monte Carlo: {e}", exc_info=True)
        print(f"Erro na simulacao de Monte Carlo: {e}")
        return None
