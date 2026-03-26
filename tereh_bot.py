import telebot
import pg8000.native
import matplotlib.pyplot as plt
import matplotlib
import os
import time
from datetime import datetime,timedelta
import threading

matplotlib.use('Agg')

bot = telebot.TeleBot("8747592387:AAFf_wrtuXWMNbzELurYq10Xpn605HPAgq4")
Sanya_id = "1072652989"
admins=["8542564114", Sanya_id]
con = pg8000.native.Connection(user="postgres", database="testdb", password="admin")
data=[
    {"rq": "1.Как вы считаете, имеет ли влияние соц. сфера на организм беременной женщины? (Один)",
     "rp0": "1.да, имеет",
     "rp1": "1.частично",
     "rp2": "1.нет, не имеет"},
    {"rq": "2. Как вы считаете какие факторы влияют на беременную женщину?(несколько)",
     "rp0": "Экономические факторы",
     "rp1": "семейные отношения",
     "rp2": "работа",
     "rp3": "психологические факторы",
     "rp4": "Материальные условия",
     "rp5": "2.другие варианты _____",
     "send": "2.отправить"},
    {"rq": "3.  Как вы считаете какие виды помощи будущим матерям вы знаете?(несколько)",
     "rp0": "Медицинская помощь",
     "rp1": "Финансовая поддержка",
     "rp2": "Социальные и трудовые гарантии",
     "rp3": "Психологическая и социальная помощь",
     "rp4": "3.другие варианты _____",
     "send": "3.отправить"},
    {"rq": "4.как вы считаете имеет ли соц. сфера влияние на плод?(один)",
     "rp0": "4.да, имеет",
     "rp1": "4.частично",
     "rp2": "4.нет, не имеет",},
    {"rq": "5. Как вы считаете какие факторы влияют на плод?(несколько)",
     "rp0": "материальные услови",
     "rp1": "образ жизни матери",
     "rp2": "психологический стресс",
     "rp3": "экологическая обстановка",
     "rp4": "5.другие варианты _____",
     "send": "5.отправить"
     }
    ]
res={}


def AlreadySended(idd):
    d = con.run("SELECT * FROM terehova_results")
    for i in range(len(d)):
        d[i] = d[i][0]
    if(idd in d): return True
    else: return False

def getResAsArray():
    d = con.run("SELECT * FROM terehova_results")
    #q = [[3,1,5],[3,5,8,3,1,"fert","tyj"],[5,6,2,4,"iuyjt","jy","er"],[3,5,2],[5,6,2,4,"iuyjt","jy","er"]]
    q = [[],[],[],[],[]]
    q1 = []
    q2=[]
    q3=[]
    q4=[]
    q5=[]
    
    for ans in d:
        q1.append(ans[1])
        q2.extend(ans[2])
        q3.extend(ans[3])
        q4.append(ans[4])
        q5.extend(ans[5])
        
    q[0].append(q1.count("0"))
    q[0].append(q1.count("1"))
    q[0].append(q1.count("2"))

    q[1].append(q2.count("0"))
    q[1].append(q2.count("1"))
    q[1].append(q2.count("2"))
    q[1].append(q2.count("3"))
    q[1].append(q2.count("4"))
    q[1].append([])
    for ans in q2:
        if(not(ans in ["0","1","2","3","4"])):
            q[1][5].append(ans)

    q[2].append(q3.count("0"))
    q[2].append(q3.count("1"))
    q[2].append(q3.count("2"))
    q[2].append(q3.count("3"))
    q[2].append([])
    for ans in q3:
        if(not(ans in ["0","1","2","3"])):
            q[2][4].append(ans)
    
    q[3].append(q4.count("0"))
    q[3].append(q4.count("1"))
    q[3].append(q4.count("2"))

    q[4].append(q5.count("0"))
    q[4].append(q5.count("1"))
    q[4].append(q5.count("2"))
    q[4].append(q5.count("3"))
    q[4].append([])
    for ans in q5:
        if(not(ans in ["0","1","2","3"])):
            q[4][4].append(ans)
    return q

def getResAsStringWithArrays():
    d = getResAsArray()
    res = ""
    res+="Вопрос 1:\n"
    res+=str(d[0]) + "\n"
    res+="Вопрос 2:\n"
    res+=str(d[1]) + "\n"
    res+="Вопрос 3:\n"
    res+=str(d[2]) + "\n"
    res+="Вопрос 4:\n"
    res+=str(d[3]) + "\n"
    res+="Вопрос 5:\n"
    res+=str(d[4]) + "\n"
    return(res)

def getResAsString():
    d = getResAsArray()
    res = ""
    for quest in range(len(d)):
        res+= "На вопрос " + str(quest+1) + " дали ответы: \n"
        for resp in range(len(d[quest])):
            if(type(d[quest][resp]) != type([])):
                res+= "ответ " + str(resp+1) + ": " + str(d[quest][resp]) + " раз\n"
            else:
                res+="Ответы пользователей: \n"
                for pers_resp in d[quest][resp]:
                    res+=pers_resp + "\n"
                    
    return(res)

@bot.message_handler(commands=['start'])    
def start_handler(message):
    chat_id = message.chat.id
#    print(getResAsArray())
#    print(getResAsString())
    if(not(AlreadySended(chat_id))):
        res[chat_id] = [0,[],[],0,[]]
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        resp0 = telebot.types.KeyboardButton(text=data[0]['rp0'])
        resp1 = telebot.types.KeyboardButton(text=data[0]['rp1'])
        resp2 = telebot.types.KeyboardButton(text=data[0]['rp2'])
        keyboard.add(resp0,resp1,resp2)
        bot.send_message(chat_id, data[0]["rq"], reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "Ответ уже был отправлен!")


#@bot.message_handler(commands=['AdminStart'])
#def start_handler(message):
#    chat_id = message.chat.id
#    res[chat_id] = [0,[],[],0,[]]
#    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#    resp0 = telebot.types.KeyboardButton(text=data[0]['rp0'])
#    resp1 = telebot.types.KeyboardButton(text=data[0]['rp1'])
#    resp2 = telebot.types.KeyboardButton(text=data[0]['rp2'])
#    keyboard.add(resp0,resp1,resp2)
#    bot.send_message(chat_id, data[0]["rq"], reply_markup=keyboard)



def createKeyboard1():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    resp0 = telebot.types.KeyboardButton(text=data[1]['rp0'])
    resp1 = telebot.types.KeyboardButton(text=data[1]['rp1'])
    resp2 = telebot.types.KeyboardButton(text=data[1]['rp2'])
    resp3 = telebot.types.KeyboardButton(text=data[1]['rp3'])
    resp4 = telebot.types.KeyboardButton(text=data[1]['rp4'])
    resp5 = telebot.types.KeyboardButton(text=data[1]['rp5'])
    send = telebot.types.KeyboardButton(text=data[1]['send'])
    keyboard.add(resp0,resp1,resp2,resp3,resp4,resp5,send)
    return keyboard 
@bot.message_handler(func=lambda message: message.text == data[0]["rp0"])
def resp0_0(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][0] = "0"
        keyboard = createKeyboard1()
        bot.send_message(chat_id, data[1]["rq"], reply_markup=keyboard)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[0]["rp1"])
def resp0_1(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][0] = "1"
        keyboard = createKeyboard1()
        bot.send_message(chat_id, data[1]["rq"], reply_markup=keyboard)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[0]["rp2"])
def resp0_2(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][0] = "2"
        keyboard = createKeyboard1()
        bot.send_message(chat_id, data[1]["rq"], reply_markup=keyboard)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")





def getClientAnswer1(message):
    chat_id = message.chat.id
    if(message.text!=data[1]['rp5']):
        res[chat_id][1].append(message.text)
def createKeyboard2():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    resp0 = telebot.types.KeyboardButton(text=data[2]['rp0'])
    resp1 = telebot.types.KeyboardButton(text=data[2]['rp1'])
    resp2 = telebot.types.KeyboardButton(text=data[2]['rp2'])
    resp3 = telebot.types.KeyboardButton(text=data[2]['rp3'])
    resp4 = telebot.types.KeyboardButton(text=data[2]['rp4'])
    send = telebot.types.KeyboardButton(text=data[2]['send'])
    keyboard.add(resp0,resp1,resp2,resp3,resp4,send)
    return keyboard
@bot.message_handler(func=lambda message: message.text == data[1]["rp0"])
def resp1_0(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][1].append("0")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")    
@bot.message_handler(func=lambda message: message.text == data[1]["rp1"])
def resp1_1(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][1].append("1")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[1]["rp2"])
def resp1_2(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][1].append("2")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[1]["rp3"])
def resp1_3(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][1].append("3")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[1]["rp4"])
def resp1_4(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][1].append("4")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[1]["rp5"])
def resp1_5(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        bot.send_message(chat_id, "Ваш вариант:")
        bot.register_next_step_handler(message, getClientAnswer1)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[1]["send"])
def send1(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        if(res[chat_id][1] != []):
            keyboard = createKeyboard2()
            bot.send_message(chat_id, data[2]["rq"], reply_markup=keyboard)
        else:
            bot.send_message(chat_id, "Выберите хотя бы один вариант ответа!")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")









def getClientAnswer2(message):
    chat_id = message.chat.id
    if(message.text != data[2]['rp4']):
        res[chat_id][2].append(message.text)
def createKeyboard3():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    resp0 = telebot.types.KeyboardButton(text=data[3]['rp0'])
    resp1 = telebot.types.KeyboardButton(text=data[3]['rp1'])
    resp2 = telebot.types.KeyboardButton(text=data[3]['rp2'])
    keyboard.add(resp0,resp1,resp2)
    return keyboard
@bot.message_handler(func=lambda message: message.text == data[2]["rp0"])
def resp2_0(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][2].append("0")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[2]["rp1"])
def resp2_1(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][2].append("1")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[2]["rp2"])
def resp2_2(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][2].append("2")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[2]["rp3"])
def resp2_3(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][2].append("3")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[2]["rp4"])
def resp2_4(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        bot.send_message(chat_id, "Ваш вариант:")
        bot.register_next_step_handler(message, getClientAnswer2)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[2]["send"])
def send2(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        if(res[chat_id][2] != []):
            keyboard = createKeyboard3()
            bot.send_message(chat_id, data[3]["rq"], reply_markup=keyboard)
        else:
            bot.send_message(chat_id, "Выберите хотя бы один вариант ответа!")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")






def createKeyboard4():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    resp0 = telebot.types.KeyboardButton(text=data[4]['rp0'])
    resp1 = telebot.types.KeyboardButton(text=data[4]['rp1'])
    resp2 = telebot.types.KeyboardButton(text=data[4]['rp2'])
    resp3 = telebot.types.KeyboardButton(text=data[4]['rp3'])
    resp4 = telebot.types.KeyboardButton(text=data[4]['rp4'])
    send = telebot.types.KeyboardButton(text=data[4]['send'])
    keyboard.add(resp0,resp1,resp2,resp3,resp4,send)
    return keyboard 
@bot.message_handler(func=lambda message: message.text == data[3]["rp0"])
def resp3_0(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][3] = "0"
        keyboard = createKeyboard4()
        bot.send_message(chat_id, data[4]["rq"], reply_markup=keyboard)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[3]["rp1"])
def resp3_1(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][3] = "1"
        keyboard = createKeyboard4()
        bot.send_message(chat_id, data[4]["rq"], reply_markup=keyboard)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[3]["rp2"])
def resp3_2(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][3] = "2"
        keyboard = createKeyboard4()
        bot.send_message(chat_id, data[4]["rq"], reply_markup=keyboard)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")


def arrayConvert(x):
    return str(x).replace("[", "ARRAY[")


def getInsertReqier(chat_id):
    return 'INSERT INTO terehova_results VALUES (' + str(chat_id) + ",'" + res[chat_id][0] + "'," + arrayConvert(res[chat_id][1]) +","+ arrayConvert(res[chat_id][2]) + ",'" + res[chat_id][3] + "',"+ arrayConvert(res[chat_id][4])+")"
def convertRes(x):
    res = ""
    res+="Вопрос 1: " + data[0]['rp'+x[0]] + "\n"
    res+="Вопрос 2: "
    for i in x[1]:
        if(i=="0" or i=="1" or i=="2" or i=="3" or i=="4"):
            res += data[1]["rp" + i] + ", "
        else:
            res += i + ", "
    res+="\nВопрос 3: "
    for i in x[2]:
        if(i=="0" or i=="1" or i=="2" or i=="3"):
            res += data[2]["rp" + i] + ", " 
        else:
            res += i + ", "
    res+="\nВопрос 4: " + data[3]['rp'+x[3]] + "\n"
    res+="Вопрос 5: "
    for i in x[4]:
        if(i=="0" or i=="1" or i=="2" or i=="3"):
            res += data[4]["rp" + i] + ", "
        else:
            res += i + ", "

    return res
def getClientAnswer3(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        if(message.text !=data[4]['rp4']):
            res[chat_id][4].append(message.text)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[4]["rp0"])
def resp4_0(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][4].append("0")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[4]["rp1"])
def resp4_1(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][4].append("1")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[4]["rp2"])
def resp4_2(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][4].append("2")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[4]["rp3"])
def resp4_3(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        res[chat_id][4].append("3")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[4]["rp4"])
def resp4_5(message):
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        bot.send_message(chat_id, "Ваш вариант:")
        bot.register_next_step_handler(message, getClientAnswer3)
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
@bot.message_handler(func=lambda message: message.text == data[4]["send"])
def send4(message):
    global res
    chat_id = message.chat.id
    if(chat_id in res.keys()):
        if(res[chat_id][4] != []):
            keyboard = telebot.types.ReplyKeyboardRemove()
            bot.send_message(chat_id,"Спасибо за прохождение теста!",reply_markup=keyboard)
            res[chat_id][1] = list(set(res[chat_id][1]))
            res[chat_id][2] = list(set(res[chat_id][2]))
            res[chat_id][4] = list(set(res[chat_id][4]))
            #Сделать, чтобы id  не повторялись
    #        print(getInsertReqier(chat_id))
            if(not(AlreadySended(chat_id))):
                con.run(getInsertReqier(chat_id))
                #bot.send_message(Sanya_id, str(res[chat_id]) + "\n" + convertRes(res[chat_id]))
            else:
                bot.send_message(chat_id, "Ответ уже отправлен!")
            del res[chat_id]
        else:
            bot.send_message(chat_id, "Выберите хотя бы один вариант ответа!")
    else: bot.send_message(chat_id, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")

#@bot.message_handler(commands=['AdminSend'])
#def send4(message):
#    global res
#    chat_id = message.chat.id
#    if(res[chat_id][4] != []):
#        keyboard = telebot.types.ReplyKeyboardRemove()
#        bot.send_message(chat_id,"Спасибо за прохождение теста!",reply_markup=keyboard)
#        res[chat_id][1] = list(set(res[chat_id][1]))
#        res[chat_id][2] = list(set(res[chat_id][2]))
#        res[chat_id][4] = list(set(res[chat_id][4]))
#        print(getInsertReqier(chat_id))
#        con.run(getInsertReqier(chat_id))
#        bot.send_message(Sanya_id, str(res[chat_id]) + "\n" + convertRes(res[chat_id]))
#        del res[chat_id]
#    else:
#        bot.send_message(chat_id, "Выберите хотя бы один вариант ответа!")



    
@bot.message_handler(commands = ['BotExit'])
def botExit(message):
    if(str(message.chat.id) in admins):
        bot.send_message(message.chat.id, "Бот выключен")
        exit()

@bot.message_handler(commands = ['getRes'])
def getRes(message):
    if(str(message.chat.id) in admins):
        bot.send_message(message.chat.id, str(getResAsArray()))
        bot.send_message(message.chat.id, str(getResAsStringWithArrays()))
        bot.send_message(message.chat.id, str(getResAsString()))

@bot.message_handler(commands = ['getResInFile'])
def getRes(message):
    if(str(message.chat.id) in admins):
        with open('res.txt', 'w', encoding='utf-8') as file:
            file.write(str(getResAsArray()) + "\n\n\n" + str(getResAsStringWithArrays()) + "\n\n\n" +str(getResAsString()))
        with open("res.txt", "rb") as file:
            bot.send_document(message.chat.id, file)
        os.remove("C:/Users/Kirill/Desktop/res.txt")


@bot.message_handler(commands = ['getResAsDiagrams'])
def getResDiagrams(message):
    if(str(message.chat.id) in admins):
        #plt.figure(figsize=(10, 6))
        d = getResAsArray()
        
        for resp in range(len(d)):
            if(resp in [1,2,4]):
                d[resp].pop(len(d[resp])-1)
            
            categories = list(range(1, len(d[resp])+1))
            values = list(map(int, d[resp]))
            plt.bar(categories, values)
            plt.title('вопрос номер ' + str(resp+1))
            plt.xlabel('Вариант ответа')
            plt.ylabel('Количество ответов')
            plt.savefig('diag.png')
            bot.send_photo(message.chat.id, open("diag.png", "rb"))
            plt.clf()
        os.remove("C:/Users/Kirill/Desktop/diag.png")


@bot.message_handler(commands = ['getClients'])
def botExit(message):
    if(str(message.chat.id) in admins):
        bot.send_message(message.chat.id, str(res))


@bot.message_handler(commands = ['getClientsCount'])
def botExit(message):
    if(str(message.chat.id) in admins):
        d = con.run("SELECT * FROM terehova_results")
        bot.send_message(message.chat.id, str(len(d)))
    


def resetRes():
    global res
    for i in res.keys():
        bot.send_message(i, "Бот перезагрузился. Для продолжения прохождения теста введите команду /start")
    res = {}
def background_task():
    while True:
        now = datetime.now()
        next_hour_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        sleep_time = (next_hour_time - now).total_seconds() % 3600
        
        # Ожидаем полного часа
        if sleep_time > 0:
            time.sleep(sleep_time)
            
        # Сброс переменной x
        resetRes()
    


if __name__ == "__main__":
    thread = threading.Thread(target=background_task)
    thread.start()


    

    
bot.polling(none_stop=True)




