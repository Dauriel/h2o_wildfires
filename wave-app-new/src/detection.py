import os
from .ui_utils import *

from .components import make_example_image_dialog

TOOL_INFO = '''
This page allows to create smoke detection starting from images;
'''


async def detection(q:Q):
    if q.args.open_upload_image_dialog:
        #TODO Handle image uploading
        print('Unhandled button')
    elif q.args.open_example_image_dialog:
        await open_example_image_dialog(q)
    elif q.args.example_image_chosen:
        await example_image_chosen(q)


async def open_example_image_dialog(q: Q):
    await make_example_image_dialog(q)
    await q.page.save()

async def example_image_chosen(q: Q):
    q.page['meta'].dialog = None
    q.app.target_image = q.args.example_image_selected
    await make_base_ui(q)