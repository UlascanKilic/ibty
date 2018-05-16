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
        dictory = {'sayi1': sayi1,
                   'fazla': sayi2,
                   'ise': ise,
                   'sayi': cevap,
                   'sonuc': sonuc
                   }
        sorulistesi = list(dictory.values())
        cevap = str(sorulistesi[2])
        soru = "Bir sayinin " + str(sorulistesi[0]) + " katinin " + str(sorulistesi[1]) + " fazlasi " + str(
            sorulistesi[3]) + " ise o sayi kactir ?"
        dizi = [cevap, soru]
        return dizi

    elif(operator == "-"):
        ise = (cevap - sayi1) + sayi2
        sonuc = (ise - sayi2) + sayi1
        dictory = {'sayi1': sayi1,
                   'fazla': sayi2,
                   'ise': ise,
                   'sayi': cevap,
                   'sonuc': sonuc
                   }
        sorulistesi = list(dictory.values())
        cevap = str(sorulistesi[2])
        soru = "Bir sayinin " + str(sorulistesi[0]) + " eksigi " + str(sorulistesi[1]) + " fazlasi " + str(
            sorulistesi[3]) + " ise o sayi kactir ?"
        dizi = [cevap, soru]
        return dizi
    elif(operator == "+"):
        ise = (cevap + sayi1) - sayi2
        sonuc = (ise + sayi2) - sayi1
        dictory = {'sayi1': sayi1,
                   'fazla': sayi2,
                   'ise': ise,
                   'sayi': cevap,
                   'sonuc': sonuc
                   }
        sorulistesi = list(dictory.values())
        cevap = str(sorulistesi[2])
        soru = "Bir sayinin " + str(sorulistesi[0]) + " fazlasi " + str(sorulistesi[1]) + " eksigi " + str(
            sorulistesi[3]) + " ise o sayi kactir ?"
        dizi = [cevap, soru]
        return dizi







