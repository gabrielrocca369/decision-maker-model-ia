import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from analysis.data_import import import_file
from analysis.data_analysis import analyze_data
from visualization.plots import visualize_results, plot_boxplot  # Atualizado para plot_boxplot
from visualization.reports import download_results
from analysis.recommendations import explain_results
from utils.helpers import draw_button, load_logo
import logging
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import pandas as pd

# Configuração de logging para console e arquivo
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("error_log.txt"),
                        logging.StreamHandler()
                    ])

# Variáveis globais
results = None
df = None
processing = False
column_name = None  # Variável global para rastrear a coluna selecionada

# Caminho para a fonte Open Sans
FONT_PATH = os.path.join(
    'C:/Users/GabrielRocca/source/repos/games/decision-maker/assets/fonts/Open_Sans/static',
    'OpenSans-Regular.ttf'
)

def run_analysis(df, data_column_name, plot_boxplot_flag=False):
    """
    Função para executar a análise de dados em uma thread separada.
    """
    global results
    global processing
    processing = True

    def analyze():
        global results
        global processing
        try:
            logging.info("Iniciando análise dos dados...")
            results = analyze_data(df, data_column_name, plot_histogram_flag=plot_boxplot_flag)

            if plot_boxplot_flag:
                # Obter data_column e dates para o box plot
                data_column = df[data_column_name]
                data_column = pd.to_numeric(data_column, errors='coerce').dropna()
                dates = data_column.index

                # Chamar plot_boxplot com os argumentos necessários
                plot_boxplot(data_column, dates, column_name=data_column_name)
            logging.info("Análise dos dados concluída com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao analisar dados: {e}")
            results = None  # Garantir que results seja None em caso de erro
        finally:
            processing = False
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))  # Postar um evento customizado para atualizar a interface

    analysis_thread = threading.Thread(target=analyze)
    analysis_thread.start()

def run_app():
    """
    Função principal para executar a interface gráfica com pygame.
    """
    global results
    global df
    global processing
    global column_name  # Acessar a variável global

    # Inicialização do pygame
    pygame.init()

    # Configurações da tela
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Análise de Dados - DecisionMaker")

    # Cores
    white = (248, 248, 242)
    black = (40, 44, 52)
    green = (0, 250, 0)
    dark_green = (0, 200, 0)  # Cor para o hover (um verde mais escuro)
    blue = (0, 0, 250)
    dark_blue = (25, 25, 112)
    text_color = black

    # Fonte
    try:
        font = pygame.font.Font(FONT_PATH, 24)
    except FileNotFoundError:
        logging.error("Fonte Open Sans não encontrada. Certifique-se de que o caminho está correto.")
        font = pygame.font.Font(None, 24)

    # Dimensões e posição do botão
    button_width = 350  # Largura do botão
    button_height = 50
    center_x = (screen_width - button_width) // 2

    # Carregar e redimensionar a imagem do logo
    logo_image, logo_rect = load_logo(screen_width)

    # Verificar se o logo foi carregado com sucesso
    if logo_image and logo_rect:
        # Ajustar a posição do logo
        logo_rect.top = 50  # Posição vertical do logotipo
        logo_height = logo_rect.height
    else:
        logo_height = 0
        logo_rect = pygame.Rect(0, 0, 0, 0)  # Evitar erros ao desenhar a interface

    # Definir uma margem entre o logotipo e o primeiro botão
    margem = 20

    # Calcular a posição vertical do primeiro botão
    primeiro_botao_y = logo_rect.top + logo_height + margem

    # Atualizar as posições dos botões
    button_y_positions = [
        primeiro_botao_y,
        primeiro_botao_y + 70,  # Espaçamento de 70 pixels entre os botões
        primeiro_botao_y + 140,
        primeiro_botao_y + 210,
        primeiro_botao_y + 280  # Novo botão para o box plot
    ]

    running = True

    while running:
        screen.fill(black)

        # Exibir imagem do logo
        if logo_image and logo_rect:
            screen.blit(logo_image, logo_rect)

        # Renderizar botões
        draw_button(screen, "Importar Arquivo", center_x, button_y_positions[0],
                    button_width, button_height, green, dark_green, text_color, font)

        if df is not None and column_name is not None and not processing:
            # Mostrar botões adicionais apenas se não estiver processando e df e column_name estão definidos
            draw_button(screen, "Visualizar Resultado", center_x, button_y_positions[1],
                        button_width, button_height, green, dark_green, text_color, font)
            draw_button(screen, "Baixar Resultado", center_x, button_y_positions[2],
                        button_width, button_height, green, dark_green, text_color, font)
            draw_button(screen, "Como Avaliar os Resultados", center_x, button_y_positions[3],
                        button_width, button_height, green, dark_green, text_color, font)

            # Botão para visualizar o box plot
            draw_button(screen, "Visualizar Box Plot", center_x, button_y_positions[4],
                        button_width, button_height, blue, dark_blue, white, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if center_x <= mouse_x <= center_x + button_width:
                    if button_y_positions[0] <= mouse_y <= button_y_positions[0] + button_height:
                        if not processing:
                            df = import_file()
                            if df is not None:
                                # Obter colunas numéricas e solicitar ao usuário que selecione uma
                                numeric_columns = df.select_dtypes(include='number').columns.tolist()
                                if not numeric_columns:
                                    root = tk.Tk()
                                    root.withdraw()
                                    messagebox.showerror("Erro", "O DataFrame não contém colunas numéricas para análise.")
                                    root.destroy()
                                    continue

                                root = tk.Tk()
                                root.withdraw()
                                column_name = simpledialog.askstring(
                                    "Seleção de Coluna",
                                    f"Digite o nome de uma das colunas numéricas para análise:\n{', '.join(numeric_columns)}"
                                )
                                root.destroy()

                                if column_name not in numeric_columns:
                                    root = tk.Tk()
                                    root.withdraw()
                                    messagebox.showerror("Erro", "Coluna inválida ou não numérica selecionada.")
                                    root.destroy()
                                    continue

                                # Iniciar a análise
                                run_analysis(df, column_name)
                    elif df is not None and column_name is not None and not processing:
                        if button_y_positions[1] <= mouse_y <= button_y_positions[1] + button_height:
                            if results is not None:
                                visualize_results(results)
                            else:
                                root = tk.Tk()
                                root.withdraw()
                                messagebox.showerror("Erro", "Os resultados ainda não estão disponíveis.")
                                root.destroy()
                        elif button_y_positions[2] <= mouse_y <= button_y_positions[2] + button_height:
                            if results is not None:
                                download_results(results)
                            else:
                                root = tk.Tk()
                                root.withdraw()
                                messagebox.showerror("Erro", "Os resultados ainda não estão disponíveis.")
                                root.destroy()
                        elif button_y_positions[3] <= mouse_y <= button_y_positions[3] + button_height:
                            explain_results(screen)
                        elif button_y_positions[4] <= mouse_y <= button_y_positions[4] + button_height:
                            # Executar análise e visualizar o box plot
                            if not processing:
                                run_analysis(df, column_name, plot_boxplot_flag=True)

            elif event.type == pygame.USEREVENT:
                # Evento customizado para garantir que a interface atualize após a conclusão do processamento
                logging.info("Atualizando interface após processamento.")

    pygame.quit()

if __name__ == "__main__":
    run_app()
