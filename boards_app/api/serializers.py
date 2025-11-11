from rest_framework import serializers
from boards_app.models import Boards
from django.contrib.auth.models import User

class BoardListSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Boards
        fields = [
            'id',
            'title',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id'
        ]

    def get_member_count(self, obj):
        #return obj.members.count()
        return 0

    def get_ticket_count(self, obj):
        #return obj.tasks.count()
        return 0

    def get_tasks_to_do_count(self, obj):
        #return obj.tasks.filter(status='to-do').count()
        return 0

    def get_tasks_high_prio_count(self, obj):
        #return obj.tasks.filter(priority='high').count()
        return 0
    
class BoardCreateSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Boards
        fields = ['title', 'members']

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        owner = self.context["request"].user
        board = Boards.objects.create(owner=owner, **validated_data)
        users = User.objects.filter(id__in=members)
        board.members.set(users)

        return board