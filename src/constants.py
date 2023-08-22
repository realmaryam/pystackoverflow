from types import SimpleNamespace
import emoji

from src.utils.keyboard import create_keyboard

keys = SimpleNamespace(
    settings=emoji.emojize(':gear: Settings'),
    cancel=emoji.emojize(':cross_mark: Cancel'),
    back=emoji.emojize(':arrow_left: Back'),
    ask_question=emoji.emojize(':red_question_mark: Ask Question'),
    send_question=emoji.emojize(':envelope_with_arrow: Send Question'),
)

keyboards = SimpleNamespace(
    main=create_keyboard(keys.ask_question, keys.settings),
    ask_question=create_keyboard(keys.cancel, keys.send_question)
)

states = SimpleNamespace(
    main='MAIN',
    ask_question= 'ASK QUESTION'
)