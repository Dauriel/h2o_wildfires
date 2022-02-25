import os
from .components import *
from .ui_utils import make_base_ui

import plotly.express as px

from skimage.io import imread
import numpy as np
import cv2
import io

import datetime
import time

import plotly
from plotly.missing_ipywidgets import FigureWidget

def to_html(fig: FigureWidget):
    config = {'scrollZoom': False, 'showLink': False, 'displayModeBar': False}
    return plotly.io.to_html(fig, validate=False, include_plotlyjs='cdn', config=config)

def reset_pipeline_variables(q: Q):
    q.app.running_pipeline = False
    q.app.upload_complete = False
    q.app.detection_in_progress = False
    q.app.detection_complete = False


async def open_upload_image_dialog(q: Q):
    await make_upload_image_dialog(q)
    await q.page.save()


async def open_example_image_dialog(q: Q):
    await make_example_image_dialog(q)
    await q.page.save()


async def example_image_chosen(q: Q):
    q.page['meta'].dialog = None
    q.app.target_image = q.args.example_image_selected
    q.app.upload_complete = True
    await make_base_ui(q)


async def reset_target_image(q: Q):
    reset_pipeline_variables(q)
    q.app.target_image = None
    await make_base_ui(q)


async def target_image_upload(q: Q):
    links = q.args.target_image_upload
    if links:
        q.app.target_image = links[0]
        q.page['meta'].dialog = None
        await make_base_ui(q)

"""
    Video handlers
"""

async def open_example_video_dialog(q: Q):
    await make_example_video_dialog(q)
    await q.page.save()

async def reset_target_video(q: Q):
    q.app.reset_video = False
    reset_pipeline_variables(q)
    q.app.target_video = None
    await make_base_ui(q)

async def target_video_upload(q: Q):
    await reset_target_video(q)
    links = q.args.target_video_upload
    if links:
        q.app.target_video = links[0]
        q.page['meta'].dialog = None
        await make_base_ui(q)

async def open_upload_video_dialog(q: Q):
    await make_upload_video_dialog(q)
    await q.page.save()

async def example_video_chosen(q: Q):
    await reset_target_video(q)
    q.page['meta'].dialog = None
    q.app.upload_complete = True
    q.app.target_video = q.args.example_video_selected
    await make_base_ui(q)

"""
    Run pipeline for image
"""

async def run(q: Q):
    q.app.detection_in_progress = True
    q.app.upload_complete = True
    await make_base_ui(q)

    hub_address = os.environ.get(f'H2O_WAVE_ADDRESS', 'http://127.0.0.1:10101')
    im = imread(f'{hub_address}{q.app.target_image}')

    predictions = q.app.model.inference(im)
    image = q.app.model.create_image(im, predictions)

    q.app.predicted_html = await q.run(to_html,
                                       px.imshow(image).update_xaxes(showticklabels=False).update_yaxes(showticklabels=False))
    q.app.detection_complete = True

    await make_base_ui(q)
    await q.page.save()

async def play(q: Q):
    q.app.detection_in_progress = True
    q.app.upload_complete = True
    await make_base_ui(q)
    
    hub_address = os.environ.get(f'H2O_WAVE_ADDRESS', 'http://127.0.0.1:10101')
    vidcap = cv2.VideoCapture(f'{hub_address}{q.app.target_video}')
    success, img = vidcap.read()

    r_image = cv2.resize(img, dsize=(640, 480), interpolation=cv2.INTER_CUBIC)
    predictions = q.app.model.inference(r_image)

    count = 0
    index = 0
    FPS = 1/30

    while success and q.app.reset_video:

        r_image = cv2.resize(img, dsize=(640, 480), interpolation=cv2.INTER_CUBIC)

        if count % 2:
            predictions = q.app.model.inference(r_image)
            for idx, row in predictions.iterrows():
                issue = [datetime.datetime.now(), q.app.target_video.split('/')[-1], row.confidence]
                q.app.issues.append(issue)
            if len(predictions) == 0:
                issue = [datetime.datetime.now(), q.app.target_video.split('/')[-1], 0]
                q.app.issues.append(issue)

        image = q.app.model.create_image(r_image, predictions)

        _, img = cv2.imencode('.jpg', image.astype(np.uint8))
        await q.site.uplink('stream_1', 'image/jpeg', io.BytesIO(img))

        success, img = vidcap.read()

        count += 1
        time.sleep(FPS)

    print('VIDEO - DONE')
    q.app.detection_complete = True
    await make_base_ui(q)
    await q.page.save()
