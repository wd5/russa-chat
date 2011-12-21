import re

def to_smile(match):
    smiles = {
        ':big_smile:' : '<img src=\'/static/smiles/standart/big_smile.gif\'/>',
        ':fuck_yeah:' : '<img src=\'/static/smiles/standart/fuck_yeah.gif\'/>',
        ':fun_run:' : '<img src=\'/static/smiles/standart/fun_run.gif\'/>',
        ':clap:' : '<img src=\'/static/smiles/standart/clap.gif\'/>',
        ':angel:' : '<img src=\'/static/smiles/standart/angel.gif\'/>',
        ':blink:' : '<img src=\'/static/smiles/standart/blink.gif\'/>',
        ':bye:' : '<img src=\'/static/smiles/standart/bye.gif\'/>',
        ':cool:' : '<img src=\'/static/smiles/standart/cool.gif\'/>',
        ':drool:' : '<img src=\'/static/smiles/standart/drool.gif\'/>',
        ':dry:' : '<img src=\'/static/smiles/standart/dry.gif\'/>',
        ':lol:' : '<img src=\'/static/smiles/standart/lol.gif\'/>',
        ':mad:' : '<img src=\'/static/smiles/standart/mad.gif\'/>',
        ':ohmy:' : '<img src=\'/static/smiles/standart/ohmy.gif\'/>',
        ':popcorn:' : '<img src=\'/static/smiles/standart/popcorn.gif\'/>',
        ':rant:' : '<img src=\'/static/smiles/standart/rant.gif\'/>',
        ':rolleyes:' : '<img src=\'/static/smiles/standart/rolleyes.gif\'/>',
        ':sad:' : '<img src=\'/static/smiles/standart/sad.gif\'/>',
        ':shy:' : '<img src=\'/static/smiles/standart/shy.gif\'/>',
        ':smile:' : '<img src=\'/static/smiles/standart/smile.gif\'/>',
        ':tears:' : '<img src=\'/static/smiles/standart/tears.gif\'/>',
        ':tongue:' : '<img src=\'/static/smiles/standart/tongue.gif\'/>',
        ':unsure:' : '<img src=\'/static/smiles/standart/unsure.gif\'/>',
        ':what:' : '<img src=\'/static/smiles/standart/what.gif\'/>',
        ':wink:' : '<img src=\'/static/smiles/standart/wink.gif\'/>',
    }
    return smiles[match.group()]

smiles_code = ':angel:|:fuck_yeah:|:fun_run:|clap:|:blink:|:bye:|:cool:|:drool:|:dry:|:lol:|:mad:|:ohmy:|:popcorn:|:rant:|:rolleyes:|:sad:|:shy:|:smile:|:tears:|:tongue:|:unsure:|:what:|:wink:|:big_smile:'

def unescape(match):
    message = str(match.group())
    return message.replace("&lt;","<").replace("/&gt;",">")

def format_message(message):
    format_message = re.sub(smiles_code, to_smile, message)
    format_message = re.sub('&lt;img src=\'/static/.*&gt;',unescape, format_message)
    format_message = re.sub('http:\/\/(?P<name>[^\s]+)', '<a href="http://\g<name>" target="_blank">\g<name></a>', format_message)
    return format_message

