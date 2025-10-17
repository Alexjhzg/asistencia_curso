from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PerfilLaboral
from .serializers import PerfilLaboralSerializer

class PerfilPorCedulaView(APIView):
    def get(self, request, cedula):
        try:
            perfil = PerfilLaboral.objects.get(cedula=cedula)
            serializer = PerfilLaboralSerializer(perfil)
            return Response(serializer.data)
        except PerfilLaboral.DoesNotExist:
            return Response(
                {"error": "No se encontró ninguna persona con esa cédula"},
                status=status.HTTP_404_NOT_FOUND
            )