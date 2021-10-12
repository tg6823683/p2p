#初始化日志配置
    #2、设置日志级别
    #3、创建控制台日志处理器和文件日志处理器
    #4、设置日志格式，创建格式化器
    #fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    #5、将格式化器设置到日志器中
    #6、将日志处理器添加到日志对象
import json
import  logging

import requests,pymysql,app
from bs4 import BeautifulSoup
from  logging import handlers

def init_logger():
    logger=logging.getLogger()  #初始化日志对象
    logger.setLevel(logging.INFO) #设置日志级别，只有比它级别高的可以打印(包括自己)
    sh = logging.StreamHandler() #创建控制台日志处理器
    #创建文件日志处理器
    filename = app.BASE_DIR + "/log/p2p.log"
    fh = handlers.TimedRotatingFileHandler(filename, when='M', interval=3, backupCount=5, encoding='utf-8')
    #设置日志格式，创建格式化器
    fmt = '%(asctime)s , %(levelname)s , %(filename)s %(funcName)s line %(lineno)s , %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S %a'
    formatter = logging.Formatter(fmt=fmt,datefmt=datefmt)
    #将格式化器设置到日志器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    #将日志处理器添加到日志对象
    logger.addHandler(sh)
    logger.addHandler(fh)

# 测试日志代码
# init_logger()
# logging.info("asasas")
# logging.debug("bug")
# logging.warning('warn')


#封装响应断言的方法
def assert_utils(self,response,status_code,status,description):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get('status'))
    self.assertEqual(description, response.json().get('description'))


#利用beautifulSoup解析html或者xml方法
def request_third_api(form_data):
    # 解析form表单中的内容，并提取第三方请求的参数
    soup = BeautifulSoup(form_data, "html.parser") #html.parser html数据解析器
    third_url = soup.form['action'] #获取form标签的action属性
    logging.info("third request url = {}".format(third_url))
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value']) #往字典里加数据  获取input标签的属性name和value的值
    logging.info("third request data = {}".format(data))
    # 发送第三方请求
    response = requests.post(third_url, data=data) #拼接成字典发送数据
    return response

#操作数据库。自动化时候做数据的清理
class DButils:
    @classmethod
    def get_conn(cls,db_name):
        conn = pymysql.connect(app.DB_URL,app.DB_USERNAME,app.DB_PASSWORD,db_name,autocommit=True)
        return conn

    @classmethod
    def close(cls,cursor=None,conn=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls,db_name,sql):
        try:
            conn = cls.get_conn(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor,conn)

#从文件中获取图片验证数据，完成参数话的改造
def read_imgverify_data(file_name):
    file=app.BASE_DIR+"/data/"+file_name
    test_case_data=[]
    with open(file,encoding="utf-8") as f:
        verify_data=json.load(f) #将json格式的字符串转换为字典
        test_data_list=verify_data.get('test_get_img_verify_code')
        for test_data in test_data_list:
            test_case_data.append((test_data.get('type'),test_data.get('status_code')))
        print('json data={}'.format(test_case_data))
        return  test_case_data

#注册信息测参数化
def read_register_data(file_name):
    #注册的测试数据的文件路径
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file,encoding="utf-8") as f:
        #将json的数据格式，转化为字典的数据格式
        register_data = json.load(f)
        #获取所有的测试数据的列表
        test_data_list = register_data.get("test_register")
        #依次读取测试数据列表中的每一条数据，并进行相应字段的提取
        for test_data in test_data_list:
            test_case_data.append((test_data.get("phone"),test_data.get("pwd"),test_data.get("imgVerifyCode"),test_data.get("phoneCode"),test_data.get("dyServer"),test_data.get("invite_phone"),test_data.get("status_code"),test_data.get("status"),test_data.get("description")))
        print("test_case_data = {}".format(test_data_list))
    return test_case_data


#以上俩方法存在大量的重复代码，观察后其实还可以封装为下面的方法
#定义统一的读取所有参数数据文件的方法
def read_param_data(filename,method_name,param_names):
    #filename： 参数数据文件的文件名
    #method_name: 参数数据文件中定义的测试数据列表的名称，如：test_get_img_verify_code
    #param_names: 参数数据文件一组测试数据中所有的参数组成的字符串，如："type,status_code"

    #获取测试数据文件的文件路径
    file = app.BASE_DIR + "/data/" + filename
    test_case_data = []
    with open(file,encoding="utf-8") as f:
        #将json字符串转换为字典格式
        file_data = json.load(f)
        #获取所有的测试数据的列表
        test_data_list = file_data.get(method_name)
        for test_data in test_data_list:
            #先将test_data对应的一组测试数据，全部读取出来，并生成一个列表
            test_params = []
            for param in param_names.split(","):
                #依次获取同一组测试数中每个参数的值，添加到test_params中，形成一个列表
                test_params.append(test_data.get(param))
            #每完成一组测试数据的读取，就添加到test_case_data后，直到所有的测试数据读取完毕
            test_case_data.append(test_params)
    print("test_case_data = {}".format(test_case_data))
    return test_case_data