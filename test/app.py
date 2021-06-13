import json

import re
import time
import datetime

from aliyunsdkcore.request import CommonRequest
from flask import Flask, render_template, request
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkiot.request.v20180120.QueryDevicePropertiesDataRequest import QueryDevicePropertiesDataRequest

accessKeyId = 'LTAI4GKWJfofRnLAfTE4cZZA'
accessSecret = 'v1oQgJlwGZ4fBpBQ7sZ44JxNgAeeAC'
ProductKey = 'a1cm1SFrUuh'
DeviceName = 'test'
RegionId = 'cn-shanghai'
client = AcsClient(accessKeyId, accessSecret, RegionId)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index/')
def hello(name=None):
    name = "张三"
    return render_template('index.html', name=name)


@app.route('/info/')
def test():
    request_ali = QueryDevicePropertiesDataRequest()
    print(request_ali.__dict__)
    request_ali.set_accept_format('json')

    request_ali.set_ProductKey(ProductKey)
    request_ali.set_DeviceName(DeviceName)
    request_ali.set_Asc("0")
    request_ali.set_EndTime("1620144000000")
    request_ali.set_StartTime("1651680000000")
    # request_ali.set_Identifiers(["LockSwitch", "Version", "CurrentVoltage", "GeoLocation", "BatteryPercentage"])
    request_ali.add_query_param('Identifier.1','CurrentVoltage')
    request_ali.add_query_param('Identifier.2','Version')
    request_ali.add_query_param('Identifier.3','BatteryPercentage')
    request_ali.add_query_param('Identifier.4', 'LockSwitch')
    request_ali.add_query_param('Identifier.5', 'GeoLocation')
    request_ali.set_PageSize("10")

    response = client.do_action_with_exception(request_ali)

    # print(str(response, encoding='utf-8')) json
    # print(type(response))

    response_dict = json.loads(response)
    # print(type(response_dict))
    # response_dict_str = str(response, encoding='utf-8')

    # print(response_dict_str)
    print(response_dict['PropertyDataInfos'])
    data = response_dict['PropertyDataInfos']['PropertyDataInfo']
    print(len(data))
    CurrentVoltage = data[0]['List']['PropertyInfo'][0]['Value']
    Version = data[1]['List']['PropertyInfo'][0]['Value']
    BatteryPercentage = data[2]['List']['PropertyInfo'][0]['Value']
    LockSwitch = data[3]['List']['PropertyInfo'][0]['Value']
    GeoLocation = data[4]['List']['PropertyInfo'][0]['Value']
    # GeoLocation ='GeoLocation'
    print(type(data))
    print(CurrentVoltage)
    print(Version)
    print(BatteryPercentage)
    print(LockSwitch)
    print(GeoLocation)
    print(type(CurrentVoltage))
    return render_template('test.html', LockSwitch=LockSwitch, CurrentVoltage=CurrentVoltage, Version=Version,
                           BatteryPercentage=BatteryPercentage, GeoLocation=GeoLocation)


@app.route('/SetLockSwitch', methods=['POST'])
def SetLockSwitch():
    if request.method == 'POST':
        # print(request.data)
        # print(type(request.data))
        string = str(request.data, encoding='utf-8')
        data = eval(string)
        print(data)
        # print(json.dumps(request.data))
        # data = json.dumps(request.data)
        #
        value = data['LockSwitch']
        print(data['LockSwitch'])
        print(type(value))
        Items = {"LockSwitch": int(value)}
        print(type(Items))
        request_ali = CommonRequest()
        request_ali.set_accept_format('json')
        request_ali.set_domain('iot.cn-shanghai.aliyuncs.com')
        request_ali.set_method('POST')
        request_ali.set_protocol_type('https')  # https | http
        request_ali.set_version('2018-01-20')
        request_ali.set_action_name('SetDeviceProperty')
        request_ali.add_query_param('Items', json.dumps(Items))
        request_ali.add_query_param('ProductKey', ProductKey)
        request_ali.add_query_param('DeviceName', DeviceName)
        response = client.do_action_with_exception(request_ali)
        print(str(response, encoding='utf-8'))
        return str(response, encoding='utf-8')
    return 'false'

#查询设备详情
@app.route('/QueryDeviceDetail')
def QueryDeviceDetail():
    #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('QueryDeviceDetail')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('ProductKey', ProductKey)
    request.add_query_param('DeviceName', DeviceName)
    try:
        # <class 'bytes'>
        response = client.do_action_with_exception(request)
        # <class 'dict'>
        rep= json.loads(response)
        print(rep)
        #<class 'str'>
        #print(str(response, encoding='utf-8'))

    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)

#注册设备
@app.route('/RegisterDevice')
def RegisterDevice():
    #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('RegisterDevice')
    request.add_query_param('ProductKey',ProductKey)
    request.add_query_param('DeviceName',DeviceName)
    try:
        #<bytes>
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)

#查询指定设备运行状态
@app.route('/GetDeviceStatus')
def GetDeviceStatus():
        #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('GetDeviceStatus')
    request.add_query_param('ProductKey', ProductKey)
    request.add_query_param('DeviceName', DeviceName)
    try:
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
        print(rep)
        print(str(response,encoding='utf-8'))
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)

#查询指定产品下的所有设备 QueryDevice
@app.route('/QueryDevice')
def QueryDevice():
    #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('QueryDevice')
    request.add_query_param('ProductKey',ProductKey)
    try:
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
        print(rep)
        # print(str(response,encoding='utf-8'))
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)

#查询指定产品物模型中的功能定义详情
@app.route('/QueryThingModel')
def QueryThingModel():
        #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('QueryThingModel')
    request.add_query_param('ProductKey',ProductKey)
    try:
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
        print(rep)
        print('---')
        print(str(response, encoding='utf-8'))
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)

#批量查询指定设备的多个属性的历史数据 QueryDevicePropertiesData
@app.route('/QueryDevicePropertiesData')
def QueryDevicePropertiesData():
     
    # print (t)                       #原始时间数据
    # print (int(t))                  #秒级时间戳
    # print (int(round(t * 1000)))    #毫秒级时间戳
    # print (int(round(t * 1000000))) #微秒级时间戳

    print('---datetime---')
    now_time=datetime.datetime.now()
    now_time_timestamp=time.mktime(now_time.timetuple())
    lastmonth_time=now_time-datetime.timedelta(days=30)
    lastmonth_time_timeStamp =(time.mktime(lastmonth_time.timetuple()))
    startime=int(round(lastmonth_time_timeStamp*1000))
    endtime=int(round(now_time_timestamp*1000))
    
    #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('QueryDevicePropertiesData')
    request.add_query_param('Asc',"1")
    request.add_query_param('DeviceName',DeviceName)
    request.add_query_param('ProductKey',ProductKey)
    
    request.add_query_param('EndTime', endtime)
   
    request.add_query_param('StartTime', startime)
    # request.add_query_param('Identifier.1','CurrentVoltage')
    # request.add_query_param('Identifier.2','GeoLocation')
    # request.add_query_param('Identifier.3', 'BatteryPercentage')
    # request.add_query_param('Identifier.4', 'LockSwitch')
    request.add_query_param('Identifier.1','GPIO1')
    request.add_query_param('Identifier.2','GPIO2')

    request.add_query_param('PageSize',"20")
    try:
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
        print(rep)
        print('---')
        # print(str(response, encoding='utf-8'))
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)


#调用指定设备上的指定服务 InvokeThingService
@app.route('/InvokeThingService')
def InvokeThingService():
        #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('InvokeThingService')
    request.add_query_param('Args','{"LockSwitch":1}')
    request.add_query_param('Identifier','Test')
    request.add_query_param('ProductKey',ProductKey)
    request.add_query_param('DeviceName',DeviceName)
    try:
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
        print(rep)
        print('---')
        # print(str(response, encoding='utf-8'))
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)

#指定设备设置属性值 SetDeviceProperty
@app.route('/SetLockSwitch_1')
def SetLockSwitch_1():
        #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('SetDeviceProperty')
    request.add_query_param('Items','{"LockSwitch":1,"CurrentVoltage":6,"BatteryPercentage":56}')
    request.add_query_param('DeviceName',DeviceName)
    request.add_query_param('ProductKey',ProductKey)
    try:
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
        print(rep)
        print('---')
        # print(str(response, encoding='utf-8'))
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)

@app.route('/SetLockSwitch_0')
def SetLockSwitch_0():
        #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('SetDeviceProperty')
    request.add_query_param('Items','{"LockSwitch":0}')
    request.add_query_param('DeviceName',DeviceName)
    request.add_query_param('ProductKey',ProductKey)
    try:
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
        print(rep)
        print('---')
        # print(str(response, encoding='utf-8'))
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)

@app.route('/SetLow')
def SetLow():
        #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('SetDeviceProperty')
    request.add_query_param('Items','{"GPIO1":0}')
    request.add_query_param('DeviceName',DeviceName)
    request.add_query_param('ProductKey',ProductKey)
    try:
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
        print(rep)
        print('---')
        # print(str(response, encoding='utf-8'))
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)

@app.route('/SetHigh')
def SetHigh():
        #创建Request对象。
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('iot.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2018-01-20')

    request.set_action_name('SetDeviceProperty')
    request.add_query_param('Items','{"GPIO1":1}')
    request.add_query_param('DeviceName',DeviceName)
    request.add_query_param('ProductKey',ProductKey)
    try:
        response = client.do_action_with_exception(request)
        rep = json.loads(response)
        print(rep)
        print('---')
        # print(str(response, encoding='utf-8'))
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    return json.dumps(rep,ensure_ascii=False)
@app.route('/SetProperty', methods=['POST'])
def SetProperty():
    if request.method == 'POST':
        # print(request.data)
        # print(type(request.data))
        string = str(request.data, encoding='utf-8')
        data = eval(string)
        print(data)
        # print(json.dumps(request.data))
        # data = json.dumps(request.data)
        #
        property=data['property']
        propertyvalue = data['propertyvalue']
        print(data['property'])
        print(data['propertyvalue'])

        print(type(property))
        print(type(propertyvalue))
        Items = {property: propertyvalue}
        print(type(Items))
        request_ali = CommonRequest()
        request_ali.set_accept_format('json')
        request_ali.set_domain('iot.cn-shanghai.aliyuncs.com')
        request_ali.set_method('POST')
        request_ali.set_protocol_type('https')  # https | http
        request_ali.set_version('2018-01-20')
        request_ali.set_action_name('SetDeviceProperty')
        request_ali.add_query_param('Items', json.dumps(Items))
        request_ali.add_query_param('ProductKey', ProductKey)
        request_ali.add_query_param('DeviceName', DeviceName)
        response = client.do_action_with_exception(request_ali)
        print(str(response, encoding='utf-8'))
        return str(response, encoding='utf-8')
    
    return 'false'
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
