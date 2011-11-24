import re

def to_smile(match):
    smiles = {
        ':aggressive:' : '<img src=\'/static/smiles/standart/aggressive.gif\'/>',
        ':agree:' : '<img src=\'/static/smiles/standart/agree.gif\'/>',
        ':air_kiss:' : '<img src=\'/static/smiles/standart/air_kiss.gif\'/>',
        ':bad:' : '<img src=\'/static/smiles/standart/bad.gif\'/>',
        ':beee:' : '<img src=\'/static/smiles/standart/beee.gif\'/>',
        ':black_eye:' : '<img src=\'/static/smiles/standart/black_eye.gif\'/>',
        ':blum2:' : '<img src=\'/static/smiles/standart/blum2.gif\'/>',
        ':blum3:' : '<img src=\'/static/smiles/standart/blum3.gif\'/>',
        ':blush:' : '<img src=\'/static/smiles/standart/blush.gif\'/>',
        ':blush2:' : '<img src=\'/static/smiles/standart/blush2.gif\'/>',
        ':boast:' : '<img src=\'/static/smiles/standart/boast.gif\'/>',
        ':boredom:' : '<img src=\'/static/smiles/standart/boredom.gif\'/>',
        ':censored:' : '<img src=\'/static/smiles/standart/censored.gif\'/>',
        ':clapping:' : '<img src=\'/static/smiles/standart/clapping.gif\'/>',
        ':cray:' : '<img src=\'/static/smiles/standart/cray.gif\'/>',
        ':cray2:' : '<img src=\'/static/smiles/standart/cray2.gif\'/>',
        ':dance:' : '<img src=\'/static/smiles/standart/dance.gif\'/>',
        ':dance2:' : '<img src=\'/static/smiles/standart/dance2.gif\'/>',
        ':dance3:' : '<img src=\'/static/smiles/standart/dance3.gif\'/>',
        ':dance4:' : '<img src=\'/static/smiles/standart/dance4.gif\'/>',
        ':declare:' : '<img src=\'/static/smiles/standart/declare.gif\'/>',
        ':derisive:' : '<img src=\'/static/smiles/standart/derisive.gif\'/>',
        ':dirol:' : '<img src=\'/static/smiles/standart/dirol.gif\'/>',
        ':dntknw:' : '<img src=\'/static/smiles/standart/dntknw.gif\'/>',
        ':don-t_mention:' : '<img src=\'/static/smiles/standart/don-t_mention.gif\'/>',
        ':download:' : '<img src=\'/static/smiles/standart/download.gif\'/>',
        ':drinks:' : '<img src=\'/static/smiles/standart/drinks.gif\'/>',
        ':fool:' : '<img src=\'/static/smiles/standart/fool.gif\'/>',
        ':friends:' : '<img src=\'/static/smiles/standart/friends.gif\'/>',
        ':good:' : '<img src=\'/static/smiles/standart/good.gif\'/>',
        ':good2:' : '<img src=\'/static/smiles/standart/good2.gif\'/>',
        ':good3:' : '<img src=\'/static/smiles/standart/good3.gif\'/>',
        ':grin:' : '<img src=\'/static/smiles/standart/grin.gif\'/>',
        ':heat:' : '<img src=\'/static/smiles/standart/heat.gif\'/>',
        ':help:' : '<img src=\'/static/smiles/standart/help.gif\'/>',
        ':i-m_so_happy:' : '<img src=\'/static/smiles/standart/i-m_so_happy.gif\'/>',
        ':ireful1:' : '<img src=\'/static/smiles/standart/ireful1.gif\'/>',
        ':ireful2:' : '<img src=\'/static/smiles/standart/ireful2.gif\'/>',
        ':ireful3:' : '<img src=\'/static/smiles/standart/ireful3.gif\'/>',
        ':kiss:' : '<img src=\'/static/smiles/standart/kiss.gif\'/>',
        ':laugh1:' : '<img src=\'/static/smiles/standart/laugh1.gif\'/>',
        ':laugh2:' : '<img src=\'/static/smiles/standart/laugh2.gif\'/>',
        ':laugh3:' : '<img src=\'/static/smiles/standart/laugh3.gif\'/>',
        ':lazy:' : '<img src=\'/static/smiles/standart/lazy.gif\'/>',
        ':lazy2:' : '<img src=\'/static/smiles/standart/lazy2.gif\'/>',
        ':lazy3:' : '<img src=\'/static/smiles/standart/lazy3.gif\'/>',
        ':mda:' : '<img src=\'/static/smiles/standart/mda.gif\'/>',
        ':meeting:' : '<img src=\'/static/smiles/standart/meeting.gif\'/>',
        ':mosking:' : '<img src=\'/static/smiles/standart/mosking.gif\'/>',
        ':nea:' : '<img src=\'/static/smiles/standart/nea.gif\'/>',
        ':negative:' : '<img src=\'/static/smiles/standart/negative.gif\'/>',
        ':no2:' : '<img src=\'/static/smiles/standart/no2.gif\'/>',
        ':not_i:' : '<img src=\'/static/smiles/standart/not_i.gif\'/>',
        ':offtopic:' : '<img src=\'/static/smiles/standart/offtopic.gif\'/>',
        ':ok:' : '<img src=\'/static/smiles/standart/ok.gif\'/>',
        ':pardon:' : '<img src=\'/static/smiles/standart/pardon.gif\'/>',
        ':party:' : '<img src=\'/static/smiles/standart/party.gif\'/>',
        ':pleasantry:' : '<img src=\'/static/smiles/standart/pleasantry.gif\'/>',
        ':polling:' : '<img src=\'/static/smiles/standart/polling.gif\'/>',
        ':popcorm1:' : '<img src=\'/static/smiles/standart/popcorm1.gif\'/>',
        ':popcorm2:' : '<img src=\'/static/smiles/standart/popcorm2.gif\'/>',
        ':punish:' : '<img src=\'/static/smiles/standart/punish.gif\'/>',
        ':punish2:' : '<img src=\'/static/smiles/standart/punish2.gif\'/>',
        ':read:' : '<img src=\'/static/smiles/standart/read.gif\'/>',
        ':resent:' : '<img src=\'/static/smiles/standart/resent.gif\'/>',
        ':rofl:' : '<img src=\'/static/smiles/standart/rofl.gif\'/>',
        ':sad:' : '<img src=\'/static/smiles/standart/sad.gif\'/>',
        ':scare:' : '<img src=\'/static/smiles/standart/scare.gif\'/>',
        ':scare2:' : '<img src=\'/static/smiles/standart/scare2.gif\'/>',
        ':sclerosis:' : '<img src=\'/static/smiles/standart/sclerosis.gif\'/>',
        ':scratch_one-s_head:' : '<img src=\'/static/smiles/standart/scratch_one-s_head.gif\'/>',
        ':search:' : '<img src=\'/static/smiles/standart/search.gif\'/>',
        ':secret:' : '<img src=\'/static/smiles/standart/secret.gif\'/>',
        ':SHABLON_padonak_04:' : '<img src=\'/static/smiles/standart/SHABLON_padonak_04.gif\'/>',
        ':SHABLON_padonak_05:' : '<img src=\'/static/smiles/standart/SHABLON_padonak_05.gif\'/>',
        ':SHABLON_padonak_06:' : '<img src=\'/static/smiles/standart/SHABLON_padonak_06.gif\'/>',
        ':shout:' : '<img src=\'/static/smiles/standart/shout.gif\'/>',
        ':smile3:' : '<img src=\'/static/smiles/standart/smile3.gif\'/>',
        ':smoke:' : '<img src=\'/static/smiles/standart/smoke.gif\'/>',
        ':snooks:' : '<img src=\'/static/smiles/standart/snooks.gif\'/>',
        ':sorry:' : '<img src=\'/static/smiles/standart/sorry.gif\'/>',
        ':sorry2:' : '<img src=\'/static/smiles/standart/sorry2.gif\'/>',
        ':stink:' : '<img src=\'/static/smiles/standart/stink.gif\'/>',
        ':stop:' : '<img src=\'/static/smiles/standart/stop.gif\'/>',
        ':superstition:' : '<img src=\'/static/smiles/standart/superstition.gif\'/>',
        ':swoon:' : '<img src=\'/static/smiles/standart/swoon.gif\'/>',
        ':swoon2:' : '<img src=\'/static/smiles/standart/swoon2.gif\'/>',
        ':take_example:' : '<img src=\'/static/smiles/standart/take_example.gif\'/>',
        ':taunt:' : '<img src=\'/static/smiles/standart/taunt.gif\'/>',
        ':thank_you:' : '<img src=\'/static/smiles/standart/thank_you.gif\'/>',
        ':thank_you2:' : '<img src=\'/static/smiles/standart/thank_you2.gif\'/>',
        ':this:' : '<img src=\'/static/smiles/standart/this.gif\'/>',
        ':threaten:' : '<img src=\'/static/smiles/standart/threaten.gif\'/>',
        ':to_clue:' : '<img src=\'/static/smiles/standart/to_clue.gif\'/>',
        ':to_take_umbrage:' : '<img src=\'/static/smiles/standart/to_take_umbrage.gif\'/>',
        ':tongue:' : '<img src=\'/static/smiles/standart/tongue.gif\'/>',
        ':umnik:' : '<img src=\'/static/smiles/standart/umnik.gif\'/>',
        ':umnik2:' : '<img src=\'/static/smiles/standart/umnik2.gif\'/>',
        ':unsure:' : '<img src=\'/static/smiles/standart/unsure.gif\'/>',
        ':victory:' : '<img src=\'/static/smiles/standart/victory.gif\'/>',
        ':whistle:' : '<img src=\'/static/smiles/standart/whistle.gif\'/>',
        ':whistle2:' : '<img src=\'/static/smiles/standart/whistle2.gif\'/>',
        ':whistle3:' : '<img src=\'/static/smiles/standart/whistle3.gif\'/>',
        ':wink3:' : '<img src=\'/static/smiles/standart/wink3.gif\'/>',
        ':yahoo:' : '<img src=\'/static/smiles/standart/yahoo.gif\'/>',
        ':yes:' : '<img src=\'/static/smiles/standart/yes.gif\'/>',
        ':yes2:' : '<img src=\'/static/smiles/standart/yes2.gif\'/>',
        ':yes3:' : '<img src=\'/static/smiles/standart/yes3.gif\'/>',
        ':yes4:' : '<img src=\'/static/smiles/standart/yes4.gif\'/>',
        ':yu:' : '<img src=\'/static/smiles/standart/yu.gif\'/>',
    }
    return smiles[match.group()]

smiles_code = ':acute:|:aggressive:|:agree:|:air_kiss:|:bad:|:beee:|:black_eye:|:blum2:|:blum3:|:blush:|:blush2:|:boast:|:boredom:|:censored:|:clapping:|:cray:|:cray2:|:dance:|:dance2:|:dance3:|:dance4:|:declare:|:derisive:|:dirol:|:dntknw:|:don-t_mention:|:download:|:drinks:|:fool:|:friends:|:good:|:good2:|:good3:|:grin:|:heat:|:help:|:i-m_so_happy:|:ireful1:|:ireful2:|:ireful3:|:kiss:|:laugh1:|:laugh2:|:laugh3:|:lazy:|:lazy2:|:lazy3:|:mda:|:meeting:|:mosking:|:nea:|:negative:|:no2:|:not_i:|:offtopic:|:ok:|:pardon:|:party:|:pleasantry:|:polling:|:popcorm1:|:popcorm2:|:punish:|:punish2:|:read:|:resent:|:rofl:|:sad:|:scare:|:scare2:|:sclerosis:|:scratch_one-s_head:|:search:|:secret:|:SHABLON_padonak_04:|:SHABLON_padonak_05:|:SHABLON_padonak_06:|:shout:|:smile3:|:smoke:|:snooks:|:sorry:|:sorry2:|:stink:|:stop:|:superstition:|:swoon:|:swoon2:|:take_example:|:taunt:|:thank_you:|:thank_you2:|:this:|:threaten:|:to_clue:|:to_take_umbrage:|:tongue:|:umnik:|:umnik2:|:unsure:|:victory:|:whistle:|:whistle2:|:whistle3:|:wink3:|:yahoo:|:yes:|:yes2:|:yes3:|:yes4:|:yu:'

def unescape(match):
    message = str(match.group())
    return message.replace("&lt;","<").replace("/&gt;",">")

def format_message(message):
    format_message = re.sub(smiles_code, to_smile, message)
    return re.sub('&lt;img src=\'/static/.*&gt;',unescape, format_message)

