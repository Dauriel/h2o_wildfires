import os
import sys
import traceback
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Optional

from h2o_wave import Q, ui
from h2o_wave.core import expando_to_dict

from const import GLOBAL_HANDLERS


@dataclass
class WaveColors:
    # Colors from Wave default Theme.
    # https://github.com/h2oai/wave/blob/4ec0f6a6a2b8f43f11cdb557ba35a540ad23c13c/ui/src/theme.ts#L86
    red: str = '#F44336'
    pink: str = '#E91E63'
    purple: str = '#9C27B0'
    violet: str = '#673AB7'
    indigo: str = '#3F51B5'
    blue: str = '#2196F3'
    azure: str = '#03A9F4'
    cyan: str = '#00BCD4'
    teal: str = '#009688'
    mint: str = '#4CAF50'
    green: str = '#8BC34A'
    lime: str = '#CDDC39'
    yellow: str = '#FFEB3B'
    amber: str = '#FFC107'
    orange: str = '#FF9800'
    tangerine: str = '#FF5722'
    brown: str = '#795548'
    gray: str = '#9E9E9E'


@dataclass
class WhiteSpace:
    # https://qwerty.dev/whitespace/
    zero_width: str = '​'
    hair: str = ' '
    six_per_em: str = ' '
    thin: str = ' '
    punctuation: str = ' '
    four_per_em: str = ' '
    three_per_em: str = ' '
    figure: str = ' '
    en: str = ' '
    em: str = ' '
    braille: str = '⠀'


def clear_cards(q: Q):
    for x in q.app.cards:
        del q.page[x]


async def ui_crash_card(q: Q, app_name, card_name, box, label, path):
    error_msg_items = [
        ui.text_xl('Error!'),
        ui.text_l(
            'Sorry for the Inconvenience. '
            f'Please refresh your browser to restart {app_name}. '
        ),
        ui.buttons(
            items=[ui.button(name='show_autodoc_reports', label='Close', primary=True)],
            justify='start',
        ),
        ui.text_xs('⠀'),
    ]
    error_report_items = [
        ui.text('To report this crash, please go to'),
        ui.link(label=label, path=path, target='_blank'),
        ui.text_xs('⠀'),
    ]
    type_, value_, traceback_ = sys.exc_info()
    stack_trace = traceback.format_exception(type_, value_, traceback_)
    stack_trace_items = [ui.text('**Stack Trace**')] + [
        ui.text(f'`{x}`') for x in stack_trace
    ]
    q_args = [f'{k}: {v}' for k, v in expando_to_dict(q.args).items()]
    q_args_str = '**q.args**\n```\n' + '\n'.join(q_args) + '\n```'
    q_args_items = [ui.text_m(q_args_str)] + [ui.text_xs('⠀')]
    error_report_items.extend(q_args_items + stack_trace_items)
    error_report = [
        ui.expander(
            name='error_report',
            label='Report this error',
            expanded=False,
            items=error_report_items,
        )
    ]
    error_items = error_msg_items + error_report + [ui.text_xs('⠀')] * 2
    q.page[card_name] = ui.form_card(box=box, items=error_items)
    await q.page.save()


def default_qualifier(q: Q, arg_name: str) -> bool:
    return getattr(q.args, arg_name)


def handler(qualifier: Optional[Callable[[Q, Any], bool]] = default_qualifier):
    def handler_decorator(func):
        @wraps(func)
        async def handle_func(q: Q, *args, **kwargs):
            if qualifier(q, func.__name__):
                print(f'Calling {func.__name__} ...')
                await func(q, *args, **kwargs)

        GLOBAL_HANDLERS.append(handle_func)
        return handle_func

    return handler_decorator
