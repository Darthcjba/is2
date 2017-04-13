from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Pagina de inicio a polireserva</h1>")