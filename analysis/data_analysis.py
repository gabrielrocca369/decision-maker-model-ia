import pandas as pd
from scipy.stats import linregress
from scipy.stats import skew
from .monte_carlo import monte_carlo_simulation
from .recommendations import generate_recommendations
import logging

def analyze_data(df, data_column_name=None):
    try:
        logging.info("Iniciando a função analyze_data")

        # Verificar se o DataFrame tem pelo menos uma coluna
        if df.shape[1] < 1:
            logging.error("O DataFrame não contém colunas.")
            raise ValueError("O DataFrame deve conter pelo menos uma coluna.")

        # Verificar se a coluna selecionada existe no DataFrame
        if data_column_name not in df.columns:
            logging.error(f"A coluna '{data_column_name}' não existe no DataFrame.")
            raise ValueError(f"A coluna '{data_column_name}' não existe no DataFrame.")

        logging.info(f"Coluna selecionada para análise: {data_column_name}")

        # Obter os dados da coluna selecionada
        data_column = df[data_column_name]

        # Converter para numérico, transformando erros em NaN
        data_column = pd.to_numeric(data_column, errors='coerce')

        # Remover valores nulos resultantes da conversão
        initial_count = len(data_column)
        data_column = data_column.dropna()
        final_count = len(data_column)
        logging.info(f"Valores iniciais na coluna: {initial_count}, após remoção de NaN: {final_count}")

        # Verificar se há dados suficientes para análise
        if data_column.shape[0] < 2:
            logging.error("Dados insuficientes após remoção de valores não numéricos.")
            raise ValueError("A coluna selecionada não contém dados numéricos suficientes para análise.")

        # Cálculos de análise
        mean_value = data_column.mean()
        max_value = data_column.max()
        min_value = data_column.min()
        ideal_value = mean_value * 1.618  # Proporção Áurea (Fibonacci)
        pareto_80_20 = data_column.quantile(0.8)
        std_dev = data_column.std()

        logging.info(f"Média: {mean_value}, Máximo: {max_value}, Mínimo: {min_value}")
        logging.info(f"Valor Ideal (Proporção Áurea): {ideal_value}")
        logging.info(f"Pareto 80/20: {pareto_80_20}, Desvio Padrão: {std_dev}")

        # Análise de distribuição dos dados
        skewness = skew(data_column)
        logging.info(f"Assimetria dos dados (skewness): {skewness}")
        if abs(skewness) > 1:
            logging.warning("Os dados são altamente assimétricos, considere uma transformação antes de prosseguir com a análise.")

        # Regressão linear
        x_values = range(len(data_column))
        slope, intercept, r_value, p_value, std_err = linregress(x_values, data_column)
        future_projection = slope * (len(data_column) + 1) + intercept

        logging.info(f"Slope: {slope}, Intercept: {intercept}, R-squared: {r_value ** 2}, P-value: {p_value}, Std Err: {std_err}")

        # Validar o coeficiente de determinação (R-squared)
        if r_value ** 2 < 0.5:
            logging.warning("O ajuste linear tem um r-squared baixo, a projeção futura pode não ser precisa.")

        logging.info(f"Projeção Futura: {future_projection}")

        # Simulação de Monte Carlo
        simulated_projections = monte_carlo_simulation(slope, intercept, std_dev, len(data_column))
        logging.info("Simulação de Monte Carlo concluída")

        # Recomendações baseadas nos resultados
        recommendations = generate_recommendations(mean_value, ideal_value, pareto_80_20, std_dev, future_projection)
        logging.info("Geração de recomendações concluída")

        # Resultados
        results = {
            "Coluna Analisada": data_column_name,
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
        logging.info("Análise de dados concluída com sucesso")
        return results

    except Exception as e:
        logging.error(f"Erro ao analisar dados: {e}", exc_info=True)
        print(f"Erro ao analisar dados: {e}")
        return None
