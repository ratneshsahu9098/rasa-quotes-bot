# Rasa Quotes Bot - Beginner's Guide 🤖 quotes

Welcome to your new custom Rasa Quote Recommendation Bot! This guide will walk you through the basic terminal commands you need to run, train, and test your bot.

---
## 0. VERY IMPORTANT
Read important_command.txt , this help's you a lot 
i am using kaggle Qoutes- 500k for dataset here is the link "https://www.kaggle.com/datasets/manann/quotes-500k?resource=download".

## 1. Prerequisites
First, open your terminal and navigate to the directory where you cloned or downloaded this bot:
```bash
cd path/to/your/folder/rasa_quotes_bot
```
*(Replace `path/to/your/folder` with the actual path on your computer)*

**Note on Dataset**: Ensure you have placed the `quotes.csv` file inside the `actions/` folder, as the bot relies on it to recommend quotes.

---

## 2. The Core Commands

### 🧠 Train the Bot
Whenever you change `data/nlu.yml`, `data/stories.yml`, `data/rules.yml`, or `domain.yml`, you must retrain the bot so it learns the new data.
```bash
rasa train
```
*Wait for this to finish. It will create a new model file in the `models/` folder.*

### 🚀 Run the Actions Server (Custom Python Code)
Our bot uses a custom python script (`actions/actions.py`) to read the huge Kaggle CSV dataset and fetch quotes. You **must** have this running in the background for the bot to fetch quotes!
Open a **new, separate terminal window** and run:
```bash
cd path/to/your/folder/rasa_quotes_bot
rasa run actions
```
*Leave this terminal window open and running!*

### 💬 Talk to the Bot (Terminal Mode)
If you just want to quickly test the bot in your terminal text interface:
```bash
rasa shell
```
*Once it loads, type "hi", "I'm sad", "who made you?", or "inspire me!" and press Enter.*

### 🌐 Run the Bot for the Web UI (REST API Mode)
If you want to use the beautiful Web UI we created (`web/index.html`), the bot needs to run as a backend server that accepts API requests rather than a terminal shell.
Run this command:
```bash
rasa run -m models --enable-api --cors "*"
```
*Once this is running, you can double-click `web/index.html` to open your web page and chat!*

---

## 3. Recap: Full Startup Process for the Web UI
To get everything running perfectly for the web page, you need two terminal windows:

**Terminal 1 (Action Server):**
```bash
cd path/to/your/folder/rasa_quotes_bot
rasa run actions
```

**Terminal 2 (Rasa Server):**
```bash
cd path/to/your/folder/rasa_quotes_bot
rasa run -m models --enable-api --cors "*"
```

Now open `web/index.html` in your browser and enjoy! 🎉
