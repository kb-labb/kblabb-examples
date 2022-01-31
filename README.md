## KBLab code examples

A repository to share useful code snippets and tutorials for projects that may not warrant their own repositories. 
This repo is organized in the following manner:

- 	**api**: Examples and tutorials on how to use the datalab and betalab APIs.
-	**text**: Text processing and NLP. 
-	**image**: How to work with images datalab/betalab APIs.
-	**docker**: docker environment and dockerfile setups for common tasks. 

Examples can be found in subfolders of the above listed directories. Each example (subfolder) should have its own README with instructions and explanations.

After an example is submitted, authors are encouraged to add a link to the example (subfolder) in this README file with a short summary of the purpose and contents of the example. 

## Example Links

### api

[**Filter packages**](https://github.com/kb-labb/kblabb-examples/tree/master/api/filter_packages): Select only the specific newspapers, parliamentary minutes, etc., that you are interested in. Learn to use `kblab` python package and custom API calls to filter search queries based on title, creation date, textual content and more. 

### text

[**Machine Translation on the GPU using MarianNMT**](https://github.com/kb-labb/kblabb-examples/tree/master/text/machine_translation_gpu): Perform Neural Machine Translation to translate sentences from one language to another. We provide an inference script that is better (more efficient) than the examples provided in the official huggingface documentation. Useful if you want to translate a large number of sentences with good GPU utilization. 

### image

[**Download and annotation of images from datalab**](https://github.com/kb-labb/kblabb-examples/tree/master/images/annotation): Shows how to download metadata of all newspaper packages in datalab API, followed by an example how to use that downloaded metadata to sample relevant packages. We then download useful OCR data from the sampled packages as well as images of each newspaper page and save them to disk. Finally we show how to import OCR boxes to the annotation software Label Studio as predictions.

### docker 
