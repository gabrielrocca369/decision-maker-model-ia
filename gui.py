import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from analysis.data_import import import_file
from analysis.data_analysis import analyze_data
from visualization.plots import visualize_results
from visualization.plots import plot_histogram
from visualization.reports import download_results
from analysis.recommendations import explain_results
from utils.helpers import draw_button, load_logo
import logging
import threading
import tkinter as tk
from tkinter import simpledialog

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
column_name = None  # Adicionar variável global para rastrear a coluna selecionada

def run_analysis(df, data_column_name, plot_histogram_flag=False):
    global results
    global processing
    processing = True

    def analyze():
        global results
        global processing
        try:
            logging.info("Iniciando análise dos dados...")
            results = analyze_data(df, data_column_name, plot_histogram_flag=plot_histogram_flag)
            
            if plot_histogram_flag:
                # Chamar a função diretamente sem passar o 'screen'
                plot_histogram(results['Simulação de Monte Carlo'], "Simulação de Monte Carlo")
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
    green = (0, 255, 0)
    dark_green = (0, 200, 0)  # Cor para o hover (um verde mais escuro)
    text_color = black

    # Fonte
    font = pygame.font.Font(None, 32)

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

        # Obter a altura do logotipo
        logo_height = logo_rect.height
    else:
        logo_height = 0
        # Definir logo_rect como um Rect vazio para evitar erros
        logo_rect = pygame.Rect(0, 0, 0, 0)

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
        primeiro_botao_y + 280  # Novo botão para o histograma
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

        if results and not processing:
            # Mostrar botões adicionais apenas se não estiver processando
            draw_button(screen, "Visualizar Resultado", center_x, button_y_positions[1],
                        button_width, button_height, green, dark_green, text_color, font)
            draw_button(screen, "Baixar Resultado", center_x, button_y_positions[2],
                        button_width, button_height, green, dark_green, text_color, font)
            draw_button(screen, "Como Avaliar os Resultados", center_x, button_y_positions[3],
                        button_width, button_height, green, dark_green, text_color, font)

            # Botão para visualizar o histograma
            draw_button(screen, "Visualizar Histograma", center_x, button_y_positions[4],
                        button_width, button_height, green, dark_green, text_color, font)

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
                                    tk.messagebox.showerror("Erro", "O DataFrame não contém colunas numéricas para análise.")
                                    continue

                                root = tk.Tk()
                                root.withdraw()
                                column_name = simpledialog.askstring(
                                    "Seleção de Coluna",
                                    f"Digite o nome de uma das colunas numéricas para análise:\n{', '.join(numeric_columns)}"
                                )
                                root.destroy()

                                if column_name not in numeric_columns:
                                    tk.messagebox.showerror("Erro", "Coluna inválida ou não numérica selecionada.")
                                    continue

                                # Iniciar a análise
                                run_analysis(df, column_name)
                    elif results and not processing:
                        if button_y_positions[1] <= mouse_y <= button_y_positions[1] + button_height:
                            visualize_results(results)
                        elif button_y_positions[2] <= mouse_y <= button_y_positions[2] + button_height:
                            download_results(results)
                        elif button_y_positions[3] <= mouse_y <= button_y_positions[3] + button_height:
                            explain_results(screen)
                        elif button_y_positions[4] <= mouse_y <= button_y_positions[4] + button_height:
                            # Executar análise e visualizar o histograma
                            run_analysis(df, column_name, plot_histogram_flag=True)

            elif event.type == pygame.USEREVENT:
                # Evento customizado para garantir que a interface atualize após a conclusão do processamento
                logging.info("Atualizando interface após processamento.")

    pygame.quit()

if __name__ == "__main__":
    run_app()
