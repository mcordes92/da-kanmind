from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Tasks, TaskComments

class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.profile.full_name

class TaskSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='assignee', required=False, write_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='reviewer', required=False, write_only=True)

    comments_count = serializers.SerializerMethodField()

    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer', 'due_date', 'comments_count', 'assignee_id', 'reviewer_id']

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def validate(self, value):
        board = self._get_board(value)

        self._validate_user(value.get('assignee'), board, 'Assignee')
        self._validate_user(value.get('reviewer'), board, 'Reviewer')
        self._prevent_board_change(value)
        return value

    def _get_board(self, value):
        return value.get('board') or getattr(self.instance, 'board', None)
    
    def _validate_user(self, user, board, role):
        if user and user not in board.members.all():
            raise serializers.ValidationError(f"The {role} must be a member of the board.")
        
    def _prevent_board_change(self, value):
        if self.instance and 'board' in value and value['board'] != self.instance.board:
            raise serializers.ValidationError("The board of a task cannot be changed.")
        
class TaskCommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    author = serializers.CharField(source='author.profile.full_name', read_only=True)

    class Meta:
        model = TaskComments
        fields = ['id', 'created_at', 'author', 'content']

    def validate(self, value):
        if not value.get('content').strip():
            raise serializers.ValidationError("The comment content must not be empty.")
        return value
