import vk_api
import vk_api.bot_longpoll
tk = "3230fc14d6a45fbdcf1fe1cc947f4680e1a3cf7713fe66c054be5f5ece32028d0d194ea253400fcfa67c8"
vk = vk_api.VkApi(token=tk)
api = vk.get_api()
au_genre={
    '1':'Rock',
    '2':'Pop',
    '3':'Rap & Hip-Hop',
    '4':'Easy Listening',
    '5':'House & Dance',
    '6':'Instrumental',
    '7':'Metal',
    '21':'Alternative',
    '8':'Dubstep',
    '1001':'Jazz & Blues',
    '10':'Drum & Bass',
    '11':'Trance',
    '12':'Chanson',
    '13':'Ethnic',
    '14':'Acoustic & Vocal',
    '15':'Reggae',
    '16':'Classical',
    '17':'Indie Pop',
    '19':'Speech',
    '22':'Electropop & Disco',
    '18':'Other'
}

def write_msg(id, msg):
    api.messages.send(peer_id = id, message = msg, random_id = 0)

def removing_id (request):
    if '@public212144576' in request:
        if ', ' in request:
           request= request[34:]
        else:
           request = request[33:]
    elif 'musicbot' in request.lower():
        if ', ' in request:
            request= request[26:]
        else:
            request = request[25:]  
    return request
    
def audio_func(event,attachments):
    score=0
    for p in attachments:
        if p['type'] == 'audio':
            score+=1
            s_link=api.utils.getShortLink(url=p['audio']['url'],private=0)['short_url']
            try:
                write_msg( event.message.peer_id,'Автор - '+p['audio']['artist'] +'\n'+ 'Название - '+ p['audio']['title']+ '\nЖанр - '+au_genre[str(p['audio']['genre_id'])]+'\nСсылка - '+ s_link)
            except:
                write_msg( event.message.peer_id,'Автор - '+p['audio']['artist'] +'\n'+ 'Название - '+ p['audio']['title']+ '\nСсылка - '+ s_link)
    if score==0:                  
        write_msg( event.message.peer_id, "Не поняла вашего ответа...")   
