import numpy as np
import logging

def monte_carlo_simulation(slope, intercept, std_dev, data_length, skewness=0, n_simulations=1000):
    """
    Realiza uma simulação de Monte Carlo para projetar valores futuros com base em
    uma regressão linear e um desvio padrão para aleatoriedade.

    Parâmetros:
    - slope: Inclinação da linha de regressão.
    - intercept: Intercepto da linha de regressão.
    - std_dev: Desvio padrão dos dados.
    - data_length: Comprimento dos dados usados na regressão.
    - skewness: Assimetria (skewness) dos dados. Utilizado para ajustar a distribuição normal se for assimétrica.
    - n_simulations: Número de simulações de Monte Carlo.

    Retorno:
    - Uma lista com as projeções simuladas.
    """
    try:
        # Verificar se std_dev é positivo
        if std_dev <= 0:
            raise ValueError("O desvio padrão deve ser positivo para a simulação de Monte Carlo.")

        # Verificar se data_length é um inteiro positivo
        if data_length <= 0 or not isinstance(data_length, int):
            raise ValueError("O comprimento dos dados deve ser um inteiro positivo.")

        logging.info(f"Executando simulação de Monte Carlo com {n_simulations} simulações")

        # Se os dados forem assimétricos, usamos uma distribuição log-normal
        if abs(skewness) > 1:
            logging.warning(f"Assimetria alta detectada: {skewness}. Usando distribuição log-normal para simulações.")
            simulated_projections = slope * (data_length + 1) + intercept + np.random.lognormal(mean=0, sigma=std_dev, size=n_simulations)
        else:
            # Se não houver assimetria significativa, usamos a distribuição normal
            simulated_projections = slope * (data_length + 1) + intercept + np.random.normal(0, std_dev, n_simulations)

        logging.info("Simulação de Monte Carlo concluída com sucesso")
        return simulated_projections

    except Exception as e:
        logging.error(f"Erro na simulação de Monte Carlo: {e}", exc_info=True)
        print(f"Erro na simulação de Monte Carlo: {e}")
        return None
