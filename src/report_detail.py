"""
Bonus 3: Tao bao cao precision / recall chi tiet cho mo hinh vua huan luyen.

Doc models/model.joblib va tap holdout, ghi confusion matrix cung precision /
recall cua tung lop ra outputs/detail.txt. Duoc goi trong cicd.yml sau buoc Train.
"""
import os
import joblib
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score

LABELS = {0: "thu_nhap_thap", 1: "thu_nhap_cao"}


def build_report(
    model_path: str = "models/model.joblib",
    eval_path: str = "data/holdout.csv",
) -> str:
    model = joblib.load(model_path)
    df_eval = pd.read_csv(eval_path)
    X_eval = df_eval.drop(columns=["target"])
    y_eval = df_eval["target"]
    preds = model.predict(X_eval)

    tn, fp, fn, tp = confusion_matrix(y_eval, preds, labels=[0, 1]).ravel()
    precision = precision_score(y_eval, preds, labels=[0, 1], average=None, zero_division=0)
    recall = recall_score(y_eval, preds, labels=[0, 1], average=None, zero_division=0)

    lines = [
        "Confusion matrix (hang = thuc te, cot = du doan)",
        f"{'':>16}{'pred=0':>10}{'pred=1':>10}",
        f"{'actual=0':>16}{tn:>10}{fp:>10}",
        f"{'actual=1':>16}{fn:>10}{tp:>10}",
        "",
        f"{'Lop':<20}{'precision':>10}{'recall':>10}",
    ]
    for cls, name in LABELS.items():
        lines.append(f"{f'{cls} ({name})':<20}{precision[cls]:>10.4f}{recall[cls]:>10.4f}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    report = build_report()
    print(report)
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/detail.txt", "w") as f:
        f.write(report)
