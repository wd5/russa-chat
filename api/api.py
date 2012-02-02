import re

def to_smile(match):
    smiles = {
        ':facepalm:' : '<img src=\'/static/smiles/standart/facepalm.gif\'/>',
        ':avtor:' : '<img src=\'/static/smiles/standart/avtor.png\'/>',
        ':loveshower:' : '<img src=\'/static/smiles/standart/loveshower.gif\'/>',
        ':guitar:' : '<img src=\'/static/smiles/standart/guitar.gif\'/>',
        ':rock:' : '<img src=\'/static/smiles/standart/rock.gif\'/>',
        ':cheerleader:' : '<img src=\'/static/smiles/standart/cheerleader.gif\'/>',
        ':dancing_chilli:' : '<img src=\'/static/smiles/standart/dancing_chilli.gif\'/>',
        ':crazygirl:' : '<img src=\'/static/smiles/standart/crazygirl.gif\'/>',
        ':nun:' : '<img src=\'/static/smiles/standart/nun.gif\'/>',
        ':guns:' : '<img src=\'/static/smiles/standart/guns.gif\'/>',
        ':kruger:' : '<img src=\'/static/smiles/standart/kruger.gif\'/>',
        ':mol:' : '<img src=\'/static/smiles/standart/mol.gif\'/>',
        ':rev:' : '<img src=\'/static/smiles/standart/rev.gif\'/>',
        ':big_smile:' : '<img src=\'/static/smiles/standart/big_smile.gif\'/>',
        ':celebrity:' : '<img src=\'/static/smiles/standart/celebrity.gif\'/>',
        ':clap:' : '<img src=\'/static/smiles/standart/clap.gif\'/>',
        ':crazy:' : '<img src=\'/static/smiles/standart/crazy.gif\'/>',
        ':crazynuts:' : '<img src=\'/static/smiles/standart/crazynuts.gif\'/>',
        ':crazyny:' : '<img src=\'/static/smiles/standart/crazyny.gif\'/>',
        ':csotona:' : '<img src=\'/static/smiles/standart/csotona.gif\'/>',
        ':flyhigh:' : '<img src=\'/static/smiles/standart/flyhigh.gif\'/>',
        ':fuck_yeah:' : '<img src=\'/static/smiles/standart/fuck_yeah.gif\'/>',
        ':fuck_you:' : '<img src=\'/static/smiles/standart/fuck_you.gif\'/>',
        ':fun_run:' : '<img src=\'/static/smiles/standart/fun_run.gif\'/>',
        ':kult:' : '<img src=\'/static/smiles/standart/kult.gif\'/>',
        ':laugh:' : '<img src=\'/static/smiles/standart/laugh.gif\'/>',
        ':metal:' : '<img src=\'/static/smiles/standart/metal.gif\'/>',
        ':shuffle:' : '<img src=\'/static/smiles/standart/shuffle.gif\'/>',
        ':tarantino_dance:' : '<img src=\'/static/smiles/standart/tarantino_dance.gif\'/>',
        ':ura:' : '<img src=\'/static/smiles/standart/ura.gif\'/>',
        ':wall:' : '<img src=\'/static/smiles/standart/wall.gif\'/>',
        ':bpr:' : '<img src=\'/static/smiles/sex/bpr.gif\'/>',
        ':bps:' : '<img src=\'/static/smiles/sex/bps.gif\'/>',
        ':bpt:' : '<img src=\'/static/smiles/sex/bpt.gif\'/>',
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
        ':dubina:' : '<img src=\'/static/smiles/big/dubina.gif\'/>',
        ':peace:' : '<img src=\'/static/smiles/big/peace.gif\'/>',
        ':girl:' : '<img src=\'/static/smiles/big/girl.gif\'/>',
        ':chips:' : '<img src=\'/static/smiles/big/chips.gif\'/>',
        ':wc:' : '<img src=\'/static/smiles/big/wc.gif\'/>',
        ':ass:' : '<img src=\'/static/smiles/big/ass.gif\'/>',
        ':sacar:' : '<img src=\'/static/smiles/big/sacar.gif\'/>',
        ':kick:' : '<img src=\'/static/smiles/big/kick.gif\'/>',
        ':music_girl:' : '<img src=\'/static/smiles/big/music_girl.gif\'/>',
        ':up:' : '<img src=\'/static/smiles/big/up.gif\'/>',
        ':rolls:' : '<img src=\'/static/smiles/big/rolls.gif\'/>',
        ':car:' : '<img src=\'/static/smiles/big/car.gif\'/>',
        ':snowmobile:' : '<img src=\'/static/smiles/big/snowmobile.gif\'/>',
        ':trollface:' : '<img src=\'/static/smiles/special/Trollface.png\'/>',
        ':ufff:' : '<img src=\'/static/smiles/special/ufff.gif\'/>',
        ':brutal:' : '<img src=\'/static/smiles/big/brutal.gif\'/>',
        ':rose:' : '<img src=\'/static/smiles/big/rose.gif\'/>',
    }
    return smiles[match.group()]

smiles_code = ':avtor:|:loveshower:|:ufff:|:facepalm:|:brutal:|:rose:|:guitar:|:ass:|:trollface:|:snowmobile:|:up:|:car:|:rolls:|:wc:|:kick:|:music_girl:|:sacar:|:rock:|:chips:|:dubina:|:girl:|:peace:|:dancing_chilli:|:cheerleader:|:guns:|:kruger:|:mol:|:nun:|:rev:|:crazygirl:|:big_smile:|:celebrity:|:clap:|:crazy:|:crazynuts:|:crazyny:|:csotona:|:flyhigh:|:fuck_yeah:|:fuck_you:|:fun_run:|:kult:|:laugh:|:metal:|:shuffle:|:tarantino_dance:|:ura:|:wall:|:bpr:|:bps:|:bpt:|:wxa:|:wxb:|:wxc:|:wxd:|:wxf:|:wxg:|:wxh:|:wxi:|:wxj:|:wxk:'

def unescape(match):
    message = str(match.group())
    return message.replace("&lt;","<").replace("/&gt;",">")

def format_message(message):
    format_message = re.sub(smiles_code, to_smile, message)
    format_message = re.sub('&lt;img src=\'/static/.*&gt;',unescape, format_message)
    format_message = re.sub('https?:\/\/(?P<name>[^\s]+)', '<a href="http://\g<name>" target="_blank">\g<name></a>', format_message)
    return format_message

