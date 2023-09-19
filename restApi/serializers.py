from rest_framework import serializers
from restApi.models import LogInfo


class LogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogInfo
        fields = ['id', 'restGbn', 'crudMod', 'remark', 'temp1', 'temp2', 'reg_date']


class LogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogInfo
        fields = ['restGbn', 'crudMod', 'remark', 'temp1', 'temp2']
