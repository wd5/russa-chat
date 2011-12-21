import re

def to_smile(match):
    smiles = {
        ':big_smile:' : '<img src=\'/static/smiles/standart/big_smile.gif\'/>',
        ':crazyny:' : '<img src=\'/static/smiles/standart/crazyny.gif\'/>',
        ':crazynuts:' : '<img src=\'/static/smiles/standart/crazynuts.gif\'/>',
        ':csotona:' : '<img src=\'/static/smiles/standart/csotona.gif\'/>',
        ':crazy:' : '<img src=\'/static/smiles/standart/crazy.gif\'/>',
        ':avtor:' : '<img src=\'/static/smiles/standart/avtor.png\'/>',
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
        ':bpr:' : '<img src=\'/static/smiles/sex/bpr.gif\'/>',
        ':bps:' : '<img src=\'/static/smiles/sex/bps.gif\'/>',
        ':bpt:' : '<img src=\'/static/smiles/sex/bpt.gif\'/>',
        ':bpu:' : '<img src=\'/static/smiles/sex/bpu.gif\'/>',
        ':wxa:' : '<img src=\'/static/smiles/sex/wxa.gif\'/>',
        ':wxb:' : '<img src=\'/static/smiles/sex/wxb.gif\'/>',
        ':wxc:' : '<img src=\'/static/smiles/sex/wxc.gif\'/>',
        ':wxd:' : '<img src=\'/static/smiles/sex/wxd.gif\'/>',
        ':wxf:' : '<img src=\'/static/smiles/sex/wxf.gif\'/>',
        ':wxg:' : '<img src=\'/static/smiles/sex/wxg.gif\'/>',
        ':wxh:' : '<img src=\'/static/smiles/sex/wxh.gif\'/>',
        ':wxi:' : '<img src=\'/static/smiles/sex/wxi.gif\'/>',
        ':wxj:' : '<img src=\'/static/smiles/sex/wxj.gif\'/>',
        ':wxk:' : '<img src=\'/static/smiles/sex/wxk.gif\'/>',
    }
    return smiles[match.group()]

smiles_code = ':angel:|:crazy:|:csotona:|:crazynuts:|:crazyny:|:avtor:|:fuck_yeah:|:fun_run:|clap:|:blink:|:bye:|:cool:|:drool:|:dry:|:lol:|:mad:|:ohmy:|:popcorn:|:rant:|:rolleyes:|:sad:|:shy:|:smile:|:tears:|:tongue:|:unsure:|:what:|:wink:|:big_smile:|:bpr:|:bps:|:bpt:|:wxa:|:wxb:|:wxc:|:wxd:|:wxf:|:wxg:|:wxh:|:wxi:|:wxj:|:wxk:'

def unescape(match):
    message = str(match.group())
    return message.replace("&lt;","<").replace("/&gt;",">")

def format_message(message):
    format_message = re.sub(smiles_code, to_smile, message)
    format_message = re.sub('&lt;img src=\'/static/.*&gt;',unescape, format_message)
    format_message = re.sub('http:\/\/(?P<name>[^\s]+)', '<a href="http://\g<name>" target="_blank">\g<name></a>', format_message)
    return format_message

