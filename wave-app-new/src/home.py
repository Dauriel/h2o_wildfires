from .model import *

async def home(q:Q):
    issues = []

    # Home description
    q.page['ds'] = ui.form_card(box=ui.box('description', order=2), items=[
        ui.message_bar(type='info', text=open('data/home.md').read())
    ])

    await q.page.save()



