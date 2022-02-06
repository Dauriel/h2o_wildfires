from .model import *
from const import example_images

import pandas as pd

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
                    ui.tag(label='NO', color='$mint'),
                    ui.tag(label='YES', color='$red'),
                    ]
    )),
    ui.table_column(name='confidence', label='Confidence', sortable=True, )
]

# Functions for data tab.

async def home(q:Q):

    issues = []

    # Render figure's html on on the form card.
    q.page['hm'] = ui.form_card(box=ui.box('home', order=2), items=[
        ui.message_bar(type='info', text=open('README.MD').read())
    ])

    await q.page.save()

    # get history dataframe
    df = q.app.detection_history

    # create monitoring table
    for row in df.itertuples(index=False):
        # print(row[0], row[1], row[2], row[3])
        issues.append(
            Issue(
                timestamp=row[0],
                text=row[1],
                state=('YES' if row[2] == 1 else 'NO'),
                confidence=row[3]
            )
        )

    q.page['left'] = ui.form_card(box=ui.box('left'), items=[
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

    q.page['right'] = ui.form_card(box=ui.box('right'), items=[
        ui.text('Stats')
    ])

    await q.page.save()


# Init existing datasets for the app.
async def load_history(q: Q):
    q.app. detection_history = {}
    data_dir = 'data'

    df = pd.read_csv(f'{data_dir}/history.csv', parse_dates=['timestamp'], sep=';')
    # Add this dataset to the list of app's datasets.
    q.app.detection_history = df


