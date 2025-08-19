import re
import finnhub
from ollama import chat, ChatResponse
import pandas as pd


# API-Key & Parameter
API_KEY = "YOUR FINNHUB API HERE"


# Dynamically generate the system prompt
def build_system_prompt(symbol: str) -> dict:
    return {
        'role': 'system',
        'content': (
            f"You are a professional sentiment analysis assistant working for a high-stakes finance firm. "
            f"Your job is to evaluate headlines and summaries related to stocks and determine the investment sentiment "
            f"specifically for the company with ticker symbol '{symbol}'. "
            f"Your analysis must be precise and consistent – your performance directly affects the firm's success. "
            f"Always assess the sentiment strictly from the perspective of '{symbol}', even if the news mentions competitors, industry trends, or general market conditions. "
            f"Respond with one numeric value only:\n"
            f"- Between 0.5 and 1 for positive sentiment (buy),\n"
            f"- Between -1 and -0.5 for negative sentiment (sell),\n"
            f"- Between -0.5 and 0.5 for neutral sentiment (hold).\n"
            f"If the headline and summary contain no meaningful or relevant information about '{symbol}', return exactly 2.\n"
            f"Do not explain your reasoning. Just return the number."
        )
    }

#  Remove hidden <think> tags
def clean(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# Sentiment Analysis with Ollama
def analyze(text: str, symbol: str) -> float:
    system_prompt = build_system_prompt(symbol)
    response: ChatResponse = chat(
        model='gemma3:27b',
        messages=[system_prompt, {'role': 'user', 'content': text}]
    )
    try:
        return float(clean(response.message.content))
    except ValueError:
        print(f"⚠️ Ungültiger Wert: {response.message.content}")
        return 0.0

# Evaluate Fundamentals
def evaluate_fundamentals(data: dict) -> float:
    score = 0.0
    weight_total = 0.0

    try:
        current_ratio = data["series"]["annual"]["currentRatio"][0]["v"]
        score += 1.0 if current_ratio >= 1.5 else 0.5 if current_ratio >= 1.0 else -0.5
        weight_total += 1

        sales = data["series"]["annual"]["salesPerShare"]
        if len(sales) >= 2:
            growth = sales[0]["v"] - sales[1]["v"]
            score += 1.0 if growth > 0 else -0.5
            weight_total += 1

        net_margin = data["series"]["annual"]["netMargin"][0]["v"]
        score += 1.0 if net_margin >= 0.2 else 0.5 if net_margin >= 0.1 else -0.5
        weight_total += 1

        price_return = data["metric"]["52WeekPriceReturnDaily"]
        score += 1.0 if price_return > 50 else 0.5 if price_return > 0 else -0.5
        weight_total += 1

        beta = data["metric"]["beta"]
        score += 0.5 if beta < 1.2 else -0.5 if beta > 1.5 else 0.0
        weight_total += 1

    except (KeyError, IndexError, TypeError):
        print("⚠️ Fehler beim Auswerten der Fundamentaldaten.")

    return round(score / weight_total, 2) if weight_total > 0 else 0.0

# Evaluate Analyst Recommendations
def evaluate_recommendation_trends(data: list[dict]) -> float:
    if not data:
        return 0.0

    total_score = 0.0
    total_periods = 0

    for entry in data:
        pos = entry.get("strongBuy", 0) + entry.get("buy", 0)
        neutral = entry.get("hold", 0)
        neg = entry.get("sell", 0) + entry.get("strongSell", 0)
        total = pos + neutral + neg

        if total == 0:
            continue

        score = (pos - neg) / total
        total_score += score
        total_periods += 1

    return round(total_score / total_periods, 2) if total_periods > 0 else 0.0

# Combined Recommendation
def recommend_combined(sentiment_scores_filtered: list[float], fundamental_score: float, analyst_score: float) -> str:
    if not sentiment_scores_filtered:
        return "⚠️ Keine gültigen Sentiment-Werte vorhanden."

    sentiment_avg = sum(sentiment_scores_filtered) / len(sentiment_scores_filtered)
    combined_score = (sentiment_avg * 0.5) + (fundamental_score * 0.3) + (analyst_score * 0.2)

    print(f"\n🧮 Sentiment average: {sentiment_avg:.2f}")
    print(f"📊 Fundamentals score: {fundamental_score:.2f}")
    print(f"🗣️ Analyst score: {analyst_score:.2f}")
    print(f"🔗 Combined score: {combined_score:.2f}")

    if combined_score > 0.5:
        return "📈 Buy"
    elif combined_score < 0.3:
        return "📉 Sell"
    return "⏸️ Hold"

#  Save Results to File
def save_results(symbol, start_date, end_date, news_items, sentiment_scores_all, sentiment_scores_filtered, f_score, analyst_score, recommendation, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"🔎 Analyze {symbol} from {start_date} to {end_date}\n\n")

        for i, item in enumerate(news_items):
            headline = item.get("headline", "")
            summary = item.get("summary", "")
            score = sentiment_scores_all[i]
            f.write(f"📰 {headline}\n📝 {summary}\n📊 Sentiment: {score:.2f}\n{'-'*50}\n")

        sentiment_avg = sum(sentiment_scores_filtered) / len(sentiment_scores_filtered) if sentiment_scores_filtered else 0
        combined_score = sentiment_avg * 0.5 + f_score * 0.3 + analyst_score * 0.2

        f.write(f"\n🧮 Sentiment average: {sentiment_avg:.2f}\n")
        f.write(f"📊 Fundamentals score: {f_score:.2f}\n")
        f.write(f"🗣️ Analyst score: {analyst_score:.2f}\n")
        f.write(f"🔗Combined score: {combined_score:.2f}\n")
        f.write(f"\n{recommendation}\n")


# Multi-Symbol Main Function
def main_multi(symbols: list[str], start_date: str, end_date: str):
    """
    Runs the complete analysis for multiple stock symbols.
    Steps:
      1. Retrieves news, fundamentals, and analyst data from Finnhub.
      2. Uses Ollama AI to analyze sentiment for each news item.
      3. Calculates fundamentals and analyst scores.
      4. Combines them into a final recommendation.
      5. Saves detailed results and an overall Excel summary.
    """
    client = finnhub.Client(api_key=API_KEY)
    results = []

    for symbol in symbols:
        print(f"\n🔎 Analyzing news for {symbol} from {start_date} to {end_date}...\n")

        try:
            news_items = client.company_news(symbol, _from=start_date, to=end_date)
            fundamentals = client.company_basic_financials(symbol, 'all')
            analyst_data = client.recommendation_trends(symbol)
        except Exception as e:
            print(f"⚠️ Error for symbol '{symbol}': {e}")
            print("⏭️ Skipping this symbol.\n" + "-"*60)
            continue

        analyst_score = evaluate_recommendation_trends(analyst_data)

        sentiment_scores_all = []
        sentiment_scores_filtered = []

        for item in news_items:
            headline = item.get("headline", "")
            summary = item.get("summary", "")
            text = f"{headline} — {summary}"
            print(f"📰 {text}")

            score = analyze(text, symbol)
            sentiment_scores_all.append(score)

            if -1 <= score <= 1:
                sentiment_scores_filtered.append(score)

            print(f"📊 Sentiment: {score}\n{'-'*50}")

        f_score = evaluate_fundamentals(fundamentals)
        recommendation = recommend_combined(sentiment_scores_filtered, f_score, analyst_score)
        print(f"\n✅ {recommendation}")

        filename = f"analysis_result_{symbol}_{end_date}.txt"
        save_results(
            symbol,
            start_date,
            end_date,
            news_items,
            sentiment_scores_all,  # All scores for the file
            sentiment_scores_filtered,
            f_score,
            analyst_score,
            recommendation,
            filename
        )
        print(f"📝 Results saved to '{filename}'.")

        sentiment_avg = sum(sentiment_scores_filtered) / len(sentiment_scores_filtered) if sentiment_scores_filtered else 0.0
        combined_score = sentiment_avg * 0.5 + f_score * 0.3 + analyst_score * 0.2

        results.append({
            "Symbol": symbol,
            "Start Date": start_date,
            "End Date": end_date,
            "Sentiment Average": round(sentiment_avg, 2),
            "Fundamentals Score": round(f_score, 2),
            "Analyst Score": round(analyst_score, 2),
            "Combined Score": round(combined_score, 2),
            "Recommendation": recommendation
        })

    # Save Excel summary file
    df = pd.DataFrame(results)
    excel_filename = f"full_analysis_{end_date}.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"\n📊 Overall results saved to '{excel_filename}'")
    
    

# Run for different lists
if __name__ == "__main__":
    
    START_DATE = "2025-07-19"
    END_DATE = "2025-08-19"
    
    NASDAQ_LIST = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "AVGO", "NFLX",
    "COST", "PLTR", "AMD", "CSCO", "ASML", "TMUS", "AZN", "LIN", "INTU", "PEP",
    "BKNG", "ISRG", "TXN", "SHOP", "AMGN", "PDD", "QCOM", "ARM", "ADBE", "AMAT",
    "GILD", "HON", "APP", "MELI", "LRCX", "MU", "ADP", "CMCSA", "KLAC", "SNPS",
    "PANW", "ADI", "CRWD", "DASH", "CEG", "MSTR", "SBUX", "CDNS", "VRTX", "CTAS",
    "REGN", "FTNT", "ROST", "MRVL", "IDXX", "TEAM", "ZS", "CHTR", "PAYX", "ODFL",
    "BIIB", "EXC", "FAST", "XEL", "EA", "DXCM", "WBD", "MAR", "DLTR", "BIDU",
    "NTES", "ALGN", "VRSK", "GEN", "PCAR", "ON", "KDP", "TTD", "LCID", "SIRI",
    "VRSN", "SBAC", "CTSH", "CDW", "INCY", "NXPI", "MTCH", "TTWO", "VERI", "ZS",
    "FISV", "OKTA", "ANSS", "META", "AEP", "EXPE", "WBA", "KHC", "MNST", "UAL"]
    
    DOW_LIST = [
    "MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT",
    "NKE", "PG", "CRM", "TRV", "UNH", "VZ", "V", "WBA", "WMT", "DIS"]
    
    SINGLE_SYMBOL = ['MSFT']
    
    DIV_STRAT = ['MAIN', 'O', 'ABBV', 'OHI', 'VZ']
    
    main_multi(NASDAQ_LIST, START_DATE, END_DATE)
