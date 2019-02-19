from datetime import datetime, timedelta
from notifications.constants import TZ_DEFAULT
import requests
import random
import html

o_msg = ['Beaubourg est ouvert ! :door:',
         'Woooah... grosse gueule de bois là... Qui vient me reveiller ? :dizzy_face::dizzy_face::dizzy_face:',
         'Bonne nuit les suricats :night_with_stars: euh oula attends je me suis gourré.. ',
         'Oh un suricats ! Coucou toi :relaxed:',
         '{"error": "I forgot what I have to say..."}',
         "Bin ch'est y a quequ'un qui a ouvert la cahute ! :door:"]
c_msg = ['Bonne nuit les suricats :night_with_stars:',
         "Super journée aujourd'hui ! ça part en after chez moi ?",
         'Beaubourg est ouvert ! ou fermé... je sais plus...',
         "Ne m'abandonnez pas :cry::cry:",
         ':alert:',
         "Bonne nuite mes loutes ! :night_with_stars:"]


def get_random_message():
    idx = random.randint(1, 4)
    print(idx)
    try:
        # Normal
        if idx == 1:
            idx = random.randint(1, 1000)
            return o_msg[idx % len(o_msg)], c_msg[idx % len(c_msg)]
        # Chuck Norris Fact
        elif idx == 2:
            r = requests.get('https://www.chucknorrisfacts.fr/api/get?data=tri:alea;nb:1')
            r = r.json()
            msg = ':chuck: : ' + html.unescape(r[0]['fact'])

        # Cats facts
        elif idx == 3:
            r = requests.get('https://cat-fact.herokuapp.com/facts')
            r = r.json()
            facts = r['all']
            msg = ':cat: : ' + facts[random.randrange(0, len(facts))]['text']
        # Quote
        else:
            r = requests.get('https://quotes.rest/qod')
            r = r.json()
            msg = ':speaking_head_in_silhouette: : ' + r['contents']['quotes'][0]['quote']
        return msg, msg
    except Exception as e:
        # return type(e).__name__, str(e)
        return o_msg[0], c_msg[0]
