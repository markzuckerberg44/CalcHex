from decimal import Decimal
from django.shortcuts import render
from django.views import View
from .forms import transformationForm
import math

class index(View):
    def get(self, request):
        form = transformationForm
        return render(request, 'calculator/index.html', {'form': form})

    def post(self, request):
        form = transformationForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']
            base = form.cleaned_data['base']
            conversion_type = form.cleaned_data['conversion_type']
            lista = []
            result = ''


            if number % 1 == 0:
                number = int(number)
                
                if conversion_type == "binary":
                    #loop
                    while number > 0:
                        if number % 2 == 0:
                            lista.append(0)
                        else:
                            lista.append(1)
                        number = number//2

                    lista.reverse()
                    result = lista
                elif conversion_type == "octal":

                    while number > 0:
                        if number % 8 == 0:
                            lista.append(0)
                        else:
                            division = number/8
                            division = round(division, 1)
                            pEntera = math.trunc(division)
                            divStr = str(division)
                            pDecimal = divStr[-1]
                            pDecimal = int(pDecimal)

                        number = pEntera
                        lista.append(pDecimal)    



                    lista.reverse()
                    result = lista


                elif conversion_type == "hexadecimal":
                    while number > 0:
                        division = number/16
                        partEntera = math.trunc(division)
                        partDecimal = division - partEntera
                        resto = int(partDecimal*16)   
                        if resto > 9:
                            if resto == 10:
                                resto = 'A'
                            elif resto == 11:
                                resto = 'B'
                            elif resto == 12:
                                resto = 'C'
                            elif resto == 13:
                                resto = 'D'
                            elif resto == 14:
                                resto = 'E'
                            elif resto == 15:
                                resto = 'F'
                        lista.append(resto)
                        number = partEntera
                    lista.reverse()
                    result = lista


            else:
                if base == 2:
                    result = format(float(number), '.2f')
                elif base == 8:
                    result = format(float(number), '.2f')
                elif base == 16:
                    result = format(float(number), '.2f')
                else:
                    result = str(number)

            return render(request, 'calculator/index.html', {'form': form, 'result': result})
        else:
            return render(request, 'calculator/index.html', {'form': form})