import logging
import unittest
import random
import requests
from api.LoginAPI import LoginAPI
import utils
import  time
from parameterized  import  parameterized

class Login(unittest.TestCase):
    phone = '13799768731'
    phone2 = '13038799031'
    phone3 = '13998768639'
    phone4 = '13569768699'
    phone5 = '16799968639'
    imgVerifyCode = '8888'
    phoneCode = '666666'
    pwd = 'test123'

    def setUp(self):
        self.loginApi = LoginAPI()
        self.session = requests.session()

    def tearDown(self):
        self.session.close()

    #获取图片验证码参数化写法1
    # @parameterized.expand(utils.read_imgverify_data("imgVerify.json"))
    # def test01_get_img_verify_code(self, type, status_code):
    #     # 根据不同的type类型准备不同的参数数据
    #     r = ''
    #     if type == 'float':
    #         r = str(random.random())
    #     elif type == 'int':
    #         r = str(random.randint(10000000, 90000000))
    #     # 发送请求
    #     response = self.loginApi.getImgCode(self.session, r)
    #     logging.info("r = {} response = {}".format(r, response))
    #     # 对响应结果进行断言
    #     self.assertEqual(status_code, response.status_code)

    #获取图片验证码参数化写法2
    @parameterized.expand(utils.read_param_data("imgVerify.json","test_get_img_verify_code","type,status_code"))
    def test01_get_img_verify_code(self, type, status_code):
            # 根据不同的type类型准备不同的参数数据
            r = ''
            if type == 'float':
                r = str(random.random())
            elif type == 'int':
                r = str(random.randint(10000000, 90000000))
            # 发送请求
            response = self.loginApi.getImgCode(self.session, r)
            logging.info("r = {} response = {}".format(r, response))
            # 对响应结果进行断言
            self.assertEqual(status_code, response.status_code)


        # 获取短线验证码参数都正确

    def test04_getSmsCode_Success(self):
        # 先调用下获取图片验证码的接口
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, self.phone, self.imgVerifyCode)
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "短信发送成功")  # 封装为方法
        # self.assertEqual(200, response.status_code)
        # self.assertEqual(200, response.json().get('status'))
        # self.assertEqual("短信发送成功", response.json().get('description'))

    # 图片验证码错误
    def test05_getSmsCode_wrong_imgCode(self):
        # 先调用下获取图片验证码的接口
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        error_img_code = "8899"
        response = self.loginApi.getSmsCode(self.session, self.phone, error_img_code)
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "图片验证码错误")  # 封装为方法

    # 图片验证码为空
    def test06_getSmsCode_null_imgCode(self):
        # 先调用下获取图片验证码的接口
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, self.phone, "")
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "图片验证码错误")  # 封装为方法

    # 手机号码为空
    def test07_getSmsCode_null_telNum(self):
        # 先调用下获取图片验证码的接口
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, '', self.imgVerifyCode)
        logging.info("sms ge response={}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get('status'))
        # 获取短线验证码参数都正确

    # 未获取图片验证码
    def test08_getSmsCode_Fail(self):
        response = self.loginApi.getSmsCode(self.session, self.phone, self.imgVerifyCode)
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "图片验证码错误")  # 封装为方法

    #注册的参数化写法1
    # @parameterized.expand(utils.read_register_data('register.json'))
    # def test09_resister(self,phone,pwd,imgVerifyCode,phoneCode,dyServer,invite_phone,status_code,status,description):
    #     # 获取图片验证码
    #     r = random.random()
    #     response = self.loginApi.getImgCode(self.session, str(r))
    #     self.assertEqual(200, response.status_code)
    #     # 获取手机验证码
    #     response = self.loginApi.getSmsCode(self.session, phone, self.imgVerifyCode)
    #     logging.info("sms ge response={}".format(response.json()))
    #     utils.assert_utils(self, response, 200, 200, "短信发送成功")  # 封装为方法
    #     # 注册
    #     response = self.loginApi.register(self.session, phone, pwd, imgVerifyCode,phoneCode,dyServer,invite_phone)
    #     logging.info("sms ge response={}".format(response.json()))
    #     utils.assert_utils(self, response, status_code, status, description)  # 封装为方法

    # 注册的参数化写法2
    @parameterized.expand(utils.read_param_data("register.json", "test_register","phone,pwd,imgVerifyCode,phoneCode,dyServer,invite_phone,status_code,status,description"))
    def test09_resister(self,phone,pwd,imgVerifyCode,phoneCode,dyServer,invite_phone,status_code,status,description):
        # 获取图片验证码
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取手机验证码
        response = self.loginApi.getSmsCode(self.session, phone, self.imgVerifyCode)
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "短信发送成功")  # 封装为方法
        # 注册
        response = self.loginApi.register(self.session, phone, pwd, imgVerifyCode,phoneCode,dyServer,invite_phone)
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, status_code, status, description)  # 封装为方法



    #登录成功
    def test16_Login_Sucess(self):
            # 获取图片验证码
            response=self.loginApi.Login(self.session)
            logging.info("sms ge response={}".format(response.json()))
            utils.assert_utils(self, response, 200, 200, "登录成功")

    # 用户不存在
    def test17_Login_userError_fail(self):
        # 获取图片验证码
        response = self.loginApi.Login(self.session,phone='13800002226')
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200,100, "用户不存在")

    # 密码为空
    def test18_Login_pwdNull_fail(self):
        response = self.loginApi.Login(self.session,pwd='')
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200,100, "密码不能为空")

        # 密码连续错误的状态
    def test19_Login_pwdError_fail(self):
        response = self.loginApi.Login(self.session, pwd='error')
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")

        response = self.loginApi.Login(self.session, pwd='error')
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")

        response = self.loginApi.Login(self.session, pwd='error')
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        response = self.loginApi.Login(self.session)
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        time.sleep(60)

        response = self.loginApi.Login(self.session)
        logging.info("sms ge response={}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
