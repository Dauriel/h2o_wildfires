from .model import *

async def home(q:Q):
    issues = []

    # Home description
    q.page['ds'] = ui.article_card(box=ui.box('description', order=2), title="TEAM HTB - Smoke Detection", content=open('data/home.md').read())

    await q.page.save()



