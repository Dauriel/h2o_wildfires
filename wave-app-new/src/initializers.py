from h2o_wave import main, app, Q, ui

from .ui_utils import init_ui
from .detection import load_model
from const import example_images, example_videos

from .model_description import load_metrics

def reset_pipeline_variables(q: Q):
    q.app.running_pipeline = False
    q.app.upload_complete = False
    q.app.detection_in_progress = False
    q.app.detection_complete = False


# A client is a private browser tab, which stores it's own run-time information.
async def init_client(q: Q):
    # Render the header and footer.
    await init_ui(q)

    # Begin application flow with the data tab.
    q.client.tabs = 'home'

    # Flag client as initialized.
    q.client.initialized = True

    await q.page.save()

# App-level initialization, run-time information shared across all users.
async def init_app(q:Q):
    # Get the list of available datasets.
    # await load_datasets(q)
    await load_model(q)
    await load_metrics(q)

    # Load example images
    wave_paths = await q.site.upload([image['path'] for image in example_images])
    for p, example_image in zip(wave_paths, example_images):
        example_image.update({'wave_path': p})
    q.app.example_images = example_images

    # Load example videos
    wave_paths = await q.site.upload([video['path'] for video in example_videos])
    for p, example_video in zip(wave_paths, example_videos):
        example_video.update({'wave_path': p})
    q.app.example_videos = example_videos

    # Reset pipeline variables
    reset_pipeline_variables(q)

    q.app.issues = []

    # Flag app as initialized.
    q.app.initialized = True

