import os
from .ui_utils import *
import cv2

"""
    Images components
"""

def get_target_image(q: Q):
    return ui.form_card(
        box='left',
        title='Input image card',
        items=[
            ui.text('Pick an image and detect smoke with the detect button.'),

            ui.text(''),  # margin top hack

            ui.button(
                name='open_upload_image_dialog',
                label='Upload target image',
                primary=True,
            ),
            ui.button(
                name='open_example_image_dialog',
                label='Use an example image',
            ),
        ],
    )


def get_target_image_display(q: Q):
    return ui.form_card(
        box='left',
        title='Target image',
        items=[
            ui.text(content=''),  # margin top hack
            ui.text(content=f'![target image]({q.app.target_image})', width="620px"),
            ui.button(name="reset_target_image", label="Reset target image")
        ],
    )

"""
    Video components
"""

def get_target_video_display(q: Q, endpoint):
    return ui.form_card(
            box='left',
            title='Target video',
            items=[
                ui.text(content=''),  # margin top hack
                ui.image('Image Stream', path=endpoint),
                ui.button(name="reset_target_video", label="Reset target video")
            ],
        )


def get_target_video(q: Q):
    return ui.form_card(
        box='left',
        title='Input video card',
        items=[
            ui.text('Pick a video and detect smoke with the detect button.'),

            ui.text(''),  # margin top hack

            ui.button(
                name='open_upload_video_dialog',
                label='Upload target video',
                primary=True,
            ),
            ui.button(
                name='open_example_video_dialog',
                label='Use an example video',
            ),
        ],
    )


async def make_upload_video_dialog(q: Q):
    q.page['meta'].dialog = None
    await q.page.save()
    q.page['meta'].dialog = ui.dialog(
        title='Upload target video',
        closable=True,
        items=[
            ui.file_upload(
                name='target_video_upload',
                label='Upload',
                file_extensions=['mp4'],
                height='180px',
            )
        ]
    )

async def make_example_video_dialog(q: Q):
    q.page['meta'].dialog = None
    await q.page.save()

    if 'example_videos' in q.app:
        q.page['meta'].dialog = ui.dialog(
            title='Select example video',
            closable=True,
            items=[
                ui.dropdown(
                    name='example_video_selected',
                    label='Select video',
                    value=q.app.example_videos[0]['wave_path'],
                    choices=[
                        ui.choice(name=vid['wave_path'], label=vid['label'])
                        for vid in q.app.example_videos
                    ],
                ),
                ui.button(name='example_video_chosen', label='Select', primary=True)
            ],
        )
    else:
        q.page['meta'].dialog = ui.dialog(
            title='Loading example videos',
            closable=True,
            items=[
                ui.text('Example videos have not loaded yet. Check back in a few seconds.')
            ],
        )

    await q.page.save()

def get_action_card_video(q: Q):
    sliderSensitivity = q.args.sensitivity if 'sensitivity' in q.args else 60

    return ui.form_card(
        box='right',
        title='Video uploaded',
        items=[
            ui.text('Smoke Detection Model'),
            ui.button(name='play', label='Detect', primary=True, disabled=not q.app.target_video or q.app.running_pipeline),
            ui.message_bar(type='info', text='If the video does not load at the first attempt, please press the reset button and try to upload it again.')
        ],
    )

"""
    ====================
"""

def get_action_card(q: Q):
    sliderSensitivity = q.args.sensitivity if 'sensitivity' in q.args else 60

    return ui.form_card(
        box='right',
        title='Parameters',
        items=[
            ui.text('Smoke Detection Model'),
            ui.button(name='run', label='Detect', primary=True, disabled=not q.app.target_image or q.app.running_pipeline),
        ],
    )

async def make_upload_image_dialog(q: Q):
    q.page['meta'].dialog = None
    await q.page.save()
    q.page['meta'].dialog = ui.dialog(
        title='Upload target image',
        closable=True,
        items=[
            ui.file_upload(
                name='target_image_upload',
                label='Upload',
                file_extensions=['jpg', 'png', 'jpeg'],
                height='180px',
            )
        ]
    )

async def make_example_image_dialog(q: Q):
    q.page['meta'].dialog = None
    await q.page.save()

    if 'example_images' in q.app:
        q.page['meta'].dialog = ui.dialog(
            title='Select example image',
            closable=True,
            items=[
                ui.dropdown(
                    name='example_image_selected',
                    label='Select image',
                    value=q.app.example_images[0]['wave_path'],
                    choices=[
                        ui.choice(name=img['wave_path'], label=img['label'])
                        for img in q.app.example_images
                    ],
                ),
                ui.button(name='example_image_chosen', label='Select', primary=True)
            ],
        )
    else:
        q.page['meta'].dialog = ui.dialog(
            title='Loading example images',
            closable=True,
            items=[
                ui.text('Example images have not loaded yet. Check back in a few seconds.')
            ],
        )

    await q.page.save()

def get_stepper(q: Q):
    return ui.form_card(
        box='results',
        items=[
            ui.stepper(
                name='pipeline-stepper',
                items=[
                    ui.step(label='Upload', icon='CloudUpload', done=bool(q.app.upload_complete)),
                    # ui.step(label='Detection', icon='Compare', done=bool(q.app.model_in_progress)),
                    ui.step(label='Detection', icon='BuildQueueNew', done=bool(q.app.detection_in_progress)),
                    ui.step(label='Inspection', icon='Bullseye', done=bool(q.app.detection_complete)),
                ],
            )
        ],
    )

def get_detection_progress_card(q: Q):
    return ui.form_card(
        box='detection',
        items=[
            ui.progress(label='Detection in progress', caption='Working...')
        ]
    )

def get_predicted_image(q: Q):
    return ui.form_card(box='right', items=[
        ui.frame(content=q.app.predicted_html, height='580px'),
    ])