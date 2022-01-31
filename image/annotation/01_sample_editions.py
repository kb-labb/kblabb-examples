import pandas as pd
from pandas.core.frame import DataFrame

df: DataFrame = pd.read_feather("data/all_metadata.feather")
df = df[df["created"] >= "1990-01-01"]
# Keep only one edition when newspaper has multiple editions in same day
df = df.drop_duplicates(subset=["title", "created"], keep="first")

most_common_newspapers = (
    df.groupby("title").count().sort_values("dark_id", ascending=False).iloc[0:15,].index.values
)
df = df[df["title"].isin(most_common_newspapers)]
df = df.sample(n=200, random_state=1)

df = df.reset_index(drop=True)
df.to_feather("data/sampled_editions.feather")
