from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, action
from restApi.models import LogInfo
from restApi.serializers import LogListSerializer, LogCreateSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from datetime import datetime

from rest_framework import mixins
from rest_framework import generics

from rest_framework import viewsets


# fbv로 만드는 crud (조회, 생성)
@api_view(['GET', 'POST'])
def log_list_fbv(request):
    if request.method == 'GET':
        log = LogInfo.objects.all()
        serializer = LogListSerializer(log, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = LogListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# fbv로 만드는 crud (단일조회, 단일수정, 단일삭제)
@api_view(['GET', 'PUT', 'DELETE'])
def log_dtl_fbv(request, pk):
    try:
        log = LogInfo.objects.get(pk=pk)
        # 자료가 없다면 에러처리
    except LogInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':  # 조회
        serializer = LogListSerializer(log)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':  # 수정
        serializer = LogListSerializer(log, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':  # 삭제
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# cbv로 만드는 crud (조회, 생성)
class LogListCbv(APIView):
    def get(self, request):
        log = LogInfo.objects.all()
        serializer = LogListSerializer(log, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LogListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# cbv로 만드는 crud (단일조회, 단일수정, 단일삭제)
class LogDtlCbv(APIView):
    def get(self, request, pk):
        # log = get_object_or_404(pk=pk)
        try:
            log = LogInfo.objects.get(id=pk)
        except LogInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LogListSerializer(log)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            log = LogInfo.objects.get(id=pk)
        except LogInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # print("log : ", log.pk)
        # print("request.data : ", request.data)
        serializer = LogListSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        print("now : ", datetime.now())
        try:
            log = LogInfo.objects.get(id=pk)
        except LogInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        log.delete()
        return Response("delete ok", status=status.HTTP_200_OK)


# CreateModlMixin : post 요청 받았을 때, 생성할 때 create하는 로직
# ListModelMixin : get 요청 받앗을 때, 목록 조회
# RetrieveModelMixin : get 요청 받았을 때, 상세 보기 조회
# UpdateModelMixin : put 또는 patch 요청 받았을 때, 수정
# DestroyModelMixin : delete 요청 받았을 때, 삭제

# mixins 전체검색/생성
class LogListMix(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = LogInfo.objects.all()
    serializer_class = LogListSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class LogDtlMix(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    # APIview 와 다르게 Loginfo 안에서 get으로 단일건 처리해서 가져오지 않아도댐/ 우선가져와서 아래에서 id검색
    queryset = LogInfo.objects.all()
    serializer_class = LogListSerializer

    def get(self, request, pk):
        return self.retrieve(request, id=pk)

    def put(self, request, pk):
        return self.update(request, id=pk)

    def delete(self, request, pk):
        return self.destroy(request, id=pk)


# generics.CreateAPIView : post 요청일 때, create의 매핑되어 object 생성
# generics.ListAPIView : get 요청일 때, list와 매핑되어 object list 제공
# generics.RetrieveAPIView : get 요청일 때, retrieve와 매핑되어 object 상세 정보 제공
# generics.DestroyAPIView : delete 요청일 때, destory와 매핑되어 object 삭제
# generics.UpdateAPIView : put 요청일 때는 update, patch 요청일 때는 partial_update와 매핑
# generics.ListCreateAPIView : CreateAPIView와 ListAPIView를 통합
# generics.RetrieveUpdateAPIView : RetrieveAPIView와 UpdateAPIView를 통합
# generics.RetrieveDestoryAPIView : RetrieveAPIView와 DestroyAPIView를 통합
# generics.RetrieveUpdateDestroyAPIView : RetrieveAPIView, UpdateAPIView, DestroyAPIView 통합

# geneircs 를 통한 전체조회/생성
class LogListGen(generics.ListCreateAPIView):
    queryset = LogInfo.objects.all()
    serializer_class = LogListSerializer


class LogDtlGen(generics.RetrieveUpdateDestroyAPIView):
    queryset = LogInfo.objects.all()
    serializer_class = LogListSerializer


class LogViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = LogInfo.objects.all()
        serializer = LogListSerializer(queryset, many=True)
        return Response(serializer.data)


class LogModelViewSet(viewsets.ModelViewSet):
    queryset = LogInfo.objects.all()
    # serializer_class = LogListSerializer

    def get_serializer_class(self):
        print(self.action)
        if self.action == ('list' or 'retrieve'):
            print('조회 : list or retrieve')
            return LogListSerializer
        else:
            print('create / update / delete ...')
            return LogCreateSerializer

    # 실제로 save를 일으키는 CreateModelMixin 내의 함수인데 커스텀이 필요하다면 view내에서 선언하고 수정처리필요
    # def perform_create(self, serializer):
    #     # profile = LogInfo.objects.get(user=self.request.user)
    #     # serializer.save(author=self.request.user, profile=profile)
    #     print('???????????????????????????????????????? perform_create')

    @action(methods=['get'], detail=False, url_path='dispatch', url_name='dispatchTest')
    def dispatchTest(self, request, pk=None):
        return Response(request.data)


class LogReadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogInfo.objects.all()
    serializer_class = LogListSerializer
