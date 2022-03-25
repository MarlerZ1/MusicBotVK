from os import close
import vk_api
import vk_api.bot_longpoll
import func
import time

# API-ключ созданный ранее
tk = ""

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=tk)
api = vk.get_api()
dic = {} # Создаем пустой словарь

# Работа с сообщениями
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk, group_id=206046127)
while True:
    try:
        # Основной цикл
        for event in longpoll.listen():

            # Если пришло новое сообщение
            if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            
                # Если оно имеет метку для меня( то есть бота)
                if event.from_user or event.from_chat:
                
                    # Сообщение от пользователя
                    request = event.message.text

                    # Каменная логика ответа

                    with open("ans.txt", encoding='utf-8') as file: #Читаем файл
                        lines = file.read().splitlines() # read().splitlines() - чтобы не было пустых строк
                    file.close()

                    for line in lines: # Проходимся по каждой строчке
                        key,value = line.split(':') # Разделяем каждую строку по двоеточии(в key будет - пицца, в value - 01)
                        dic.update({key:value})	 # Добавляем в словарь

                    print(dic) # Вывод словаря на консоль
                    
                    request = func.removing_id (request)         
                    try:
                        if request!='':
                            func.write_msg(event.message.peer_id, dic[request.lower()])
                            continue
                    except:
                        print(request)
                        if '?' == request[0] and ':' in request:
                            flag=0
                            for memb in api.groups.getMembers(group_id= 206046127, filter= 'managers')['items']:
                                print(memb['id'], ' имеет роль ', memb['role'])
                                if event.message.from_id == memb['id'] and (memb['role'] == 'administrator' or memb['role'] == 'creator'):
                                        flag=1
                                        print('test 1 - success')
                                        writable = request[1:]
                                        key,value = writable.split(':')
                                        key= key.lower()
                                        print(writable)
                                        if key not in dic:
                                            print('test 2 - success')
                                            with open("ans.txt",'a', encoding='utf-8') as file: 
                                                file.write(key+':'+value+ '\n')
                                                dic.update({key:value})	 # Добавляем в словарь
                                            file.close()
                                            func.write_msg( event.message.peer_id, 'Готово')
                                        else:
                                            func.write_msg( event.message.peer_id, 'Уже имеется: '+ str(key) + ' ' + str(dic[key.lower()]) +'. Заменить (Да/Нет)?')
                                            for event in longpoll.listen():
                                                
                                                if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
                                                    print('+++++++123qwe')
                                                    # Если оно имеет метку для меня( то есть бота)
                                                    if event.from_user or event.from_chat:
                                                        
                                                        with open("ans.txt",'r', encoding='utf-8') as file: 
                                                            # Сообщение от пользователя
                                                            request = event.message.text
                                                            print(request)
                                                            request= func.removing_id (request)
                                                            if request.lower()=='нет':
                                                                func.write_msg( event.message.peer_id, "Как хочешь -_-")
                                                                break
                                                            elif request.lower()=='да':

                                                                data=file.read()
                                                                print(dic[key.lower()])
                                                                data= data.replace(dic[key.lower()],value)
                                                                print('-----------')
                                                                print(data)

                                                                file.close()
                                                                with open("ans.txt",'w', encoding='utf-8') as file: 
                                                                    file.write(data)
                                                                    func.write_msg(event.message.peer_id, "Готово")
                                                                    del dic[key]
                                                                    dic.update({key:value})
                                                            elif request.lower()=='удалить':
                                                                lines=file.readlines()
                                                                print(dic[key.lower()])

                                                                print('-----------')

                                                                print(lines)
                                                                file.close()
                                                                with open("ans.txt",'w', encoding='utf-8') as file: 
                                                                    for line in lines:
                                                                        if line !=(key.lower()+':'+dic[key.lower()]+'\n'):
                                                                            file.write(line)    
                                                                            print('success')
                                                                    func.write_msg( event.message.peer_id, "Готово")
                                                                    del dic[key]                                                   
                                                    break
                            if flag != 1 :
                                func.write_msg(event.message.peer_id, "Не поняла вашего ответа...")
                            continue

                        elif not event.message.attachments:
                            func.write_msg(event.message.peer_id, "Не поняла вашего ответа...")
                            continue
                        else:
                            func.audio_func(event,event.message.attachments)
                            continue
                    func.audio_func(event,event.message.attachments)
    except:
        time.sleep(1)
        print('____TIMEOUT_____ +_=')