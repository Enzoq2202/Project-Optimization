import numpy as np
from typing import Tuple, List
from utils import calculate_daily_returns, generate_random_weights, portfolio_return, annualized_return, portfolio_volatility, sharpe_ratio
import pandas as pd
import logging
from tqdm import tqdm

def simulate_portfolio(tickers: List[str], prices: pd.DataFrame, n_simulations: int = 1000, progress_queue=None) -> Tuple[np.ndarray, float, np.ndarray]:
    """Simula n_simulations carteiras para uma combinação de tickers, respeitando restrições de pesos."""
    logging.debug(f"Simulando {n_simulations} carteiras para {tickers}")
    try:
        # Verificar tickers ausentes no DataFrame
        missing_tickers = [t for t in tickers if t not in prices.columns]
        if missing_tickers:
            logging.error(f"Tickers ausentes no DataFrame: {missing_tickers}")
            raise ValueError(f"Tickers ausentes: {missing_tickers}")
        
        # Verificar se há dados suficientes
        if prices.shape[0] < 2:
            logging.error("Dados insuficientes para calcular retornos")
            raise ValueError("Menos de 2 dias de dados")
        
        # Calcular retornos diários
        returns = calculate_daily_returns(prices[tickers])
        if returns.size == 0 or np.all(np.isnan(returns)):
            logging.error("Matriz de retornos vazia ou contém apenas NaN")
            raise ValueError("Matriz de retornos inválida")
        logging.debug(f"Shape dos retornos: {returns.shape}")
        
        # Calcular matriz de covariância anualizada
        cov_matrix = np.cov(returns.T) * 252
        if np.any(np.isnan(cov_matrix)) or np.any(np.isinf(cov_matrix)):
            logging.error("Matriz de covariância contém NaN ou Inf")
            raise ValueError("Matriz de covariância inválida")
        logging.debug(f"Shape da matriz de covariância: {cov_matrix.shape}")
        
        # Gerar pesos aleatórios (já respeitando w_i <= 0.2 em generate_random_weights)
        weights = generate_random_weights(len(tickers), n_simulations)
        logging.debug(f"Shape dos pesos: {weights.shape}")
        
        # Verificar se gerou o número esperado de simulações
        if len(weights) < n_simulations:
            logging.warning(f"Gerou apenas {len(weights)} pesos válidos, ajustando n_simulations")
            n_simulations = len(weights)
        weights = weights[:n_simulations]  # Garantir o número correto de simulações
        
        # Inicializar variáveis para encontrar o melhor Sharpe
        best_sharpe = -np.inf
        best_weights = None
        
        # Iterar sobre os pesos para calcular o Sharpe Ratio
        for w in tqdm(weights, total=n_simulations, desc=f"Simulações {tickers[0]}...", leave=False, unit="sim"):
            try:
                # Validação adicional para garantir que os pesos respeitam w_i <= 0.2
                if any(wi > 0.2 for wi in w):
                    logging.debug(f"Peso inválido detectado: {w}, ignorando simulação")
                    continue
                
                # Calcular retorno e volatilidade da carteira
                port_ret = annualized_return(portfolio_return(w, returns))
                port_vol = portfolio_volatility(w, cov_matrix)
                if port_vol == 0:
                    logging.debug("Volatilidade zero detectada, ignorando simulação")
                    continue
                
                # Calcular Sharpe Ratio
                sharpe = sharpe_ratio(port_ret, port_vol)
                if np.isnan(sharpe) or np.isinf(sharpe):
                    logging.debug("Sharpe Ratio inválido (NaN ou Inf)")
                    continue
                
                # Atualizar melhor resultado
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_weights = w
                    logging.debug(f"Novo melhor Sharpe: {sharpe:.4f}")
            except Exception as e:
                logging.error(f"Erro na simulação de pesos: {e}", exc_info=True)
                continue
        
        # Verificar se encontrou uma simulação válida
        if best_weights is None:
            logging.error("Nenhum Sharpe Ratio válido calculado")
            raise ValueError("Nenhuma simulação válida concluída")
        
        logging.info(f"Melhor Sharpe para {tickers}: {best_sharpe:.4f}")
        return best_weights, best_sharpe, returns
    except Exception as e:
        logging.error(f"Erro na simulação de {tickers}: {e}", exc_info=True)
        raise