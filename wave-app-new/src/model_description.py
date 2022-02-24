from .model import *
from const import example_images

import plotly.express as px

import pandas as pd

async def model_description(q:Q):
    q.page['ds'] = ui.form_card(box='description', items=[
        ui.message_bar(type='info', text=open('data/model.md').read())
    ])

    df = q.app.model_metrics
    df['F1'] = 2*df["precision"] * df["recall"] / (df["precision"] + df["recall"])

    q.page['l0'] = ui.small_stat_card(
        box='l0',
        title="Best epoch",
        value="83",
    )

    q.page['c0'] = ui.small_stat_card(
        box='c0',
        title="F1-Score",
        value="0.7183",
    )

    q.page['r0'] = ui.small_stat_card(
        box='r0',
        title="mAP:0.5:0.95",
        value="0.31895",
    )

    fig = px.line(df, x="epoch", y=['precision', 'recall', 'F1'])
    fig.update_layout(legend=dict(orientation = "h", yanchor="bottom", y=-.50, xanchor="right", x=1))
    plot_pr = await q.run(to_html, fig)

    fig = px.line(df, x="epoch", y=df.columns[6:8], color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_layout(legend=dict(orientation = "h", yanchor="bottom", y=-.50, xanchor="right", x=1))
    plot_map = await q.run(to_html, fig)

    q.page['l1'] = ui.form_card(box='l1', items=[
        ui.message_bar(type='info', text='Precision is the ratio between True Positives and all predictions. This metric describes how accurate our model is when detecting smoke on an image. On the other hand, Recall is the ratio between True Positives and all possible positives. To describe this simply: A low precision implies that from all the predictions a model does, only a low percentage are correct, whereas a high precision implies that the predictions the model does are mostly accurate. On the other hand, a low recall implies that the model only finds a small percentage of the possible predictions, whereas a high recall implies that the model is capable of finding most of positives available.'),
        ui.frame(content=plot_pr, height='500px')
    ])

    q.page['r1'] = ui.form_card(box='r1', items=[
        ui.message_bar(type='info', text='The Mean Average Precision (mAP) is a common metric in Object Detection tasks. This metric computes the overlap between the bounding box predicted by the model and the groundtruth bounding box. The higher the score, the bigger of an overlap there is between both. This bounding box overlap has a confidence value, usually set at 0.5. The mAP@0.5:0.95 simply computes the mAP between 0.5 to 0.95 with a 0.05 step'),
        ui.frame(content=plot_map, height='500px')
    ])


    await q.page.save()


# Init existing datasets for the app.
async def load_metrics(q: Q):
    q.app. model_metrics = {}
    data_dir = 'data'

    df = pd.read_csv(f'{data_dir}/train.csv')
    # Add this dataset to the list of app's datasets.
    q.app.model_metrics = df
