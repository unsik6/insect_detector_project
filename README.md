# Insect Detector-Classifier Project
- This codes are written for the project of a club <i>seeds</i>, which is developing the application of insect, pest. I have participated as the developer of embedded AI application.
- This repository consists of two parts, crawler and preprocessor. Because AI is based on <a href = "https://github.com/ultralytics/yolov5">YOLOv5</a> of <i>ultralytics</i>, I have focused on applying well-known method of training models and preprocessing dataset.

## [ 01 ] <a href = "https://github.com/unsik6/insect_detector_project/blob/main/img_crawler_embedded.py">Crawler</a>
&nbsp;&nbsp;Image crawler is based on <a href = "https://www.selenium.dev/"><i>selenium</i></a> and <i>Google Chrome Driver</i>. By compatibility, the version of own chrome has to be 113.-. If there is no input files for keywords this crawler searchs for keywords in input files, else creates default input keywords files and searchs for default keywords.
  - \<preparing\> 1) get the input file for classes. 2) create or get the input files as diverse extensions.

<br/>

## [ 02 ] <a href = "https://github.com/unsik6/insect_detector_project/blob/main/pseudo_labeler.py">Pseudo-Labeler</a>
&nbsp;&nbsp;Pseudo-labeler is labeling the raw images using pre-trained yolov5 model. This model is pre-trained using <a href = "https://www.kaggle.com/datasets/vencerlanz09/insect-village-synthetic-dataset">Insect Village Synthetic Dataset of MARIONETTE 👺</a>. This pseudo-labeler make the working time more less. You can specify whether the keywords given by argument is crawled by crawler. And, run <i>detect.py</i> of pre-trained yolov5 (also given by argument) with source images, which crawled by embedded-crawler or just given.

```bash
python psedo_labeler.py --images-path [images path] --labeler [yolov5 parent dir] --labels [names of labels] --index [starte index] --conf [confidence threshold] --num [maximum number of crawling each images] (--crawl)
```
<details>
<summary>Arguments</summary>
<div>
	<b>images-path</b> (str) <br/>
	&nbsp;&nbsp;The path of source images (folder or file);<br/>
	- If you don't turn on <i>crawl</i> option, you have to put this path.<br/>
	<br/>
	<b>labeler</b> (str) <br/>
  	&nbsp;&nbsp;The path of yolov5 parent folder; This yolov5 model is used as pseudo-labeler, so <i>detect.py</i> of this yolov5 is called in script. To run this script well, don't revise the name and directory of <i>detect.py</i> and <i>run</i> folder. <br/>
	<br/>
	<b>labels</b> (str, list) <br/>
	&nbsp;&nbsp;The names of label or multiple labels; If you don't turn on <i>crawl</i>i> option, you have to input just one label.
	<b>index</b> (int) (default = 0) <br/>
 	&nbsp;&nbsp;The index of start index of the given label; If the input label is one, then all indices of detected class using pre-trained yolov5 are changed to the given index. Else (multiple labels are given), pseudo-labeling each label is run sequentially. So, Starting with the given index, given labels are mapped in a given order, and the indices detected class are changed.<br/>
	<br/>
	<b>conf</b> (float) (default = 0.25) <br/>
 	&nbsp;&nbsp;Confidence threshold; This argument is passed to <i>detect.py</i> of pre-trained yolov5.<br/>
	<br/>
	<b>num</b> (int) (default = 1000)<br/>
 	&nbsp;&nbsp;The maximum number of crawling each images; This argument is used only when <i>crawl</i> opiton is turned on.<br/>
	<br/>
	<b>crawl</b> (store-true) <br/>
	&nbsp;&nbsp;Crawling option; If on, <i>img_crawler_embedded.py</i> is run using all given labels.
</div>
</details>

<br/>

## [ 03 ] <a href = "https://github.com/unsik6/insect_detector_project/blob/main/wiki_searcher.py">Wiki-Searcher</a>
&nbsp;&nbsp;This wiki data searcher is searching input keywords in <i>Namu-wiki</i> Dump DB. This wiki site is in korean. The base DB is <a href = "https://huggingface.co/datasets/heegyu/namuwiki">namu wiki raw dataset<a> and <a href = "https://huggingface.co/datasets/heegyu/namuwiki-extracted">namu wiki extracted dataset</a> in <i>Hugging Face</i> served by <a href = "https://huggingface.co/heegyu"><i>heegyu</i></a>. The latter is parsed to remove HTML and Markdown elements by <i>heegyu</i>, allowing you to see the data intuitively. But, some data are missing from raw data.

<br/>

## [ 04 ] <a href = "https://github.com/unsik6/insect_detector_project/tree/main/Dataset">Dataset</a>
&nbsp;&nbsp;The dataset in this repository consists of total 2456 images of 20 insects labeled for YOLO. Because the goal of this project is detecting pests, we choose them accordingly. Note that "Drosophila melanogaster"(No.9) belongs to "Drosophilidae"(No.10).

&nbsp;&nbsp;The insects data is collected using scientific name of each insect as keyword for avoiding confusing. **Sadly, the balance of the number of data and the uniformity of the scale or size of images is not good, because there are a few data for some insects.** Thus, I recommand preprocessing handling the number of data and scaling images such as data augmentation.

&nbsp;&nbsp;Because I labeled all data alone, I gave up to construct full dataset. **Note that the lexicographical order to insect name does not equal to label number. And, the label number is not continuous number and zero-based. So, as you already know, you must handle the label numbers before using this data.** (Initially, I composed this dataset with 27 insects and sorted them by species, which led to this issue.)

|No|Scientific name|English name|Korean name|Label|Number of data|
|---|---|---|---|---|---|
|1|Asiablatta kyotensis|Asian wood roach|경도바퀴|4|55|
|2|Asilidae|Bee killer, Robber fly|파리매|19|373|
|3|Bibio tenebrosus|Bibio tenebrosus|검털파리|25|116|
|4|Blaptica dubia|Dubia roach, Orange spotted roach, Guyana spotted roach, Argentinian wood roach|두비아바퀴벌레|11|204|
|5|Blattella germanica|German cockroach|독일바퀴|2|148|
|6|Bradysia agrestis|Bradysia agrestis|작은뿌리파리|20|11|
|7|Cryptocercus kyebangensis|Wood roach|갑옷바퀴|6|23|
|8|Dermatobia hominis|Human botfly|사람피부파리|24|14|
|9|Drosophila melanogaster|Common fruit fly|노랑초파리|23|87|
|10|Drosophilidae|Fruit fly, vinegar fly, pomace fly|초파리|17|105|
|11|Gasterophilus|Moth fly, drain fly|나방파리|14|21|
|12|Glossina|Tsetse botfly|체체파리|16|69|
|13|Gromphadorhina portentosa|Madagascar hissing cockroach|마다가스카르휘파람바퀴|8|320|
|14|Lasioderma serricorne|Cigar beetle, Cigarette beetle, Tobacco beetle|권연벌레|1|142|
|15|Lucilia caesar|Common greenbottle|금파리|22|316|
|16|Lycoriella mali|Lycoriella mali|긴수염버섯파리|18|13|
|17|Musca domestica|Housefly|집파리|21|235|
|18|Oestridae|Botfly, Warble fly, Heel fly, Gadfly|쇠파리|15|109|
|19|Penthetria japonica|Plecia nearctica|계피우단털파리|27|59|
|20|Periplaneta americana|American cockroach|이질바퀴|3|35|
