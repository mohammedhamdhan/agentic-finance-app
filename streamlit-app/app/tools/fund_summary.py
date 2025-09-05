def summarize_fund(ticker: str) -> dict:
    # Day 1 stub; B will RAG real PDFs
    return {
        "ticker": ticker,
        "objective": "Track the S&P 500 index.",
        "benchmark": "S&P 500",
        "fees": "0.03%",
        "top_holdings": ["AAPL","MSFT","NVDA","AMZN","GOOGL"],
        "risks": "Equity market risk; concentration risk in large-cap tech.",
        "doc_date": "2025-06-30",
        "source_url": "issuer-pdf",
        "citations": [{"page":1,"snippet":"Seeks to track the performance of the S&P 500 Index."}]
    }
