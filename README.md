# FinAIc - Splintered information. Sharp decisions. 

AI-powered stock insight toolkit. Assembling a mosaic of market signals.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [Ideal Use Cases](#ideal-use-cases)
- [License](#license)
- [Contributing](#contributing)

---

## Overview

FinAIc is a side project born out of curiosity for markets, data, and machine learning. It blends AI-powered sentiment analysis, basic fundamental scoring, and analyst rating trends to spit out rough buy/hold/sell signals.
It pulls in real-time news, key financial ratios, and aggregated Wall Street opinions to surface patterns and spark ideas. Whether you're a trader, a quant, or just someone who enjoys tinkering with financial data, this toolkit is meant to be explored, not blindly followed.

⚠️ Disclaimer: This is not financial advice. It’s a hobby project. If the code says “Buy,” don’t take it personally — or literally.

The codebase has been cleaned up and documented with AI assistance to make it easier to read, tweak, and build on. Fork it, break it, improve it — all welcome.

---

## Features

- **Real-Time News Sentiment Analysis**  
  Fetches headlines and summaries from Finnhub, then uses an Ollama NLP model to assign a numeric sentiment score.

- **Fundamental Data Scoring**  
  Calculates health metrics such as current ratio, sales growth, net margin, and beta to gauge financial strength.

- **Analyst Recommendation Trends**  
  Aggregates buy/hold/sell ratings from multiple analysts for a wider perspective on market consensus.

- **Multi-Signal Recommendation Engine**  
  Weights sentiment, fundamentals, and analyst scores to generate a unified recommendation.

- **Exportable Results**  
  Outputs detailed `.txt` reports and summary `.xlsx` files for deeper research or record-keeping.

---

## Tech Stack

- **Language:** Python 3.x  
- **Core Libraries:**  
  - `pandas` — data manipulation and Excel export  
  - `finnhub-python` — market data API client  
  - `ollama` — AI/NLP sentiment scoring  
  - `re` — text cleaning & preprocessing  

- **APIs:**  
  - Finnhub.io for news and fundamentals (but you can modify it for every other API)  
  - Ollama for local or server-based LLM-driven sentiment  

---

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/FinAIc.git
cd FinAIc

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

1. Obtain a free API key from [Finnhub.io](https://finnhub.io).  
2. Set your Finnhub API key in the script.  
3. Ensure Ollama is installed and your chosen model (e.g., `gemma3:27b`) is running.  
4. Run the analysis:

   ```bash
   python finsight_ai.py
   ```

5. Check your output files in the project folder:  
   - `analysis_result_<symbol>_<enddate>.txt`  
   - `full_analysis_<enddate>.xlsx`

The example files follow the naming convention shown above  
and can be found in the main repository folder.
 

---

## Example Output

```text
🧮 Sentiment Average:   0.65
📊 Fundamental Score:   0.80
🗣️ Analyst Score:      0.55
🔗 Combined Score:      0.67

✅ Recommendation:      Buy
```

---

## 🔮 Ideal Use Cases

- Day traders seeking instant sentiment snapshots  
- Long-term investors validating fundamentals before entry  
- Quantitative analysts integrating sentiment into larger models  

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Pull requests are welcome!  

Before submitting, please:

1. Open an issue to discuss your proposed change.  
2. Fork the repo and create a feature branch.  
3. Write clear commit messages and include tests or examples when applicable.  
4. Submit a pull request once your work is ready for review.  
