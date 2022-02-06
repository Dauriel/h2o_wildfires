from h2o_wave import main, app, Q, ui

from .components import *

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
    pages = ['df', 'hm', 'map', 'models', 'metrics', 'options', 'target_image', 'action_card',
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

    await q.page.save()