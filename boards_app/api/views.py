from rest_framework import viewsets, views
from .serializers import BoardListSerializer, BoardCreateSerializer, BoardDetailSerializer, BoardUpdateSerializer, BoardUpdateResSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from boards_app.models import Boards
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsBoardMemberOrOwner

class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.action == "list":
            return BoardListSerializer
        elif self.action == "create":
            return BoardCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return BoardUpdateSerializer
        return BoardDetailSerializer


    def get_queryset(self):
        user = self.request.user
        return (Boards.objects.filter(owner=user) | Boards.objects.filter(members=user)).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        board = serializer.save() 
        return Response(BoardListSerializer(board).data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={"request": request})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()
        return Response(BoardUpdateResSerializer(board).data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        board = self.get_object()

        if board.owner != request.user:
            return Response({"detail": "Nur der Eigentümer darf dieses Board löschen."}, status=status.HTTP_403_FORBIDDEN)

        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      
class EmailCheck(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response({"detail": "E-Mail-Parameter fehlt."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            fullname = user.profile.full_name

            return Response({
                "id": user.id,
                "email": user.email,
                "fullname": fullname
            })
        except User.DoesNotExist:
            return Response({"detail": "Benutzer mit dieser E-Mail existiert nicht."}, status=status.HTTP_404_NOT_FOUND)