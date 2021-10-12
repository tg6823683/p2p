import  requests
import  app


class LoginAPI():
    def __init__(self):
        self.getImgCodeUrl=app.BASE_URL+'/common/public/verifycode1/'
        self.getSmsCodeUrl=app.BASE_URL+'/member/public/sendSms'
        self.registerUrl=app.BASE_URL+'/member/public/reg'
        self.loginUrl=app.BASE_URL+'/member/public/login'

    # 获取图片验证码
    def getImgCode(self,session,r):
        url=self.getImgCodeUrl+r    
        response=session.get(url)
        return  response

    #获取手机短信验证码
    def getSmsCode(self,session,phone,imgVerifyCode,type="reg"):
        #准备参数
        data={"phone":phone,"imgVerifyCode":imgVerifyCode,"type":type}
        #发送请求
        response=session.post(url=self.getSmsCodeUrl,data=data)
        #返回数据
        return  response

        # 获取手机短信验证码
    def register(self, session, phone, password, verifycode='8888',phone_code='666666',dy_server='on',invite_phone='13800002222'):
            # 准备参数
            data = {
                "phone": phone,
                "password": password,
                 "verifycode": verifycode,
                "phone_code":phone_code,
                "dy_server":dy_server,
                "invite_phone":invite_phone
            }
            # 发送请求
            response = session.post(url=self.registerUrl, data=data)
            # 返回数据
            return response

    def Login(self,session,phone='14599768731',pwd='test123'):
        data={
            "keywords":phone,
            "password":pwd
        }
        response=session.post(url=self.loginUrl,data=data)
        return  response
