import torch
import cv2

class ModelInference(object):

    def __init__(self,
                 yolov5_folder_path: str,
                 model_checkpoint_path: str) -> None:
        """
        Creates an instance of the object detection models
        :param yolov5_folder_path: (str) Path to the git cloned folder (git clone https://github.com/ultralytics/yolov5.git)
        :param model_checkpoint_path: (str) Path to the yolov5s6 checkpoint
        """
        self.model = torch.hub.load(yolov5_folder_path,
                                    'custom',
                                    path=model_checkpoint_path,
                                    force_reload=True)  # local repo
        self.model.conf = 0.25

    def inference(self,
                  img: "numpy.ndarray") -> None:
        """
        Processes images and returns a Pandas DataFrame with the bounding boxes
        :param img: ("numpy.ndarray") Image array
        :return: ("pandas.DataFrame") DataFrame with the bounding boxes
        """
        prediction = self.model(img)
        return prediction.pandas().xyxy[0]


    def create_image(self,
                     img: "numpy.ndarray",
                     predictions: "pandas.DataFrame") -> "numpy.ndarray":
        """
        Creates rectangles for the bounding boxes in a given image
        :param img: ("numpy.ndarray") Image to be annotated
        :param predictions: ("pandas.DataFrame") DataFrame containing the bounding boxes
        :return: ("numpy.ndarray") Annotated image (xmin, ymin, xmax, ymax, confidence)
        """
        for idx, row in predictions.iterrows():
            xmin = int(row.xmin)
            ymin = int(row.ymin)
            xmax = int(row.xmax)
            ymax = int(row.ymax)
            cv2.rectangle(img, (xmin, ymin),
                          (xmax, ymax),
                          (255, 0, 0), 2)

        return img