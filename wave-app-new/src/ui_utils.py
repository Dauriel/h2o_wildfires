from h2o_wave import main, app, Q, ui

from .components import *

import io
import numpy as np

# Tabs for the app's navigation menu.
tabs = [
    ui.tab(name='home', label='Home'),
    ui.tab(name='detection', label='Image'),
        ui.tab(name='realtime', label='Real Time')
]

# Display header and footer just once per client.
async def init_ui(q: Q):
    # Header card for title ecc .
    q.page['header'] = ui.header_card(box='header', title='Smoke Detection Tool', subtitle='HTB Team')

    # Footer card to display a caption of embeded html for the footer.
    q.page['footer'] = ui.footer_card(
        box='footer',
            caption='Made with 💛️ using H2O Wave - HTB Team'
    )


# Display a navigation menu with tabs.
async def render_menu(q:Q):
    if q.client.initialized:
        q.page['tabs'] = ui.tab_card(name='tabs', box='tabs', link=True, value=q.client.tabs, items=[
            *tabs,
        ])
        await q.page.save()


# UI util function to make a ui.markdown_table from a pd.dataframe.
async def make_markdown_table(fields, rows):
    def make_markdown_row(values):
        return f"| {' | '.join([str(x) for x in values])} |"

    return '\n'.join([
        make_markdown_row(fields),
        make_markdown_row('---' * len(fields)),
        '\n'.join([make_markdown_row(row) for row in rows]),
    ])


# Each time a new tab is rendered, clean the 'body' zone, i.e. delete the pages for the other tabs.
async def reset_pages(q:Q):
    pages = ['df', 'hm', 'map', 'models', 'metrics', 'options', 'target_image', 'target_video', 'action_card',
             'left', 'right', 'stepper', 'detection']

    for page in pages:
        del q.page[page]
    
    await q.page.save()


async def make_base_ui(q: Q):
    await reset_pages(q)

    if q.client.tabs == "detection":

        if (q.app.target_image):
            q.page['target_image'] = get_target_image_display(q)
        else:
            q.page['target_image'] = get_target_image(q)

        q.page['action_card'] = get_action_card(q)

        q.page['stepper'] = get_stepper(q)

        if q.app.detection_complete:
            q.page['detection'] = get_predicted_image(q)
        elif q.app.detection_in_progress:
            q.page['detection'] = get_detection_progress_card(q)
        else:
            del q.page['detection']

    if q.client.tabs == "realtime":

        if (q.app.target_video):
            hub_address = os.environ.get(f'H2O_WAVE_ADDRESS', 'http://127.0.0.1:10101')
            vidcap = cv2.VideoCapture(f'{hub_address}{q.app.target_video}')
            success, image = vidcap.read()

            r_image = cv2.resize(image, dsize=(640, 480), interpolation=cv2.INTER_CUBIC)

            if success:
                _, img = cv2.imencode('.jpg', r_image.astype(np.uint8))
                io.BytesIO(img)
                endpoint = await q.site.uplink('stream_1', 'image/jpeg', io.BytesIO(img))
                q.page['target_video'] = get_target_video_display(q, endpoint)

                await q.page.save()
            else:
                q.page['target_video'] = get_target_video(q)
        else:
            q.page['target_video'] = get_target_video(q)

        q.page['action_card'] = get_action_card_video(q)

        q.page['stepper'] = get_stepper(q)

    await q.page.save()