# -*- encoding=utf8 -*-
__author__ = "gaozhiwei"
__title__ = "《新仙魔九界》隐私政策自动化测试脚本"
__desc__ = """
    隐私政策功能测试
    
    跑云测时
    1.需要把preprocessing.air文件夹放到privacy.air目录下，与privacy.py文件同层级
    2.需要把path注释掉一个
"""

from qamanage.public_api import *

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"preprocessing.air")  # 本地运行
# path = os.path.join(os.path.dirname(__file__), r"preprocessing.air")  # 云测平台运行

using(path)
from preprocessing import Preprocessing, Common


class Privacy(Common):
    """
        针对隐私政策的功能测试
    """

    # 初始化父类的unity poco对象
    def __init__(self):
        super().__init__()

    # 处理登录时的隐私权限
    def login_privacy(self):
        super().account_login()
        super().reject_privacy()
        super().account_login()
        super().agree_privacy()
        # 输入帐号密码后，点击登录
        super().input_text("AccountLogin", "WidgetInputAccount", "InputField", "gzwtest40")
        super().input_text("AccountLogin", "WidgetInputPassword", "InputField", "gzw123")
        super().login_button()
        super().first_login_popup()
        super().exit_game()

    # 处理切换帐号时的隐私权限
    def switch_privacy(self):
        super().switch_account()
        super().reject_privacy()
        super().switch_account()
        super().agree_privacy()
        super().confirm_button()
        super().exit_game()

    # 处理切换帐号后，再点击帐号登录的隐私权限
    def switch_login_privacy(self):
        super().switch_account()
        super().agree_privacy()
        super().close_button()
        super().account_login()
        super().close_button()
        super().quick_login()

    # 运行所有测试步骤
    def run_all(self):
        super().update_handler()
        super().quick_login()
        super().close_button()
        self.login_privacy()
        self.switch_privacy()
        self.switch_login_privacy()
        log("测试结束", snapshot=True)


# 自动设置设备
auto_setup(__file__)

# 初始化预处理对象
pre = Preprocessing()
pre.privacy_pre()

# 初始化privacy对象
privacy = Privacy()
# 运行隐私政策功能测试用例
privacy.run_all()

# 用例执行结束，关闭游戏
pre.stop_app()
