from h2o_wave import main, app, Q, ui

from .ui_utils import *
from .initializers import *
from . import home, detection, realtime, model_description

import warnings
warnings.filterwarnings("ignore")

@app('/')
async def serve(q: Q):
    # Initialize app and client if not already initialized.
    if not q.app.initialized:
        await init_app(q)

    if not q.client.initialized:
        await init_client(q)

    # Attach a flex layout for the cards.
    await layouts(q)

    # Check which tab is active and invoke the corresponding handler.
    await handler(q)

# A FLEX LAYOUT FOR AN ADAPTIVE UI
async def layouts(q:Q):
    q.page['meta'] = ui.meta_card(box='', theme='h2o-light', title = 'Smoke Detection | HTB Team', layouts=[
        # Apply layout to all viewport widths.
        ui.layout(breakpoint='xs', zones=[
            # Predefine app's wrapper height to 100% viewpoer height.
            ui.zone(name='main', size='100vh', zones=[
                # Zone for the header.
                ui.zone(name='header', size='80px'),
                # Zone for navigation menu.
                ui.zone('tabs'),
                # Zone for the actual content and data.
                ui.zone(name='body', size='1', zones=[
                    ui.zone(name='description'),
                    ui.zone(name='data'),
                    ui.zone(name='map'),
                    # Image Smoke Detection
                    ui.zone(
                        'split',
                        direction=ui.ZoneDirection.ROW,
                        zones=[
                            ui.zone('left', align='center', size='50%', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('right', size='50%', direction=ui.ZoneDirection.COLUMN),
                        ],
                    ),
                    ui.zone(
                        'split2',
                        direction=ui.ZoneDirection.ROW,
                        zones=[
                            ui.zone('left-df', size='50%', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('right-st', size='50%', direction=ui.ZoneDirection.COLUMN),
                        ],
                    ),
                    ui.zone(
                        's0',
                        direction=ui.ZoneDirection.ROW,
                        zones=[
                            ui.zone('l0', size='33%', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('c0', size='33%', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('r0', size='33%', direction=ui.ZoneDirection.COLUMN),
                        ],
                    ),
                    ui.zone(
                        's1',
                        direction=ui.ZoneDirection.ROW,
                        zones=[
                            ui.zone('l1', size='50%', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('r1', size='50%', direction=ui.ZoneDirection.COLUMN),
                        ],
                    ),
                    ui.zone(name='results')
                ]),
                # App footer of fixed sized, aligned in the center.
                ui.zone(name='footer', size='120px', align='center')
            ])
        ])
    ])

# Handler for tab content.
async def handler(q: Q):
    # Clear ui, delete pages/cards of other tabs.
    await reset_pages(q)

    # Set the current tab to the user-selected tab, otherwise stay on the same tab.
    q.client.tabs = q.args.tabs or q.client.tabs

    # Display the menu bar with different tabs.
    await render_menu(q)

    # Handler for each tab / menu option.
    if q.client.tabs == "home":
        reset_pipeline_variables(q)
        await make_base_ui(q)
        await home.home(q)

    # Handler for each tab / menu option.
    if q.client.tabs == "detection":
        reset_pipeline_variables(q)
        q.app.target_video=None
        await make_base_ui(q)
        await detection.detection(q)

    # Handler for each tab / menu option.
    if q.client.tabs == "realtime":
        reset_pipeline_variables(q)
        q.app.reset_video = True
        q.app.target_image = None
        await make_base_ui(q)
        await realtime.realtime(q)

    if q.client.tabs == 'model_description':
        await model_description.model_description(q)



