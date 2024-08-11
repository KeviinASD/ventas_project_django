from django.shortcuts import render, redirect
from django.views import View
from .models import Cliente
from django.shortcuts import get_object_or_404
from .forms import ClienteForm
from django.http import JsonResponse

# Create your views here.
class ClienteView(View):
    template_name = 'cliente.html'

    def get(self, request):
        clientes = Cliente.objects.filter(estado=True)
        form = ClienteForm()
        ctx = {
            "clientes": clientes,
            "form": form
        }
        return render(request, self.template_name, ctx)
    
    def post(self, request):
        form = ClienteForm(request.POST)
        if form.is_valid():
            nombres = form.cleaned_data['nombres']
            
            if Cliente.objects.filter(nombres=nombres, estado=True).exists():
                return JsonResponse({"error": "El cliente ya existe"})
            else:
                form.save()
                return JsonResponse({"success": "Cliente registrado correctamente"}, status=201)
        
        return JsonResponse({"error": "Error al registrar el cliente"}, status=400)

def cliente_delete(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.estado = False
    cliente.save()
    return redirect('clientes')

def cliente_edit(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)

        ruc_dni = request.POST.get('ruc_dni')
        if Cliente.objects.filter(ruc_dni=ruc_dni, estado=True).exclude(id=id).exists():
            return JsonResponse({"error": "El cliente ya existe"}, status=400)

        if form.is_valid():
            form.save()
            return JsonResponse({"success": "Cliente editado correctamente"}, status=200)
        else:
            return JsonResponse({"error": "Error al editar el cliente"}, status=400)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

def getCliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    data = {
        'id': cliente.id,
        'nombres': cliente.nombres,
        'direccion': cliente.direccion,
        'ruc_dni': cliente.ruc_dni,
        'telefono': cliente.telefono,
        'email': cliente.email
    }
    return JsonResponse(data)