# Insect Ditector-Classifier Project
- This codes are written for the project of a club <i>seeds</i>, which is developing the application of insect, pest. I have participated as the developer of embedded AI application.
- This repository consists of two parts, crawler and preprocessor. Because AI is based on <a href = "https://github.com/ultralytics/yolov5">YOLOv5</a> of <i>ultralytics</i>, I have focused on applying well-known method of training models and preprocessing dataset.

## [ 01 ] Crawler
- Image crawler is based on <a href = "https://www.selenium.dev/"><i>selenium</i></a> and <i>Google Chrome Driver</i>.
- By compatibility, the version of own chrome has to be 113.-. 
- If there is no input files for keywords this crawler searchs for keywords in input files, else creates default input keywords files and searchs for default keywords.
	- \<preparing\> 1) get the input file for classes. 2) create or get the input files as diverse extensions.
