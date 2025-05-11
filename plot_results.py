import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os

def plot_portfolio_allocation(portfolio: pd.DataFrame):
    """Gera gráfico de alocação da melhor carteira."""
    logging.debug("Gerando gráfico de alocação da carteira")
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Weight', y='Ticker', data=portfolio.sort_values('Weight', ascending=False))
        plt.title('Alocação da Melhor Carteira')
        plt.xlabel('Peso')
        plt.ylabel('Ação')
        plt.tight_layout()
        os.makedirs('results/plots', exist_ok=True)
        plt.savefig('results/plots/portfolio_allocation.png')
        plt.close()
        logging.info("Gráfico de alocação salvo em results/plots/portfolio_allocation.png")
    except Exception as e:
        logging.error(f"Erro ao gerar gráfico de alocação: {e}")
        raise

def plot_performance_comparison(seq_time: float, par_time: float):
    logging.debug("Gerando gráfico de comparação de tempos")
    try:
        if par_time >= seq_time:
            logging.warning(f"Paralelismo ({par_time}s) não foi mais rápido que sequencial ({seq_time}s)")
        plt.figure(figsize=(8, 5))
        times = [seq_time, par_time]
        labels = ['Sem Paralelismo', 'Com Paralelismo']
        sns.barplot(x=labels, y=times)
        plt.title('Comparação de Tempo de Execução')
        plt.ylabel('Tempo (segundos)')
        plt.tight_layout()
        os.makedirs('results/plots', exist_ok=True)
        plt.savefig('results/plots/performance_comparison.png')
        plt.close()
        logging.info("Gráfico de comparação salvo em results/plots/performance_comparison.png")
    except Exception as e:
        logging.error(f"Erro ao gerar gráfico de comparação: {e}")
        raise