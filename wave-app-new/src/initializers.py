from h2o_wave import main, app, Q, ui

from .ui_utils import init_ui
from .data import load_datasets
from .model import load_models

def reset_pipeline_variables(q: Q):
    q.app.running_pipeline = False
    q.app.upload_complete = False
    q.app.detection_in_progress = False
    q.app.detection_complete = False
    q.app.classification_in_progress = False
    q.app.classification_complete = False
    q.app.identification_in_progress = False
    q.app.identification_complete = False

# A client is a private browser tab, which stores it's own run-time information.
async def init_client(q: Q):
    # Render the header and footer.
    await init_ui(q)

    # Begin application flow with the data tab.
    q.client.tabs = 'data'

    # Flag client as initialized.
    q.client.initialized = True

    await q.page.save()

# App-level initialization, run-time information shared across all users.
async def init_app(q:Q):
    # Get the list of available datasets.
    await load_datasets(q)
    # Reset pipeline variables
    # TODO manage video pipeline vars
    reset_pipeline_variables(q)
    # Flag app as initialized.
    q.app.initialized = True
