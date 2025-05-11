import itertools
import numpy as np
import pandas as pd
from multiprocessing import Pool, cpu_count
from data_loader import load_data, get_dow_jones_tickers
from simulate import simulate_portfolio
import logging
import time
import os
from tqdm import tqdm

try:
    from plot_results import plot_portfolio_allocation, plot_performance_comparison
except ImportError as e:
    logging.error(f"Erro ao importar plot_results: {e}")
    raise

# Configuração de logging
os.makedirs('results/logs', exist_ok=True)
logging.basicConfig(
    filename='results/logs/simulation.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_simulation(args: tuple) -> dict:
    """Executa simulação para uma combinação de tickers."""
    tickers, train_data, progress_queue = args
    try:
        missing_tickers = [t for t in tickers if t not in train_data.columns]
        if missing_tickers:
            logging.error(f"Tickers ausentes em train_data: {missing_tickers}")
            raise ValueError(f"Tickers ausentes: {missing_tickers}")
        
        weights, sharpe, _ = simulate_portfolio(list(tickers), train_data, n_simulations=1000, progress_queue=progress_queue)
        return {'tickers': tickers, 'weights': weights, 'sharpe': sharpe}
    except Exception as e:
        logging.error(f"Erro na simulação {tickers}: {str(e)}", exc_info=True)
        return None

def evaluate_portfolio(weights: np.ndarray, tickers: tuple, data: pd.DataFrame) -> tuple:
    """Avalia o Sharpe Ratio, retorno e volatilidade de uma carteira em novos dados."""
    from utils import calculate_daily_returns, portfolio_return, annualized_return, portfolio_volatility, sharpe_ratio
    logging.debug(f"Avaliando portfólio para tickers: {tickers}")
    try:
        if data.shape[0] < 2:
            logging.error("Dados de teste insuficientes para calcular retornos")
            raise ValueError("Menos de 2 dias de dados em test_data")
        
        tickers_list = list(tickers)
        returns = calculate_daily_returns(data[tickers_list])
        logging.debug(f"Shape dos retornos de teste: {returns.shape}")
        cov_matrix = np.cov(returns.T) * 252
        port_ret = annualized_return(portfolio_return(weights, returns))
        port_vol = portfolio_volatility(weights, cov_matrix)
        logging.debug(f"Retorno: {port_ret:.4f}, Volatilidade: {port_vol:.4f}")
        if port_vol == 0:
            logging.warning("Volatilidade zero detectada, Sharpe será -inf")
            sharpe = -np.inf
        else:
            sharpe = sharpe_ratio(port_ret, port_vol)
        logging.info(f"Sharpe Ratio calculado: {sharpe:.4f}")
        return sharpe, port_ret, port_vol
    except Exception as e:
        logging.error(f"Erro ao avaliar portfólio: {e}", exc_info=True)
        return -np.inf, np.nan, np.nan

def compare_execution_time(combinations: list, train_data: pd.DataFrame, n_runs: int = 5) -> tuple:
    logging.info(f"Iniciando comparação de tempos ({n_runs} execuções)")
    times_sequential = []
    for run in range(n_runs):
        start_time = time.time()
        for combo in combinations[:100]:
            run_simulation((combo, train_data, None))
        elapsed = time.time() - start_time
        times_sequential.append(elapsed)
        logging.info(f"Sem paralelismo, iteração {run+1}: {elapsed:.2f}s")
    
    times_parallel = []
    for run in range(n_runs):
        start_time = time.time()
        with Pool(processes=4) as pool:
            pool.map(run_simulation, [(combo, train_data, None) for combo in combinations[:100]])
        elapsed = time.time() - start_time
        times_parallel.append(elapsed)
        logging.info(f"Com paralelismo, iteração {run+1}: {elapsed:.2f}s")
    
    return np.mean(times_sequential), np.mean(times_parallel)

if __name__ == '__main__':
    logging.info("Iniciando o programa")
    logging.info(f"Número de CPUs disponíveis: {cpu_count()}")
    
    # Carregar dados
    logging.debug("Carregando dados...")
    train_data, test_data = load_data()
    logging.info(f"Dados de treino: {train_data.shape[0]} dias, {train_data.shape[1]} ações")
    logging.info(f"Dados de teste: {test_data.shape[0]} dias, {test_data.shape[1]} ações")
    if train_data.empty or test_data.empty:
        logging.error("Dados carregados estão vazios")
        raise ValueError("Dados carregados estão vazios")
    if train_data.shape[0] < 2:
        logging.error("Dados de treino insuficientes")
        raise ValueError("Menos de 2 dias de dados em train_data")

    # Gerar combinações de 25 ações
    tickers = [t for t in get_dow_jones_tickers() if t in train_data.columns]
    n_tickers_per_combination = 25
    combinations = list(itertools.combinations(tickers, n_tickers_per_combination))
    logging.info(f"Total de combinações: {len(combinations)}")
    
    if not combinations:
        logging.error("Nenhuma combinação gerada")
        raise ValueError("Não foi possível gerar combinações")

    # Testar uma simulação
    test_result = run_simulation((combinations[0], train_data, None))
    if test_result is None:
        logging.error("Simulação de teste falhou")
        raise ValueError("Simulação de teste falhou")

    # Comparar tempos
    seq_time, par_time = compare_execution_time(combinations, train_data)
    logging.info(f"Tempo médio sem paralelismo: {seq_time:.2f}s")
    logging.info(f"Tempo médio com paralelismo: {par_time:.2f}s")

    # Executar simulações em paralelo
    results = []
    with Pool(processes=6, maxtasksperchild=100) as pool:
        with tqdm(total=len(combinations), desc="Simulando combinações", unit="comb") as pbar:
            for result in pool.imap_unordered(run_simulation, [(combo, train_data, None) for combo in combinations]):
                if result is not None:
                    results.append(result)
                pbar.update(1)

    if not results:
        logging.error("Nenhum resultado válido")
        raise ValueError("Nenhum resultado válido gerado")

    logging.info(f"Total de simulações válidas processadas: {len(results)}/{len(combinations)}")

    # Encontrar a melhor carteira
    best_portfolio = max(results, key=lambda x: x['sharpe'])
    logging.info(f"Melhor Sharpe Ratio: {best_portfolio['sharpe']:.4f}")

    # Salvar resultados
    os.makedirs('results', exist_ok=True)
    weights = best_portfolio['weights'] / np.sum(best_portfolio['weights'])
    portfolio_df = pd.DataFrame({
        'Ticker': best_portfolio['tickers'],
        'Weight': weights
    })
    portfolio_df.to_csv('results/best_portfolio.csv', index=False)
    logging.info("Resultados salvos em results/best_portfolio.csv")

    # Avaliar no período de teste
    test_sharpe, test_return, test_vol = evaluate_portfolio(best_portfolio['weights'], best_portfolio['tickers'], test_data)
    logging.info(f"Sharpe Ratio no período de teste: {test_sharpe:.4f}")

    # Salvar métricas
    metrics_df = pd.DataFrame({
        'Metric': ['Sharpe_Treino', 'Sharpe_Teste', 'Retorno_Teste', 'Volatilidade_Teste'],
        'Value': [best_portfolio['sharpe'], test_sharpe, test_return, test_vol]
    })
    metrics_df.to_csv('results/performance_metrics.csv', index=False)
    logging.info("Métricas salvas em results/performance_metrics.csv")

    # Gerar gráficos
    try:
        plot_portfolio_allocation(portfolio_df)
        plot_performance_comparison(seq_time, par_time)
        logging.info("Gráficos gerados em results/plots/")
    except Exception as e:
        logging.error(f"Erro ao gerar gráficos: {e}", exc_info=True)
        raise