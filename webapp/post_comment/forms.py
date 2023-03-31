from django import forms
from .models import BoardComment ,BoardPost


class BoardPostForm(forms.ModelForm):
    class Meta:
        model = BoardPost  # 사용할 모델
        fields = ['title', 'content']  # PostsForm에서 사용할 Posts 모델의 속성
        # 질문등록란에 '제목' , '내용' 글씨 추가
        labels = {
            'title': '제목',
            'content': '내용',
        }  

class BoardCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = BoardComment
        fields = ('content',)
        labels = {'content': '댓글'}
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '댓글을 입력하세요'
            })
        }