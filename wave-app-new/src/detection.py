import os
from .ui_utils import *

from .components import make_example_image_dialog, make_upload_image_dialog

from .initializers import reset_pipeline_variables

TOOL_INFO = '''
            This page allows to create smoke detection starting from images;
            '''


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