import os
from .ui_utils import *
from .handlers import *
import io
from .ui_utils import make_base_ui
import time
import uuid

import cv2
from h2o_wave import app, Q, ui, main
import numpy as np

frame_count = 256

import pandas as pd

import time

_id = 0

class Issue:
    def __init__(self, timestamp: str, text: str, state: str, confidence: str):
        global _id
        _id += 1
        self.id = f'I{_id}'
        self.timestamp = timestamp
        self.text = text
        self.state = state
        self.confidence = confidence

# Create columns for our issue table.
columns = [
    ui.table_column(name='created', label='Timestamp', sortable=True, data_type='time'),
    ui.table_column(name='file', label='File Name', sortable=True, searchable=True),
    ui.table_column(name='tag', label='Smoke Detected', cell_type=ui.tag_table_cell_type(name='tags', tags=[
                    ui.tag(label='FATAL', color='$red'),
                    ui.tag(label='WARNING', color='$yellow')
                    ]
    )),
    ui.table_column(name='confidence', label='Confidence', sortable=True, )
]

# Functions for data tab.


def create_random_image():
    frame = (np.random.rand(100, 100, 3) * 255).astype(np.uint8)
    _, img = cv2.imencode('.jpg', frame)
    return io.BytesIO(img)


async def realtime(q:Q):

    if q.args.open_upload_video_dialog:
        await open_upload_video_dialog(q)

    elif q.args.open_example_video_dialog:
        await open_example_video_dialog(q)

    elif q.args.example_video_chosen:
        await example_video_chosen(q)

    elif q.args.reset_target_video:
        await reset_target_video(q)

    elif q.args.target_video_upload:
        await target_video_upload(q)

    elif q.args.play:
        q.app.reset_video = True
        await play(q)