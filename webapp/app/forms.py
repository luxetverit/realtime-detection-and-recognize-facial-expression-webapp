from django import forms
from app.models import Comments,Posts


class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts  # 사용할 모델
        fields = ['title', 'content']  # PostsForm에서 사용할 Posts 모델의 속성
        # 질문등록란에 '제목' , '내용' 글씨 추가
        labels = {
            'title': '제목',
            'content': '내용',
        }  

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        labels = {
            'content': '답변내용',
        }