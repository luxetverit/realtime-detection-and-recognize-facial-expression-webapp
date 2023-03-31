from account.models import User
from django.db import models

# 질문란
class BoardPost(models.Model):
    # CASCADE : User를 삭제하면 관련있는 모든 현재 테이블의 데이터 삭제
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True,auto_now=True)
    # 작성한 질문이 제목으로 보여지게 함
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'boardpost'
        verbose_name_plural = "boardPosts"

# 댓글란
class BoardComment(models.Model):
    boardpost=models.ForeignKey(BoardPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True,auto_now=True)
    
    # 작성한 답변이 제목으로 보여지게 함
    def __str__(self):
        return self.content

    class Meta:
        db_table = 'boardcomment'
        verbose_name_plural = "boardComments"
