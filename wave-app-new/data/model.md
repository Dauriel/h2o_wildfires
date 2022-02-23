## Technical Documentation

### Summary
Our approach consists on a lightweight Yolo model trained to detect smoke. This model is trained over the [Wildfire Smoke Detection Dataset](https://github.com/aiformankind/wildfire-smoke-detection-research) created by [AI for Mankind](https://aiformankind.org/).

The solution is in the form of a jupyter notebook that contains detailed descriptions of each step. We developed the code on a Google Colab instance, so just by uploading it and running it fully you should obtain equivalent results to ours.

### Model description

| Info       |          |
|------------|----------|
| Model      | Yolov5s6 |
| Batch size | 32       |
| Img size   | 64       |
| Epochs     | 100      |

Training time: 1.578 hours

### Dataset

The Dataset is provided by AI for Mankind. It is comprised of 2191 labelled images. These images were taken using a HPWREN camera lp-s-mobo-c. This was the only Dataset we found that with this characteristics.

### Disclaimer

A big limitation of our model is the training data. It contains a small number of images and they all come from a relatively similar context. Due to the nature of this dataset, the model might not perform accurately when exposed to images that vary significantly from the original context the model was trained in. However, given the simplicity of the model and our approach, finetuning the model should not be a problem. 

### Future ideas

Our approach is just the basis and there are many ways in which it can be developed further:

1. - We treat the problem as an object detection problem due to the dataset available. Another approach would be treating it as a binary image classification problem, where images are labelled positive or negative based on the presence of smoke and the model just predicts if there is smoke in the image or not.
2. - All of the training images are set during the day. Another way of improving the model would be considering different contexts (day, night, etc). Creating a more homogeneous dataset would definitely improve the capability of our model to generalize to other contexts.
3. - All images come from the same camera. Increase the spectrum of image sizes and resolutions in the dataset would improve the performance of the model.
4. - Increasing the size of the dataset should also improve the model.
5. - We did not use any augmentation when training the model. Using some simple augmentations, like HorizontalFlip or CLAHE would also improve this.
6. - Adding cloud images should also improve the robustness of the model.
