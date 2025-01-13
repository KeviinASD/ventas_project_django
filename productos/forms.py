from django import forms
from .models import productoFields, Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = productoFields
        labels = {
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'unidad': 'Unidad',
            'precio': 'Precio',
            'stock': 'Stock'
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'w-full px-3 py-3 border border-gray-300 text-sm rounded-md shadow-sm focus:outline-none focus:ring-0 sm:text-sm', 'placeholder': 'Ingrese la descripción del producto'}),
            'categoria': forms.Select(attrs={'class': 'w-full px-3 py-3 border border-gray-300 text-sm rounded-md shadow-sm focus:outline-none focus:ring-0 sm:text-sm'}),
            'unidad': forms.Select(attrs={'class': 'w-full px-3 py-3 border border-gray-300 text-sm rounded-md shadow-sm focus:outline-none focus:ring-0 sm:text-sm'}),
            'precio': forms.NumberInput(attrs={'class': 'w-full px-3 py-3 border border-gray-300 text-sm rounded-md shadow-sm focus:outline-none focus:ring-0 sm:text-sm', 'placeholder': 'Ingrese el precio del producto'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full px-3 py-3 border border-gray-300 text-sm rounded-md shadow-sm focus:outline-none focus:ring-0 sm:text-sm', 'placeholder': 'Ingrese el stock del producto'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        # Filtrar productos con estado igual a 1
        self.fields['categoria'].queryset = self.fields['categoria'].queryset.filter(estado=True)
        self.fields['unidad'].queryset = self.fields['unidad'].queryset.filter(estado=True)
        
        