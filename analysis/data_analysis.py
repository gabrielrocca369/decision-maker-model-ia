import pandas as pd
from scipy.stats import linregress
from .monte_carlo import monte_carlo_simulation
from .recommendations import generate_recommendations
import logging

def analyze_data(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Formato de arquivo não suportado. Apenas .csv e .xlsx são permitidos.")

        # Usando a segunda coluna (coluna B) para os dados
        data_column = df.iloc[:, 1]

        # Cálculos de análise
        mean_value = data_column.mean()
        max_value = data_column.max()
        min_value = data_column.min()
        ideal_value = mean_value * 1.618  # Proporção Áurea (Fibonacci)
        pareto_80_20 = data_column.quantile(0.8)
        std_dev = data_column.std()
        slope, intercept, r_value, p_value, std_err = linregress(range(len(data_column)), data_column)
        future_projection = slope * (len(data_column) + 1) + intercept

        # Simulação de Monte Carlo
        simulated_projections = monte_carlo_simulation(slope, intercept, std_dev, len(data_column))

        # Recomendações baseadas nos resultados
        recommendations = generate_recommendations(mean_value, ideal_value, pareto_80_20, std_dev, future_projection)

        results = {
            "Média": mean_value,
            "Maior Valor": max_value,
            "Menor Valor": min_value,
            "Valor Ideal (Proporção Áurea)": ideal_value,
            "Pareto 80/20": pareto_80_20,
            "Desvio Padrão": std_dev,
            "Projeção Futura": future_projection,
            "Simulação de Monte Carlo": simulated_projections,
            "Recomendações": recommendations
        }
        return results
    except Exception as e:
        logging.error(f"Erro ao analisar dados: {e}")
        print("Erro ao analisar dados. Verifique o log para mais detalhes.")
        return None
