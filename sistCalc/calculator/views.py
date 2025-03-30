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
        number = str(number).upper()
        n = len(number)-1
        resultado = 0
        if "." not in number:            
            if origin_base == 'binary':
                for i, d in enumerate(number):
                    operacion = int(d) * (2**(n-i))
                    resultado += operacion
            elif origin_base == 'octal':
                for i, d in enumerate(number):
                    operacion = int(d) * (8**(n-i))
                    resultado += operacion
            elif origin_base == 'hexadecimal':
                hex_map = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
                for i, d in enumerate(number):
                    if d in hex_map:
                        digito = hex_map[d]
                    else:
                        digito = int(d)
                    operacion = digito * (16**(n-i))
                    resultado += operacion
        else:
            number_parts = number.split('.')
            parte_entera = number_parts[0]
            parte_fraccion = number_parts[1]
            resultado += self.something_to_decimal(parte_entera, origin_base)
            if origin_base == 'binary':
                for i, d in enumerate(parte_fraccion):
                    operacion = int(d) * (2**-(i+1))
                    resultado += operacion
            elif origin_base == 'octal':
                for i, d in enumerate(parte_fraccion):
                    operacion = int(d) * (8**-(i+1))
                    resultado += operacion
            elif origin_base == 'hexadecimal':
                hex_map = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
                for i, d in enumerate(parte_fraccion):
                    if d in hex_map:
                        digito = hex_map[d]
                    else:
                        digito = int(d)
                    operacion = digito * (16**-(i+1))
                    resultado += operacion
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

            result = str(result)

            return render(request, 'calculator/index.html', {'form': form, 'result': result})
    
        else:
            return render(request, 'calculator/index.html', {'form': form})