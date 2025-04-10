# chess-trainer
AI-powered PGN analyzer with move evaluation, tips, and GIF replay
Chess Trainer - Setup Instructions
🧠 Overview
Chess Trainer is an AI-powered chess analysis and coaching tool. It allows users to upload PGN files, choose their side (white or black), and receive categorized evaluations, tips, best move recommendations, visual graphs, and Excel reports.
 
✅ Prerequisites
•	macOS (tested)
•	Python 3.11+
•	Homebrew (for installing Stockfish)
 
📦 Installation Steps
1.	Clone or Download the Project
cd Desktop
mkdir chess-trainer
cd chess-trainer

# (Move project files into this directory)
2. Set Up Python Virtual Environment

python3.11 -m venv chesstrainer-env
source chesstrainer-env/bin/activate
 

3. Install Dependencies

pip install --upgrade pip
pip install flask stockfish python-chess pandas openpyxl matplotlib pillow cairosvg

4. Install Stockfish (via Homebrew)
brew install stockfish
Make sure it's located at:
/opt/homebrew/bin/stockfish
Or update the STOCKFISH_PATH in analyzer.py accordingly.
 
🚀 Running the App
1. Activate the Environment
source chesstrainer-env/bin/activate
2. Set the Flask App and Run
export FLASK_APP=backend/app.py
flask run
Open browser at:
http://127.0.0.1:5000
 
 
🧩 Features
•	Upload PGN and choose your color
•	Evaluation of each move
•	Classification: Best, Excellent, Inaccuracy, Mistake, Blunder
•	Coaching tips and best move recommendations
•	Animated chess replay GIF
•	Excel report export
•	Mistake tracking across games
 
📁 File Structure
  
🧪 Sample PGNs
Put your test .pgn files into the pgns/ folder or upload them via the homepage.
 
![image](https://github.com/user-attachments/assets/2c73358f-921b-4553-90d0-24e1b4339152)
