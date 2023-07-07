secret_word = "stop"

####    FUNC'S
def verifiAction(string):
    formatedString = string.replace(' ', '')[0]
    if '1' in formatedString:
        return 'Configuração'
    elif '2' in formatedString:
        return 'Ajuste'
    elif '3' in formatedString:
        return 'Instalação'
    elif '4' in formatedString:
        return 'Download'
    elif '5' in formatedString:
        return 'Informação'
    elif '6' in formatedString:
        return 'Criação'
    elif '7' in formatedString:
        return 'Ativação'
    else:
        return 'Operador não registrado'
    
def verifiConfig():
    configList          = ['Data', 'Grupo', 'Obrigatório']
    resultListConfig    = ''

    for c in configList:
        txt = input(" > "+str(c) + ': ')
        resultListConfig += " > " + str(c) +": " + txt.upper() + "\n"

    return resultListConfig

#   Template de para a escrita do check: 2 o_ele_é tipo grupo obrigatório
def chkWordAnalict(string):
    config  = verifiConfig()
    action  = verifiAction(string)
    content = string.replace(string[0], '')
    return action + " -" + content + ".\n" + config.rstrip() + "\n"

####    MAIN
print("---------- CHECK LIST HELP ----------\n")

print("AÇÕES:\n")
print(" 1 - Configuração\n 2 - Ajuste\n 3 - Instalação\n 4 - Download\n 5 - Informação\n 6 - Criação\n 7 - Ativação\n")

title       = input("Insira o título do CheckList: ")
position    = int(1)
checkList   = []

print()

print("---------- "+ title.upper() +" ----------")
while True:
    check   = input("\nInforme sobre o check: ")
    
    if check == secret_word:
        print()
        break
    
    checkList += [chkWordAnalict(check)]

for ck in  checkList:
    print(ck)


open("check.txt", "w") 
arquivo = open("check.txt", "a")
arquivo.write("Titulo: " + title + "\n")
arquivo.writelines(checkList)
# string = "Evidência - Coletada as informações sobre o processo ao todo
# +"" > Data: Bolean ""
#  > Grupo: 
#  > Remoto Obrigatório: SIM."
arquivo.write("Evidência - Coletada as informações sobre o processo ao todo - Data: Bolean Grupo: Remoto Obrigatório: SIM.")

# Evidência - Coletada as informações sobre o processo ao todo