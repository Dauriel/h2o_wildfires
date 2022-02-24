from h2o_wave import main, app, Q, ui
import pandas as pd
import plotly.express as px
from .plot import *

import time

_id = 0

class Issue:
    def __init__(self, timestamp: str, text: str, state: str, confidence: str):
        global _id
        _id += 1
        self.id = f'I{_id}'
        self.timestamp = timestamp
        self.text = text
        self.state = state
        self.confidence = confidence

# Create columns for our issue table.
columns = [
    ui.table_column(name='created', label='Timestamp', sortable=True, data_type='time'),
    ui.table_column(name='file', label='File Name', sortable=True, searchable=True),
    ui.table_column(name='tag', label='Smoke Detected', cell_type=ui.tag_table_cell_type(name='tags', tags=[
                    ui.tag(label='FATAL', color='$red'),
                    ui.tag(label='WARNING', color='$yellow')
                    ]
    )),
    ui.table_column(name='confidence', label='Confidence', sortable=True, )
]

# Functions for data tab.

async def report(q:Q):
    issues = []

    # Home description
    q.page['ds'] = ui.form_card(box=ui.box('description', order=2), items=[
        ui.message_bar(type='info', text="This section serves as report of real time detection. Here we can monitor "
                                         "the timestamp and the occurences of smoke for a specific video/camera.")
    ])

    # get history dataframe
    df = pd.DataFrame(q.app.issues, columns =['Timestamp', 'Camera', 'Confidence'])
    df.Confidence = df.Confidence.astype('float64')

    # create monitoring table
    for row in df.itertuples(index=False):
        # print(row[0], row[1], row[2], row[3])
        if row[2] != 0:
            issues.append(
                Issue(
                    timestamp=row[0],
                    text=row[1],
                    state=('FATAL' if row[2] >= 0.70 else 'WARNING'),
                    confidence=int(row[2]*100)
                )
            )

    q.page['left-df'] = ui.form_card(box='left-df', items=[
        ui.text('Detection history'),
        ui.table(
            name='issues',
            columns=columns,
            rows=[ui.table_row(
                name=issue.id,
                cells=[issue.timestamp.isoformat(), issue.text, issue.state, str(issue.confidence)]
            ) for issue in issues],
            groupable=True,
            downloadable=True,
            resettable=True,
            height='400px'
        )
    ])

    q.page.save()

    fig = px.line(df, x='Timestamp', y='Confidence', color='Camera', title='Time Series with Rangeslider')
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-.50, xanchor="right", x=1))
    plt = await q.run(to_html, fig)

    q.page['right-st'] = ui.form_card(box='right-st', items=[
        ui.frame(content=plt, height='500px')
    ])

    fig = px.line(df, x='Timestamp', y='Confidence', color='Camera',title='Time Series with Rangeslider')
    fig.update_xaxes(rangeslider_visible=True)

    await q.page.save()



