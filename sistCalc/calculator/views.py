from decimal import Decimal
from django.shortcuts import render
from django.views import View
from .forms import transformationForm
import math

class index(View):
    def get(self, request):
        form = transformationForm
        return render(request, 'calculator/index.html', {'form': form})

    def something_to_decimal(self, number, origin_base):

        #logica por si recibimos un numero entero a transformar
        if number%1 == 0:
            n = len(str(number))-1
            i = 0
            digitos = [int(d) for d in str(number)]
            resultado = 0
            if origin_base == 'binary':
                while i <= n:
                    operacion = digitos[i] * (2**(n-i))
                    resultado+= operacion
                    i+=1
            elif origin_base == 'octal':
                while i <= n:
                    operacion = digitos[i] * (8**(n-i))
                    resultado+= operacion
                    i+=1
            elif origin_base == 'hexadecimal':
                
                while i <= n:
                    if type(digitos[i]) == str:
                        if digitos[i] == 'A':
                            digitos[i] = 10
                        elif digitos[i] == 'B':
                            digitos[i] = 11
                        elif digitos[i] == 'C':
                            digitos[i] = 12
                        elif digitos[i] == 'D':
                            digitos[i] = 13
                        elif digitos[i] == 'E':
                            digitos[i] = 14
                        elif digitos[i] == 'F':
                            digitos[i] = 15
                    operacion = digitos[i] * (16**(n-i))
                    resultado+= operacion
                    i+=1

            
            # aqui implementamos la logica si recibimos un numero con "," para transformar
            

        return resultado

                
        

    def decimal_to_something(self, number, conversion_type):
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
                    resto = number % 8  # Calcula el resto de la división entre 8
                    lista.append(resto)  # Agrega el resto a la lista
                    number = number // 8  # Divide el número entre 8 (división entera)
                       
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
        return result        
 
    def post(self, request):
        form = transformationForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']
            #base = form.cleaned_data['base']
            conversion_type = form.cleaned_data['conversion_type']
            origin_base = form.cleaned_data['num_to_convert']	

            if conversion_type == origin_base:
                return render(request, 'calculator/index.html', {'form': form, 'result': 'Error: No se puede convertir a la misma base.'})

            if origin_base == 'decimal':
                result = self.decimal_to_something(number, conversion_type)

            elif origin_base == 'binary':
                #primero debemos pasar de binario a decimal
                result = self.something_to_decimal(number, origin_base)
                #despues de decimal a la base que queremos
                if conversion_type != 'decimal':
                    result = self.decimal_to_something(result, conversion_type)

            elif origin_base == 'octal':
                #primero debemos pasar de octal a decimal
                result = self.something_to_decimal(number, origin_base)
                #despues de decimal a la base que queremos
                if conversion_type != 'decimal':
                    result = self.decimal_to_something(result, conversion_type)
            
            elif origin_base == 'hexadecimal':
                #primero debemos pasar de hexadecimal a decimal
                result = self.something_to_decimal(number, origin_base)
                #despues de decimal a la base que queremos
                if conversion_type != 'decimal':
                    result = self.decimal_to_something(result, conversion_type)
            
            if isinstance(result, int):
                result = [result]

            result = ''.join(map(str, result))

            return render(request, 'calculator/index.html', {'form': form, 'result': result})
    
        else:
            return render(request, 'calculator/index.html', {'form': form})