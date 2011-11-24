import re

def to_smile(match):
    smiles = {
        ':acute:' : '<img src=\'/static/smiles/standart/acute.gif\'/>',
        ':aggressive:' : '<img src=\'/static/smiles/standart/aggressive.gif\'/>',
    }
    return smiles[match.group()]

smiles_code = ':acute:|:aggressive:'

def unescape(match):
    message = str(match.group())
    return message.replace("&lt;","<").replace("/&gt;",">")

def format_message(message):
    format_message = re.sub(':acute:|:aggressive:',to_smile, message)
    return re.sub('&lt;img src=\'/static/.*&gt;',unescape, format_message)

