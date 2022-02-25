from .ui_utils import *
from .handlers import *
from model.model_interface import ModelInference

TOOL_INFO = ''' This page allows to create smoke detection starting from images; '''

async def detection(q:Q):
    if q.args.open_upload_image_dialog:
        await open_upload_image_dialog(q)

    elif q.args.open_example_image_dialog:
        await open_example_image_dialog(q)

    elif q.args.example_image_chosen:
        await example_image_chosen(q)

    elif q.args.reset_target_image:
        await reset_target_image(q)

    elif q.args.target_image_upload:
        await target_image_upload(q)

    elif q.args.run:
        await run(q)


# Load app's existing models stored in the local file system.
async def load_model(q: Q):
    q.app.model = ModelInference('ultralytics/yolov5', 'model/model_artifacts.pt')
