# -*- encoding=utf8 -*-
__author__ = "gaozhiwei"
__title__ = "《新仙魔九界》兼容测试脚本"
__desc__ = """
1.清除游戏数据
2.拉起游戏
3.快速登录
4.退出游戏
"""

from qamanage.public_api import *

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"preprocessing.air")  # 本地运行
# path = os.path.join(os.path.dirname(__file__), r"preprocessing.air")  # 云测平台运行

using(path)
from preprocessing import Preprocessing, Common


class Compatibility(Common):
    """
        兼容测试
    """

    # 初始化父类的unity poco对象
    def __init__(self):
        super().__init__()

    # 运行兼容性测试
    def run_all(self):
        super().update_handler()
        super().quick_login()
        # 处理实名认证弹窗
        try:
            self.poco(text="实名认证").wait_for_appearance(timeout=30)
            super().input_text("UIPNormalCertification", "WidgetInputRealName", "InputField", "高志炜")
            super().input_text("UIPNormalCertification", "WidgetInputIDCard", "InputField", "32068219970528713X")
            self.poco("btn_confirm").click(sleep_interval=10)
        except Exception as e:
            log(e, desc="当前界面未找到实名认证弹窗", snapshot=True)
        # 最后截张图
        log("兼容性测试结束", snapshot=True)


# 自动设置设备
auto_setup(__file__)

# 前置处理
pre = Preprocessing()
pre.common_pre()

# 快速登录
co = Compatibility()
co.run_all()

# 停止运行
pre.stop_app()
