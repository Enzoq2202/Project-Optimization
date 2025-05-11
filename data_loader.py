import yfinance as yf
import pandas as pd
from typing import Tuple
import logging

def get_dow_jones_tickers() -> list:
    """Retorna a lista de tickers do Dow Jones."""
    logging.debug("Obtendo lista de tickers do Dow Jones")
    tickers = [
        'AAPL', 'MSFT', 'JPM', 'KO', 'PG', 'MMM', 'AXP', 'AMGN', 'BA', 'CAT',
        'CSCO', 'CVX', 'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ',
        'MCD', 'MRK', 'NKE', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT', 'XOM'
    ]
    logging.info(f"Tickers obtidos: {len(tickers)} empresas")
    return tickers

def download_data(tickers: list, start_date: str, end_date: str) -> pd.DataFrame:
    """Baixa dados de preços ajustados das ações via yfinance."""
    logging.debug(f"Baixando dados de {start_date} a {end_date}")
    try:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False, auto_adjust=False)
        if data.empty:
            logging.error(f"Nenhum dado retornado para {start_date} a {end_date}")
            raise ValueError("Nenhum dado retornado pela API yfinance")
        
        if isinstance(data, pd.DataFrame) and 'Adj Close' in data.columns:
            data = data['Adj Close']
        elif isinstance(data, pd.DataFrame) and data.columns.nlevels > 1:
            data = data.xs('Adj Close', level=1, axis=1)
        else:
            logging.error("Coluna 'Adj Close' não encontrada")
            raise ValueError("Coluna 'Adj Close' não encontrada")
        
        initial_columns = data.columns
        data = data.dropna(axis=1, how='any')
        if data.empty:
            logging.error("Todos os dados foram removidos após dropna")
            raise ValueError("Nenhum dado válido após remover NaN")
        
        dropped_columns = [col for col in initial_columns if col not in data.columns]
        if dropped_columns:
            logging.warning(f"Ações removidas devido a dados ausentes: {dropped_columns}")
        
        logging.info(f"Dados baixados: {data.shape[0]} dias, {data.shape[1]} ações")
        return data
    except Exception as e:
        logging.error(f"Erro ao baixar dados: {e}", exc_info=True)
        raise

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    logging.debug("Iniciando carregamento de dados")
    try:
        train_data = download_data(get_dow_jones_tickers(), '2024-08-01', '2024-12-31')
        test_data = download_data(get_dow_jones_tickers(), '2023-01-01', '2024-03-31')
        if len(train_data.columns) < 30 or len(test_data.columns) < 30:
            logging.warning(f"Apenas {len(train_data.columns)} tickers disponíveis em treino e {len(test_data.columns)} em teste")
        logging.info("Carregamento de dados concluído")
        return train_data, test_data
    except Exception as e:
        logging.error(f"Erro no carregamento de dados: {e}", exc_info=True)
        raise