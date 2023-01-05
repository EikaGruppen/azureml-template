from pathlib import Path
import argparse
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import mlflow

parser = argparse.ArgumentParser("model_selection")
parser.add_argument("--train_input_path", type=str, help="Input path of the train set")
parser.add_argument("--C", type=float, help="C")
parser.add_argument("--model_output_path", type=str, help="Output path of the model")
parser.add_argument(
    "--params_output_path", type=str, help="Output path for the parameters used"
)

args = parser.parse_args()

train_dat = pd.read_parquet(args.train_input_path)

scores = []
for fold_key in train_dat.fold.unique():
    train_folds = train_dat.loc[lambda x: x.fold != fold_key].drop(columns=["fold"])
    val_fold = train_dat.loc[lambda x: x.fold == fold_key].drop(columns="fold")

    train_y = train_folds.pop("species").values
    val_y = val_fold.pop("species").values

    train_X = train_folds.to_numpy()
    val_X = val_fold.to_numpy()

    lr = LogisticRegression(C=args.C, penalty="l2", multi_class="multinomial")
    lr.fit(X=train_X, y=train_y)
    y_pred = lr.predict(val_X)

    scores.append(accuracy_score(val_y, y_pred))

accuracy = np.mean(np.array(scores))
print(f"Accuracy: {accuracy}")
mlflow.log_metric("accuracy", accuracy)
mlflow.sklearn.save_model(lr, args.model_output_path)

params = {"C": args.C}
with Path(args.params_output_path).open(mode="w") as f:
    json.dump(params, f)
