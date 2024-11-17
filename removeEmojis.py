"""
Module Name: removeEmojis
Description: This script removes emojis from a given ASS subtitle file.
"""

import re
import sys
import os

regex = r"(?:[0-9#*]️⃣|[☝✊-✍🎅🏂🏇👂👃👆-👐👦👧👫-👭👲👴-👶👸👼💃💅💏💑💪🕴🕺🖐🖕🖖🙌🙏🛀🛌🤌🤏🤘-🤟🤰-🤴🤶🥷🦵🦶🦻🧒🧓🧕🫃-🫅🫰🫲-🫸][🏻-🏿]?|⛓(?:️‍💥)?|[⛹🏋🏌🕵](?:️‍[♀♂]️|[🏻-🏿](?:‍[♀♂]️)?)?|❤(?:️‍[🔥🩹])?|🇦[🇨-🇬🇮🇱🇲🇴🇶-🇺🇼🇽🇿]|🇧[🇦🇧🇩-🇯🇱-🇴🇶-🇹🇻🇼🇾🇿]|🇨[🇦🇨🇩🇫-🇮🇰-🇵🇷🇺-🇿]|🇩[🇪🇬🇯🇰🇲🇴🇿]|🇪[🇦🇨🇪🇬🇭🇷-🇺]|🇫[🇮-🇰🇲🇴🇷]|🇬[🇦🇧🇩-🇮🇱-🇳🇵-🇺🇼🇾]|🇭[🇰🇲🇳🇷🇹🇺]|🇮[🇨-🇪🇱-🇴🇶-🇹]|🇯[🇪🇲🇴🇵]|🇰[🇪🇬-🇮🇲🇳🇵🇷🇼🇾🇿]|🇱[🇦-🇨🇮🇰🇷-🇻🇾]|🇲[🇦🇨-🇭🇰-🇿]|🇳[🇦🇨🇪-🇬🇮🇱🇴🇵🇷🇺🇿]|🇴🇲|🇵[🇦🇪-🇭🇰-🇳🇷-🇹🇼🇾]|🇶🇦|🇷[🇪🇴🇸🇺🇼]|🇸[🇦-🇪🇬-🇴🇷-🇹🇻🇽-🇿]|🇹[🇦🇨🇩🇫-🇭🇯-🇴🇷🇹🇻🇼🇿]|🇺[🇦🇬🇲🇳🇸🇾🇿]|🇻[🇦🇨🇪🇬🇮🇳🇺]|🇼[🇫🇸]|🇽🇰|🇾[🇪🇹]|🇿[🇦🇲🇼]|🍄(?:‍🟫)?|🍋(?:‍🟩)?|[🏃🚶🧎](?:‍(?:[♀♂]️(?:‍➡️)?|➡️)|[🏻-🏿](?:‍(?:[♀♂]️(?:‍➡️)?|➡️))?)?|[🏄🏊👮👰👱👳👷💁💂💆💇🙅-🙇🙋🙍🙎🚣🚴🚵🤦🤵🤷-🤹🤽🤾🦸🦹🧍🧏🧔🧖-🧝](?:‍[♀♂]️|[🏻-🏿](?:‍[♀♂]️)?)?|🏳(?:️‍(?:⚧️|🌈))?|🏴(?:‍☠️|󠁧(?:󠁢(?:󠁥󠁮󠁧|󠁳󠁣󠁴)󠁿)?)?|🐈(?:‍⬛)?|🐕(?:‍🦺)?|🐦(?:‍[⬛🔥])?|🐻(?:‍❄️)?|👁(?:️‍🗨️)?|👨(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?👨|👦(?:‍👦)?|👧(?:‍[👦👧])?|[👨👩]‍(?:👦(?:‍👦)?|👧(?:‍[👦👧])?)|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳])|🏻(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?👨[🏻-🏿]|🤝‍👨[🏼-🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏼(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?👨[🏻-🏿]|🤝‍👨[🏻🏽-🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏽(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?👨[🏻-🏿]|🤝‍👨[🏻🏼🏾🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏾(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?👨[🏻-🏿]|🤝‍👨[🏻-🏽🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏿(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?👨[🏻-🏿]|🤝‍👨[🏻-🏾]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?)?|👩(?:‍(?:[⚕⚖✈]️|❤️‍(?:[👨👩]|💋‍[👨👩])|👦(?:‍👦)?|👧(?:‍[👦👧])?|👩‍(?:👦(?:‍👦)?|👧(?:‍[👦👧])?)|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳])|🏻(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?[👨👩][🏻-🏿]|🤝‍[👨👩][🏼-🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏼(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?[👨👩][🏻-🏿]|🤝‍[👨👩][🏻🏽-🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏽(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?[👨👩][🏻-🏿]|🤝‍[👨👩][🏻🏼🏾🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏾(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?[👨👩][🏻-🏿]|🤝‍[👨👩][🏻-🏽🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏿(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?[👨👩][🏻-🏿]|🤝‍[👨👩][🏻-🏾]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?)?|[👯🤼🧞🧟](?:‍[♀♂]️)?|😮(?:‍💨)?|😵(?:‍💫)?|😶(?:‍🌫️)?|🙂(?:‍[↔↕]️)?|🧑(?:‍(?:[⚕⚖✈]️|🤝‍🧑|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎄🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]|(?:🧑‍)?🧒(?:‍🧒)?)|🏻(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?🧑[🏼-🏿]|🤝‍🧑[🏻-🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎄🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏼(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?🧑[🏻🏽-🏿]|🤝‍🧑[🏻-🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎄🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏽(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?🧑[🏻🏼🏾🏿]|🤝‍🧑[🏻-🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎄🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏾(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?🧑[🏻-🏽🏿]|🤝‍🧑[🏻-🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎄🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?|🏿(?:‍(?:[⚕⚖✈]️|❤️‍(?:💋‍)?🧑[🏻-🏾]|🤝‍🧑[🏻-🏿]|[🦯🦼🦽](?:‍➡️)?|[🌾🍳🍼🎄🎓🎤🎨🏫🏭💻💼🔧🔬🚀🚒🦰-🦳]))?)?|[©®‼⁉™ℹ↔-↙↩↪⌚⌛⌨⏏⏩-⏳⏸-⏺Ⓜ▪▫▶◀◻-◾☀-☄☎☑☔☕☘☠☢☣☦☪☮☯☸-☺♀♂♈-♓♟♠♣♥♦♨♻♾♿⚒-⚗⚙⚛⚜⚠⚡⚧⚪⚫⚰⚱⚽⚾⛄⛅⛈⛎⛏⛑⛔⛩⛪⛰-⛵⛷⛸⛺⛽✂✅✈✉✏✒✔✖✝✡✨✳✴❄❇❌❎❓-❕❗❣➕-➗➡➰➿⤴⤵⬅-⬇⬛⬜⭐⭕〰〽㊗㊙🀄🃏🅰🅱🅾🅿🆎🆑-🆚🈁🈂🈚🈯🈲-🈺🉐🉑🌀-🌡🌤-🍃🍅-🍊🍌-🎄🎆-🎓🎖🎗🎙-🎛🎞-🏁🏅🏆🏈🏉🏍-🏰🏵🏷-🐇🐉-🐔🐖-🐥🐧-🐺🐼-👀👄👅👑-👥👪👹-👻👽-💀💄💈-💎💐💒-💩💫-📽📿-🔽🕉-🕎🕐-🕧🕯🕰🕳🕶-🕹🖇🖊-🖍🖤🖥🖨🖱🖲🖼🗂-🗄🗑-🗓🗜-🗞🗡🗣🗨🗯🗳🗺-😭😯-😴😷-🙁🙃🙄🙈-🙊🚀-🚢🚤-🚳🚷-🚿🛁-🛅🛋🛍-🛒🛕-🛗🛜-🛥🛩🛫🛬🛰🛳-🛼🟠-🟫🟰🤍🤎🤐-🤗🤠-🤥🤧-🤯🤺🤿-🥅🥇-🥶🥸-🦴🦷🦺🦼-🧌🧐🧠-🧿🩰-🩼🪀-🪈🪐-🪽🪿-🫂🫎-🫛🫠-🫨]|🫱(?:🏻(?:‍🫲[🏼-🏿])?|🏼(?:‍🫲[🏻🏽-🏿])?|🏽(?:‍🫲[🏻🏼🏾🏿])?|🏾(?:‍🫲[🏻-🏽🏿])?|🏿(?:‍🫲[🏻-🏾])?)?)+"

try:
    danmakuFile = os.getenv('ASS_PATH')
    print(f"Processing danmaku file at: {danmakuFile}")

    with open(danmakuFile, 'r', encoding='utf-8') as file:
        originalFile = file.read()

    result = re.sub(regex, "", originalFile, 0, re.MULTILINE)
    if result:
        with open(danmakuFile, 'w', encoding='utf-8') as output_file:
            output_file.write(result)
except FileNotFoundError:
    print("file not exists.")
except UnicodeDecodeError:
    print("The file encoding may be inconsistent with the specified UTF-8 encoding.")
