# Forex Trading Bot with Transformer and EMA

This project is a forex trading bot that connects to the IQ Option API, uses a Transformer model to predict market movements, and incorporates an Exponential Moving Average (EMA) strategy to make informed trading decisions. The bot operates only when the predicted probability, combined with the EMA trend, exceeds a 70% confidence threshold.

## Features
- **Real-time connection to IQ Option**: The bot fetches real-time candle data (OHLC) from IQ Option and processes it.
- **Transformer model for prediction**: A trained Transformer model predicts whether the market will rise (call) or fall (put).
- **EMA (Exponential Moving Average)**: The bot uses a 20-period EMA to adjust its decision-making process.
- **Confidence threshold**: The bot only operates when the probability of a successful trade exceeds 70%.

## Requirements
- Python 3.7+
- An IQ Option account (credentials stored securely in a `.env` file)
- Required Python libraries (see installation below)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Seem1019/forexia.git
    cd forex-trading-bot
    ```

2. Set up a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
   - Create a `.env` file in the root directory and add your IQ Option credentials:
    ```makefile
    IQ_OPTION_EMAIL=your-email@example.com
    IQ_OPTION_PASSWORD=your-password
    ```

5. Download the trained Transformer model:
    - Ensure the trained model (`transformer_model.pth`) is available in the `models/` directory.

## How to Use

To start the bot, execute the `mainia.py` file:

```bash
python mainia.py
```
# The bot will:
- Connect to the IQ Option API.
- Fetch real-time candle data for the specified currency pair (e.g., EUR/USD OTC).
- Use the Transformer model to predict whether to make a call (buy) or put (sell) based on the current market.
- Adjust the prediction using the EMA to determine the market trend.
- Only place a trade if the adjusted prediction probability is greater than 70%.
## How It Works

### Transformer Model
- The bot uses a Transformer-based model trained on historical candle data to predict market movements.
- It processes 20 consecutive candles (OHLC data) and outputs a prediction for whether the price will rise (call) or fall (put).

### EMA (Exponential Moving Average)
- The bot calculates a 20-period EMA using the closing prices of the most recent candles.
- If the current price is above the EMA, it indicates an uptrend, and a bias of +0.2 is added to the model’s prediction.
- If the current price is below the EMA, it indicates a downtrend, and a bias of -0.2 is applied.

### Confidence Threshold
- After combining the model’s prediction with the EMA bias, the bot operates only if the final probability is greater than 70%.
- If the probability is lower, no trade is executed, and the bot waits for new data.

## Customization

### Modify Trading Pair
- You can change the trading pair (e.g., EUR/USD, USD/JPY) directly in the `mainia.py` file:
    ```python
    ciclo_de_operaciones_transformer(iq_handler, "EURUSD-OTC", model)
    ```

### Adjust the EMA Period
- To change the EMA period from the default of 20 to another value, modify the `calcular_ema` function in `mainia.py`:
    ```python
    ema_actual = calcular_ema(close_prices, timeperiod=20)
    ```

### Set a Different Confidence Threshold
- You can adjust the confidence threshold for placing trades by changing this value in the `hacer_inferencia_transformer` function:
    ```python
    if probabilidad >= 0.7:
        # Proceed with trade
    ```

## Example Output

Upon running the bot, you should see output like the following:

```vbnet
Connected to IQ Option successfully.
EURUSD-OTC is available for trading.
Fetching 25 candles for EURUSD-OTC...
Logits: 0.62, Probability: 0.72
Uptrend (price above EMA). Adjusted probability: 0.92
Action: Call
```
## Disclaimer
This project is for educational purposes only. Trading involves substantial risk and is not suitable for every investor. You are solely responsible for any trades or decisions made based on the results of this bot.
