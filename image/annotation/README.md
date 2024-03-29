## Overview

Project to set up annotation for images and captions from newspapers using object detection. The image+text pairs may be used to train a Swedish CLIP model. 

This repository samples newspaper editions and downloads their respective newspaper page images. Metadata is also downloaded from the segmentation already performed by OCR. These are used as a starting point for manual annotation with the annotation software Label Studio. 

1. `00_get_metadata.py`: Download metadata about all (newspaper) packages in datalab and save as `all_metadata.feather`.
2. `01_sample_editions.py`: Example of how to sample from the generated metadata file in previous step. 
3. `02_download_content.py`: Download useful information from content.json and structure.json files of each package we have sampled.
4. `03_download_page_images.py`: Download the image of the newspaper page for every page in our sampled packages. 
5. `04_create_labelstudio_preds.py`: Code to turn data of existing OCR-boxes into a format that can be imported into Label Studio as "predictions".

## Import to Label Studio

Run all files in sequential order. Install [Label Studio](https://labelstud.io/). To initialize a project named `newspaper_segmentation` run

```bash
label-studio start newspaper_segmentation --init -db postgresql
```

This initializes the project with a PostgreSQL database instead of SQLite. Open the project `newspaper_segmentation`, go to `Setting` and choose a `Labeling interface`. Here is an example template:

```xml
<View>
  <Image name="image" value="$image" zoom="true"/>
  <RectangleLabels name="label" toName="image">
    <Label value="image" predicted_values="image, image1" background="#e3736d"/>
    <Label value="caption" predicted_values="caption" background="#6774c0"/>
    <Label value="ad" background="#dac860"/>
  </RectangleLabels>
  <Choices name="choice" toName="image" showInLine="true">
    <Choice value="editorial" background="green"/>
    <Choice value="ad" background="red"/>
    <Choice value="mixed" background="yellow"/>
  </Choices>
</View>
```

After this you can import the `data/preannotations.json` file that was generated by running the python scripts and the data should be successfully imported.

To restart Label Studio service after closing it down you only need to be in the same folder as the postgresql file and run `label-studio -db postgresql`.

## Machine Learning backend

To connect an object detection ML backend model trained with the `mmdetection` package, install `label-studio-ml-backend` package. Follow the relevant instructions [here](https://github.com/heartexlabs/label-studio/blob/master/docs/source/tutorials/object-detector.md). Once properly installed and initiated, the ML backend can be started by running a command similar to this one pointing to all your relevant config and model files. 

**Note**: Start this backend in an environment where mmdetection was also installed. 

```bash
label-studio-ml start coco-detector --with \
config_file=mmdetection/work_dirs/config_folder/config_file.py \
checkpoint_file=mmdetection/work_dirs/config_folder/latest.pth \
device=cuda
```

Import the backend by going to `Settings` inside Label Studio. The ML backend is hosted on `http://localhost:9090` by default. Enter this as the URL when connecting to the backend. 