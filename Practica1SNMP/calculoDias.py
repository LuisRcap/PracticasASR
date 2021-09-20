def diasHastaFecha(dia1, mes1, year1, dia2, mes2, year2):
    # Función para calcular si un año es bisiesto o no
    def esBisiesto(year):
        return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)

    # Caso de años diferentes

    if year1 < year2:
        # Días restantes primer año
        if not esBisiesto(year1):
            diasMes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            diasMes = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        restoMes = diasMes[mes1] - dia1

        restoYear = 0
        i = mes1 + 1

        while i <= 12:
            restoYear += diasMes[i]
            i += 1

        primerYear = restoMes + restoYear

        # Suma de días de los años que hay en medio
        sumYear = year1 + 1
        totalDias = 0

        while sumYear < year2:
            if not esBisiesto(sumYear):
                totalDias += 365
                sumYear += 1
            else:
                totalDias += 366
                sumYear += 1

        # Días año actual
        if not esBisiesto(year2) :
            diasMes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            diasMes = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        llevaYear = 0
        ultimoYear = 0
        i = 1

        while i < mes2:
            llevaYear += diasMes[i]
            i += 1

        ultimoYear = llevaYear + dia2

        return totalDias + primerYear + ultimoYear

    # Si estamos en el mismo año
    else:
        if not esBisiesto(year1):
            diasMes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            diasMes = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        llevaYear = 0
        total = 0
        i = mes1

        if i < mes2 :
            while i < mes2 :
                llevaYear += diasMes[i]
                i += 1

            total = dia2 + llevaYear - 1
            return total
        else:
            total =dia2 - dia1
            return total


[dia1, mes1, year1] = list(map(int, input("Introduzca la primera fecha en numeros separados por espacios:\n").split()))

[dia2, mes2, year2] = list(map(int, input("Introduzca la segunda fecha en numeros separados por espacios:\n").split()))

totalDias = diasHastaFecha(dia1, mes1, year1, dia2, mes2, year2)

print("El total de días es: ", totalDias)