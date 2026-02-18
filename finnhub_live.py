from flask import Flask, render_template_string
import finnhub

app = Flask(__name__)

api_key = "d6a4ot1r01qsjlb9nsi0d6a4ot1r01qsjlb9nsig"   # <-- PUT YOUR REAL API KEY HERE
client = finnhub.Client(api_key=api_key)

symbols = [
    "BINANCE:BTCUSDT",
    "BINANCE:ETHUSDT",
    "BINANCE:SOLUSDT",
    "BINANCE:BNBUSDT"
]

def calculate_signal(symbol):
    try:
        data = client.quote(symbol)

        current = data.get('c', 0)
        prev_close = data.get('pc', 1)
        high = data.get('h', current)
        low = data.get('l', current)
        change_percent = data.get('dp', 0)

        trend_strength = ((current - prev_close) / prev_close) * 100
        volatility_ratio = (high - low) / prev_close

        score = 0
        score += trend_strength * 20
        score += change_percent * 15

        if volatility_ratio > 0.02:
            score += 20

        buy_probability = max(0, min(100, 50 + score))
        sell_probability = max(0, min(100, 50 - score))

        if buy_probability > 60:
            bias = "BUY"
        elif sell_probability > 60:
            bias = "SELL"
        else:
            bias = "NO TRADE"

        return {
            "symbol": symbol,
            "price": round(current, 2),
            "buy": int(buy_probability),
            "sell": int(sell_probability),
            "bias": bias
        }

    except Exception:
        return {
            "symbol": symbol,
            "price": "API ERROR",
            "buy": 0,
            "sell": 0,
            "bias": "ERROR"
        }

@app.route("/")
def home():
    return "Trading AI is running 🚀"

def dashboard():
    results = [calculate_signal(symbol) for symbol in symbols]

    html = """
    <html>
    <head>
        <title>Crypto Signal Dashboard</title>
        <meta http-equiv="refresh" content="10">
        <style>
            body { font-family: Arial; background: #111; color: white; text-align: center; }
            table { margin: auto; border-collapse: collapse; width: 70%; }
            th, td { padding: 12px; border-bottom: 1px solid #333; }
            th { background: #222; }
            .buy { color: #00ff88; font-weight: bold; }
            .sell { color: #ff4d4d; font-weight: bold; }
            .neutral { color: #ccc; }
            .error { color: orange; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>🚀 Real-Time Crypto Signal Dashboard</h2>
        <table>
            <tr>
                <th>Symbol</th>
                <th>Price</th>
                <th>BUY %</th>
                <th>SELL %</th>
                <th>Bias</th>
            </tr>
            {% for r in results %}
            <tr>
                <td>{{ r.symbol }}</td>
                <td>{{ r.price }}</td>
                <td>{{ r.buy }}%</td>
                <td>{{ r.sell }}%</td>
                <td class="
                    {% if r.bias == 'BUY' %}buy
                    {% elif r.bias == 'SELL' %}sell
                    {% elif r.bias == 'ERROR' %}error
                    {% else %}neutral
                    {% endif %}
                ">
                    {{ r.bias }}
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(html, results=results)

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

