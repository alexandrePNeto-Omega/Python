####    Import's
import datetime

####    Class's
class User:
    def __init__(self, name):
        self.name   = name

####    Functions
def chatShow():
    #   Getting first user was sent a msg
    firstAqr = open("chat.txt", "r")
    listAqr = firstAqr.readlines()
    lastUser = str(str(listAqr[0]).split(':')[0])

    while True:
        arq = open("chat.txt", "r")
        listMsg = arq.readlines()
        tempList = ['']
        for m in listMsg:
            formtMsg = str(m.replace('\n', ''))
            if '&$#@24!%@' not in formtMsg and formtMsg != '':
                #   Hour                
                hora = datetime.datetime.now()
                finalTime = str(hora).split('.')
                nowUser = str(formtMsg.split(':')[0])
                
                #   Print, validete & lastUser
                if nowUser != lastUser:
                    print('\n' + finalTime[0] + ' ' + m.replace('\n', ''))
                else:
                    print(finalTime[0] + ' ' + m.replace('\n', ''))

                tempList += [str(m.replace('\n', '')) + ' - &$#@24!%@\n']   
                lastUser = formtMsg.split(':')[0] 

                #   Reset       
                reset = open("chat.txt", "w")
                reset.writelines(tempList)         

def regUser():
    print("\n------------------- CADASTRO US -------------------\n")
    nameUS  = str(input("Nome: "))
    user = User(nameUS)
    print("\n > Usuário cadastrado com sucesso, bom proveito!\n")
    print("\n---------------------------------------------------\n")
    return user

def cadMsg(user, msg):
    setAqr = open("chat.txt", "a")
    setAqr.write(user.name + ": " + msg + "\n")

####    Main
print("\n---------------- BEM-VINDO AO CHAT ----------------")

choise  = str(input("\nDeseja iniciar a tela de bate-papo? (S/n) -> ")).upper()

if choise != "S":
    user = regUser()
else:
    print("\n > Chat iniciado com sucesso, bom proveito!")
    print("\n---------------------------------------------------")
    chatShow()

while True:
    msg = str(input("Texto: "))
    if msg == "./":
        break
    cadMsg(user, msg)

print("\n------ CHAT FINALIZADO ------\n")