# archivo: cargar_datos.py (corregido para leer códigos numéricos)
# Ejecutar con: python cargar_datos.py (desde la carpeta proyecto_evp con venv activo)

import os
import sys
import django
import pandas as pd
from django.conf import settings

# --- Configuración de Django ---
proyecto_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(proyecto_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_evp.settings')
django.setup()

from asistencia.models import (
    Sexo, NivelEducativo, Organizacion, Gerencia, Estado, Coordinacion,
    Alianza, CargoSegen, Cargo, Persona, PerfilLaboral
)

# --- Diccionarios de Mapeo ---
# Estos mapean los valores numéricos del Excel a los nombres descriptivos
# Basados en la hoja 'choices' de encuesta evp.xlsx
MAPEO_SEXO = {
    1: "Femenino",
    2: "Masculino",
    # Añadir más si existen códigos diferentes
}

MAPEO_NIVEL_EDUCATIVO = {
    1: "Básica",
    2: "Bachiller",
    3: "TSU",
    4: "Universitario",
    5: "Especialización",
    6: "Maestría",
    7: "Doctorado",
    # Añadir más si existen códigos diferentes
}

MAPEO_ORGANIZACION = {
    1: "INE",
    2: "SEGEN",
    # Añadir más si existen códigos diferentes
}

MAPEO_GERENCIA = {
    1: "INE Central", # Asociado a INE
    2: "Gerencia Estadal INE", # Asociado a INE
    # Añadir más según el Excel y XLSForm
    # El Excel parece tener códigos 1 y 2 para gerencia
}

MAPEO_CARGO_SEGEN = {
    1: "Coordinador de NODO",
    2: "Supervisor en el NODO",
    3: "Encuestador integral en el NODO",
    # Añadir más según sea necesario
}

MAPEO_ESTADO = {
    1: "Amazonas",
    2: "Anzoátegui",
    3: "Apure",
    4: "Aragua",
    5: "Barinas",
    6: "Bolívar",
    7: "Carabobo",
    8: "Cojedes",
    9: "Delta Amacuro",
    10: "Distrito capital",
    11: "Falcón",
    12: "Guárico",
    13: "La Guaira",
    14: "Lara",
    15: "Mérida",
    16: "Miranda",
    17: "Monagas",
    18: "Nueva Esparta",
    19: "Portuguesa",
    20: "Sucre",
    21: "Táchira",
    22: "Trujillo",
    23: "Yaracuy",
    24: "Zulia",
    # Añadir más según sea necesario
}

MAPEO_ALIANZA = {
    1: "Brigadistas Hugo Chávez",
    2: "Comunas",
    3: "Chamba Juvenil",
    4: "Educación",
    5: "Comunidad",
    6: "Otros (Alcaldia, Gobernación, Cultura)",
    7: "Milicia",
    # Añadir más según sea necesario, basado en el XLSForm o el Excel
    # El Excel 'que_alianza_pertenece' (col K) tiene códigos (1, 3, 5...).
    # El Excel 'alianza' (col L) tiene textos ("Educación", "Comunas", "Milicia", "Comunidad", 0).
    # Usamos 'que_alianza_pertenece' (col K) y MAPEO_ALIANZA.
}

MAPEO_CARGO = {
    1: "Apoyo Administrativo",
    2: "Apoyo Profesional",
    3: "Coordinador",
    4: "Gerente de Línea",
    5: "Gerente General",
    6: "Supervisor de proyecto",
    7: "Analista integral de proyecto",
    8: "Apoyo administrativo",
    9: "Apoyo profesional",
    10: "Coordinador de proyecto",
    11: "Gerente estatal",
    12: "Supervisor en el NODO", # Asumiendo basado en XLSForm y Excel
    13: "Otro",
    # Añadir más según sea necesario, basado en XLSForm
    # El Excel 'cual_es_su_cargo' (col M) tiene códigos (1, 7, 10...).
    # El Excel 'cargo' (col N) tiene textos.
    # Usamos 'cual_es_su_cargo' (col M) y MAPEO_CARGO.
}

def cargar_datos_desde_excel(nombre_archivo_excel):
    """
    Lee el archivo Excel y carga los datos en las tablas Persona y PerfilLaboral,
    creando objetos de catálogo si no existen, usando mapeos de códigos a nombres.
    """
    print(f"Leyendo archivo: {nombre_archivo_excel}")
    df = pd.read_excel(nombre_archivo_excel)

    # Itera sobre cada fila del DataFrame
    for index, row in df.iterrows():
        print(f"\n--- Procesando fila {index}: {row['nombre']} {row['apellido']} (Cédula: {row['cedula']}) ---")

        # --- 1. OBTENER/CREAR OBJETOS DE CATÁLOGO ---
        # Mapea las columnas de CÓDIGO del Excel a los nombres descriptivos usando los diccionarios
        # Maneja valores '0', 0, o cadenas vacías ("") como nulos si es necesario

        # Sexo (usa 'sexo' que tiene código 1, 2) - CORRECTO
        sexo_codigo = row.get('sexo')
        if pd.notna(sexo_codigo) and sexo_codigo not in [0, '0', '']: # Verifica si no es nulo, 0, '0' o ''
            sexo_nombre = MAPEO_SEXO.get(sexo_codigo) # Busca el nombre en el mapeo
            if sexo_nombre:
                sexo_obj, created = Sexo.objects.get_or_create(nombre=sexo_nombre)
                if created:
                    print(f"  - Sexo '{sexo_nombre}' creado.")
            else:
                sexo_obj = None
                print(f"  - Código de Sexo '{sexo_codigo}' no encontrado en el mapeo.")
        else:
            sexo_obj = None
            print(f"  - Sexo no encontrado o es nulo para fila {index}.")

        # Nivel Educativo (usa 'nivel' que tiene código 1, 2, 3, 4...) - CAMBIAR AQUI
        nivel_edu_codigo = row.get('nivel') # <-- CAMBIADO DE 'nivel_educativo' A 'nivel'
        if pd.notna(nivel_edu_codigo) and nivel_edu_codigo not in [0, '0', '']:
            nivel_edu_nombre = MAPEO_NIVEL_EDUCATIVO.get(nivel_edu_codigo)
            if nivel_edu_nombre:
                nivel_edu_obj, created = NivelEducativo.objects.get_or_create(nombre=nivel_edu_nombre)
                if created:
                    print(f"  - Nivel Educativo '{nivel_edu_nombre}' creado.")
            else:
                nivel_edu_obj = None
                print(f"  - Código de Nivel Educativo '{nivel_edu_codigo}' no encontrado en el mapeo.")
        else:
            nivel_edu_obj = None
            print(f"  - Nivel Educativo no encontrado o es nulo para fila {index}.")

        # Organizacion (usa 'organizacion' que tiene código 1, 2) - CORRECTO
        org_codigo = row.get('organizacion')
        if pd.notna(org_codigo) and org_codigo not in [0, '0', '']:
            org_nombre = MAPEO_ORGANIZACION.get(org_codigo)
            if org_nombre:
                org_obj, created = Organizacion.objects.get_or_create(nombre=org_nombre)
                if created:
                    print(f"  - Organización '{org_nombre}' creada.")
            else:
                org_obj = None
                print(f"  - Código de Organización '{org_codigo}' no encontrado en el mapeo.")
        else:
            org_obj = None
            print(f"  - Organización no encontrada o es nula para fila {index}.")

        # Gerencia (usa 'gerencia' que tiene código 1, 2) - CORRECTO
        gerencia_codigo = row.get('gerencia')
        gerencia_obj = None
        if pd.notna(gerencia_codigo) and gerencia_codigo not in [0, '0', ''] and org_obj: # Requiere org_obj
            gerencia_nombre = MAPEO_GERENCIA.get(gerencia_codigo)
            if gerencia_nombre:
                gerencia_obj, created = Gerencia.objects.get_or_create(
                    nombre=gerencia_nombre,
                    organizacion=org_obj # Clave foránea
                )
                if created:
                    print(f"  - Gerencia '{gerencia_nombre}' (Org: {org_obj.nombre}) creada.")
            else:
                print(f"  - Código de Gerencia '{gerencia_codigo}' no encontrado en el mapeo.")
        elif not org_obj:
             print(f"  - ADVERTENCIA: No se puede crear/get Gerencia con código '{gerencia_codigo}' sin Organización.")

        # Coordinacion (usa 'nombre_de_la_gerenciacoordinacion_de_adscripcion_a_la_que_pertenece_a_nivel_central' que tiene texto)
        # Si el valor es '0', lo tratamos como nulo
        coord_nombre = row.get('nombre_de_la_gerenciacoordinacion_de_adscripcion_a_la_que_pertenece_a_nivel_central')
        coord_obj = None
        if pd.notna(coord_nombre) and coord_nombre not in [0, '0', '']: # Verifica si no es nulo, 0, '0' o ''
            # Asegurarse de que sea string antes de comparar
            if isinstance(coord_nombre, (int, float)) and coord_nombre == 0:
                 coord_nombre = None
            elif coord_nombre == '0':
                 coord_nombre = None
            if coord_nombre:
                coord_obj, created = Coordinacion.objects.get_or_create(nombre=coord_nombre)
                if created:
                    print(f"  - Coordinación '{coord_nombre}' creada.")
        else:
            print(f"  - Coordinación no encontrada o es nula para fila {index}.")

        # Cargo SEGEN (usa 'cargo_ocupa_en_el_segen' que tiene código 1, 2, 3) - CAMBIAR AQUI
        cargo_sg_codigo = row.get('cargo_ocupa_en_el_segen') # <-- CAMBIADO DE 'cargo_segen' A 'cargo_ocupa_en_el_segen'
        cargo_sg_obj = None
        if pd.notna(cargo_sg_codigo) and cargo_sg_codigo not in [0, '0', '']:
             cargo_sg_nombre = MAPEO_CARGO_SEGEN.get(cargo_sg_codigo)
             if cargo_sg_nombre:
                 cargo_sg_obj, created = CargoSegen.objects.get_or_create(nombre=cargo_sg_nombre)
                 if created:
                     print(f"  - Cargo SEGEN '{cargo_sg_nombre}' creado.")
             else:
                 print(f"  - Código de Cargo SEGEN '{cargo_sg_codigo}' no encontrado en el mapeo.")
        else:
             print(f"  - Cargo SEGEN no encontrado o es nulo para fila {index}.")

        # Estado (usa 'cual_estado' que tiene código 1, 2, 3...) - CAMBIAR AQUI
        estado_codigo = row.get('cual_estado') # <-- CAMBIADO DE 'estado' A 'cual_estado'
        estado_obj = None
        if pd.notna(estado_codigo) and estado_codigo not in [0, '0', '']:
            estado_nombre = MAPEO_ESTADO.get(estado_codigo)
            if estado_nombre:
                estado_obj, created = Estado.objects.get_or_create(nombre=estado_nombre)
                if created:
                    print(f"  - Estado '{estado_nombre}' creado.")
            else:
                print(f"  - Código de Estado '{estado_codigo}' no encontrado en el mapeo.")
        else:
            print(f"  - Estado no encontrado o es nulo para fila {index}.")

        # Alianza (usa 'que_alianza_pertenece' que tiene código 1, 3, 5...) - CAMBIAR AQUI
        alianza_codigo = row.get('que_alianza_pertenece') # <-- CAMBIADO DE 'alianza' A 'que_alianza_pertenece'
        alianza_obj = None
        if pd.notna(alianza_codigo) and alianza_codigo not in [0, '0', '']:
            alianza_nombre = MAPEO_ALIANZA.get(alianza_codigo)
            if alianza_nombre:
                alianza_obj, created = Alianza.objects.get_or_create(nombre=alianza_nombre)
                if created:
                    print(f"  - Alianza '{alianza_nombre}' creada.")
            else:
                print(f"  - Código de Alianza '{alianza_codigo}' no encontrado en el mapeo.")
        else:
            print(f"  - Alianza no encontrada o es nula para fila {index}.")

        # Cargo (INE) (usa 'cual_es_su_cargo' que tiene código 1, 2, 3...) - CAMBIAR AQUI
        cargo_codigo = row.get('cual_es_su_cargo') # <-- CAMBIADO DE 'cargo' A 'cual_es_su_cargo'
        cargo_obj = None
        if pd.notna(cargo_codigo) and cargo_codigo not in [0, '0', '']:
             cargo_nombre = MAPEO_CARGO.get(cargo_codigo)
             if cargo_nombre:
                 # Opcional: intentar asociar con gerencia_contexto si es relevante en tu modelo Cargo
                 # Por ahora, solo por nombre
                 cargo_obj, created = Cargo.objects.get_or_create(nombre=cargo_nombre)
                 if created:
                     print(f"  - Cargo '{cargo_nombre}' creado.")
             else:
                 print(f"  - Código de Cargo '{cargo_codigo}' no encontrado en el mapeo.")
        else:
             print(f"  - Cargo no encontrado o es nulo para fila {index}.")

        # Profesion (almacenado directamente en Persona, usa 'profesion' que tiene texto)
        profesion_nombre = row.get('profesion', '') # Valor por defecto si no existe la columna o es nulo
        # Manejar profesión vacía o nula
        if pd.isna(profesion_nombre) or profesion_nombre == '':
            profesion_nombre = '' # o None si el campo lo permite

        # --- 2. CREAR/ACTUALIZAR PERSONA ---
        if not sexo_obj or not nivel_edu_obj:
            print(f"  - ERROR: Sexo o Nivel Educativo faltantes (sexo_obj: {sexo_obj}, nivel_edu_obj: {nivel_edu_obj}). Saltando Persona {row['cedula']}.")
            continue # Salta a la siguiente fila si campos requeridos no se pueden obtener

        persona_defaults = {
            'nombre': row.get('nombre', ''),
            'apellido': row.get('apellido', ''),
            'correo': row.get('correo', ''),
            'edad': row.get('edad'),
            'profesion': profesion_nombre,
            'sexo': sexo_obj,
            'nivel_educativo': nivel_edu_obj,
        }

        # update_or_create: Busca por cedula, si no existe crea con defaults
        persona_obj, persona_created = Persona.objects.update_or_create(
            cedula=str(row['cedula']), # Convertir a string por si acaso
            defaults=persona_defaults
        )
        if persona_created:
            print(f"  - Persona '{persona_obj.nombre} {persona_obj.apellido}' (Cédula: {persona_obj.cedula}) creada.")
        else:
            print(f"  - Persona '{persona_obj.nombre} {persona_obj.apellido}' (Cédula: {persona_obj.cedula}) actualizada.")


        # --- 3. CREAR/ACTUALIZAR PERFIL_LABORAL ---
        # Requiere que persona_obj exista
        # Asegúrate de que gerencia_obj sea requerido según tu modelo. Si no lo es, omítelo o maneja None.
        if not gerencia_obj:
             print(f"  - ADVERTENCIA: No se encontró gerencia para {persona_obj.nombre}. No se creará/actualizará PerfilLaboral.")
             # Puedes decidir si continuar o no aquí. Si gerencia es requerida en el modelo, fallará la creación/update.
             # Para este ejemplo, asumiremos que puede ser nulo si el modelo lo permite, o se omite si es un error lógico.
             # Si es requerido y no se puede obtener, deberías saltar esta parte o asignar un valor por defecto si aplica.
             # Por ahora, solo actualizamos si gerencia_obj es válido.
             continue

        perfil_defaults = {
            'organizacion': org_obj,
            'estado': estado_obj,
            'coordinacion': coord_obj,
            'cargo_segen': cargo_sg_obj,
            'cargo': cargo_obj,
            'gerencia': gerencia_obj, # Requerido según el modelo original
            'alianza': alianza_obj,
        }

        # update_or_create para PerfilLaboral
        perfil_obj, perfil_created = PerfilLaboral.objects.update_or_create(
            cedula=persona_obj, # Clave foránea/OneToOneField a Persona
            defaults=perfil_defaults
        )
        if perfil_created:
            print(f"  - Perfil Laboral para '{persona_obj.nombre} {persona_obj.apellido}' creado.")
        else:
            print(f"  - Perfil Laboral para '{persona_obj.nombre} {persona_obj.apellido}' actualizado.")

    print("\n--- Carga de datos completada. ---")

# --- Punto de entrada del script ---
if __name__ == "__main__":
    # Ruta al archivo Excel
    # Ajusta la ruta si el archivo no está en la misma carpeta que este script
    nombre_archivo = "Respaldo personal_evp.xlsx"

    # Ejecuta la función de carga
    try:
        cargar_datos_desde_excel(nombre_archivo)
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
