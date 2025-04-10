from trends import get_repeat_mistake_summary
import csv
from analyzer import generate_game_gif
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory
from analyzer import analyze_pgn, plot_evaluation_graph, save_excel_report, get_average_accuracy
import os

app = Flask(__name__)
UPLOAD_FOLDER = "pgns"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["pgn_file"]
    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], "uploaded.pgn")
    file.save(filepath)
    side = request.form.get("player_side", "white")
    generate_game_gif(filepath)


    analysis = analyze_pgn(filepath)
    plot_evaluation_graph(analysis)
    save_excel_report(analysis)
    player_moves = [m for i, m in enumerate(analysis) if (side == "white" and i % 2 == 0) or (side == "black" and i % 2 == 1)]
    opponent_moves = [m for i, m in enumerate(analysis) if (side == "white" and i % 2 == 1) or (side == "black" and i % 2 == 0)]


    # Save for trend tracking
    with open("backend/static/all_games.csv", "a", newline="") as f:
        writer = csv.writer(f)
        for row in analysis:
            writer.writerow([datetime.now().isoformat()] + list(row))

    avg_accuracy = get_average_accuracy(analysis)
    trends = get_repeat_mistake_summary()

    return render_template(
    "results.html",
    avg_accuracy=avg_accuracy,
    trends=trends,
    moves=player_moves,
    opponent_moves=opponent_moves,
    side=side
)



    return f'''
        <h1>Analysis Complete!</h1>
        <img src="/static/eval_graph.png" width="700"><br><br>
        <strong>Average Accuracy:</strong> {avg_accuracy}%<br>
        <strong>Repeated Issues Detected:</strong><br>
        - Mistakes: {trends['mistakes']}<br>
        - Blunders: {trends['blunders']}<br>
        - Inaccuracies: {trends['inaccuracies']}<br>
        - Mistake Rate: {trends['mistake_percent']}% of all moves<br><br>
        <a href="/static/analysis_report.xlsx" download>📥 Download Excel Report</a><br><br>
        <a href="/">🔁 Analyze Another Game</a>
    '''


if __name__ == "__main__":
    app.run(debug=True)
