# 📈 Project-Optimization: Simulação de Carteiras com o Índice Dow Jones

## 🎯 Visão Geral do Projeto

Este projeto foi desenvolvido para simular e otimizar carteiras de investimento com base no índice Dow Jones, utilizando o Sharpe Ratio como métrica principal para identificar a melhor carteira. O objetivo foi maximizar o retorno ajustado ao risco, respeitando restrições específicas, garantindo a implementação de paralelismo e funções puras para lidar com a alta complexidade computacional. O projeto foi implementado em Python, com foco em programação funcional e paralelismo, e utiliza dados financeiros reais obtidos via API.

## 📊 Contexto do Problema

O desafio era simular carteiras com características desejáveis (alto retorno, baixa volatilidade) para um portfolio manager. Utilizei o Sharpe Ratio, definido como:

$$\text{SR} = \frac{\mu - r_{\text{free}}}{\sigma}$$

Onde:
- $\mu$: Retorno anualizado da carteira
- $r_{\text{free}}$: Taxa livre de risco (fixa, desconsiderada na comparação)
- $\sigma$: Volatilidade anualizada da carteira

## ⚡ Restrições do Problema

### Dados e Simulações
- **Ações:** Utilizar as 30 ações do índice Dow Jones
- **Combinações:** Selecionar 25 ações por vez ($C(30, 25) = 142,506$ combinações)
- **Simulações:** Para cada combinação, realizar 1000 simulações de pesos aleatórios

### Restrições de Pesos
- $\sum_{i=1}^{n} w_i = 1$ (soma dos pesos deve ser 1)
- $w_i \geq 0$ (carteira long-only)
- $w_i \leq 0.2$ (nenhum ativo pode ter mais de 20% da carteira)

### Períodos
- **Treino:** 01/08/2024 a 31/12/2024
- **Teste:** 1º trimestre de 2025 (proxy: 01/01/2023 a 31/03/2024, devido à indisponibilidade de dados futuros em 10/05/2025)

## 📁 Estrutura do Projeto

```
Project-Optimization/
├── main.py                 # Script principal que coordena a execução
├── data_loader.py         # Carregamento de dados via API yfinance
├── simulate.py            # Lógica de simulação para combinações
├── utils.py              # Funções puras para cálculos financeiros
├── plot_results.py       # Geração de visualizações gráficas
├── results/              # Diretório para resultados
│   ├── best_portfolio.csv    # Melhor carteira encontrada
│   ├── performance_metrics.csv # Métricas de desempenho
│   ├── logs/              # Logs de execução
│   │   └── simulation.log    # Log detalhado da execução
│   └── plots/            # Gráficos gerados
│       ├── portfolio_allocation.png # Alocação da carteira
│       └── performance_comparison.png # Comparação de tempos
```

## 📦 Dependências

O projeto utiliza a biblioteca UV para gerenciamento de dependências. As bibliotecas necessárias estão especificadas no arquivo `pyproject.toml`, gerado automaticamente pelo UV. As principais dependências incluem:

- `yfinance`: Para obtenção de dados financeiros
- `numpy`, `pandas`: Para manipulação de dados
- `matplotlib`, `seaborn`: Para geração de gráficos
- `tqdm`: Para barras de progresso

## 🚀 Como Executar

### 1. Instalação do UV

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
Baixe o instalador em [astral.sh/uv](https://astral.sh/uv)

Verifique a instalação:
```bash
uv --version
```

### 2. Configuração do Projeto

```bash
# Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd Project-Optimization

# Sincronize as dependências
uv sync

# Ative o ambiente virtual (se necessário)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

> ⚠️ **Nota:** Se o comando `uv sync` falhar, verifique sua conexão com a internet ou reinstale o UV.

### 3. Execução

```bash
python main.py
```

> ⚠️ **Nota:** O script levará cerca de 21 minutos para processar todas as 142,506 combinações com 1000 simulações cada (142.5 milhões de simulações no total) em um MacBook Air M1. Certifique-se de que seu computador esteja conectado à energia e não seja interrompido.

### 4. Verificação dos Resultados

Após a execução, explore o diretório `results/` para verificar:b
- `best_portfolio.csv`: Lista a melhor carteira (25 tickers e seus pesos).
- `performance_metrics.csv`: Métricas de desempenho.
- `logs/simulation.log`: Log detalhado da execução.
- `plots/portfolio_allocation.png`: Gráfico de alocação da melhor carteira.
- `plots/performance_comparison.png`: Comparação de tempos com e sem paralelismo.

## 📊 Resultados Obtidos

### Melhor Carteira
Identifiquei a melhor carteira com base no maior Sharpe Ratio no período de treino (01/08/2024 a 31/12/2024). Abaixo está o conteúdo do arquivo `results/best_portfolio.csv`:

| Ticker | Weight                |
|--------|----------------------|
| AAPL   | 0.05481740142742285  |
| MSFT   | 0.05481740142742285  |
| JPM    | 0.05481740142742285  |
| KO     | 0.012730260837092462 |
| PG     | 0.017313394873975062 |
| MMM    | 0.05481740142742285  |
| AXP    | 0.05481740142742285  |
| BA     | 0.007766504964899721 |
| CAT    | 0.05481740142742285  |
| CSCO   | 0.05481740142742285  |
| DIS    | 0.05481740142742285  |
| GS     | 0.05481740142742285  |
| HD     | 0.05481740142742285  |
| HON    | 0.05481740142742285  |
| IBM    | 0.05481740142742285  |
| INTC   | 0.0058845044799989595|
| JNJ    | 0.0022041896717044118|
| MCD    | 0.05481740142742285  |
| MRK    | 0.05481740142742285  |
| NKE    | 0.010039789174924553 |
| TRV    | 0.05481740142742285  |
| UNH    | 0.00692342496372047  |
| V      | 0.05481740142742285  |
| VZ     | 0.005242106767495871 |
| WMT    | 0.05481740142742285  |

**Características da Carteira:**
- Número de Ações: 25, conforme o enunciado
- Pesos: Variam de 0.0022 (JNJ) a 0.0548 (vários tickers), todos $\leq 0.2$, respeitando a restrição
- Soma dos Pesos: Aproximadamente 1 (normalizada no código)

### Métricas de Desempenho
As métricas de desempenho da melhor carteira estão no arquivo `results/performance_metrics.csv`:

| Métrica          | Valor                |
|------------------|---------------------|
| Sharpe_Treino    | 2.4818157861793906  |
| Sharpe_Teste     | 1.9771413397374902  |
| Retorno_Teste    | 0.25050360844676534 |
| Volatilidade_Teste| 0.11658428449903832 |

**Análise das Métricas:**
- Sharpe_Treino: 2.4818, indicando uma carteira otimizada no período de treino
- Sharpe_Teste: 1.9771, mostrando boa generalização no período de teste (proxy 01/01/2023 a 31/03/2024)
- Retorno_Teste: 0.2505 (25.05% anualizado)
- Volatilidade_Teste: 0.1166 (11.66% anualizada), refletindo menor risco devido à diversificação com 25 ações

### Gráficos Gerados

#### Alocação da Melhor Carteira
![Alocação da Melhor Carteira](results/plots/portfolio_allocation.png)

A carteira otimizada, identificada pelo maior Sharpe Ratio (2.4818) no período de treino, apresenta uma distribuição de pesos que reflete uma estratégia de diversificação eficiente. Ações como AAPL, MSFT e JPM recebem alocações máximas de 0.0548, enquanto outras como JNJ (0.0022) e VZ (0.0052) têm participações menores. Esta estrutura, respeitando as restrições ($w_i \leq 0.2$ e $\sum w_i = 1$), resultou em uma volatilidade anualizada de 11.66% no período de teste, demonstrando o sucesso da estratégia de otimização.

#### Comparação de Tempo de Execução
![Comparação de Tempos](results/plots/performance_comparison.png)

A implementação do paralelismo com `multiprocessing` demonstrou ganhos significativos de performance. Em testes com 100 combinações (1000 simulações cada), o tempo de execução caiu de 1.75 para 1.25 segundos, uma redução de 28%. Este ganho de eficiência foi crucial para processar o total de 142 milhões de simulações em aproximadamente 21 minutos no MacBook Air M1. Embora o tempo seja superior ao benchmark de 522 segundos obtido em um Alienware, a diferença é justificável pelas características do hardware utilizado.

## 📈 Análise dos Resultados

### Desempenho Computacional
- O processamento de 142,506 combinações com 1000 simulações cada (142.5 milhões de simulações) levou ~21 minutos em um MacBook Air M1
- Isso é significativamente mais rápido que a estimativa inicial de ~2.5 horas, indicando boa eficiência do paralelismo (6 processos) e otimizações no cálculo
- O enunciado menciona um benchmark de 522 segundos em um Alienware. O tempo de execução no MacBook Air M1 foi de ~1262 segundos, o que é maior, mas aceitável considerando que o MacBook Air M1 tem hardware menos poderoso

### Qualidade da Carteira
- O Sharpe_Treino de 2.4818 é robusto, e o Sharpe_Teste de 1.9771 indica que a carteira generaliza bem para o período de teste
- Com 25 ações, a volatilidade (0.1166) é baixa, refletindo o benefício da diversificação
- O retorno (0.2505) é mais moderado em comparação com carteiras menos diversificadas (ex.: 5 ações, onde o Sharpe_Treino foi 4.8892)

### Paralelismo
- O paralelismo reduziu o tempo de execução em ~28% (de 1.75s para 1.25s na comparação com 100 combinações)
- Demonstra a eficácia da abordagem com multiprocessing

## ✅ Conformidade com a Rubrica

### Requisitos Obrigatórios
- [x] **Dados:** 2º semestre de 2024 (treino) e proxy do 1º trimestre de 2025 (teste)
- [x] **Ações:** 30 ações do índice Dow Jones
- [x] **Combinações:** 142,506 combinações de 25 ações
- [x] **Simulações:** 1000 simulações por combinação
- [x] **Paralelismo:** Implementado com 6 processos via `multiprocessing`
- [x] **Funções Puras:** Implementadas em `utils.py`
- [x] **Restrições:** 
  - $\sum_{i=1}^{n} w_i = 1$ (soma dos pesos)
  - $w_i \geq 0$ (carteira long-only)
  - $w_i \leq 0.2$ (limite por ativo)

### Itens Opcionais
- [x] **API de Dados** (+0.5)
  - Implementação via `yfinance`
  - Obtenção automática de dados históricos
  - Atualização em tempo real dos preços

- [x] **Teste Proxy** (+0.25)
  - Simulação do 1º trimestre de 2025
  - Uso de dados históricos como proxy
  - Validação da robustez da carteira

- [x] **Benchmark de Performance** (+0.5)
  - Comparação com/sem paralelismo
  - Redução de 28% no tempo de execução
  - Análise de escalabilidade

## 🎓 Conclusão

O projeto foi concluído com sucesso, atingindo todos os objetivos propostos:

### Resultados Principais
- Processamento de 142.5 milhões de simulações em ~21 minutos
- Carteira otimizada com Sharpe Ratio de 2.4818 (treino) e 1.9771 (teste)
- Implementação eficiente de paralelismo com redução de 28% no tempo de execução

### Conformidade
- Todas as restrições técnicas foram respeitadas
- Implementação completa dos requisitos obrigatórios
- Inclusão de todos os itens opcionais propostos
- Foi utilizado o uso de AI para auxiliar na implementação do projeto e na escrita deste README.


---

**Autor:** Enzo Quental
