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


def create_random_image():
    frame = (np.random.rand(100, 100, 3) * 255).astype(np.uint8)
    _, img = cv2.imencode('.jpg', frame)
    return io.BytesIO(img)


async def realtime(q:Q):

    '''

        ### STORE THE VIDEOS IN q.app.stored_video

        import cv2

        # define hub address
        hub_address = os.environ.get(f'H2O_WAVE_ADDRESS', 'http://127.0.0.1:10101')

        # load video from app
        vidcap = cv2.VideoCapture(f'{hub_address}/{q.app.stored_video}')

        success,image = vidcap.read()

        prediction = q.app.model.inference(image)
        v_image = q.app.model.create_image(image, prediction)

        endpoint = await q.site.uplink(q.app.stored_video[...], 'image/jpeg', v_image)

        count = 0
        while success:
            await q.site.uplink(q.app.stored_video[...], 'image/jpeg', v_image)

            if count % 30 == 0:
                prediction = q.app.model.inference(image)

            success,image = vidcap.read()
            v_image = q.app.model.create_image(image, prediction)

            count += 1
    '''

    '''# Mint a unique name for our image stream
    stream_name = f'stream/demo/{uuid.uuid4()}.jpeg'

    # Send image
    endpoint = await q.site.uplink(stream_name, 'image/jpeg', create_random_image())

    # Display image
    q.page['map'] = ui.form_card(box='map', items=[ui.image('Image Stream', path=endpoint)])
    await q.page.save()

    t0 = time.time()
    # Update image in a loop
    for i in range(frame_count):
        # Send image (use stream name as before).
        await q.site.uplink(stream_name, 'image/jpeg', create_random_image())

    await q.site.unlink(stream_name)'''

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