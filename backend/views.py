import json
from django.shortcuts import render, HttpResponse
from repository import models
from datetime import datetime
from datetime import date


class JsonCustomEncoder(json.JSONEncoder):

    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, value)


def curd(request):
    return render(request, 'curd.html')


def curd_json(request):
    table_config = [
        {
            'q': None,  # 数据查询字段
            'title': '选择',  # 显示标题
            'display': True,  # 是否显示
            'text': {
                'tpl': "<input type='checkbox' value='{n1}' />",
                'kwargs': {'n1': '@id'}
            },
            'attrs': {'nid': '@id'}
        },
        {
            'q':'id',
            'title':'ID',
            'display': False,
            'text':{
                 'tpl':"{n1}",
                 'kwargs':{'n1':'@id'}
            },
            'attrs': {'k1': 'v1', 'k2': '@hostname'}
         },
        {
            'q': 'hostname',
            'title': '主机名',
            'display': True,
            'text': {
                'tpl': "{n1}-{n2}",
                'kwargs': {'n1': '@hostname', 'n2': '@id'}
            },
            'attrs': {'edit-enable': 'true', 'k2': '@hostname'}
        },
        # 页面显示：标题：操作：删除，标记：a标签
        {
            'q': None,
            'title': '操作',
            'display': True,
            'text':{
                'tpl':"<a href='/del?nid={nid}'>删除</a>",
                'kwargs':{'nid':'@id'}
            },
            'attrs': {'k1': 'v1', 'k2': '@hostname'}
        },
    ]
    # 普通值：原值存放即可
    # @值  ： 根据id，根据获取当前行对应数据

    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])

    server_list = models.Server.objects.values(*values_list)
    ret = {
        'server_list':list(server_list),
        'table_config':table_config
    }

    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def asset(request):
    # v = models.Server.objects.all()
    return render(request, 'asset.html')


def asset_json(request):
    table_config = [
        {
            'q': None,  # 数据查询字段
            'title': '选择',  # 显示标题
            'display': True,  # 是否显示
            'text': {
                'tpl': "<input type='checkbox' value='{n1}' />",
                'kwargs': {'n1': '@id'}
            },
            'attrs': {'nid': '@id'}
        },
        {
            'q': 'id',
            'title': 'ID',
            'display': False,
            'text': {
                'tpl': "{n1}",
                'kwargs': {'n1': '@id'}
            },
            'attrs': {'k1': 'v1', 'k2': '@id'}
        },
        {
            'q': 'device_type_id',
            'title': '资产类型',
            'display': True,
            'text': {
                'tpl': "{n1}",
                'kwargs': {'n1': '@@device_type_choices'}
            },
            'attrs': {'k1': 'v1', 'origin': '@device_type_id','edit-enable': 'true','edit-type':'select','global_key':'device_type_choices'}
        },
        {
            'q': 'device_status_id',
            'title': '状态',
            'display': True,
            'text': {
                'tpl': "{n1}",
                'kwargs': {'n1': '@@device_status_choices'}
            },
            'attrs': {'edit-enable': 'true','origin':'@device_status_id','edit-type':'select','global_key':'device_status_choices'}
        },
        {
            'q': 'cabinet_num',
            'title': '机柜号',
            'display': True,
            'text': {
                'tpl': "{n1}",
                'kwargs': {'n1': '@cabinet_num'}
            },
            'attrs': {'edit-enable': 'true','k1': 'v1', 'k2': '@id'}
        },
        {
            'q': 'idc__id',
            'title': '机房',
            'display': False,
            'text': {},
            'attrs': {}
        },
        {
            'q': 'idc__name',
            'title': '机房',
            'display': True,
            'text': {
                'tpl': "{n1}",
                'kwargs': {'n1': '@idc__name'}
            },
            'attrs': {'k1':'v1','origin':'@idc_id','edit-enable': 'true','edit-type':'select','global_key':'idc_choices'}
        },
        # 页面显示：标题：操作；删除，编辑：a标签
        {
            'q': None,
            'title': '操作',
            'display': True,
            'text': {
                'tpl': "<a href='/del?nid={nid}'>删除</a>",
                'kwargs': {'nid': '@id'}
            },
            'attrs': {'k1': 'v1', 'k2': '@id'}
        },
    ]
    # 普通值：原值存放即可
    # @值  ： 根据id，根据获取当前行对应数据
    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])

    server_list = models.Asset.objects.values(*values_list)

    ret = {
        'server_list': list(server_list),
        'table_config': table_config,
        'global_dict':{
            'device_type_choices': models.Asset.device_type_choices,
            'device_status_choices': models.Asset.device_status_choices,
            'idc_choices': list(models.IDC.objects.values_list('id','name'))
        }

    }

    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))