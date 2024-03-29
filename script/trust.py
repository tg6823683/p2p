import random
import  unittest,logging,requests
from  api.LoginAPI import LoginAPI
from api.trustAPI import trustAPI
from bs4 import BeautifulSoup

import  utils


class trust(unittest.TestCase):
    def setUp(self):
        self.login_api = LoginAPI()
        self.trust_api = trustAPI()
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

        # 开户请求

    def test01_trust_request(self):
        # 1、认证通过的账号登录
        response = self.login_api.Login(self.session)
        logging.info("login response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        # 2、 发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info("trust register response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 3、 发送第三方的开户请求
        form_data = response.json().get("description").get("form")
        logging.info('form response={}'.format(form_data))
        # 调用第三方接口的请求方法
        response = utils.request_third_api(form_data)
        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual('UserRegister OK', response.text)

    def test02_trust_get_verifycode_sucess(self):
        response = self.login_api.Login(self.session)
        logging.info("login response = {}".format(response.json()))
        utils.assert_utils(self, response, 200, 200, "登录成功")
        r=random.randint(1,99999999)
        response=self.trust_api.get_recharge_verify_code(self.session,str(r))
        self.assertEqual(200, response.status_code)


    #......"成功·获取注册图片验证码  随机小数 ....

        # 充值成功
    def test03_recharge(self):
            # 1、登录成功
            # 1、认证通过的账号登录
            response = self.login_api.Login(self.session)
            logging.info("login response = {}".format(response.json()))
            utils.assert_utils(self, response, 200, 200, "登录成功")
            # 2、 获取充值验证码
            r = random.random()
            response = self.trust_api.get_recharge_verify_code(self.session, str(r))
            logging.info("get recharge verify code reponse = {}".format(response.status_code))
            self.assertEqual(200, response.status_code)
            # 3、 发送充值请求
            response = self.trust_api.recharge(self.session, '10000')
            logging.info("recharge response = {}".format(response.json()))
            self.assertEqual(200, response.status_code)
            self.assertEqual(200, response.json().get("status"))
            # 4、 发送第三方充值请求
            # 获取响应中form表单的数据，并提取为后续第三方请求的参数
            form_data = response.json().get("description").get("form")
            logging.info('form response={}'.format(form_data))
            # 调用第三方请求的接口
            response = utils.request_third_api(form_data)
            logging.info('third recharge response={}'.format(form_data))
            # 断言response是否正确
            self.assertEqual('NetSave OK', response.text)

