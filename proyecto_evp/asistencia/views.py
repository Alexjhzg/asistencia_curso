from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import F # Importar F para usar en las consultas de opciones
from .models import Organizacion, Gerencia, Cargo, CargoSegen, Estado, Coordinacion, Alianza, Ubicacion, Curso, Persona, PerfilLaboral
import json

def formulario_asistencia(request):
    # Obtener listas de opciones para el frontend
    organizaciones = list(Organizacion.objects.values('id', 'nombre'))
    estados = list(Estado.objects.values('id', 'nombre'))
    coordinaciones = list(Coordinacion.objects.values('id', 'nombre'))
    alianzas = list(Alianza.objects.values('id', 'nombre'))
    ubicaciones = list(Ubicacion.objects.values('id', 'nombre'))
    cursos = list(Curso.objects.values('id', 'tema', 'fecha_curso'))

    # Pasarlas al contexto de la plantilla
    context = {
        'organizaciones': json.dumps(organizaciones),
        'estados': json.dumps(estados),
        'coordinaciones': json.dumps(coordinaciones),
        'alianzas': json.dumps(alianzas),
        'ubicaciones': json.dumps(ubicaciones),
        'cursos': json.dumps(cursos),
    }
    return render(request, 'asistencia/formulario.html', context)

# Vista para obtener Gerencias filtradas por Organización
def get_gerencias(request):
    org_id = request.GET.get('organizacion_id')
    if org_id:
        gerencias = Gerencia.objects.filter(organizacion_id=org_id).values('id', 'nombre')
        return JsonResponse(list(gerencias), safe=False)
    else:
        # Si no se proporciona ID, devolver lista vacía
        return JsonResponse([], safe=False)

# Vista para obtener Cargos filtrados por Gerencia
def get_cargos(request):
    gerencia_id = request.GET.get('gerencia_id')
    if gerencia_id:
        cargos = Cargo.objects.filter(gerencia_contexto_id=gerencia_id).values('id', 'nombre')
        return JsonResponse(list(cargos), safe=False)
    else:
        # Si no se proporciona ID, devolver lista vacía
        return JsonResponse([], safe=False)

# Vista para buscar datos de una persona por cédula
def get_datos_persona(request):
    cedula = request.GET.get('cedula')
    if not cedula:
        return JsonResponse({'error': 'Cédula no proporcionada'}, status=400)

    try:
        persona = Persona.objects.get(cedula=cedula)
        perfil = PerfilLaboral.objects.get(cedula=cedula)

        # Devolver datos relevantes
        data = {
            'nombre': persona.nombre,
            'apellido': persona.apellido,
            'correo': persona.correo,
            'edad': persona.edad,
            'profesion': persona.profesion,
            'sexo': persona.sexo.id,
            'nivel_educativo': persona.nivel_educativo.id,
            'organizacion': perfil.organizacion.id,
            'estado': perfil.estado.id if perfil.estado else None,
            'coordinacion': perfil.coordinacion.id if perfil.coordinacion else None,
            'cargo_segen': perfil.cargo_segen.id if perfil.cargo_segen else None,
            'cargo': perfil.cargo.id if perfil.cargo else None,
            'gerencia': perfil.gerencia.id,
            'alianza': perfil.alianza.id if perfil.alianza else None,
        }
        return JsonResponse(data)
    except (Persona.DoesNotExist, PerfilLaboral.DoesNotExist):
        return JsonResponse({'error': 'Persona no encontrada'}, status=404)

# Vista para guardar la participación
def guardar_participacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Procesar los datos recibidos de SurveyJS
            cedula = data.get('cedula')
            telefono = data.get('telefono')
            otro_telefono = data.get('otro_telefono')
            comentario = data.get('comentario')
            registrado = data.get('registrado')
            encuentra = data.get('encuentras') # Nombre del campo en el formulario SurveyJS
            curso_id = data.get('curso_id')

            if not all([cedula, encuentra, curso_id, telefono, registrado is not None]):
                return JsonResponse({'error': 'Faltan campos obligatorios.'}, status=400)

            # Validar que la persona exista
            try:
                persona = Persona.objects.get(cedula=cedula)
            except Persona.DoesNotExist:
                return JsonResponse({'error': 'La persona no existe.'}, status=400)

            # Validar que el curso exista
            try:
                curso = Curso.objects.get(id=curso_id)
            except Curso.DoesNotExist:
                return JsonResponse({'error': 'El curso no existe.'}, status=400)

            # Validar que la ubicación exista
            try:
                ubicacion = Ubicacion.objects.get(id=encuentra)
            except Ubicacion.DoesNotExist:
                return JsonResponse({'error': 'La ubicación no existe.'}, status=400)

            # Crear o actualizar la participación
            participacion = ParticipacionCurso.objects.create(
                cedula=persona,
                telefono=telefono,
                otro_telefono=otro_telefono,
                comentario=comentario,
                registrado=registrado,
                encuentra=ubicacion,
                curso_id=curso
            )

            return JsonResponse({'success': True, 'message': 'Participación registrada exitosamente.'})
        except ValidationError as e:
            # Manejar errores de validación del modelo (ej: formato de teléfono)
            return JsonResponse({'error': f'Error de validación: {e.message_dict}'}, status=400)
        except Exception as e:
            print(f"Error al guardar participación: {e}") # Log para debugging
            return JsonResponse({'error': 'Error interno al guardar la participación.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

# Vistas auxiliares para opciones dinámicas de SurveyJS
def get_sexo_choices(request):
    choices = Sexo.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_nivel_edu_choices(request):
    choices = NivelEducativo.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_cargo_segen_choices(request):
    choices = CargoSegen.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_organizacion_choices(request):
    choices = Organizacion.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_estado_choices(request):
    choices = Estado.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_coordinacion_choices(request):
    choices = Coordinacion.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_alianza_choices(request):
    choices = Alianza.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_ubicacion_choices(request):
    choices = Ubicacion.objects.values('id').annotate(value=F('id'), text=F('nombre'))
    return JsonResponse(list(choices), safe=False)

def get_curso_choices(request):
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
