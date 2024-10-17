import pandas as pd
from scipy.stats import linregress
from scipy.stats import skew
from .monte_carlo import monte_carlo_simulation
from .recommendations import generate_recommendations
# Removida a importação de plot_histogram, pois agora usamos plot_boxplot em plots.py
# from visualization.plots import plot_histogram  # Não é mais necessário
import logging

def analyze_data(df, data_column_name=None, plot_histogram_flag=False):
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

        # Obter as datas correspondentes aos dados
        dates = data_column.index

        # Cálculos de análise
        mean_value = data_column.mean()
        median_value = data_column.median()
        max_value = data_column.max()
        min_value = data_column.min()
        ideal_value = mean_value * 1.618  # Proporção Áurea (Fibonacci)
        tension_value = mean_value * 0.618  # Proporção de Tensão (Fibonacci)
        pareto_80_20 = data_column.quantile(0.8)
        std_dev = data_column.std()
        coef_var = (std_dev / mean_value) * 100  # Cálculo do coeficiente de variação

        logging.info(f"Média: {mean_value}, Mediana: {median_value}, Máximo: {max_value}, Mínimo: {min_value}")
        logging.info(f"Valor Ideal Fibonacci: {ideal_value}, Valor de Tensão: {tension_value}")
        logging.info(f"Pareto 80/20: {pareto_80_20}, Desvio Padrão: {std_dev}, Coeficiente de Variação: {coef_var}%")

        # Análise de distribuição dos dados
        skewness = skew(data_column)
        logging.info(f"Assimetria dos dados (skewness): {skewness}")
        if abs(skewness) > 1:
            logging.warning("Os dados são altamente assimétricos, considere uma transformação antes de prosseguir com a análise.")

        # Regressão linear para progressão simples
        x_values = range(len(data_column))
        slope, intercept, r_value, p_value, std_err = linregress(x_values, data_column)
        future_projection = slope * (len(data_column) + 1) + intercept

        logging.info(f"Slope: {slope}, Intercept: {intercept}, R-squared: {r_value ** 2}, P-value: {p_value}, Std Err: {std_err}")

        # Validar o coeficiente de determinação (R-squared)
        if r_value ** 2 < 0.5:
            logging.warning("O ajuste linear tem um r-squared baixo, a projeção futura pode não ser precisa.")

        logging.info(f"Projeção Futura: {future_projection}")

        # Cálculo da Taxa de Crescimento Composta (CAGR) - Série Temporal
        if len(data_column) > 1 and min_value > 0:
            initial_value = data_column.iloc[0]
            final_value = data_column.iloc[-1]
            years = len(data_column) - 1  # Considerando a série ao longo do tempo
            cagr = ((final_value / initial_value) ** (1 / years) - 1) * 100
        else:
            cagr = None
            logging.warning("CAGR não pode ser calculado devido à falta de dados suficientes ou valores negativos/zero.")

        logging.info(f"CAGR: {cagr}%")

        # Simulação de Monte Carlo
        simulated_projections = monte_carlo_simulation(slope, intercept, std_dev, len(data_column))
        logging.info("Simulação de Monte Carlo concluída")

        # Geração de Box Plot se o plot_histogram_flag for True
        if plot_histogram_flag:
            logging.info(f"Gerando Box Plot para a coluna {data_column_name}.")
            # Aqui você pode chamar plot_boxplot se desejar plotar diretamente na análise
            # No entanto, conforme as recomendações anteriores, é melhor evitar isso para separar responsabilidades
            # Portanto, deixaremos essa linha comentada
            # plot_boxplot(data_column, dates, column_name=data_column_name)
            pass  # Placeholder para evitar execução

        # Recomendações baseadas nos resultados
        recommendations = generate_recommendations(mean_value, ideal_value, tension_value, pareto_80_20, std_dev, future_projection)
        logging.info("Geração de recomendações concluída")

        # Resultados
        results = {
            "Coluna Analisada": data_column_name,
            "Média": mean_value,
            "Mediana": median_value,
            "Maior Valor": max_value,
            "Menor Valor": min_value,
            "Valor Ideal Fibonacci": ideal_value,
            "Valor de Tensão": tension_value,
            "Pareto 80/20": pareto_80_20,
            "Desvio Padrão": std_dev,
            "Coeficiente de Variação": coef_var,
            "Projeção Futura": future_projection,
            "CAGR": cagr,  # Incluímos a CAGR como métrica para séries temporais
            "Simulação de Monte Carlo": simulated_projections,
            "Recomendações": recommendations
        }
        logging.info("Análise de dados concluída com sucesso")
        return results

    except Exception as e:
        logging.error(f"Erro ao analisar dados: {e}", exc_info=True)
        print(f"Erro ao analisar dados: {e}")
        return None
