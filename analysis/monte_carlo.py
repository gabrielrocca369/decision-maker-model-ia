import numpy as np
import logging

def monte_carlo_simulation(slope, intercept, std_dev, data_length, skewness=0, n_simulations=1000, projection_steps=1):
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
    - projection_steps: Número de períodos no futuro que se deseja projetar.

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

        # Verificar se n_simulations é um número válido
        if n_simulations <= 0 or not isinstance(n_simulations, int):
            raise ValueError("O número de simulações deve ser um inteiro positivo.")

        # Verificar se projection_steps é um número válido
        if projection_steps <= 0 or not isinstance(projection_steps, int):
            raise ValueError("O número de períodos de projeção deve ser um inteiro positivo.")

        logging.info(f"Executando simulação de Monte Carlo com {n_simulations} simulações e {projection_steps} períodos projetados")

        # Inicializar a matriz de projeções
        projections = []

        for step in range(1, projection_steps + 1):
            # Se os dados forem assimétricos, usamos uma distribuição log-normal ajustada
            if abs(skewness) > 1:
                logging.warning(f"Assimetria alta detectada (skewness = {skewness}). Usando distribuição log-normal para simulações no período {step}.")
                # Ajustamos a simulação para valores não negativos com desvio padrão adequado
                simulated_step = slope * (data_length + step) + intercept + np.random.lognormal(mean=0, sigma=np.log(1 + std_dev), size=n_simulations)
            else:
                # Se não houver assimetria significativa, usamos a distribuição normal
                simulated_step = slope * (data_length + step) + intercept + np.random.normal(loc=0, scale=std_dev, size=n_simulations)
            
            projections.append(simulated_step)

        # Convertendo a lista de projeções para um array 2D (projeções x simulações)
        projections_array = np.array(projections)

        logging.info("Simulação de Monte Carlo concluída com sucesso")
        return projections_array

    except Exception as e:
        logging.error(f"Erro na simulação de Monte Carlo: {e}", exc_info=True)
        print(f"Erro na simulação de Monte Carlo: {e}")
        return None
