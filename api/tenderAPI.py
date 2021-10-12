import app

class tenderAPI():
    def __init__(self):
        self.get_loaninfo_url = app.BASE_URL + "/common/loan/loaninfo"  #投资产品详情
        self.tender_url = app.BASE_URL + "/trust/trust/tender"  #请求后台投资
        self.tenderlist_url = app.BASE_URL + "/loan/tender/mytenderlist"  #查看投资列表

    # 投资产品详情
    def get_loaninfo(self,session,tender_id):
        data = {"id": tender_id}
        response = session.post(self.get_loaninfo_url,data=data)
        return response

    # 请求后台投资
    def tender(self,session,tender_id,amount):
        data = {"id": tender_id, "amount": amount,"depositCertificate":"-1"}
        response = session.post(self.tender_url,data=data)
        return response

    # 查看投资列表
    def get_tenderlist(self,session,status):
        data = {"status": status}
        response = session.post(self.tenderlist_url,data=data)
        return response