# **FinSight‑AI**  
*AI‑Powered Stock Market Sentiment & Fundamentals Analysis Toolkit*  

## 📌 Overview  
FinSight‑AI is an advanced **Python‑based financial analysis toolkit** that combines **AI‑driven sentiment analysis**, **fundamental data evaluation**, and **analyst recommendation trends** to generate **clear buy/hold/sell investment signals**.  

Built for **traders, investors, and quantitative analysts**, it leverages **real‑time market news**, **key financial ratios**, and **analyst sentiment** to deliver actionable market intelligence.  

---

## 🚀 Features  
- 📰 **Real‑Time News Sentiment Analysis**  
  Uses AI (via Ollama NLP models) to score stock‑specific headlines and summaries.  

- 📊 **Fundamental Data Scoring**  
  Evaluates company health using metrics like **current ratio**, **sales growth**, **net margin**, and **beta**.  

- 🗣 **Analyst Recommendation Trends**  
  Incorporates aggregated Wall Street ratings for a more rounded perspective.  

- 🔗 **Multi‑Signal Recommendation Engine**  
  Blends sentiment, fundamentals, and analyst scores into a single actionable output.  

- 📂 **Exportable Results**  
  Generates `.txt` detail reports and `.xlsx` summary files for further research.  

---

## 🛠 Tech Stack  
- **Language:** Python 3.x  
- **Libraries:**  
  - `pandas` — Data analysis & Excel export  
  - `finnhub-python` — Market data API  
  - `ollama` — AI/NLP sentiment scoring  
  - `re` — Text cleaning and preprocessing  
- **APIs:** Finnhub, Ollama  

---

## 🔍 Ollama Integration  
FinSight‑AI uses **Ollama** as its AI/NLP engine for sentiment scoring. The process works as follows:  
1. Headlines and summaries are fetched from **Finnhub** for a given stock symbol.  
2. These are sent to an Ollama model (e.g., `gemma3:27b`) with a **strict system prompt** to rate the sentiment from the perspective of that stock only.  
3. Ollama returns a **numeric sentiment score** which is then weighted with fundamentals and analyst data to form the final recommendation.  

**Why Ollama?**  
- Runs locally or on a server, ensuring control over model usage.  
- Flexible model choice — swap in different LLMs for experimentation.  
- Ensures consistent output format for automated scoring pipelines.  

---

## 📥 Installation  
```bash
# Clone the repository
git clone https://github.com/<your-username>/FinSight-AI.git
cd FinSight-AI

# Install dependencies
pip install -r requirements.txt
```

---

## ⚡ Usage  
1. **Obtain an API key** from [Finnhub.io](https://finnhub.io).  
2. **Configure your API key** in the script.  
3. Ensure **Ollama** is installed and your desired model is available.  
4. Run an analysis:
```bash
python finsight_ai.py
```
5. Results will be saved as:
   - `analyse_ergebnis_<symbol>_<enddate>.txt`
   - `gesamtanalyse_<enddate>.xlsx`

---

## 📈 Example Output  
```
🧮 Sentiment Average: 0.65
📊 Fundamental Score: 0.80
🗣️ Analyst Score: 0.55
🔗 Combined Score: 0.67

✅ Recommendation: Buy
```

---

## 🔮 Ideal Use Cases  
- **Day traders** looking for instant sentiment snapshots  
- **Long‑term investors** validating fundamentals before buying  
- **Quantitative analysts** integrating sentiment into models  

---

## 📜 License  
This project is licensed under the MIT License.  

---

## 💡 Contributing  
Pull requests are welcome — open an issue first to discuss potential changes.  

---

Do you want me to now **add badges and a visual architecture diagram** so your README looks like a top‑tier GitHub project? That would make this pop visually.
