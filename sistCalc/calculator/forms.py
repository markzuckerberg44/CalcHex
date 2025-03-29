from django import forms

class transformationForm(forms.Form):

    number = forms.DecimalField(label='Numero', max_digits=10, decimal_places=2)

    num_to_convert = forms.ChoiceField(
        label="Base de origen",
        choices=[('decimal', 'Decimal'), ('binary', 'Binario'), ('octal', 'Octal'), ('hexadecimal', 'Hexadecimal')],
        widget=forms.Select, required=False
    )
    
    conversion_type = forms.ChoiceField(
        label="Tipo de conversion",
        choices=[('decimal', 'Decimal'),('binary', 'A Binario'), ('octal', 'A Octal'), ('hexadecimal', 'A Hexadecimal')],
        widget=forms.Select, required=False
    )  

    #base = forms.IntegerField(label='Base')
    #result = forms.CharField(label='Result', max_length=100, required=False)   