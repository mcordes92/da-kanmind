from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Boards
from tasks_app.api.serializers import TaskSerializer
from tasks_app.models import Tasks

# Serializer for board list view with computed statistics
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
        return obj.members.count()

    def get_ticket_count(self, obj):
        return Tasks.objects.filter(board=obj).count()

    def get_tasks_to_do_count(self, obj):
        return Tasks.objects.filter(board=obj, status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return Tasks.objects.filter(board=obj, priority='high').count()
    
# Serializer for creating a new board with member assignments
class BoardCreateSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Boards
        fields = ['title', 'members']

    def create(self, validated_data):
        # Extract member IDs and assign current user as board owner
        members = validated_data.pop("members", [])
        owner = self.context["request"].user
        board = Boards.objects.create(owner=owner, **validated_data)
        users = User.objects.filter(id__in=members)
        board.members.set(users)

        return board
    
# Serializer for user data with profile full name
class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.profile.full_name
    
# Serializer for detailed board view including members and tasks
class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source='owner.id')
    members = UserSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Boards
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']

    def get_tasks(self, obj):
        qs = Tasks.objects.filter(board=obj)
        tasks = TaskSerializer(qs, many=True).data
        return tasks

# Serializer for updating board title and members
class BoardUpdateSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    title = serializers.CharField(required=False)

    class Meta:
        model = Boards
        fields = ['title', 'members']

    def validate_members(self, value):
        # Ensure all provided user IDs exist in database
        valid_members = User.objects.filter(id__in=value)
        missing_ids = set(value) - set(valid_members.values_list('id', flat=True))

        if missing_ids:
            raise serializers.ValidationError(
                f"invalid user ids: {', '.join(map(str, missing_ids))}"
            )
        return value
    
    def update(self, instance, validated_data):
        members = validated_data.pop("members", None)
        title = validated_data.get("title", None)

        if title is not None:
            instance.title = title

        if members is not None:
            users = User.objects.filter(id__in=members)
            instance.members.set(users)

        instance.save()
        return instance
    
# Serializer for board update response with owner and member details
class BoardUpdateResSerializer(serializers.ModelSerializer):
    owner_data = UserSerializer(source='owner', read_only=True)
    members_data = UserSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Boards
        fields = ['id', 'title', 'owner_data', 'members_data']