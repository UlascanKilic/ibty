from random import randint

def dortislem(random):
    operatorler = ["-", "+", "*"]
    operator = operatorler[randint(0, 2)]
    sayi1 = randint(0, random)
    sayi2 = randint(0, random)
    if (operator == "+"):
        sonuc = sayi1 + sayi2
        soru = str(sayi1) +" "+ str(operator)+" " + str(sayi2)+" = ?"
        dizi = [sonuc, soru]

        return dizi
    elif (operator == "-"):
        sonuc = sayi1 - sayi2
        soru = str(sayi1) + " " + str(operator) + " " + str(sayi2)+" = ?"
        dizi = [sonuc, soru]
        return dizi
    elif (operator == "*"):
        sonuc = sayi1 * sayi2
        soru = str(sayi1) + " " + "x" " " + str(sayi2)+" = ?"
        dizi = [sonuc, soru]
        return dizi



def terstenislem():
    operatorler = ["-", "+", "*"]
    operator = operatorler[randint(0, 2)]
    cevap = randint(1, 15)
    sayi1 = randint(1, 5)
    sayi2 = randint(1, 20)
    if(operator == "*"):
        ise = (cevap * sayi1) + sayi2
        sonuc = (ise - sayi2) / sayi1

        soru = "Bir sayinin " + str(sayi1) + " katinin " + str(sayi2) + " fazlasi " + str(
            ise) + " ise o sayi kactir ?"
        dizi = [sonuc, soru]
        return dizi

    elif(operator == "-"):
        ise = (cevap - sayi1) + sayi2
        sonuc = (ise + sayi1) - sayi2

        soru = "Bir sayinin " + str(sayi1) + " eksigi " + str(sayi2) + " fazlasi " + str(
            ise) + " ise o sayi kactir ?"
        dizi = [sonuc, soru]
        return dizi

    elif(operator == "+"):
        ise = (cevap + sayi1) - sayi2
        sonuc = (ise + sayi2) - sayi1

        soru = "Bir sayinin " + str(sayi1) + " fazlasi " + str(sayi2) + " eksigi " + str(
            ise) + " ise o sayi kactir ?"
        dizi = [sonuc, soru]
        return dizi
