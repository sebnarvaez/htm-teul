"""
Automatically generated Test Data Set
"""

trainingData = (
    (['move', 'tothe', 'north'], ['mover-event', 'arriba-event']),
    (['move', 'towardsthe', 'north'], ['mover-event', 'arriba-event']),
    (['move', 'towardsthe', 'south'], ['mover-event', 'abajo-event']),
    (['please', 'move', 'tothe', 'left'], ['mover-event', 'derecha-event']),
    (['please', 'move', 'tothe', 'north'], ['mover-event', 'arriba-event']),
    (['please', 'move', 'tothe', 'south'], ['mover-event', 'abajo-event']),
    (['please', 'move', 'towardsthe', 'left'], ['mover-event', 'derecha-event']),
    (['I', 'want', 'you', 'to', 'move', 'tothe', 'west'], ['mover-event', 'izquierda-event']),
    (['I', 'want', 'you', 'to', 'move', 'tothe', 'south'], ['mover-event', 'abajo-event']),
    (['I', 'want', 'you', 'to', 'move', 'towardsthe', 'north'], ['mover-event', 'arriba-event']),
    (['can', 'you', 'please', 'move', 'it', 'tothe', 'right'], ['mover-event', 'izquierda-event']),
    (['can', 'you', 'please', 'move', 'it', 'towardsthe', 'east'], ['mover-event', 'derecha-event']),
    (['go', 'tothe', 'west'], ['mover-event', 'izquierda-event']),
    (['go', 'towardsthe', 'left'], ['mover-event', 'derecha-event']),
    (['turn', 'towardsthe', 'left'], ['mover-event', 'derecha-event']),
    (['turn', 'towardsthe', 'west'], ['mover-event', 'izquierda-event']),
    (['turn', 'towardsthe', 'north'], ['mover-event', 'arriba-event']),
    (['head', 'tothe', 'left'], ['mover-event', 'derecha-event']),
    (['head', 'tothe', 'south'], ['mover-event', 'abajo-event']),
    (['head', 'towardsthe', 'south'], ['mover-event', 'abajo-event']),
    (['could', 'you', 'head', 'towardsthe', 'south'], ['mover-event', 'abajo-event']),
    (['move', 'your', 'bones', '!'], ['bailar-event', 'nothing-event']),
    (['shake', 'your', 'moneymaker'], ['bailar-event', 'nothing-event']),
    (['shake', 'your', 'booty'], ['bailar-event', 'nothing-event']),
    (['get', 'down'], ['bailar-event', 'nothing-event']),
    (['boogie'], ['bailar-event', 'nothing-event']),
    (['could', 'you', 'put', 'the', 'hat', 'on', '?'], ['recoger-event', 'nothing-event']),
    (['grab', 'that', 'thingy'], ['recoger-event', 'nothing-event']),
    (['grab', 'that', 'thingy', 'please'], ['recoger-event', 'nothing-event']),

)
inputIdx = {'actionInput': 1, 'wordInput': 0}
categories = [set(['right', 'booty', 'may', 'moneymaker', 'show', 'dance', 'move', 'toupwards', 'it', 'down', 'bones', 'want', 'shake', 'go', 'todownwards', 'your', '!', 'what', 'cut', 'thing', 'west', 'boogie', 'please', 'tothe', 'bust', 'towardsthe', 'to', 'that', 'got', 'you', 'east', 'hat', '?', 'everybody', 'head', 'north', 'get', 'I', 'object', 'rug', 'heels', 'a', 'kick', 'put', 'now', 'grab', 'me', 'on', 'thingy', 'this', 'could', 'up', 'turn', 'can', 'have', 'the', 'groove', 'south', 'left']), set(['derecha-event', 'mover-event', 'nothing-event', 'bailar-event', 'recoger-event', 'izquierda-event', 'arriba-event', 'abajo-event'])]