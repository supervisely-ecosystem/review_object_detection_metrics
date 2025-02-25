<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48245050/182582390-378b2853-2038-49d4-99bb-1d656eda7fdf.png"/>

# Interactive Object Detection Metrics 

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Prerequisite">Prerequisite</a> •
  <a href="#References">Acknowledgement</a>
  <a href="#References">Screenshot</a>
</p>


[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com/apps/supervisely-ecosystem/review_object_detection_metrics/supervisely)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/review_object_detection_metrics)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/review_object_detection_metrics/supervisely.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/review_object_detection_metrics/supervisely.png)](https://supervisely.com)

</div>

# Overview
This app is an interactive visualization for object detection metrics. 
It allows to estimate performance of any detection model by comparing ground truth annotations with predictions.

⚠️ **Notice**: This app a beta version, it is in active development. In case of any issues, please let us know.

Run app and folow the following steps:
1. Select to projects: with ground truth labels and detection predictions
2. App matches images in both projects and produces detailed report about matched pairs. It allows to validate data
3. Classes from both projects are also matched, user should select some that will be used in metrics calculation. 
All non bbox classes will be automatically converted to bounding boxes
4. Configure metric settings: confidence and IoU thresholds
This app a beta version, it is in active development. In case of any issues, please let us know.
5. Then you can see confusion matrix, click on the cell to see all images. If you click on the row of the images table 
you will see the widget with matched objects. Use zoom in/out to study small objects on images

⚠️ **Notice**: Objects on images from prediction project without tag 'confidence' will be considered as correctly founded (with 'confidence' level = 1.0)
Information about these objects could be founded in app logs(they are marked as 'Warn').

# Acknowledgement
We forked the source code of [Object Detection Metrics repo](https://github.com/rafaelpadilla/Object-Detection-Metrics).
It is most popular implementation of detection metrics. We adopted it for Supervisely format and created the interactive 
dashboard with tons of visualizations. 

# Prerequisite
Prepare two projects: ground truth and predictions. Each bounding box in predictions project should have a tag 
`confidence` with value between 0 and 1. You can use our prepared sample projects: 

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/pascal_sample_gt" src="https://i.imgur.com/wYPHUJ0.png" width="350px"/>

and 

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/pascal_sample_pred" src="https://i.imgur.com/q6xUnW6.png" width="390px"/>


# Screenshot

<img src="https://i.imgur.com/xBrUAv9.png"/>
