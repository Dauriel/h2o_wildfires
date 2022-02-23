from .model import *
from const import example_images

from h2o_wave import main, app, Q, ui
import plotly.express as px

import pandas as pd

async def model_description(q:Q):
    issues = []

    # Home description
    q.page['ds'] = ui.form_card(box=ui.box('description', order=2), items=[
        ui.message_bar(type='info', text=open('data/model.md').read())
    ])

    df = q.app.model_metrics
    df['F1'] = 2*df["metrics/precision"] * df["metrics/recall"] / (df["metrics/precision"] + df["metrics/recall"])

    plot_pr = await q.run(to_html, px.line(df, x="epoch", y=['metrics/precision', 'metrics/recall', 'F1'], labels={'Epoch', '%'}))
    plot_map = await q.run(to_html, px.line(df, x="epoch", y=df.columns[6:8], color_discrete_sequence=px.colors.qualitative.Vivid))
    # plot_f1 = await q.run(to_html, px.line(df, x="epoch", y="F1"))

    q.page['l0'] = ui.form_card(box='l0', items=[
        ui.message_bar(type='info', text='Precision vs Recall plot'),
        ui.frame(content=plot_pr, height='400px')
    ])

    q.page['r0'] = ui.form_card(box='r0', items=[
        ui.message_bar(type='info', text='MAP DESCRIPTION'),
        ui.frame(content=plot_map, height='400px')
    ])


    await q.page.save()


# Init existing datasets for the app.
async def load_metrics(q: Q):
    q.app. model_metrics = {}
    data_dir = 'data'

    df = pd.read_csv(f'{data_dir}/train.csv')
    # Add this dataset to the list of app's datasets.
    q.app.model_metrics = df
