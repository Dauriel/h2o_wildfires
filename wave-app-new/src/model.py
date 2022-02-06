
from h2o_wave import main, app, Q, ui
import lightgbm as lgb
import os
from .ui_utils import *
from .plot import *

# Functions for models tab.

models_dir = 'models'

async def model(q:Q):
    # Get the available models.
    models = list(q.app.models.keys())
    val = q.args.models or models[0]

    # Show models selection/load inputs.
    q.page['models'] = ui.form_card(box=ui.box('data'), items=[
            ui.combobox(name='models', label='Models', choices=models, value=val),
            ui.buttons(justify='center', items=[
                ui.button(name='load', label='Load Model', primary=True),
            ]),
            ui.text(open('models/model_info.md').read()),
    ])
    await q.page.save()

    # Load selected models.
    await load(q, val)

async def load(q:Q, val: str):
    model = q.app.models[val]
    # Show models params with stat cards.
    q.page['metrics'] = ui.form_card(box='data', items=[
            ui.stats(justify='around', items=[
                *[ui.stat(f'{key}', f'{val}') for (key, val) in model.params.items()]
            ])
        ]
    )

    # Update map card to notify bar chart is being made.
    q.page['map'] = ui.form_card(box='map', items=[
        ui.progress(label='Preparing bar chart...')
    ])
    await q.page.save()

    # Load bar chart for the feature importance for the selected models.
    bar_chart = f"{val.strip('.txt')}_features.html"
    q.page['map'] = ui.form_card(box='map', items=[
        ui.frame(content=(open(bar_chart).read()), height='600px')
    ])
    await q.page.save()

# Load app's existing models stored in the local file system.
async def load_models(q:Q):
    q.app.models = models = {}
    models_dir = 'models'

    for model_file in os.listdir(models_dir):
        # Skip if the file is not a models, ending with `.txt`.
        if not model_file.endswith('.txt'):
            continue
        
        # The default models is a lightgbm models, which is initialized.
        model_path = f'{models_dir}/{model_file}'
        model = lgb.basic.Booster(model_file=model_path)
        model_params_file = f"{model_path.strip('.txt')}.params"
        model.params = await get_model_params(model_params_file)
        models[model_path] = model

        # Save the models in app's models dict.
        models[model_path] = model


# Read model_params for a local models from file.
async def get_model_params(model_params_file: str):
    with open(model_params_file) as f:
        contents = f.readlines()

    params = {}
    for line in contents:
        param, param_val = line.strip('\n').split(":")
        params[param] = param_val

    return params