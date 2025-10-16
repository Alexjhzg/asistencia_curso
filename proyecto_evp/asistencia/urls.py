from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('', views.formulario_asistencia, name='formulario_asistencia'),
    path('api/gerencias/', views.get_gerencias, name='get_gerencias'),
    path('api/cargos/', views.get_cargos, name='get_cargos'),
    path('api/datos_persona/', views.get_datos_persona, name='get_datos_persona'),
    path('api/guardar_participacion/', views.guardar_participacion, name='guardar_participacion'),
    # Rutas para obtener opciones de catálogo dinámicamente
    path('api/choices/sexo/', views.get_sexo_choices, name='get_sexo_choices'),
    path('api/choices/nivel_educativo/', views.get_nivel_edu_choices, name='get_nivel_edu_choices'),
    path('api/choices/cargo_segen/', views.get_cargo_segen_choices, name='get_cargo_segen_choices'),
    path('api/choices/organizacion/', views.get_organizacion_choices, name='get_organizacion_choices'),
    path('api/choices/estado/', views.get_estado_choices, name='get_estado_choices'),
    path('api/choices/coordinacion/', views.get_coordinacion_choices, name='get_coordinacion_choices'),
    path('api/choices/alianza/', views.get_alianza_choices, name='get_alianza_choices'),
    path('api/choices/ubicacion/', views.get_ubicacion_choices, name='get_ubicacion_choices'),
    path('api/choices/curso/', views.get_curso_choices, name='get_curso_choices'),
]

# Vistas auxiliares para opciones dinámicas de SurveyJS
def get_sexo_choices(request):
    from django.db.models import F
    choices = Sexo.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_nivel_edu_choices(request):
    from django.db.models import F
    choices = NivelEducativo.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_cargo_segen_choices(request):
    from django.db.models import F
    choices = CargoSegen.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_organizacion_choices(request):
    from django.db.models import F
    choices = Organizacion.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_estado_choices(request):
    from django.db.models import F
    choices = Estado.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_coordinacion_choices(request):
    from django.db.models import F
    choices = Coordinacion.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_alianza_choices(request):
    from django.db.models import F
    choices = Alianza.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_ubicacion_choices(request):
    from django.db.models import F
    choices = Ubicacion.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_curso_choices(request):
    from django.db.models import F
    choices = Curso.objects.values('id', 'tema', 'fecha_curso').annotate(
        value=F('id'),
        text=F('tema') # O puedes usar tema + fecha si lo prefieres
    )
    # Opcional: Formatear la fecha en el JSON
    formatted_choices = []
    for choice in choices:
        formatted_choices.append({
            'value': choice['value'],
            'text': f"{choice['tema']} - {choice['fecha_curso']}"
        })
    return JsonResponse(formatted_choices, safe=False)
