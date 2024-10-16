# DecisionMaker

## Descrição

**DecisionMaker** é uma ferramenta avançada de análise de dados projetada para facilitar a tomada de decisões instantâneas baseadas em informações. Utilizando métodos estatísticos, visualizações interativas e simulações de Monte Carlo, o DecisionMaker oferece uma compreensão profunda dos dados, permitindo que os usuários tomem decisões informadas e eficazes.

### Recursos Principais

- **Interface Intuitiva**: Desenvolvida com Pygame, oferecendo uma experiência amigável ao usuário.
- **Análise Estatística Completa**: Inclui cálculo de média, desvio padrão, valor ideal (proporção áurea) e análise de Pareto (80/20).
- **Simulação de Monte Carlo**: Realiza simulações probabilísticas para prever uma gama de possíveis resultados e mensurar incertezas.
- **Relatórios em PDF**: Gera relatórios automáticos, incluindo gráficos, em formato PDF para facilitar o compartilhamento.
- **Recomendações Automatizadas**: Sugere ações com base nos resultados, ajudando na tomada de decisões orientadas por dados.

## Instalação

### Pré-Requisitos

Para executar o **DecisionMaker**, você precisará de:

- **Python 3.8** ou superior
- As seguintes bibliotecas Python:
  - `pygame`
  - `matplotlib`
  - `pandas`
  - `fpdf`

Instale as dependências utilizando o arquivo `requirements.txt`:

`pip install -r requirements.txt`

## Uso

Certifique-se de **adicionar seu próprio diretório \assets com o logo.png desejado, e o diretório \data com o sample_data no formato desejado**.

Após instalar as dependências, você pode iniciar o aplicativo com o seguinte comando no terminal:

`python src/main.py`

## Estrutura do Projeto
Abaixo está a estrutura do projeto DecisionMaker para ajudá-lo a entender a organização dos arquivos:

`decision-maker/`

`│`

`├── data/                    # Arquivos de dados de exemplo`

`│   └── sample_data.csv`

`│`

`├── docs/                    # Documentação do projeto`

`│   └── README.md`

`│`

`├── src/                     # Código fonte do projeto`

`│   ├── main.py              # Arquivo principal para iniciar a aplicação`

`│   ├── gui.py               # Interface gráfica do usuário`

`│   ├── analysis/            # Módulo de análise de dados`

`│   │   ├── __init__.py`

`│   │   ├── data_import.py   # Importação de dados`

`│   │   ├── data_analysis.py # Análises estatísticas`

`│   │   ├── monte_carlo.py   # Simulação de Monte Carlo`

`│   │   └── recommendations.py # Recomendações baseadas em análise`

`│   ├── visualization/       # Módulo de visualização dos resultados`

`│   │   ├── __init__.py`

`│   │   ├── plots.py         # Geração de gráficos`

`│   │   └── reports.py       # Geração de relatórios em PDF`

`│   └── utils/               # Utilitários auxiliares`

`│       ├── __init__.py`

`│       └── helpers.py       # Funções de auxílio`

`│`

`├── tests/                   # Testes unitários do projeto`

`│   ├── __init__.py`

`│   ├── test_analysis.py     # Testes do módulo de análise`

`│   ├── test_visualization.py # Testes do módulo de visualização`

`│   └── test_gui.py          # Testes da interface gráfica`

`│`

`├── assets/                  # Arquivos estáticos, como imagens e ícones`

`│   └── logo.png`

`│`

`├── requirements.txt         # Dependências do projeto`

`├── setup.py                 # Script de configuração para instalação do projeto`

`└── LICENSE                  # Informações sobre a licença do projeto`

## Publicação no GitHub
O projeto DecisionMaker está disponível publicamente no GitHub:

[Repositório no GitHub](https://github.com/gabrielrocca369/decision-maker-model-ia)

## Contribuição
Sinta-se à vontade para contribuir com o projeto! Para isso, siga as etapas abaixo:

- Faça um fork do repositório.
- Crie uma branch para suas alterações: git checkout -b minha-branch.
- Faça commit das suas alterações: git commit -m "Descrição das alterações".
- Faça o push para a branch: git push origin minha-branch.
- Envie um Pull Request para análise.
- Todas as contribuições são muito bem-vindas!

Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.
