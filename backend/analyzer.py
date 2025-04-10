import matplotlib
matplotlib.use("Agg")  # Use a non-GUI backend for rendering
import chess.pgn
import chess.engine
import os
import matplotlib.pyplot as plt
import pandas as pd


STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"  # Default path from Homebrew on macOS

def categorize(eval_diff):
    if eval_diff == 0:
        return "Best"
    elif eval_diff <= 30:
        return "Excellent"
    elif eval_diff <= 100:
        return "Inaccuracy"
    elif eval_diff <= 300:
        return "Mistake"
    else:
        return "Blunder"

def analyze_pgn(pgn_path):
    with open(pgn_path) as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    board = game.board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    move_analysis = []

    for move_number, move in enumerate(game.mainline_moves(), start=1):
            # Best move from Stockfish
            best_result = engine.analyse(board, chess.engine.Limit(depth=15))
            best_score = best_result["score"].white().score(mate_score=10000)
            best_move = best_result["pv"][0].uci()

            # Actual move
            board.push(move)
            actual_result = engine.analyse(board, chess.engine.Limit(depth=15))
            actual_score = actual_result["score"].white().score(mate_score=10000)

            # Eval difference
            eval_diff = (best_score - actual_score) if best_score and actual_score else 0
            category = categorize(abs(eval_diff))

            # Accuracy scoring
            if move.uci() == best_move:
                accuracy = 100
            elif abs(eval_diff) <= 30:
                accuracy = 90
            elif abs(eval_diff) <= 100:
                accuracy = 70
            elif abs(eval_diff) <= 300:
                accuracy = 50
            elif abs(eval_diff) <= 1000:
                accuracy = 20
            else:
                accuracy = 0

            # 🧠 Add inside the loop, not outside!
            tip = get_tip_for_category(category)
            recommendation = f"Recommended move: {best_move}" if category in ["Mistake", "Blunder", "Inaccuracy"] else ""
            move_analysis.append((move_number, move.uci(), actual_score, category, accuracy, tip, recommendation))


    engine.quit()
    return move_analysis


def plot_evaluation_graph(move_analysis, output_path="backend/static/eval_graph.png"):
    move_nums = [move[0] for move in move_analysis]
    scores = [move[2] for move in move_analysis]

    plt.figure(figsize=(10, 5))
    plt.plot(move_nums, scores, marker='o', color='blue')
    plt.axhline(y=0, color='gray', linestyle='--', label='Even')
    plt.title("Stockfish Evaluation Over Time")
    plt.xlabel("Move Number")
    plt.ylabel("Evaluation (centipawns)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

import pandas as pd

def save_excel_report(move_analysis, output_path="backend/static/analysis_report.xlsx"):
    df = pd.DataFrame(move_analysis, columns=[
    "Move Number", "Move", "Evaluation", "Category", "Accuracy", "Tip", "Recommended Move"
    ])
    df["Accuracy %"] = df["Accuracy"]
    df.drop(columns=["Accuracy"], inplace=True)
    df.to_excel(output_path, index=False)

def get_average_accuracy(move_analysis):
    accuracies = [entry[4] for entry in move_analysis]
    return round(sum(accuracies) / len(accuracies), 2)

import chess.svg
import cairosvg
from PIL import Image
import io

def generate_game_gif(pgn_path, output_path="backend/static/game.gif"):
    with open(pgn_path) as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    board = game.board()
    frames = []

    for move in game.mainline_moves():
        board.push(move)
        svg = chess.svg.board(board=board, size=350)
        png_bytes = cairosvg.svg2png(bytestring=svg)
        image = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        frames.append(image)

    # Save as animated GIF
    frames[0].save(output_path, format="GIF", append_images=frames[1:], save_all=True, duration=800, loop=0)

def get_tip_for_category(category):
    tips = {
        "Inaccuracy": "Consider looking for stronger responses next time. Think about your opponent's threats.",
        "Mistake": "This move weakens your position. Look ahead at possible counter-plays.",
        "Blunder": "This is a major oversight. Review tactics like forks, pins, and skewers.",
    }
    return tips.get(category, "")
