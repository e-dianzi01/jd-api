from random import randint
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def send_sms_code(phone,code):
    client = AcsClient('LTAIRiQGIywYBeYN', 'ZOHiNBYPr72dCFog2fLU5Pu9RvVAIf', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "Disen工作室")
    request.add_query_param('TemplateCode', "SMS_128646125")
    request.add_query_param('TemplateParam', '{"code":"%s"}' % code)

    response = client.do_action_with_exception(request)
    return response

def get_code():
    code = str(randint(0, 999999)).zfill(6)
    return code

def get_uid():
    user_id ='jd' + str(randint(0, 999999)).zfill(8)
    return user_id

