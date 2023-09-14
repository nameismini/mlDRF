from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from restApi.models import LogInfo
from restApi.serializers import LogListSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from datetime import datetime


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
def log_detail_fbv(request, pk):
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
class LogDetailCbv(APIView):
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
