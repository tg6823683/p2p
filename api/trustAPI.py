#开户充值
import  app
class trustAPI():
    def __init__(self):
        self.trust_register_url = app.BASE_URL + '/trust/trust/register'  #请求开户
        self.get_recharge_verify_code_url = app.BASE_URL + '/common/public/verifycode/'  #获取充值图片验证码
        self.recharge_url = app.BASE_URL + '/trust/trust/recharge'  #请求后台充值

    #请求开户
    def trust_register(self, session):
        response = session.post(self.trust_register_url)
        return response
    
   #获取充值图片验证码
    def get_recharge_verify_code(self, session, r):
        url = self.get_recharge_verify_code_url + r
        response = session.get(url)
        return response

    # 请求后台充值
    def recharge(self, session, amount='1000', code='8888'):
        data = {"paymentType": "chinapnrTrust",
                "formStr": "reForm",
                "amount": amount,
                "valicode": code}
        response = session.post(self.recharge_url, data=data)
        return response
