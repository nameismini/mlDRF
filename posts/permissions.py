from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
    ## 글 조회:누구나, 생성:로그인한 유저, 편집:글 작성자
    def has_permission(self, request, view):
        print('request.user.is_authenticated : ', request.user.is_authenticated)
        if request.method == 'GET':
            return True
        return request.user.is_authenticated

    # 특정 object에 접근하는 순간 권한확인 - check_object_permissions 을 통해 호출
    # 작성자만 접근, 작성자가 아니면 Read만 가능
    def has_object_permission(self, request, view, obj):
        print('has_object_permission')
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
