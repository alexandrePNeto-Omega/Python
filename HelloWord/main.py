####    Funções
#   Monta result
def mountResult(n1, n2, op, calc):
    mounted = ""
    mounted += n1 + " " + op + " " + n2 + " = " + calc 
    return mounted

#   Corta pelo operador e retorna a lista
def calcs():
    listNum = ""

    n1 = input ("N1: ")
    if n1 == '': listNum += '0'
    listNum += n1 + " "

    n2 = input("N2: ")
    if n2 == '': listNum += '0'
    listNum += n2

    return listNum

#   Vifirca operador
def virifiOp(string):
    result  = ""
    nome    = ""
    #   Números
    verifcString = string.strip("+-*/")
    if verifcString == "":
        nums = calcs().split()
        n1 = int(nums[0])
        n2 = int(nums[1])

    if string == "+":
        nome    = "soma"
        result  = mountResult(str(n1), str(n2), string, str(n1 + n2))

    elif string == "-":
        nome    = "subtração"
        result  = mountResult(str(n1), str(n2), string, str(n1 - n2))

    elif string == "/":
        nome    = "divisão"
        result = mountResult(str(n1), str(n2), string, str(n1 / n2))

    elif string == "*":
        nome    = "multiplicação"
        result = mountResult(str(n1), str(n2), string, str(n1 * n2))

    else:
        return False
    
    return "O resultado de sua "+nome+" é: \n > " + result

####    Main
#   Var's
secret_word = "stop"
countTrue   = int(0)
countFalse  = int(0)
count       = int(1)
relList     = []
finalMesg   = "\nVocê realizou "
concatFinal = "errada"

#   body
print("\nOlá, bem-vindo a minha simples calculadora!\n")
print("Temos os seguites operadores\n - Multiplicador \"*\"\n - Divisor \"/\"\n - Soma \"+\"\n - Subtração \"-\"\n")

while True:
    calc = input("Colque seu operador aqui: ")
    if calc == secret_word:
        print("Calcuradora finalizada pela paravra secreta!")
        break
    else:
        finalResult = virifiOp(calc)
        if finalResult == False:
            print("Operador inválido, tente novamente.\n")
            countFalse += int(1)
            relList += ['Erro']
            continue
        print(finalResult+"\n")
        relList += ['Sucesso']
        countTrue += int(1)

#   Relatório de tentativas
print()
print("\n-------- Relatório de tentativas --------")
for t in relList:
    print(str(count) + "º tentativa executada com " + str(t).lower() + ".")
    count += int(1)

if countFalse > 1:
    concatFinal += "s"

if countTrue != 1:
    print(finalMesg + str(countTrue) +  " operações com suceso & " + str(countFalse) + " " + str(concatFinal))

elif countFalse == 0:
    print("Nenhum operação realizada.")

else:
    print(finalMesg + str(countTrue) +  " operação com suceso & " + str(countFalse) + " " + str(concatFinal))
