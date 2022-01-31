import pandas as pd
import re
import json
from tqdm import tqdm
from typing import List, Dict

pd.set_option("display.max_colwidth", 80)

df = pd.read_feather("data/df_content.feather")


def create_preannotation_skeleton(filenames: List[str]) -> Dict:
    """
    Pre-annotations according to Label Studios format: https://labelstud.io/guide/predictions.html
    """

    filenames = list(set(filenames))  # If the user supplies duplicate filenames

    preannotation_skeleton = []

    for filename in filenames:
        preannotation_skeleton.append(
            {
                "data": {
                    "image": f"http://localhost/images/{filename}",
                    "title": {},  # filled in later in insert_preannotations
                    "date": {},
                },
                "predictions": [{"result": []}],  # empty result list which we append to later
            }
        )

    return preannotation_skeleton


def insert_preannotations(preannotation_skeleton, df, min_area):
    df_image = df[(df["type"] == "Image") & ((df["area"]) > min_area)]
    df["date"] = df["date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df_meta = df.drop_duplicates(subset=["filename"], keep="first")[["filename", "title", "date"]]
    meta_dict = {x[1]: {"title": x[2], "date": x[3]} for x in df_meta.itertuples()}

    for i, page in enumerate(tqdm(preannotation_skeleton)):

        image_filename = re.sub("http://localhost/images/", "", page["data"]["image"])
        df_page = df_image[df_image["filename"] == image_filename]

        # fmt: off
        preannotation_skeleton[i]["data"]["title"] = meta_dict[image_filename]["title"]
        preannotation_skeleton[i]["data"]["date"] = meta_dict[image_filename]["date"]
        # fmt: on

        for j, segmentation_box in df_page.iterrows():

            preannotation_skeleton[i]["predictions"][0]["result"].append(
                {
                    "id": "result" + str(j + 1),  # segmentation_box["id"],
                    "type": "rectanglelabels",
                    "from_name": "label",
                    "to_name": "image",
                    "original_width": segmentation_box["page_image_width_local"],
                    "original_height": segmentation_box["page_image_height_local"],
                    "image_rotation": 0,
                    "value": {
                        "rotation": 0,
                        "x": round(
                            segmentation_box["x"] / segmentation_box["page_image_width"] * 100, 6,
                        ),
                        "y": round(
                            segmentation_box["y"] / segmentation_box["page_image_height"] * 100,
                            6,
                        ),
                        "width": round(
                            segmentation_box["width"]
                            / segmentation_box["page_image_width"]
                            * 100,
                            6,
                        ),
                        "height": round(
                            segmentation_box["height"]
                            / segmentation_box["page_image_height"]
                            * 100,
                            6,
                        ),
                        "rectanglelabels": [segmentation_box["type"].lower() + "1"],
                    },
                }
            )

        preannotation_skeleton[i]["predictions"][0]["score"] = 0.5

    return preannotation_skeleton


preannotation_skeleton = create_preannotation_skeleton(filenames=df["filename"].tolist())
preannotations = insert_preannotations(preannotation_skeleton, df, min_area=150000)

with open("data/preannotations.json", "w") as f:
    json.dump(preannotations, f)
