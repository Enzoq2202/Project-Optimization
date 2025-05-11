import numpy as np
import pandas as pd
import logging

def calculate_daily_returns(prices: pd.DataFrame) -> np.ndarray:
    """Calcula retornos diários a partir de preços."""
    logging.debug("Calculando retornos diários")
    try:
        if not isinstance(prices, pd.DataFrame):
            logging.error("Preços não são um DataFrame")
            raise ValueError("Preços devem ser um pandas DataFrame")
        
        returns = prices.pct_change().dropna()
        if returns.empty:
            logging.error("Matriz de retornos vazia após cálculo")
            raise ValueError("Nenhum retorno válido calculado")
        
        returns_array = returns.to_numpy()
        if returns_array.ndim == 1:
            returns_array = returns_array.reshape(-1, 1)
        logging.debug(f"Retornos calculados: shape {returns_array.shape}")
        return returns_array
    except Exception as e:
        logging.error(f"Erro ao calcular retornos diários: {e}", exc_info=True)
        raise

def generate_random_weights(n_tickers: int, n_simulations: int) -> np.ndarray:
    logging.debug(f"Gerando {n_simulations} pesos para {n_tickers} tickers")
    try:
        weights_list = []
        attempts = 0
        max_attempts = n_simulations * 10
        while len(weights_list) < n_simulations and attempts < max_attempts:
            weights = np.random.random(n_tickers)
            weights = np.minimum(weights, 0.2)
            weights_sum = np.sum(weights)
            if weights_sum > 0:  # Evita divisão por zero
                weights /= weights_sum
            if np.all(weights <= 0.2) and abs(np.sum(weights) - 1) < 1e-10:
                weights_list.append(weights)
            attempts += 1
        if len(weights_list) < n_simulations:
            raise ValueError(f"Gerou apenas {len(weights_list)} pesos válidos após {max_attempts} tentativas")
        weights = np.array(weights_list)
        logging.debug(f"Pesos gerados: shape {weights.shape}")
        return weights
    except Exception as e:
        logging.error(f"Erro ao gerar pesos: {e}", exc_info=True)
        raise


def portfolio_return(weights: np.ndarray, returns: np.ndarray) -> np.ndarray:
    """Calcula o retorno da carteira."""
    logging.debug("Calculando retorno da carteira")
    try:
        if returns.ndim != 2:
            logging.error(f"Retornos não são 2D: shape {returns.shape}")
            raise ValueError("Retornos devem ser um array 2D")
        
        if weights.ndim != 1:
            logging.error(f"Pesos não são 1D: shape {weights.shape}")
            raise ValueError("Pesos devem ser 1D para uma simulação")
        
        ret = returns @ weights
        logging.debug(f"Retorno da carteira calculado: shape {ret.shape}")
        return ret
    except Exception as e:
        logging.error(f"Erro ao calcular retorno da carteira: {e}", exc_info=True)
        raise

def annualized_return(portfolio_returns: np.ndarray) -> float:
    """Calcula o retorno anualizado."""
    logging.debug("Calculando retorno anualizado")
    try:
        mean_daily_return = np.mean(portfolio_returns)
        annualized = (1 + mean_daily_return) ** 252 - 1
        logging.debug(f"Retorno anualizado: {annualized:.4f}")
        return annualized
    except Exception as e:
        logging.error(f"Erro ao calcular retorno anualizado: {e}", exc_info=True)
        raise

def portfolio_volatility(weights: np.ndarray, cov_matrix: np.ndarray) -> float:
    """Calcula a volatilidade da carteira."""
    logging.debug("Calculando volatilidade da carteira")
    try:
        vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        logging.debug(f"Volatilidade calculada: {vol:.4f}")
        return vol
    except Exception as e:
        logging.error(f"Erro ao calcular volatilidade: {e}", exc_info=True)
        raise

def sharpe_ratio(port_return: float, port_volatility: float, risk_free_rate: float = 0.02) -> float:
    """Calcula o Sharpe Ratio."""
    logging.debug("Calculando Sharpe Ratio")
    try:
        if port_volatility == 0:
            logging.warning("Volatilidade zero, retornando -inf")
            return -np.inf
        sharpe = (port_return - risk_free_rate) / port_volatility
        logging.debug(f"Sharpe Ratio calculado: {sharpe:.4f}")
        return sharpe
    except Exception as e:
        logging.error(f"Erro ao calcular Sharpe Ratio: {e}", exc_info=True)
        raise