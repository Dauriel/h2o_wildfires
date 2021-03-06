### Summary
Our approach consists on a lightweight [YOLOv5](https://github.com/ultralytics/yolov5) model trained to detect smoke. This model is trained over the [Wildfire Smoke Detection Dataset](https://github.com/aiformankind/wildfire-smoke-detection-research) created by [AI for Mankind](https://aiformankind.org/).

### Model description

| Info       |          |
|------------|----------|
| Model      | YOLOv5s6 |
| Batch size | 32       |
| Img size   | 64       |
| Epochs     | 100      |

Training time: 1.578 hours

### Dataset

The Dataset is provided by AI for Mankind. It is comprised of 2191 labelled images. These images were taken using a HPWREN camera lp-s-mobo-c. This was the only Dataset we found that with this characteristics.

### Metrics

When it comes to selecting a good metric, smoke detection is quite similar to other Computer Vision challenges in the domain of medical imaging. A False Positive is inexpensive, as it just requires someone to verify whether the image contains smoke, whereas a False Negative can be really expensive, as it might lead to a late response and a potential catastrophe (analogously, in medical imaging, a False Positive tumor detection will lead to more tests whereas a False Negative might lead to death).

With this in mind, the two main metrics we should prioritize are True Positives and False Negatives. This ratio is the Recall metric. 

This would be true in normal circumstances. However, given that we are approaching this problem as an Object Detection task, focusing on the Mean Average Precision 0.5:0.95 (mAP@0.5:0.95) allows our model to train and generalize better. 

We obtained our best model checkpoint on the 83rd epoch, with a mAP@0.5:0.95 of 0.31895.

### Disclaimer

A big limitation of our model is the training data. It contains a small number of images and they all come from a relatively similar context. Due to the nature of this dataset, the model might not perform accurately when exposed to images that vary significantly from the original context the model was trained in. However, given the simplicity of the model and our approach, finetuning the model should not be a problem. 

### Future ideas

Our approach is just the basis and there are many ways in which it can be developed further:

- We treat the problem as an object detection problem due to the dataset available. Another approach would be treating it as a binary image classification problem, where images are labelled positive or negative based on the presence of smoke and the model just predicts if there is smoke in the image or not.
- All of the training images are set during the day. Another way of improving the model would be considering different contexts (day, night, etc). Creating a more homogeneous dataset would definitely improve the capability of our model to generalize to other contexts.
- All images come from the same camera. Increase the spectrum of image sizes and resolutions in the dataset would improve the performance of the model.
- Increasing the size of the dataset should also improve the model.
- We did not use any data augmentation when training the model. Using some simple augmentations, like HorizontalFlip or CLAHE would also improve this.
- Adding cloud images should also improve the robustness of the model.
