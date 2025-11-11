from rest_framework import viewsets
from .serializers import BoardListSerializer, BoardCreateSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from boards_app.models import Boards
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsBoardMemberOrOwner, IsBoardOwner

class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.action == "list":
            return BoardListSerializer
        elif self.action == "create":
            return BoardCreateSerializer
        return BoardListSerializer


    def get_queryset(self):
        user = self.request.user
        return (Boards.objects.filter(owner=user) | Boards.objects.filter(members=user)).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        board = serializer.save() 
        return Response(BoardListSerializer(board).data, status=status.HTTP_201_CREATED)