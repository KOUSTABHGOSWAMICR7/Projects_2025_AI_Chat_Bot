# AI Chatbot

A neural network-based conversational chatbot built with PyTorch and served via a Flask web application. The chatbot classifies user messages into predefined intents and responds accordingly. It also supports function mappings — allowing specific intents to trigger real Python functions (like fetching live data) alongside a text response.

---

## Project Structure

```
├── main.py              # Core chatbot logic — model definition, training, inference
├── app.py               # Flask web server — API routes and UI serving
├── intents.json         # Intent definitions — patterns and responses
├── dimensions.json      # Saved model metadata — input/output sizes
├── chatbot_model.pth    # Pre-trained model weights
└── templates/
    └── index.html       # Chat web interface
```

---

## How It Works

### 1. Intent Classification
The chatbot reads `intents.json`, which defines a set of **tags** (intent categories). Each tag has:
- **patterns** — example phrases a user might type
- **responses** — possible replies the bot picks from randomly

### 2. NLP Preprocessing
When a user sends a message, it goes through:
- **Tokenization** — splitting the sentence into individual words using NLTK
- **Lemmatization** — reducing words to their base form (e.g. "running" → "run")
- **Bag of Words** — converting the processed words into a binary vector against the full vocabulary

### 3. Neural Network Model
The model is a 3-layer feedforward neural network (MLP) defined in `main.py`:

```
Input Layer  →  128 neurons (ReLU + Dropout)
Hidden Layer →  64 neurons  (ReLU + Dropout)
Output Layer →  N neurons   (one per intent)
```

It uses `CrossEntropyLoss` and the `Adam` optimizer during training.

### 4. Function Mappings
Certain intents can be wired to Python functions. For example, the `stocks` intent triggers `get_stocks()`, which prints a random selection of stocks. This makes the chatbot easily extendable to real actions like querying APIs, databases, or external services.

### 5. Web Interface
`app.py` spins up a Flask server with two routes:
- `GET /` — serves the chat UI (`index.html`)
- `POST /get_response` — accepts a JSON message and returns the bot's response

---

## Prerequisites

Make sure you have Python 3.8+ installed. Then install the required packages:

```bash
pip install flask torch nltk numpy
```

NLTK data is downloaded automatically on first run, but you can also do it manually:

```python
import nltk
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

---

## Running the App

Since the model is already trained and saved (`chatbot_model.pth` and `dimensions.json` are included), you can start the web app directly.

```bash
flask --app app run --debug
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

The chatbot will be live and ready to chat.

> **Why `--debug`?**
> Debug mode does two things: it enables the **auto-reloader**, which automatically restarts the Flask server whenever you edit a file (so you don't have to stop and restart manually after every change), and it activates the **interactive debugger** in the browser if an error occurs, showing you the full traceback. This is particularly useful here since the chatbot loads the model and parses intents at startup — if something goes wrong, you'll see exactly where. Never use `--debug` in a production deployment.

---

## Training the Model (Optional)

If you want to retrain the model from scratch — for example after modifying `intents.json` — run:

```bash
python main.py
```

This will:
1. Parse `intents.json` and build the vocabulary
2. Prepare the training data (bag-of-words vectors)
3. Train the neural network for 100 epochs
4. Save the updated model to `chatbot_model.pth` and `dimensions.json`

You can adjust training parameters directly in `main.py`:

```python
assistant.train_model(batch_size=8, lr=0.001, epochs=100)
```

---

## Supported Intents

| Intent | Example Phrases | Action |
|---|---|---|
| `greeting` | "Hi", "Hello", "Hey" | Text response |
| `goodbye` | "Bye", "See you later", "cya" | Text response |
| `programming` | "What is coding?", "Tell me about programming" | Text response |
| `resource` | "Where can I learn to code?" | Text response |
| `stocks` | "What are my stocks?", "Show my stock portfolio" | Triggers `get_stocks()` + text response |

---

## Adding New Intents

Open `intents.json` and add a new intent block:

```json
{
    "tag": "your_intent_name",
    "patterns": ["Example phrase 1", "Example phrase 2"],
    "responses": ["Your bot reply here"]
}
```

If you want the intent to trigger a Python function, add a mapping in `app.py`:

```python
assistant = ChatbotAssistant("intents.json", function_mappings={
    "stocks": get_stocks,
    "your_intent_name": your_function
})
```

Then retrain the model by running `python main.py`.

---

## Running in Terminal Mode (Without Flask)

You can also chat with the bot directly in your terminal without starting the web server:

```bash
python main.py
```

When prompted, type your message and press Enter. Type `/quit` to exit.

---

## Tech Stack

- **PyTorch** — neural network model training and inference
- **NLTK** — natural language preprocessing (tokenization, lemmatization)
- **Flask** — web server and REST API
- **NumPy** — data preparation and array handling
