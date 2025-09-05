import pandas as pd, numpy as np, yfinance as yf
from datetime import datetime, timedelta

def _sma(series, window): return series.rolling(window).mean()

def run_backtest(asset: str, strategy: str, span_years: int = 5):
    try:
        end = datetime.utcnow().date()
        start = end - timedelta(days=365*span_years)
        hist = yf.download(asset, start=start.isoformat(), end=end.isoformat(), progress=False)
        if hist.empty: return {"error":"No price data."}
        px = hist["Adj Close"].rename("close").to_frame()
        if strategy == "RSI_14":
            delta = px["close"].diff()
            up = delta.clip(lower=0).rolling(14).mean()
            down = (-delta.clip(upper=0)).rolling(14).mean()
            rsi = 100 - (100 / (1 + (up/down)))
            signal = (rsi < 30).astype(int) - (rsi > 70).astype(int)
        else:
            s50 = _sma(px["close"], 50)
            s200 = _sma(px["close"], 200)
            signal = (s50 > s200).astype(int)
        ret = px["close"].pct_change().fillna(0)
        strat_ret = ret * signal.shift(1).fillna(0)
        equity = (1 + strat_ret).cumprod()
        cagr = (equity.iloc[-1])**(252/len(equity)) - 1
        sharpe = np.sqrt(252) * strat_ret.mean() / (strat_ret.std() + 1e-9)
        mdd = (equity / equity.cummax() - 1).min()
        metrics = {"CAGR": round(float(cagr),4), "Sharpe": round(float(sharpe),2), "MaxDD": round(float(mdd),4)}
        return {"metrics": metrics, "equity_curve": equity}
    except Exception as e:
        return {"error": str(e)}
