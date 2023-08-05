from types import SimpleNamespace

from src.utils.keyboard import create_keyboard

keys = SimpleNamespace(
    random_connect=':envelope: Random Connect',
    settings=':gear: Settings'
)

keyboards = SimpleNamespace(
    main=create_keyboard(keys.random_connect, keys.settings)
)

states = SimpleNamespace(
    main='MAIN',
)