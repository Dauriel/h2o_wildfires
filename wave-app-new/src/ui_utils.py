from h2o_wave import main, app, Q, ui

from .components import get_target_image, get_target_image_display, get_action_card, make_example_image_dialog

# Tabs for the app's navigation menu.
tabs = [
    ui.tab(name='data', label='Data'),
    ui.tab(name='model', label='Model'),
    ui.tab(name='predict', label='Predict'),
    ui.tab(name='detection', label='Image Detection')
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
    pages = ['df', 'map', 'models', 'metrics', 'options', 'target_image', 'action_card']

    for page in pages:
        del q.page[page]
    
    await q.page.save()

async def make_base_ui(q: Q):
    if (q.app.target_image):
        q.page['target_image'] = get_target_image_display(q)
    else:
        q.page['target_image'] = get_target_image(q)

    q.page['action_card'] = get_action_card(q)

    await q.page.save()