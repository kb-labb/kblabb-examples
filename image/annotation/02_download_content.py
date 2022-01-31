import time
import pandas as pd
import multiprocessing
import requests
from requests.auth import HTTPBasicAuth
from json import loads
from tqdm import tqdm
from itertools import product


def get_content(dark_id, backoff_factor=0.1):

    for i in range(5):
        backoff_time = backoff_factor * (2 ** i)

        content_structure = requests.get(
            f"https://datalab.kb.se/{dark_id}/content.json", auth=HTTPBasicAuth("demo", pw[0]),
        )

        if content_structure.status_code == 200:
            content_json = loads(content_structure.text)
            df = pd.DataFrame(content_json)
            df["dark_id"] = dark_id

            df = pd.concat(
                [df, pd.DataFrame(df["box"].to_list(), columns=["x", "y", "width", "height"])],
                axis=1,
            )
            df = df.drop(["font", "has_part", "box"], 1)
            df[["x", "y", "width", "height"]] = df[["x", "y", "width", "height"]].astype(int)
            df["area"] = df["width"] * df["height"]
            df = df.rename(columns={"@id": "id", "@type": "type"})
            return df

        else:
            print(f"{dark_id} failed.")

        time.sleep(backoff_time)


def get_structure(dark_id, backoff_factor=0.1):
    for i in range(5):
        backoff_time = backoff_factor * (2 ** i)

        content_structure = requests.get(
            f"https://datalab.kb.se/{dark_id}/structure.json", auth=HTTPBasicAuth("demo", pw[0]),
        )

        if content_structure.status_code == 200:
            structure_json = loads(content_structure.text)
            data_list = []

            for part in structure_json:
                for page in part["has_part"]:
                    # Extract url to page (unique id for page): page_id
                    # Extract url to image file of page: page_image_url
                    data_list.append(
                        {
                            "page_id": page["@id"],
                            "page_image_url": page["has_representation"][1],
                            "page_image_width": page["width"],
                            "page_image_height": page["height"],
                        }
                    )

            df = pd.DataFrame(data_list)
            return df

        else:
            print(f"{dark_id} failed.")

        time.sleep(backoff_time)


def join_content_structure(dark_id, backoff_factor=0.1):
    df_content = get_content(dark_id, backoff_factor)
    df_structure = get_structure(dark_id, backoff_factor)

    # https://betalab.kb.se/dark-3708703#1-3-ARTICLE54597387-ZONE524342888 -> https://betalab.kb.se/dark-3708703#1-3
    df_content["page_id"] = df_content["id"].str.extract("(.*#[0-9]-[0-9]{1,2})")

    # part_nr and page_nr from betalab.kb.se/{dark_id}/#{part_nr}-{page_nr}
    df_content["part"] = df_content["id"].str.extract("((?<=#)[0-9])")
    df_content["page"] = df_content["id"].str.extract("((?<=#[0-9]-)[0-9]{1,2})")

    df = df_content.merge(df_structure, how="left", on="page_id")

    df["page_image_width"] = pd.to_numeric(df["page_image_width"])
    df["page_image_height"] = pd.to_numeric(df["page_image_height"])

    return df


df = pd.read_feather("data/sampled_editions.feather")

file_input = open("../api_credentials.txt", "r")
pw = file_input.read().splitlines()

backoff_factor = 0.02
pool = multiprocessing.Pool()

df_list = pool.starmap(
    join_content_structure,
    tqdm(list(product(list(df["dark_id"]), [backoff_factor]))),
    chunksize=20,
)
pool.close()

df_content = pd.concat(df_list)
df_content = df_content.reset_index(drop=False)

df_content = pd.merge(df_content, df[["dark_id", "title", "created"]], how="left")
df_content = df_content.rename(columns={"created": "date"})

df_content.to_feather("data/df_content.feather")
