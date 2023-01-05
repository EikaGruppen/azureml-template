import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold

parser = argparse.ArgumentParser("train_test_split")
parser.add_argument(
    "--dataset_input_path", type=str, help="Input path of the input dataset"
)
parser.add_argument(
    "--train_output_path", type=str, help="Output path of the train set"
)
parser.add_argument("--test_output_path", type=str, help="Output path of the test set")
parser.add_argument(
    "--train_size", type=float, help="Portion of dataset to use for training"
)
parser.add_argument(
    "--num_folds", type=int, help="Number of folds to use for cross-validation"
)

args = parser.parse_args()

num_folds = args.num_folds
train_size = args.train_size
if not (0 <= train_size <= 1):
    raise ValueError("Train size must be between 0 and 1.")

dataset_path = args.dataset_input_path
train_path = args.train_output_path
test_path = args.test_output_path

print(f"Input path: {dataset_path}")
print(f"Train path: {train_path}")
print(f"Test path: {test_path}")

dat = pd.read_parquet(str(Path(dataset_path)))
N = dat.shape[0]

train_N = int(np.floor(N * train_size))
train_idx = np.random.choice(np.arange(0, N), size=train_N, replace=False)

train_dat = dat.iloc[train_idx, :].reset_index(drop=True)
test_dat = dat.iloc[~dat.index.isin(train_idx)].reset_index(drop=True)

kfold = KFold(n_splits=num_folds, shuffle=True, random_state=0)
for k, split in enumerate(kfold.split(train_dat)):
    _, fold = split
    train_dat.loc[fold, "fold"] = k + 1
train_dat["fold"] = train_dat.fold.astype(int)

train_dat.to_parquet(str(Path(train_path)))
test_dat.to_parquet(str(Path(test_path)))
