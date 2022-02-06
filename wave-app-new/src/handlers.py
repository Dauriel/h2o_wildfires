from .components import *
from .ui_utils import make_base_ui
from .plot import to_html

import plotly.express as px

from skimage import io
import time

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
    await make_base_ui(q)


async def reset_target_image(q: Q):
    # await q.site.unload(q.app.target_image)
    reset_pipeline_variables(q)
    q.app.target_image = None
    await make_base_ui(q)


async def target_image_upload(q: Q):
    links = q.args.target_image_upload
    if links:
        q.app.target_image = links[0]
        q.page['meta'].dialog = None
        await make_base_ui(q)


async def run(q: Q):
    q.app.detection_in_progress = True
    await make_base_ui(q)

    hub_address = os.environ.get(f'H2O_WAVE_ADDRESS', 'http://127.0.0.1:10101')
    im = io.imread(f'{hub_address}{q.app.target_image}')

    start = time.time()

    predictions = q.app.model.inference(im)
    image = q.app.model.create_image(im, predictions)


    q.app.predicted_html = await q.run(to_html, px.imshow(image))
    q.app.detection_complete = True

    await make_base_ui(q)
    await q.page.save()
