# -*- encoding=utf8 -*-
__author__ = "gaozhiwei"
__title__ = "《新仙魔九界》实名认证+注册登录"
__desc__ = """
1.快速游戏 & 注册帐号
2.实名认证
3.新手引导
"""

import random
from qamanage.public_api import *

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"preprocessing.air")  # 本地运行
# path = os.path.join(os.path.dirname(__file__), r"preprocessing.air")  # 云测平台运行

using(path)
from preprocessing import Preprocessing, Common


class Login(Common):
    """
        注册登录
        实名认证
    """
    def __init__(self):
        super().__init__()

    # 快速登录+实名认证+新手引导(杀进程)
    def quick_login_certification(self):
        super().update_handler()
        super().quick_login()
        self.certification_test()
        self.novice_guide_abnormal()

    # 注册帐号+实名认证+新手引导（正常）
    def create_account_certification(self):
        self.create_account_test()
        self.certification_test()
        self.novice_guide_normal()

    # 实名认证测试
    def certification_test(self):
        # 用例列表
        case_list = [
            ["", ""],
            ["高志炜", ""],
            ["", "32068219970528713X"],
            ["高志伟", "32068219970528713X"],
            ["高志炜", "320682199705287134"],
            ["高志炜", "32068219970528713x"]
        ]
        # 等待实名认证弹窗出现
        self.poco(text="实名认证").wait_for_appearance(timeout=10)
        # 执行测试用例
        for case in case_list:
            super().input_text("UIPNormalCertification", "WidgetInputRealName", "InputField", case[0])
            super().input_text("UIPNormalCertification", "WidgetInputIDCard", "InputField", case[1])
            super().confirm_button()
            if case[0] == "高志炜" and case[1] == "32068219970528713x":
                pass
            else:
                super().dialog_confirm()

    # 新手引导（正常）测试
    def novice_guide_normal(self):
        self.poco("img_role_npc").wait_for_appearance(timeout=20)  # 等待运行到新手引导
        sleep(5)

        # 点击进行对话
        try:
            if self.poco("img_next").exists():
                for i in range(3):
                    self.poco("img_next").click()
                    sleep(10)
            else:
                for i in range(3):
                    self.poco("UIPGuideDialog").offspring("img_next").click()
                    sleep(10)
        except Exception as e:
            log(e, "未找到'继续'按钮", snapshot=True)

        # 点击攻击按钮
        try:
            self.poco("XSYDUIPBattle").offspring("btn_attack").wait_for_appearance(timeout=5)
            self.poco("XSYDUIPBattle").offspring("btn_attack").click(sleep_interval=10)
        except Exception as e:
            log(e, desc="攻击按钮不存在", snapshot=True)

        # 继续对话
        self.poco("img_next").wait_for_appearance(timeout=10)
        self.poco("img_next").click(sleep_interval=5)

        # 点击元神
        try:
            self.poco("XSYDUIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[0].offspring(
                "img_skill").wait_for_appearance(timeout=5)
            self.poco("XSYDUIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[0].offspring(
                "img_skill").click(sleep_interval=45)
        except Exception as e:
            log(e, desc="元神按钮不存在", snapshot=True)

        # 继续对话
        self.poco("img_next").wait_for_appearance(timeout=10)
        self.poco("img_next").click(sleep_interval=5)

        # 点击万剑诀
        try:
            self.poco("XSYDUIPBattle").offspring("MiddleSkill").offspring("img_skill").wait_for_appearance(timeout=5)
            self.poco("XSYDUIPBattle").offspring("MiddleSkill").offspring("img_skill").click(sleep_interval=10)
        except Exception as e:
            log(e, desc="万剑诀按钮不存在", snapshot=True)

        # 点击蛇珠
        try:
            self.poco("XSYDUIPGuideClick").offspring("WidgetBoxCard (0)(Clone)").offspring(
                "img_bg").wait_for_appearance(timeout=10)
            self.poco("XSYDUIPGuideClick").offspring("WidgetBoxCard (0)(Clone)").offspring("img_bg").click(
                sleep_interval=40)
        except Exception as e:
            log(e, desc="蛇珠无法点击", snapshot=True)

        # 激活宝鉴
        try:
            if self.poco("btn_activation").exists():
                self.poco("btn_activation").click(sleep_interval=6)
            else:
                self.poco("UIPArtifactActivation").offspring("btn_activation").click(sleep_interval=6)
        except Exception as e:
            log(e, desc="激活宝鉴按钮无法点击", snapshot=True)

        # 继续对话
        self.poco("img_next").wait_for_appearance(timeout=10)
        self.poco("img_next").click(sleep_interval=10)

        # 点击任务栏，跟随引导
        self.poco("UIPBattle").offspring("txt_main_desc").wait_for_appearance(timeout=10)
        try:
            self.poco("UIPBattle").offspring("txt_main_desc").click()
        except Exception as e:
            log(e, desc="无法点击任务栏", snapshot=True)

        # 点击攻击键，暂停攻击
        try:
            if self.poco("img_attack_icon").exists():
                self.poco("img_attack_icon").click()
            else:
                self.poco("UIPBattle").offspring("img_attack_icon").click()
        except Exception as e:
            log(e, desc="未找到攻击键，可能被击杀背景图覆盖", snapshot=True)

        # 点击更多
        try:
            if self.poco(texture="game_right_btn_more").exists():
                self.poco(texture="game_right_btn_more").click()
            else:
                self.poco("UIPBattle").offspring("Normal").click()
        except Exception as e:
            log(e, desc="未找到'更多'按钮", snapshot=True)

        # 点击返回大厅
        try:
            if self.poco(texture="game_sidebar_btn_back").exists():
                self.poco(texture="game_sidebar_btn_back").click()
            else:
                self.poco("UIPBattle").offspring("Sidebar").offspring("WidgetBtnBack").offspring("Normal").click()
        except Exception as e:
            log(e, desc="未找到'返回'按钮", snapshot=True)

        # 点击提示上的确定
        super().dialog_confirm()
        sleep(2)
        # 处理每日登陆弹窗
        super().first_login_popup()
        # 点击返回到登录界面
        super().exit_game()

    # 新手引导（杀进程）
    def novice_guide_abnormal(self):
        self.poco("img_role_npc").wait_for_appearance(timeout=20)  # 等待运行到新手引导
        sleep(5)

    # 注册帐号测试
    def create_account_test(self):
        # 用例列表
        case_list = [
            [" ", "", ""],
            [",", "", ""],
            ["测试", "", ""],
            ["aaaaaaa", "", ""],
            ["1111111", "", ""],
            ["a1a1a1a1a1a1a1a", "", ""],
            ["12345678", "", ""],
            ["abcdefgh", "", ""],
            ["g7418523", "", ""],
            ["g7418523", " ", ""],
            ["g7418523", ",", ""],
            ["g7418523", "aaaaa", ""],
            ["g7418523", "11111", ""],
            ["g7418523", "abcdefghijk", ""],
            ["g7418523", "12345678901", ""],
            ["g7418523", "abcdef", ""],
            ["g7418523", "123456", ""],
            ["g7418523", "gzw123", ""],
            ["g7418523", "gzw123", " "],
            ["g7418523", "gzw123", "gzw321"]
        ]
        # 点击切换帐号
        super().switch_account()
        if self.poco(texture="start_up_privacy_bg").exists():
            super().agree_privacy()
        # 点击创建帐号按钮
        super().switch_account_create()
        # 关闭创建帐号
        super().close_button()
        # 再次点击创建帐号
        super().switch_account_create()
        # 执行测试用例
        for case in case_list:
            super().input_text("AccountCreate", "WidgetInputAccount", "InputField", case[0])
            super().input_text("AccountCreate", "WidgetInputPassword1", "InputField", case[1])
            super().input_text("AccountCreate", "WidgetInputPassword2", "InputField", case[2])
            super().create_button()
            super().dialog_confirm()
        # 单独处理成功创建
        while True:
            super().input_text("AccountCreate", "WidgetInputAccount", "InputField", "xmgzw"+str(random.randint(100, 1000)))
            super().input_text("AccountCreate", "WidgetInputPassword1", "InputField", "gzw123")
            super().input_text("AccountCreate", "WidgetInputPassword2", "InputField", "gzw123")
            super().create_button()
            if self.poco(text="实名认证").exists() or self.poco("UIPNormalCertification").child("Background").offspring("txt_title").exists():
                break
            else:
                super().dialog_confirm()

    # 帐号登录测试
    def account_login_test(self):
        # 用例列表
        case_list = [
            ["", ""],
            ["zvkaw2113", ""],
            ["gzwtest70", "gzw1997"],
            ["zvkaw2113", "gzw123"],
            ["gzwtest70", "gzw123"]
        ]
        # 点击帐号登录
        super().account_login()
        if self.poco(texture="start_up_privacy_bg").exists():
            super().agree_privacy()
        # 关闭登录弹窗
        super().close_button()
        # 再次点击帐号登录
        super().account_login()
        if self.poco(texture="start_up_privacy_bg").exists():
            super().agree_privacy()
        # 执行测试用例
        for case in case_list:
            super().input_text("AccountLogin", "WidgetInputAccount", "InputField", case[0])
            super().input_text("AccountLogin", "WidgetInputPassword", "InputField", case[1])
            super().login_button()
            if case[0] == "gzwtest70" and case[1] == "gzw123":
                pass
            else:
                super().dialog_confirm()
        # 处理各种弹窗
        super().first_login_popup()
        # 返回到大厅
        super().exit_game()

    # 删除帐号测试，需要在快速登录测试跟帐号登录测试步骤之后调用
    def delete_account(self):
        # 点击切换帐号
        super().switch_account()
        if self.poco(texture="start_up_privacy_bg").exists():
            super().agree_privacy()
        # 先登录一个帐号
        super().confirm_button()
        # 处理弹窗
        super().first_login_popup()
        # 退出返回到登录
        super().exit_game()
        # 点击切换帐号
        super().switch_account()
        if self.poco(texture="start_up_privacy_bg").exists():
            super().agree_privacy()
        # 删除一个帐号
        if self.poco("AccountSwitch").offspring("gzwtest23").child("btn_delete").exists():
            self.poco("AccountSwitch").offspring("gzwtest70").child("btn_delete").click()
        else:
            self.poco("AccountSwitch").offspring().child("btn_delete").click()


# 自动设置设备
auto_setup(__file__)

# 初始化预处理操作
pre = Preprocessing()
pre.common_pre()

# 进行快速登录，实名认证，新手引导杀进程测试
l1 = Login()
l1.quick_login_certification()
pre.stop_app()
pre.start_app()
sleep(10)

# 登录上次的游客帐号
l2 = Login()
l2.update_handler()
l2.quick_login()
l2.first_login_popup()
l2.exit_game()

# 进行创建账号，实名认证，常规新手引导测试，登录测试
l2.create_account_certification()
l2.account_login_test()
l2.delete_account()
log("测试结束", snapshot=True)
pre.stop_app()
