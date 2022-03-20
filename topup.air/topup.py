# -*- encoding=utf8 -*-
__author__ = "gaozhiwei"
__title__ = "《新仙魔九界》充值计费点测试脚本"
__desc__ = """
    充值计费点相关功能测试：
    1.首充特惠礼包；
    2.特惠礼包；
    3.vip特权；
    4.周卡特权；
    5.元神礼包；
    6.雷鸣破礼包；
    7.商城
    
    跑云测时：
    1.需要把preprocessing.air文件夹放到topup.air目录下，与topup.py文件同层级
    2.需要把path注释掉一个
"""

from qamanage.public_api import *

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"preprocessing.air")  # 本地运行
# path = os.path.join(os.path.dirname(__file__), r"preprocessing.air")  # 云测平台运行

using(path)
from preprocessing import Preprocessing, Common


class Topup(Common):
    """
        针对仙魔充值计费点的功能测试
    """

    # 初始化父类的unity poco对象
    def __init__(self, position=None, account='gzwtest101'):
        super().__init__()
        self.account = account
        self.position = position

    # 处理支付宝支付
    def alipay_handler(self):
        # 点击支付宝支付
        self.poco("Alipay").click()
        sleep(5)
        keyevent("BACK")
        sleep(2)
        # 处理提示弹窗
        super().dialog_confirm()

    # 处理微信支付
    def wechat_handler(self):
        # 点击微信支付
        self.poco("WeChat").click()
        sleep(5)
        keyevent("BACK")
        sleep(2)
        # 处理提示弹窗
        super().dialog_confirm()

    # 登录游戏
    def login(self):
        super().update_handler()
        super().account_login()
        super().input_text("AccountLogin", "WidgetInputAccount", "InputField", self.account)  # 输入帐号
        sleep(1)
        super().input_text("AccountLogin", "WidgetInputPassword", "InputField", "gzw123")  # 输入密码
        sleep(1)
        super().login_button()
        super().first_login_popup()

    # 首充特惠
    def first_recharge(self):
        case_list = [
            'btn_buy_red',
            'btn_buy_green'
        ]
        # 点击大厅界面的“首充特惠”icon
        if self.poco("WidgetBtnFirstRechargeGift").exists():
            self.poco("WidgetBtnFirstRechargeGift").click()
            sleep(2)
            # 断言计费点
            assert_equal(self.poco(case_list[0]).child().get_text(), "12", "12元计费点")
            assert_equal(self.poco(case_list[1]).child().get_text(), "28", "28元计费点")
            sleep(2)
            for case in case_list:
                # 点击计费点
                self.poco(case).click()
                sleep(2)
                # 微信支付
                self.wechat_handler()
                # 再次点击计费点
                self.poco(case).click()
                # 支付宝支付
                self.alipay_handler()
            super().close_button()
        else:
            log("已经购买过首充特惠礼包", snapshot=True)

    # 特惠礼包
    def special_gift(self):
        # 计费点字典
        price_point = {
            "WidgetLevel1": "12y",
            "WidgetLevel2": "28y",
            "WidgetLevel3": "50y",
            "WidgetLevel4": "108y",
            "WidgetLevel5": "328y",
            "WidgetLevel6": "648y"
        }

        # 断言特惠礼包中的数值
        if self.poco("WidgetBtnSpecialGift").exists():
            self.poco("WidgetBtnSpecialGift").click()
            for i in price_point:
                if self.poco("UIPSpecialGift").offspring(i).offspring("txt_price").exists():
                    result = self.poco("UIPSpecialGift").offspring(i).offspring("txt_price").get_text()
                    assert_equal(result, price_point[i], price_point[i] + "特惠礼包")
                    log(result, price_point[i])
                    self.poco("UIPSpecialGift").offspring(i).click()
                    sleep(1)
                    # 点击购买
                    self.poco("UIPSpecialGift").offspring("Buy").click()
                    # 微信支付
                    self.wechat_handler()
                    # 再次点击计费点
                    self.poco("UIPSpecialGift").offspring("Buy").click()
                    # 支付宝支付
                    self.alipay_handler()
                else:
                    log(price_point[i]+" 计费点已经购买过")
            super().close_button()
        else:
            log("该帐号已经购买过所有特惠礼包")

    # vip特权
    def vip(self):
        # 点击大厅界面的VIP特权icon
        try:
            self.poco("WidgetBtnVip").wait_for_appearance(timeout=10)
            self.poco("WidgetBtnVip").click()
            # 先统一回到vip1页面
            while self.poco("btn_go_left").exists():
                self.poco("btn_go_left").click()
                sleep(1)
            # 从vip1页面开始遍历
            for i in range(8):
                # 滑动vip特权详情
                swipe((0.7 * self.position[0], 0.5 * self.position[1]), (0.7 * self.position[0], 0.3 * self.position[1]))
                # 点击免费宝箱
                if self.poco(texture="vip_btn_click_icon").exists():
                    self.poco(texture="vip_btn_click_icon").click()
                    # 点击立即开启
                    self.poco("img_btn_open").click()
                    sleep(2)
                    # 如果vip等级没达到，则无法开启
                    if self.poco("btn_confirm").exists():
                        # 点击确定
                        super().dialog_confirm()
                        # 点击关闭
                        super().dialog_close()
                    else:
                        # 领取奖励
                        super().receive()
                else:
                    log("已经开启过免费宝箱")
                # 点击购买vip礼包
                if self.poco("BtnGroupNotBuy").exists():
                    self.poco("BtnGroupNotBuy").click()
                    # 如果vip等级没达到，则无法购买
                    if self.poco("btn_confirm").exists():
                        super().dialog_confirm()
                    else:
                        # 关闭支付方式弹窗
                        super().close_button()
                else:
                    log("已经购买过该等级的vip礼包或该vip等级没有礼包可购买")

                # 点击到下一个vip页面
                if self.self.poco("btn_go_right").exists():
                    self.poco("btn_go_right").click()
                    sleep(1)
                else:
                    break
            # 点击充值按钮
            if self.poco("btn_charge_upgrade").exists():
                self.poco("btn_charge_upgrade").click()
                # 关闭各种弹窗
                while self.poco(texture="common_btn_close").exists() is True:
                    self.poco(texture="common_btn_close").click()
            else:
                log("充值按钮不存在，关闭vip页面")
                self.poco("btn_close").click()
        except Exception as e:
            log(e, desc="vip特权入口不存在", snapshot=True)

    # 周卡特权
    def weekly_card(self):
        # 点击大厅界面的周卡icon
        if self.poco("WidgetBtnWeeklyCard").exists():
            self.poco("WidgetBtnWeeklyCard").click()
            sleep(1)
            # 点击去充值
            self.poco("btn_go_charge").click()
            self.wechat_handler()
            # 再次点击计费点
            self.poco("btn_go_charge").click()
            self.alipay_handler()
            sleep(2)
            # 关闭周卡礼包
            super().close_button()
        else:
            log("周卡礼包按钮不存在")

    # 大厅界面-商城
    def store(self):
        price_point = ['12', '28', '50', '108', '328', '648']  # 计费点列表
        real_price = []  # 声明一个空列表，用于存储通过poco获取的计费点

        # 点击商城icon或者妖灵“+”
        if self.poco("WidgetBtnStore").exists():
            self.poco("WidgetBtnStore").click()
        elif self.poco("UIPLobby").offspring("Gold").child("btn_add").exists():
            self.poco("UIPLobby").offspring("Gold").child("btn_add").click()
        else:
            log("未找到商城icon")
        # 关掉出现商城页面前的所有弹窗
        while self.poco("TabBtnGold").exists() is False and self.poco(texture="common_btn_close").exists() is True:
            self.poco(texture="common_btn_close").click()

        # 断言妖灵计费点
        for i in self.poco("UIPInfull").offspring("Content").child("WidgetGoods(Clone)"):
            real_price.append(i.offspring("txt_price").get_text())
        for i in range(6):
            assert_equal(real_price[i].split("￥")[1], price_point[i], price_point[i] + "元妖灵计费点")
        real_price.clear()

        # 点击商城中的勾玉tab
        if self.poco("TabBtnDiamond").exists():
            self.poco("TabBtnDiamond").click()
        else:
            log("勾玉充值入口不存在")

        # 断言勾玉计费点
        for i in self.poco("UIPInfull").offspring("Content").child("WidgetGoods(Clone)"):
            real_price.append(i.offspring("txt_price").get_text())
        for i in range(5):
            assert_equal(real_price[i].split("￥")[1], price_point[i], price_point[i] + "元勾玉计费点")
        real_price.clear()

        # 点击商城界面的“充值特权”
        if self.poco("btn_vip").exists():
            self.poco("btn_vip").click()
            self.poco("UIPVip").offspring("btn_close").wait_for_appearance()  # 等待“充值特权”关闭按钮出现
            self.poco("UIPVip").offspring("btn_close").click()  # 点击关闭
        else:
            log("商城界面-充值特权入口不存在")

        # 点击关闭商城
        super().close_button()

    # 大厅界面-元神礼包
    def spirit_gift(self):
        if self.poco("WidgetBtnSpiritGift").exists():
            self.poco("WidgetBtnSpiritGift").click()
            try:
                self.poco("UIPSpiritGift").offspring("btn_buy").click()
                self.wechat_handler()
                self.poco("UIPSpiritGift").offspring("btn_buy").click()
                self.alipay_handler()
            except Exception as e:
                log(e, desc="未找到购买按钮", snapshot=True)
            super().dialog_close()
        else:
            log("1.已开启元神，元神礼包不显示；2.妖灵宝鉴未达到3级")

    # 大厅界面-雷鸣破礼包
    def thunder_gift(self):
        if self.poco("WidgetBtnThunderGift").exists():
            self.poco("WidgetBtnThunderGift").click()
            try:
                self.poco("UIPThunderGift").offspring("btn_buy").click()
                self.wechat_handler()
                self.poco("UIPThunderGift").offspring("btn_buy").click()
                self.alipay_handler()
            except Exception as e:
                log(e, desc="未找到购买按钮", snapshot=True)
            super().dialog_close()
        else:
            log("已开启雷鸣破，雷鸣破礼包不显示")

    # 运行所有步骤
    def run_all(self):
        self.login()
        self.first_recharge()
        self.special_gift()
        self.vip()
        self.weekly_card()
        self.spirit_gift()
        self.thunder_gift()


auto_setup(__file__)

# 初始化预处理对象
pre = Preprocessing()
pre.common_pre()

# 获取当前设备的分辨率，以及对应帐号
position = pre.get_position()
account = pre.get_account()

# 初始化充值遍历操作对象
t = Topup(position, account)
t.run_all()

# 测试结束，杀进程
pre.stop_app()
