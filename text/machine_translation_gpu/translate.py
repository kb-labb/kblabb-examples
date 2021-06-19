import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch.utils.data import Dataset, DataLoader

# from transformers import MarianTokenizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

df = pd.read_table(
    "stsbenchmark/sts-train.csv",
    header=None,
    names=["genre", "type", "year", "id", "score", "sentence1", "sentence2"],
)

# We only translate one of the sentences for demonstration purposes.
class CaptionDataset(Dataset):
    def __init__(self, df, tokenizer_name):
        self.df = df
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        sentence1 = df.loc[index, "sentence1"]
        # sentence2 = df.loc[index, "sentence2"]

        tokens1 = self.tokenizer(
            sentence1, return_tensors="pt", padding="max_length", max_length=128
        )
        # tokens2 = self.tokenizer(
        #     sentence2, return_tensors="pt", padding="max_length", max_length=128
        # )

        return tokens1["input_ids"].squeeze_(0)


tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-sv")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-sv")

test_data = CaptionDataset(df, "Helsinki-NLP/opus-mt-en-sv")
test_dataloader = DataLoader(
    test_data, batch_size=64, shuffle=False, num_workers=4, prefetch_factor=2
)
model.to(device)

# a = next(iter(test_dataloader))

with torch.no_grad():
    decoded_tokens = []
    for i, batch in enumerate(tqdm(test_dataloader)):
        output_tokens = model.generate(batch.to(device))
        decoded_tokens += tokenizer.batch_decode(output_tokens, skip_special_tokens=True)

df["sentence1_swedish"] = decoded_tokens
df.to_csv("stsbenchmark/sts_train_swe.csv")
