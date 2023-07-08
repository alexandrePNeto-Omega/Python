import datetime


countID = int(0)

class Usuario:
    def __init__(self, nome):
        self.nome   = nome

# def chatShow():
#     while True:
#         arq = open("chat.txt", "r")
#         listMsg = arq.readlines()
#         tempList = ['']
#         for m in listMsg:
#             if 'envida' not in str(m.replace('\n', '')):
#                 print(m.replace('\n', '')+"\n")
#                 reset  = open("chat.txt", "w")
#                 tempList += [str(m.replace('\n', '')) + ' - envida\n']
#                 reset.writelines(tempList)

def chatShow():
    while True:
        arq = open("chat.txt", "r")
        listMsg = arq.readlines()
        tempList = ['']
        for m in listMsg:
            if 'envida' not in str(m.replace('\n', '')):
                hora = datetime.datetime.now()
                print(str(hora)+ ' ' + m.replace('\n', '')+"\n")
                tempList += [str(m.replace('\n', '')) + ' - envida\n']           
        reset  = open("chat.txt", "w")
        reset.writelines(tempList)

def regUser():
    print("\n------------------- CADASTRO US -------------------\n")
    nameUS  = str(input("Nome: "))
    user = Usuario(nameUS)
    print(" > Usuário cadastrado com sucesso, bom proveito!\n")
    return user

def cadMsg(user, msg):
    arquivo = open("chat.txt", "a")
    arquivo.write(user.nome + ": " + msg + "\n")

####    MAIN
print("\n--------------- BEM-VINDO AO CHAT ---------------\n")

choise  = str(input("Deseja iniciar a tela de bate-papo? (S/n) ")).upper()

if choise != "S":
    user = regUser()
else:
    print(" > Chat iniciado com sucesso, bom proveito!\n")
    chatShow()

while True:
    msg = str(input("Texto: "))
    if msg == "./":
        break

    cadMsg(user, msg)

print("\n------ CHAT FINALIZADO ------\n")