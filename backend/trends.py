import pandas as pd

def get_repeat_mistake_summary(filepath="backend/static/all_games.csv"):
    df = pd.read_csv(filepath, header=None, on_bad_lines='skip')
    df.columns = ["Timestamp", "Move Number", "Move", "Eval", "Category", "Accuracy", "Tip"]

    category_counts = df["Category"].value_counts()
    common_mistakes = category_counts.get("Mistake", 0)
    blunders = category_counts.get("Blunder", 0)
    inaccuracies = category_counts.get("Inaccuracy", 0)

    return {
        "mistakes": common_mistakes,
        "blunders": blunders,
        "inaccuracies": inaccuracies,
        "total_moves": len(df),
        "mistake_percent": round(100 * (common_mistakes + blunders + inaccuracies) / len(df), 2)
    }
