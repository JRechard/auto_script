# -*- encoding=utf8 -*-
__author__ = "gaozhiwei"
__title__ = "《新仙魔九界》游戏房间测试脚本"
__desc__ = """
    房间功能测试：
    1.
    
    跑云测时：
    1.需要把preprocessing.air文件夹放到room.air目录下，与room.py文件同层级
    2.需要把本地运行path注释掉
"""
from qamanage.public_api import *

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"preprocessing.air")  # 本地运行
# path = os.path.join(os.path.dirname(__file__), r"preprocessing.air")  # 云测平台运行
using(path)
from preprocessing import Preprocessing, Common


class Room(Common):
    """
        仙魔房间遍历
    """
    def __init__(self, account='gzwtest21'):
        super().__init__()
        self.account = account

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

    # 打开房间列表
    def game_entrance(self):
        self.poco("Normal").wait_for_appearance(timeout=5)
        self.poco("Normal").click()

    # 选择进入房间
    def enter_room(self):
        # 点击进入房间
        try:
            self.poco(texture="select_room_btn_qzy").wait_for_appearance(timeout=10)
            self.poco("LobbyCamera").click()
        except Exception as e:
            log(e, desc="房间入口不存在", snapshot=True)

    # 元神技能
    def skill_spirit(self):
        try:
            self.poco("img_attack_icon").wait_for_appearance()
            self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[0].click()  # 点击元神icon
            if self.poco("UIPAlertDialog").offspring("txt_content").exists():  # 未解3级宝鉴的情况
                super().dialog_confirm()
                log("该帐号未解锁宝鉴等级到3级")
            elif self.poco("UIPSkillInfo").offspring("txt_name").exists():  # 未激活元神的情况
                self.poco("btn_activate").click()
                sleep(2)
                if self.poco("UIPAlertDialog").offspring("txt_content").get_text() == "道具数量不足，无法激活元神":
                    super().dialog_confirm()
                    super().dialog_close()
                    super().close_button()
                log("激活元神成功/失败")
            else:
                log("元神已装备/卸下")
        except Exception as e:
            log(e, desc="未找到元神技能icon", snapshot=True)

    # 号角技能
    def skill_horn(self):
        try:
            self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[1].click()  # 点击号角icon
            self.poco("btn_boss_record").click()  # 点击Boss记录
            super().dialog_close()
            self.poco("btn_help").click()  # 点击帮助
            super().dialog_close()
            # 点击哪吒
            if self.poco("哪吒").exists():
                self.poco("哪吒").click()
            else:
                self.poco(texture="call_texture_m_090").click()
            super().dialog_close()
            # 点击神灯召唤
            self.poco("UIPGameCallBoss").offspring("哪吒").child("btn_call_lamp").click()
            if self.poco("txt_content").get_text() == "哪吒召唤将于妖灵宝鉴等级达到17级后开启\nV7用户可直升解锁":
                super().dialog_confirm()
                super().close_button()
                log("未满足召唤条件，关闭界面")
            elif self.poco("txt_content").get_text() == "您的神灯数量不足，是否使用200勾玉立即兑换100个神灯并召唤？":
                super().dialog_cancel()
                self.poco("UIPGameCallBoss").offspring("哪吒").child("btn_call_lamp").click()
                super().dialog_confirm()
                if self.poco("txt_content").exists():
                    super().dialog_confirm()
                    log("当前有BOSS在场，无法召唤")
                else:
                    log("兑换成功，直接召唤BOSS")
            elif self.poco("txt_content").get_text() == "神灯数量不足，无法召唤":
                super().dialog_confirm()
                super().close_button()
                log("神灯数量不足，无法召唤，关闭界面")
            else:
                if self.poco("txt_content").exists() and  self.poco("txt_content").get_text() == "当前有Boss在场，使用失败":
                    super().dialog_confirm()
                    log("当前有BOSS在场，无法召唤")
                else:
                    log("满足召唤条件，直接召唤BOSS")

            # 选择号角召唤
            sleep(3)
            self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[1].click()  # 点击号角icon
            self.poco("UIPGameCallBoss").offspring("哪吒").child("btn_call_horn").click()
            if self.poco("txt_content").get_text() == "您当前没有足够的号角，击败妖王BOSS有几率掉落哦":
                super().dialog_confirm()
                super().close_button()
                log("号角数量不足，无法召唤，关闭界面")
            elif self.poco("txt_content").get_text() == "哪吒召唤将于妖灵宝鉴等级达到17级后开启\nV7用户可直升解锁":
                super().dialog_confirm()
                super().close_button()
                log("未满足召唤条件，关闭界面")
            else:
                if self.poco("txt_content").exists() and self.poco("txt_content").get_text() == "当前有BOSS在场，请稍后再召唤BOSS":
                    super().dialog_confirm()
                    log("当前有BOSS在场，无法召唤")
                else:
                    log("满足召唤条件，直接召唤BOSS")
        except Exception as e:
            log(e, desc="未找到号角技能icon", snapshot=True)

    # 神灯技能
    def skill_lamp(self):
        try:
            self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[2].click()
            if self.poco("UIPGameLampCallBoss").offspring("Bosses").child("WidgetBoss(Clone)")[9].exists():
                self.poco("UIPGameLampCallBoss").offspring("Bosses").child("WidgetBoss(Clone)")[9].click()
                if self.poco("tog_check_box").exists():
                    super().dialog_cancel()
                    self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[2].click()
                    self.poco("UIPGameLampCallBoss").offspring("Bosses").child("WidgetBoss(Clone)")[9].click()
                    self.poco("tog_check_box").click()
                    super().dialog_confirm()
        except Exception as e:
            log(e, desc="未找到神灯技能icon", snapshot=True)

    # 灵石技能
    def skill_stone(self):
        try:
            self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[3].click()
            if self.poco("WidgetWarhead").exists():
                self.poco("WidgetWarhead").click()
                if self.poco("txt_content").exists() and self.poco("txt_content").get_text() == "道具数量不足":
                    super().dialog_confirm()
                else:
                    self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[3].click()
            if self.poco("WidgetWarhead (1)").exists():
                self.poco("WidgetWarhead (1)").click()
                if self.poco("txt_content").exists() and self.poco("txt_content").get_text() == "道具数量不足":
                    super().dialog_confirm()
                else:
                    self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[3].click()
            if self.poco("WidgetWarhead (2)").exists():
                self.poco("WidgetWarhead (2)").click()
                if self.poco("txt_content").exists() and self.poco("txt_content").get_text() == "道具数量不足":
                    super().dialog_confirm()
                else:
                    self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[3].click()
            if self.poco("WidgetWarhead (3)").exists():
                self.poco("WidgetWarhead (3)").click()
                if self.poco("txt_content").exists() and self.poco("txt_content").get_text() == "道具数量不足":
                    super().dialog_confirm()
                else:
                    self.poco("UIPBattle").offspring("LeftSkill").child("WidgetSkillBtn(Clone)")[3].click()
            if self.poco("WidgetWarhead (4)").exists():
                self.poco("WidgetWarhead (4)").click()
                if self.poco("txt_content").exists() and self.poco("txt_content").get_text() == "道具数量不足":
                    super().dialog_confirm()
        except Exception as e:
            log(e, desc="未找到灵石技能icon", snapshot=True)


auto_setup(__file__)
r = Room()
r.skill_stone()
