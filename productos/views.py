from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import Producto
from .forms import ProductoForm
from ventasApp.models import Categoria
from unidades.models import Unidad
from django.db.models import Q

class ProductosView(View):
    template_name = 'productos.html'

    def get(self, request):
        query = request.GET.get('q', '')
        productos = Producto.objects.filter(estado=True)

        if query:
            productos = productos.filter(
                Q(descripcion__icontains=query) | Q(id__icontains=query)
            )

        unidades = Unidad.objects.filter(estado=True)
        categorias = Categoria.objects.filter(estado=True)
        form = ProductoForm()
        ctx = {
            "productos": productos,
            "unidades": unidades,
            "categorias": categorias,
            "form": form
        }
        return render(request, self.template_name, ctx)
    
    def post(self, request):
        form = ProductoForm(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            if Producto.objects.filter(descripcion=descripcion, estado=True).exists():
                return JsonResponse({"error": "El producto ya existe"})
            else:
                form.save()
                return JsonResponse({"success": "Producto registrado correctamente"}, status=201)
        
        return JsonResponse({"error": "Error al registrar el producto"}, status=400)

def producto_delete(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.estado = False
    producto.save()
    return redirect('productos')

class ProductoEdit(View):
    template_name = 'producto_edit.html'

    def get(self, request, id):
        producto = get_object_or_404(Producto, id=id, estado=True)
        productos = Producto.objects.filter(estado=True)
        form = ProductoForm(instance=producto)
        print(producto.categoria_id)
        ctx = {
            "form": form,
            "productos": productos,
            "producto": producto
        }
        return render(request, self.template_name, ctx)
    
    def post(self, request, id):
        producto = get_object_or_404(Producto, id=id, estado=True)
        form = ProductoForm(data = request.POST or None, instance=producto)


        if form.is_valid():
        # Verificar si la descripción ya existe en otros productos activos
            descripcion = form.cleaned_data['descripcion']

            if Producto.objects.filter(descripcion=descripcion, estado=True).exclude(id=id).exists():
                return JsonResponse({"error": "La descripción del producto ya existe"}, status=400)
            else:
                form.save()
                return redirect('productos')
        
        return JsonResponse({"error": "Error al actualizar el producto"}, status=400)

""" 
    def post(self, request):
        form = ProductoForm(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            if Producto.objects.filter(descripcion=descripcion, estado=True).exists():
                return JsonResponse({"error": "El producto ya existe"})
            else:
                form.save()
                return JsonResponse({"success": "Producto registrado correctamente"}, status=201)
        
        return JsonResponse({"error": "Error al registrar el producto"}, status=400)
 """
def get_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data = {
        'id': producto.id,
        'descripcion': producto.descripcion,
        'precio': producto.precio,
        'stock': producto.stock,
        'categoria': producto.categoria.id,
        'unidad': producto.unidad.id,
    }
    return JsonResponse(data)
