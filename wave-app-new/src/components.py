import os
from .ui_utils import *

'''
    Generates ui components
'''

def get_target_image(q: Q):
    return ui.form_card(
        box='left',
        title='Challenge overview',
        items=[
            ui.text('Pick an image and detect smoke with the run button.'),

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
            ui.text(content=f'![target image]({q.app.target_image})'),
            ui.button(name="reset_target_image", label="Reset target image")
        ],
    )

def get_action_card(q: Q):
    sliderSensitivity = q.args.sensitivity if 'sensitivity' in q.args else 60

    return ui.form_card(
        box='right',
        title='Parameters',
        items=[
            ui.text('Yolo Model - Smoke Detection'),
            ui.slider(
                name='Sensitivity',
                label='Sensitivity',
                min=0,
                max=100,
                value=sliderSensitivity,
                step=1,
                tooltip='Chose the cutoff sensitivity of the model.',
            ),
            ui.button(name='run', label='Detect smoke', primary=True, disabled=not q.app.target_image or q.app.running_pipeline),
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
                    ui.step(label='Detection', icon='BuildQueueNew', done=bool(q.app.detection_complete)),
                    ui.step(label='Inspection', icon='Bullseye', done=bool(q.app.identification_complete)),
                ],
            )
        ],
    )