A script showing how to use Marian-NMT with better GPU utilization than the examples found in the standard Huggingface documentation. Marian-NMT is used to translate the Semantic Textual Similarity benchmark dataset from English to Swedish. 

## Requirements

Pytorch, pandas, huggingface, tqdm. 

## Instructions

Download the english [STSb (STSbenchmark)](http://ixa2.si.ehu.eus/stswiki/index.php/STSbenchmark). Either download it manually via the browser and untar the `.tar.gz` file or alternatively enter the following commands in your terminal:

```bash
wget http://ixa2.si.ehu.es/stswiki/images/4/48/Stsbenchmark.tar.gz
tar xvzf Stsbenchmark.tar.gz
```

After the stsbenchmark data is downloaded, you can translate by

```bash
python translate.py
```
Results are saved to `stsbenchmark/sts_train_swe.csv`.

**Note**: We assume your working directory is the folder `machine_translation_gpu` and that the stsbenchmark file was downloaded and untarred in this folder. 


## Results

We have only translated `sentence1` in `sts-train.csv` for demonstration purposes. You can adapt the Dataloader and inference loop to fit your own use case!

| genre         | type    | year     | id  | score | sentence1                                      | sentence2                                         | sentence1_swedish                        |
| ------------- | ------- | -------- | ----| ----- | -----------------------------------------------| ------------------------------------------------- | ---------------------------------------- |
| main-captions | MSRvid  | 2012test | 1   | 5.00  |                        A plane is taking off.  |                       An air plane is taking off. |                         Ett plan lyfter. |
| main-captions | MSRvid  | 2012test | 4   | 3.80  |               A man is playing a large flute.  |                         A man is playing a flute. |             En man spelar en stor flöjt. |
| main-captions | MSRvid  | 2012test | 5   | 3.80  | A man is spreading shreded cheese on a pizza.  | A man is spreading shredded cheese on an uncoo... | En man sprider strimlad ost på en pizza. |
| main-captions | MSRvid  | 2012test | 6   | 2.60  |                  Three men are playing chess.  |                        Two men are playing chess. |                   Tre män spelar schack. |
| main-captions | MSRvid  | 2012test | 9   | 4.25  |                   A man is playing the cello.  |                A man seated is playing the cello. |                     En man spelar cello. |

## Performance

Roughly 110 sentences translated per second on an RTX 3090. About 10 words per sentence, so ~1100 words/sec. 