from pathlib import Path
import seaborn as sns

iris = sns.load_dataset("iris")
iris_unlabeled = iris.drop(columns=["species"])

iris.to_parquet(Path("..", "data", "iris.parquet"))
iris_unlabeled.to_parquet(Path("..", "data", "iris_unlabeled.parquet"))

