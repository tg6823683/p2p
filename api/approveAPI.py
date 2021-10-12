import  app
class approveAPI():
    def __init__(self):
        self.approve_url = app.BASE_URL + '/member/realname/approverealname'
        self.getapprove_url = app.BASE_URL + '/member/member/getapprove'

    def approve(self,session,realname,cardId):
        data = {"realname":realname, "card_id":cardId}
        #filesi表示请求的数据类型为"Content-Type":"multipart/form-data
        response = session.post(self.approve_url,data=data,files={'x':'y'})
        return response

    def getApprove(self,session):
        response = session.post(self.getapprove_url)
        return response