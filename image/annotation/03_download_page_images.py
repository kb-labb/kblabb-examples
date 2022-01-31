import pandas as pd
import os
import requests
import multiprocessing
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
import glob
from PIL import Image


df = pd.read_feather("data/df_content.feather")
df["filename"] = (
    df["dark_id"]
    + "_part"
    + df["part"].str.pad(width=2, side="left", fillchar="0")
    + "_page"
    + df["page"].str.pad(width=3, side="left", fillchar="0")
    + ".jpg"
)

df_page = df.drop_duplicates(subset=["filename"], keep="first")


def download_page_image(
    page_image_url,
    filename,
    api_password,
    backoff_factor=0.1,
    output_height=1600,
    output_folder="images",
):

    os.makedirs(output_folder, exist_ok=True)

    for i in range(5):
        backoff_time = backoff_factor * (2 ** i)

        response = requests.get(
            url=f"{page_image_url}/full/,{output_height}/0/default.jpg",
            auth=HTTPBasicAuth("demo", api_password[0]),
        )

        if response.status_code == 200:
            break

    image = response.content
    with open(f"{output_folder}/{filename}", "wb") as image_file:
        image_file.write(image)


file_input = open("../api_credentials.txt", "r")
pw = file_input.read().splitlines()
backoff_factor = 0.02

url_and_filename = list(df_page[["page_image_url", "filename"]].itertuples(index=False))
args = [(x[0], x[1], pw, backoff_factor) for x in url_and_filename]

pool = multiprocessing.Pool()
pool.starmap(download_page_image, tqdm(args), chunksize=20)
pool.close()


def get_local_image_size(df):
    local_image_sizes = []

    for filename, page_id in zip(df.filename, df.page_id):
        image = Image.open(f"images/{filename}")
        width, height = image.size

        local_image_sizes.append(
            {
                "page_id": page_id,
                "page_image_width_local": width,
                "page_image_height_local": height,
            }
        )

    df_local_image_size = pd.DataFrame(local_image_sizes)
    df = pd.merge(df, df_local_image_size, how="left", on="page_id")

    return df


df_page = get_local_image_size(df_page)
df = pd.merge(
    df,
    df_page[["page_id", "page_image_width_local", "page_image_height_local"]],
    how="left",
    on="page_id",
)

df.to_feather("data/df_content.feather")
