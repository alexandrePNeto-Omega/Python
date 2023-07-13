
# -*- coding: utf-8 -*-
####    Import's
import datetime
import time

####    Class's
class User:
    def __init__(self, name):
        self.name   = name

####    Functions
def chatShow():
    try:
        #   Getting first user was sent a msg
        firstAqr = open("chat.txt", "r")
        listAqr = firstAqr.readlines()
        lastUser = str(str(listAqr[0]).split(':')[0])

        while True:
            arq = open("chat.txt", "r")
            listMsg = arq.readlines()
            tempList = ['']
            time.sleep(0.50)
            for m in listMsg:
                formtMsg = str(m.replace('\n', ''))
                if '&$#@24!%@' not in formtMsg and formtMsg != '':
                    #   Hour                
                    hora = datetime.datetime.now()
                    finalTime = str(hora).split('.')

                    #   Print, validete & lastUser
                    nowUser = str(formtMsg.split(':')[0])
                    if nowUser != lastUser:
                        print('\n' + finalTime[0] + ' ' + m.replace('\n', ''))
                    else:
                        print(finalTime[0] + ' ' + m.replace('\n', ''))
                    tempList += [str(m.replace('\n', '')) + ' - &$#@24!%@\n']   
                    lastUser = formtMsg.split(':')[0] 

                    #   Reset       
                    reset = open("chat.txt", "w")
                    reset.writelines(tempList)     
    except:
        print("\n----------------- CHAT FINALIZADO -----------------")    

def regUser():
    print("\n------------------- CADASTRO US -------------------\n")
    nameUS  = str(raw_input("Nome: "))
    user = User(nameUS)
    print("\n > Usuário cadastrado com sucesso, bom proveito!")
    print("\n---------------------------------------------------")
    return user

def cadMsg(user, msg):
    setAqr = open("chat.txt", "a")
    setAqr.write(user.name + ": " + msg + "\n")

####    Main
print("\n---------------- BEM-VINDO AO CHAT ----------------")

choise  = str(raw_input("\nDeseja iniciar a tela de bate-papo? (S/n) -> ")).upper()

if choise != "S":
    user = regUser()
    while True:
        try:
            msg = str(raw_input("\nTexto: "))
            if msg == "./":
                break
            cadMsg(user, msg)
        except:
            print()
            break
    print("\n----------------- CHAT FINALIZADO -----------------")
else:
    print("\n > Chat iniciado com sucesso, bom proveito!")
    print("\n---------------------------------------------------")
    chatShow()