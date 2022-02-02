import os
from .ui_utils import *

from .components import get_target_image, get_target_image_display, get_action_card

TOOL_INFO = '''
This page allows to create smoke detection starting from images;
'''


async def detection(q:Q):
    if (q.app.target_image):
        q.page['target_image'] = get_target_image_display(q)
    else:
        q.page['target_image'] = get_target_image(q)

    q.page['action_card'] = get_action_card(q)

    await q.page.save()
