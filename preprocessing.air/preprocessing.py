# -*- encoding=utf8 -*-
__author__ = "gaozhiwei"
__title__ = "《新仙魔九界》公共方法类"
__desc__ = """
    1.从拉起游戏到登录界面的处理类
    2.登录界面处理类
"""

import threading
import xlrd

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco
from qamanage.public_api import *

file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DeviceIndex.xls')


# 异常捕获装饰器
def exception_handler(desc, snapshot=True):
    def outer(func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                log(e, desc=desc, snapshot=snapshot)
        return inner
    return outer


class Preprocessing:
    """
        预处理:
            1.清理缓存
            2.拉起游戏
            3.隐私协议
            4.安卓权限
    """
    def __init__(self, package="com.shiyi.xxmjj"):
        self.pocoa = AndroidUiautomationPoco(use_airtest_input=True)
        self.package = package
        self.file_name = file_name

    # 转换excel为字典
    def excel_to_dict(self):
        data = xlrd.open_workbook(self.file_name)
        table = data.sheet_by_name('info')
        row_num = table.nrows  # 行数
        account_dict = {}
        for i in range(1, row_num):
            device_id = str(table.cell_value(i, 0))
            account = str(table.cell_value(i, 1))
            account_dict[device_id] = account
        return account_dict

    # 获取当前设备对应的测试帐号
    def get_account(self):
        account_dict = self.excel_to_dict()
        if self.pocoa.device.uuid in account_dict:
            dev = self.pocoa.device.uuid
            account = account_dict[dev]
            return account
        else:
            return "gzwtest157"

    # 获取当前设备的分辨率
    def get_position(self):
        return self.pocoa.get_screen_size()

    # 拉起应用
    def start_app(self):
        start_app(self.package)

    # 关闭应用
    def stop_app(self):
        stop_app(self.package)

    # 清理应用缓存
    def clear_app(self):
        clear_app(self.package)

    # 处理安卓权限弹框
    def auto_click_popup(self):
        auto_click_popup(self.pocoa, timeout=60)

    # 打开隐私协议和用户协议
    @staticmethod
    @exception_handler("未找到《隐私政策》和《用户协议》")
    def scan_privacy():
        pics = [r"privacy_agreement.png", r"user_agreement.png"]
        for pic in pics:
            if exists(Template(pic)):
                touch(Template(pic))
                sleep(5)
                if exists(Template(r"back.png")):
                    touch(Template(r"back.png"))
                    sleep(2)
                else:
                    keyevent("BACK")
                    sleep(2)

    # 拒绝隐私协议
    @staticmethod
    @exception_handler("未找到'拒绝'按钮")
    def click_disagreement():
        pics = [r"cancel.png", r"confirm.png"]
        # 开屏拒绝隐私协议，通过识别图像
        for pic in pics:
            wait(Template(r"disagree_privacy.png"))
            touch(Template(r"disagree_privacy.png"))
            sleep(2)
            wait(Template(pic))
            touch(Template(pic))  # 点击取消
            sleep(2)

    # 同意隐私协议
    @staticmethod
    @exception_handler("未找到'同意'按钮")
    def click_agreement():
        # 开屏隐私协议处理，通过识别图像
        wait(Template(r"consent_privacy.png"))
        touch(Template(r"consent_privacy.png"))
        sleep(2)

    # 常规测试预处理方法整合
    def common_pre(self):
        self.clear_app()
        self.start_app()
        self.click_agreement()
        self.auto_click_popup()
        sleep(3)

    # 隐私政策测试预处理方法整合
    def privacy_pre(self):
        self.clear_app()
        self.start_app()
        self.click_disagreement()
        self.start_app()
        self.scan_privacy()
        self.click_agreement()
        self.auto_click_popup()
        sleep(3)


class Common:
    """
        常用方法类
    """
    def __init__(self):
        self.poco = UnityPoco(action_interval=1.5)

    # 处理更新提示
    @exception_handler("未出现'更新'弹框")
    def update_handler(self):
        # self.poco("txt_title").wait_for_appearance(timeout=5)
        if self.poco("txt_title").exists():
            # 点击取消
            self.dialog_cancel()
        else:
            log("未打开更新")

    # 同意隐私权限
    @exception_handler("未找到'同意'按钮")
    def agree_privacy(self):
        self.poco(texture="start_up_privacy_bg").wait_for_appearance(timeout=10)  # 等待隐私政策和用户协议弹框出现
        # 点击同意
        if self.poco("btn_agree").exists():
            self.poco("btn_agree").click()
        elif self.poco("img_cloud_right").exists():
            self.poco("img_cloud_right").click()
        else:
            touch(Template(r"consent_privacy.png"))
        sleep(2)

    # 拒绝隐私权限
    @exception_handler("未找到'拒绝'按钮")
    def reject_privacy(self):
        self.poco(texture="start_up_privacy_bg").wait_for_appearance(timeout=10)  # 等待隐私政策和用户协议弹框出现
        # 点击拒绝
        if self.poco("btn_reject").exists():
            self.poco("btn_reject").click()
        elif self.poco("img_cloud_left").exists():
            self.poco("img_cloud_left").click()
        else:
            touch(Template(r"disagree_privacy.png"))
        sleep(2)

    # 快速开始游戏(游客登录)
    @exception_handler("未找到'开始游戏'按钮")
    def quick_login(self):
        self.poco("btn_exit").wait_for_appearance(timeout=300)  # 等待热更，到达登录界面
        # 点击快速登录
        if self.poco("btn_login").exists():
            self.poco("btn_login").click()
        elif self.poco("btn_fast").exists():
            self.poco("btn_fast").click()
        else:
            self.poco("img_btn").click()
        sleep(2)

    # 帐号登录
    @exception_handler("未找到'帐号登录'按钮")
    def account_login(self):
        self.poco("btn_exit").wait_for_appearance(timeout=300)  # 等待热更，到达登录界面
        # 点击帐号登录
        if self.poco("btn_account_login").exists():
            self.poco("btn_account_login").click()
        else:
            self.poco(texture="login_btn_nickname_login").click()
        sleep(2)

    # 切换帐号
    @exception_handler("未找到'切换'按钮")
    def switch_account(self):
        self.poco("btn_exit").wait_for_appearance(timeout=300)  # 等待热更，到达登录界面
        # 点击切换帐号
        if self.poco("btn_switch").exists():
            self.poco("btn_switch").click()
        elif self.poco("UIPLogin").offspring("btn_switch").exists():
            self.poco("UIPLogin").offspring("btn_switch").click()
        else:
            self.poco("Image").click()
        sleep(2)

    # 切换帐号-创建帐号
    @exception_handler("未找到'创建帐号'按钮")
    def switch_account_create(self):
        # 点击创建帐号
        if self.poco("btn_create").exists():
            self.poco("btn_create").click()
        else:
            self.poco("AccountSwitch").offspring("btn_create").click()
        sleep(2)

    # 创建按钮
    @exception_handler("未找到'创建'按钮")
    def create_button(self):
        if self.poco(texture="login_btn_create").exists():
            self.poco(texture="login_btn_create").click()
        else:
            self.poco("AccountCreate").offspring("btn_create").click()
        sleep(2)

    # 登录按钮
    @exception_handler("未找到'登录'按钮")
    def login_button(self):
        if self.poco(texture="login_btn_login").exists():
            self.poco(texture="login_btn_login").click()
        else:
            self.poco("AccountLogin").offspring("btn_login").click()
        sleep(2)

    # 确定按钮
    @exception_handler("未找到'确定'按钮")
    def confirm_button(self):
        # 点击确定按钮
        if self.poco("btn_confirm").exists():
            self.poco("btn_confirm").click()
        elif self.poco("AccountSwitch").offspring("btn_confirm").exists():
            self.poco("AccountSwitch").offspring("btn_confirm").click()  # 切换帐号界面的确定按钮
        elif self.poco("UIPSetNickname").offspring("btn_confirm").exists():
            self.poco("UIPSetNickname").offspring("btn_confirm").click()  # 设置昵称界面的确定按钮
        elif self.poco("UIPRedeemCode").offspring("btn_confirm").exists():
            self.poco("UIPRedeemCode").offspring("btn_confirm").click()  # 输入兑换码界面的确定按钮
        elif self.poco("GivePresent").offspring("btn_confirm").exists():
            self.poco("GivePresent").offspring("btn_confirm").click()  # 发送道具界面的确定按钮
        else:
            pass
        sleep(2)

    # 弹窗确定按钮
    @exception_handler("未找到弹窗上的'确定'按钮")
    def dialog_confirm(self):
        # 点击确定按钮
        if self.poco(texture="common_btn_confirm").exists():
            self.poco(texture="common_btn_confirm").click()
        elif self.poco("UIPAlertDialog").offspring("btn_confirm").exists():
            self.poco("UIPAlertDialog").offspring("btn_confirm").click()
        else:
            pass
        sleep(2)

    # 弹窗取消按钮
    @exception_handler("未找到'取消'按钮")
    def dialog_cancel(self):
        # 点击取消按钮
        if self.poco("btn_cancel").exists():
            self.poco("btn_cancel").click()
        elif self.poco("UIPAlertDialog").offspring("btn_cancel").exists():
            self.poco("UIPAlertDialog").offspring("btn_cancel").click()
        else:
            touch(Template(r"cancel.png"))
        sleep(2)

    # 关闭按钮
    @exception_handler("未找到'关闭'按钮")
    def close_button(self):
        if self.poco("btn_close").exists():
            self.poco("btn_close").click()  # 通用关闭按钮
        elif self.poco(texture="common_btn_close").exists():
            self.poco(texture="common_btn_close").click()
        elif self.poco("AccountSwitch").offspring("btn_close").exists():
            self.poco("AccountSwitch").offspring("btn_close").click()  # 切换帐号的关闭按钮
        elif self.poco("AccountLogin").offspring("btn_close").exists():
            self.poco("AccountLogin").offspring("btn_close").click()  # 帐号登录的关闭按钮
        elif self.poco("UIPNormalCertification").offspring("btn_close").exists():
            self.poco("UIPNormalCertification").offspring("btn_close").click()  # 实名认证的关闭按钮
        elif self.poco("UIPAnnouncement").offspring("btn_close").exists():
            self.poco("UIPAnnouncement").offspring("btn_close").click()  # 公告的关闭按钮
        elif self.poco("UIPSetting").offspring("btn_close").exists():
            self.poco("UIPSetting").offspring("btn_close").click()  # 设置的关闭按钮
        elif self.poco("UIPExchangeMall").offspring("btn_close").exists():
            self.poco("UIPExchangeMall").offspring("btn_close").click()  # 兑换商城的关闭按钮
        elif self.poco("UIPMail").offspring("btn_close").exists():
            self.poco("UIPMail").offspring("btn_close").click()  # 邮箱的关闭按钮
        elif self.poco("UIPWeaponLobby").offspring("btn_close").exists():
            self.poco("UIPWeaponLobby").offspring("btn_close").click()  # 锻造的关闭按钮
        else:
            pass
        sleep(2)

    # 弹窗关闭按钮(从最里层的关闭按钮开始判断)
    @exception_handler("未找到弹窗上的'关闭'按钮")
    def dialog_close(self):
        if self.poco("AccountSwitch").offspring("btn_close").exists():
            self.poco("AccountSwitch").offspring("btn_close").click()  # 创建帐号弹窗的关闭按钮
        elif self.poco("UIPInfullMode").offspring("btn_close").exists():
            self.poco("UIPInfullMode").offspring("btn_close").click()  # 支付弹窗的关闭按钮
        elif self.poco("UIPSpiritGift").offspring("btn_close").exists():
            self.poco("UIPSpiritGift").offspring("btn_close").click()  # 元神礼包弹窗的关闭按钮
        elif self.poco("UIPThunderGift").offspring("btn_close").exists():
            self.poco("UIPThunderGift").offspring("btn_close").click()  # 雷鸣破礼包弹窗的关闭按钮
        elif self.poco("UIPSkillInfo").offspring("btn_close").exists():
            self.poco("UIPSkillInfo").offspring("btn_close").click()  # 技能详情弹窗的关闭按钮
        elif self.poco("UIPWeaponCast").offspring("btn_close").exists():
            self.poco("UIPWeaponCast").offspring("btn_close").click()  # 妖灵道符弹窗的关闭按钮
        elif self.poco("SaveMoney").offspring("btn_close").exists():
            self.poco("SaveMoney").offspring("btn_close").click()  # 仓库存取弹窗的关闭按钮
        elif self.poco("PropDetail").offspring("btn_close").exists():
            self.poco("PropDetail").offspring("btn_close").click()  # 道具弹窗的关闭按钮
        elif self.poco("ExchangePage").offspring("btn_close").exists():
            self.poco("ExchangePage").offspring("btn_close").click()  # 兑换号角弹窗的关闭按钮
        elif self.poco("UIPVIPAward").offspring("UIWBtnClose").exists():
            self.poco("UIPVIPAward").offspring("UIWBtnClose").click()  # vip专属宝箱的关闭按钮
        elif self.poco("UIPGameCallBoss").offspring("btn_close").exists():
            self.poco("UIPGameCallBoss").offspring("btn_close").click()  # BOSS记录的关闭按钮
        elif self.poco("UIPGameCallBoss").child("Base").child("btn_close").exists():
            self.poco("UIPGameCallBoss").child("Base").child("btn_close").click()  # 帮助的关闭按钮
        else:
            pass
        sleep(2)

    # 通用输入框
    @exception_handler("未找到输入框")
    def input_text(self, popup_type, offspring_type, child_type, content):
        if child_type == "":
            self.poco(popup_type).offspring(offspring_type).set_text(content)
        else:
            self.poco(popup_type).offspring(offspring_type).child(child_type).set_text(content)
        log("输入了'{}'".format(content), snapshot=True)
        sleep(1)

    # 大厅内，退出登录
    @exception_handler("返回按钮不存在")
    def exit_game(self):
        if self.poco("WidgetBtnLogout").exists():
            self.poco("WidgetBtnLogout").click()
        else:
            self.poco(texture="lobby_top_btn_logout").click()
        sleep(1)
        if self.poco(text="是否重新登录？").exists():
            self.poco("btn_confirm").click()
        elif self.poco(text="您还没进行过游戏，是否立即进入游戏？").exists():
            self.poco("btn_cancel").click()
        else:
            log("提示不存在")
        sleep(5)

    # 处理首次登录到大厅的各种弹窗
    def first_login_popup(self):
        # 处理每日赠送的妖灵弹框
        if self.poco("UIPAlertDialog").offspring("txt_content").exists() and self.poco("UIPAlertDialog").offspring("txt_content").get_text()[0:7] == "恭喜你，获得了":
            self.poco("btn_confirm").click()
        else:
            log("没有赠送妖灵的提示弹框")
        sleep(1)

        # 处理每次登录时活动页面强弹
        if self.poco(texture="common_btn_close").exists():
            self.poco(texture="common_btn_close").click()
        else:
            log("没有活动需要强弹")
        sleep(1)

        # 处理首次登录大厅的每日转盘
        if self.poco("img_btn_start").exists():
            self.poco("img_btn_start").click()
            self.poco("btn_get_award").wait_for_appearance(timeout=15)  # 抽奖后，等待领取奖励
            self.poco("btn_get_award").click()
        else:
            log("已经抽过每日转盘奖励")
        sleep(1)

        # 处理每次登录时弹出各种礼包弹窗
        while self.poco(texture="common_btn_close").exists() is True:
            self.poco(texture="common_btn_close").click()
        sleep(2)

    # 通用“恭喜获得弹框”上的“立即领取”
    @exception_handler("未找到'立即领取'按钮")
    def receive(self):
        self.poco(texture="UIPShowAward_tex_title").wait_for_appearance(timeout=30)
        if self.poco("btn_get_award").exists():
            self.poco("btn_get_award").click()
        else:
            self.poco("UIPShowAward").offspring("btn_get_award").click()
        sleep(2)


# class ServerAlertHandler(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.poco = UnityPoco(action_interval=1.5)
#
#     def run(self):
#         while True:
#             try:
#                 if self.poco("UIPAlertDialog").offspring("txt_content").exists() and self.poco("UIPAlertDialog").offspring("txt_content").get_text()[0:6] == "获取数据失败":
#                     self.poco("btn_confirm").click()
#                 elif self.poco(text="无法连接服务器,请检测您的网络").exists():
#                     self.poco("btn_confirm").click()
#                 else:
#                     pass
#             except Exception as e:
#                 sleep(1)


if __name__ == "__main__":
    print("预处理操作和常用操作")
