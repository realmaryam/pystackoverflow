from types import SimpleNamespace
import emoji

from src.utils.keyboard import create_keyboard

keys = SimpleNamespace(
    settings=emoji.emojize(':gear: Settings'),
    cancel=emoji.emojize(':x: Cancel'),
    back=emoji.emojize(':arrow_left: Back'),
    ask_question=emoji.emojize(':question: Ask Question'),
)

keyboards = SimpleNamespace(
    main=create_keyboard(keys.ask_question, keys.settings)
)

states = SimpleNamespace(
    main='MAIN',
    ask_question= 'ASK QUESTION'
)