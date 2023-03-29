from account.models import User
from django.db import models

# 질문란
class Posts(models.Model):
    # CASCADE : User를 삭제하면 관련있는 모든 현재 테이블의 데이터 삭제
    board_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_at = models.DateTimeField()
    update_at = models.DateTimeField(null=True, blank=True)
    # 작성한 질문이 제목으로 보여지게 함
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'posts'
        verbose_name_plural = "posts"

# 댓글란
class Comments(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)
    
    # 작성한 답변이 제목으로 보여지게 함
    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comments'