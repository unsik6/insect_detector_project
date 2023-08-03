# Insect Detector-Classifier Project
- This codes are written for the project of a club <i>seeds</i>, which is developing the application of insect, pest. I have participated as the developer of embedded AI application.
- This repository consists of two parts, crawler and preprocessor. Because AI is based on <a href = "https://github.com/ultralytics/yolov5">YOLOv5</a> of <i>ultralytics</i>, I have focused on applying well-known method of training models and preprocessing dataset.

## [ 01 ] <a href = "https://github.com/unsik6/insect_detector_project/blob/main/img_crawler_embedded.py">Crawler</a>
&nbsp;&nbsp;Image crawler is based on <a href = "https://www.selenium.dev/"><i>selenium</i></a> and <i>Google Chrome Driver</i>. By compatibility, the version of own chrome has to be 113.-. If there is no input files for keywords this crawler searchs for keywords in input files, else creates default input keywords files and searchs for default keywords.
  - \<preparing\> 1) get the input file for classes. 2) create or get the input files as diverse extensions.

## [ 02 ] <a href = "https://github.com/unsik6/insect_detector_project/blob/main/pseudo_labeler.py">Pseudo-Labeler</a>
&nbsp;&nbsp;Pseudo-labeler is labeling the raw images using pre-trained yolov5 model. This pseudo-labeler make the working time more less. You can specify whether the keywords given by argument is crawled by crawler. And, run <i>detect.py</i> of pre-trained yolov5 (also given by argument) with source images, which crawled by embedded-crawler or just given.

### How to use
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
