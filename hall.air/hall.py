# -*- encoding=utf8 -*-
__author__ = "gaozhiwei"
__title__ = "《新仙魔九界》大厅测试脚本"
__desc__ = """
    大厅功能测试：
    1.设置昵称；
    2.公告；
    3.客服；
    4.设置；
    5.背包；
    6.技能；
    7.锻造；
    8.邮件；
    9.兑换码；
    10.兑换商城；
    11.vip转盘；
    
    跑云测时：
    1.需要把preprocessing.air文件夹放到hall.air目录下，与hall.py文件同层级
    2.需要把path注释掉一个
"""

import random
from qamanage.public_api import *

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"preprocessing.air")  # 本地运行
# path = os.path.join(os.path.dirname(__file__), r"preprocessing.air")  # 云测平台运行

using(path)
from preprocessing import Preprocessing, Common


class Hall(Common):
    """
        大厅冒烟测试
    """
    def __init__(self, position=None, account='gzwtest8'):
        super().__init__()
        self.position = position
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

    # 设置昵称
    def setup_nickname(self):
        # 用例列表
        case_list = [
            "微信123",
            "123456",
            "abcdef",
            "雨果1",
            "雨果未来雨果1"
        ]
        # 执行测试用例
        if self.poco(texture="lobby_info_modify_icon").exists() or self.poco(text="设置昵称").exists():
            try:
                self.poco(text="设置昵称").click()
                sleep(1)
                self.poco(texture="common_img_mark_bg2").click()
                sleep(1)
                for case in case_list:
                    super().input_text(popup_type="UIPSetNickname", offspring_type="InputField", child_type="", content=case)
                    super().confirm_button()
                    super().dialog_confirm()
                # 单独处理正确情况
                while True:
                    super().input_text(popup_type="UIPSetNickname", offspring_type="InputField", child_type="", content="远在天边"+str(random.randint(1000, 9999)))
                    super().confirm_button()
                    if self.poco(text="设置昵称成功").exists():
                        super().dialog_confirm()
                        break
                    else:
                        super().dialog_confirm()
            except Exception as e:
                log(e, desc="未找到'设置昵称'按钮", snapshot=True)
        else:
            log("帐号已设置过昵称", snapshot=True)

    # 公告
    def announcement(self):
        try:
            if self.poco("WidgetBtnAnnouncement").exists():
                self.poco("WidgetBtnAnnouncement").click()
            else:
                self.poco("UIPLobby").offspring("WidgetBtnAnnouncement").click()
            sleep(1)
            swipe((0.6 * self.position[0], 0.7 * self.position[1]), (0.6 * self.position[0], 0.35 * self.position[1]))
            sleep(2)
            # 关闭公告
            super().close_button()
        except Exception as e:
            log(e, desc="未找到'公告'按钮", snapshot=True)

    # 客服
    def service(self):
        try:
            if self.poco("WidgetBtnService").exists():
                self.poco("WidgetBtnService").click()
            else:
                self.poco("UIPLobby").offspring("WidgetBtnService").click()
            sleep(5)
            swipe((0.6 * self.position[0], 0.7 * self.position[1]), (0.6 * self.position[0], 0.35 * self.position[1]))
            sleep(2)
            # 点击返回
            touch(Template(r'back.png'))
            sleep(3)
            if self.poco("WidgetBtnService").exists():
                self.poco("WidgetBtnService").click()
            else:
                self.poco("UIPLobby").offspring("WidgetBtnService").click()
            sleep(5)
            # 点击“在线客服”
            touch(Template(r'online_service.png'))
            sleep(3)
            # 点击返回
            touch(Template(r'back.png'))
            sleep(3)
        except Exception as e:
            log(e, desc="未找到'客服'按钮", snapshot=True)

    # 设置
    def setting(self):
        try:
            if self.poco("WidgetBtnSetting").exists():
                self.poco("WidgetBtnSetting").click()
            else:
                self.poco(texture="lobby_top_btn_setting").click()
            sleep(1)
            # 设置背景音乐
            touch((0.657 * self.position[0], 0.385 * self.position[1]))
            sleep(1)
            # 设置游戏音效
            touch((0.66 * self.position[0], 0.47 * self.position[1]))
            sleep(1)
            # 关闭背景音乐
            touch((0.413 * self.position[0], 0.389 * self.position[1]))
            sleep(1)
            # 关闭游戏音效
            touch((0.413 * self.position[0], 0.469 * self.position[1]))
            sleep(1)
            # 点击画质
            if self.poco("UIPSetting").offspring("Quality").offspring("Foreground").exists():
                self.poco("UIPSetting").offspring("Quality").offspring("Foreground").click()
            else:
                self.poco("UIPSetting").offspring("Quality").offspring("Background").click()
            # 点击喜报
            if self.poco("UIPSetting").offspring("News").offspring("Foreground").exists():
                self.poco("UIPSetting").offspring("News").offspring("Foreground").click()
            else:
                self.poco("UIPSetting").offspring("News").offspring("Background").click()
            # 点击代理
            if self.poco("UIPSetting").offspring("Agency").offspring("Background").exists():
                self.poco("UIPSetting").offspring("Agency").offspring("Background").click()
            else:
                self.poco("UIPSetting").offspring("Agency").offspring("Foreground").click()
            # 点击用户服务协议
            if self.poco("btn_agreement").exists():
                self.poco("btn_agreement").click()
            else:
                self.poco("UIPSetting").offspring("btn_agreement").click()
            sleep(5)
            # 点击返回
            touch(Template(r'back.png'))
            sleep(1)
            # 点击隐私政策
            if self.poco("btn_privacy").exists():
                self.poco("btn_privacy").click()
            else:
                self.poco("UIPSetting").offspring("btn_privacy").click()
            sleep(5)
            # 点击返回
            touch(Template(r'back.png'))
            sleep(1)
            # 关闭设置
            super().close_button()
        except Exception as e:
            log(e, desc="未找到'设置'按钮", snapshot=True)

    # 兑换商城
    def exchange_mall(self):
        try:
            if self.poco("WidgetBtnExchangeMall").exists():
                self.poco("WidgetBtnExchangeMall").click()
            else:
                self.poco(texture="lobby_bottom_icon_exchange_mail").click()
            sleep(1)
            # 点击兑换勾玉
            if self.poco("btn_gouyu").exists():
                self.poco("btn_gouyu").click()
            else:
                self.poco("UIPExchangeMall").offspring("btn_gouyu").click()
            sleep(1)
            # 处理兑换弹窗
            if self.poco(text="您的奖券不足300张，无法兑换哦").exists():
                log("奖券不足", snapshot=True)
            elif self.poco(text="您是否消耗300张奖券，兑换500勾玉？").exists():
                log("可以兑换500勾玉", snapshot=True)
            else:
                pass
            # 点击确定
            super().dialog_confirm()
            # 处理兑换券充足或用户信息异常
            if self.poco(text="用户信息异常").exists():
                log("用户信息异常", snapshot=True)
                super().dialog_confirm()
            elif self.poco(text="恭喜，成功兑换500勾玉").exists():
                log("成功兑换勾玉", snapshot=True)
                super().dialog_confirm()
            else:
                pass
            # 点击兑换勾玉
            if self.poco("btn_stone").exists():
                self.poco("btn_stone").click()
            else:
                self.poco("UIPExchangeMall").offspring("btn_stone").click()
            sleep(1)
            # 处理兑换弹窗
            if self.poco(text="您的奖券不足300张，无法兑换哦").exists():
                log("奖券不足", snapshot=True)
            elif self.poco(text="您是否消耗300张奖券，兑换黄金灵石？").exists():
                log("可以兑换1灵石", snapshot=True)
            else:
                pass
            # 点击确定
            super().dialog_confirm()
            # 处理兑换券充足或用户信息异常
            if self.poco(text="用户信息异常").exists():
                log("用户信息异常", snapshot=True)
                super().dialog_confirm()
            elif self.poco(text="恭喜，成功兑换黄金灵石").exists():
                log("成功兑换灵石", snapshot=True)
                super().dialog_confirm()
            else:
                pass
            # 关闭兑换商城
            super().close_button()
        except Exception as e:
            log(e, desc="未找到'兑换商城'按钮", snapshot=True)

    # 兑换码
    def cdkey(self):
        case_list = [
            "",
            "adek2",
            "兑换码"
        ]
        try:
            if self.poco("WidgetBtnRedeemCode").exists():
                self.poco("WidgetBtnRedeemCode").click()
            else:
                self.poco(texture="lobby_bottom_icon_redeem_code").click()
            # 执行测试用例
            for case in case_list:
                super().input_text("UIPRedeemCode", "InputCode", "", case)
                super().confirm_button()
                super().dialog_confirm()
            # 关闭兑换码
            super().close_button()
        except Exception as e:
            log(e, desc="未找到'兑换码'按钮", snapshot=True)

    # 邮件
    def mail(self):
        try:
            # 点击邮箱按钮
            if self.poco("WidgetBtnMail").exists():
                self.poco("WidgetBtnMail").click()
            else:
                self.poco(texture="lobby_bottom_btn_mail").click()
            sleep(1)
            # 邮箱邮件情况
            if self.poco("txt_no_mail").exists() or self.poco("UIPMail").offspring("txt_no_mail").exists():
                log("邮箱没有邮件", snapshot=True)
                self.poco("btn_refresh").click()  # 刷新邮箱
                sleep(1)
                self.poco("btn_get_award").click()  # 一键领取
                sleep(1)
                if self.poco(texture="UIPShowAward_tex_title").exists():
                    super().receive()
            else:
                swipe((0.55 * self.position[0], 0.75 * self.position[1]), (0.55 * self.position[0], 0.35 * self.position[1]))
                sleep(1)
                self.poco("btn_get").click()
                sleep(1)
                super().receive()
                self.poco("btn_get_award").click()
                sleep(1)
                super().receive()
            # 关闭邮箱
            super().close_button()
        except Exception as e:
            log(e, desc="未找到'邮箱'按钮", snapshot=True)

    # 锻造
    def forge(self):
        if self.poco("WidgetBtnForge").exists() or self.poco("UIPLobby").offspring("WidgetBtnForge").child("img_icon").exists():
            self.poco("WidgetBtnForge").click()
            # 点击妖灵道符
            self.poco("red_icon").wait_for_appearance(timeout=10)
            self.poco("red_icon").click()
            sleep(1)
            # 判断铸造按钮
            if self.poco("btn_cast").exists() or self.poco(texture="weaponcast_text_zz").exists():
                self.poco("tog_use_need").click()  # 勾选原石精华
                sleep(1)
                self.poco("btn_cast").click()  # 点击铸造按钮
                sleep(5)
                if self.poco("UIPAlertDialog").offspring("txt_content").get_text() == "所需的铸造材料不足，无法为您铸造！\n铸造材料可以通过击败大妖获得！":
                    super().confirm_button()
                    log("锻造材料不足", snapshot=True)
                elif self.poco(text="勾玉数量不足").exists():
                    super().confirm_button()
                    log("勾玉数量不足", snapshot=True)
                elif self.poco("btn_confirm").exists():
                    super().confirm_button()
                    log("锻造失败", snapshot=True)
                else:
                    log("锻造成功", snapshot=True)
            else:
                log("已到达最高炮倍", snapshot=True)
            # 关闭妖灵道符锻造弹窗
            super().dialog_close()
            # 点击魔灵箭
            self.poco("green_icon").wait_for_appearance(timeout=10)
            self.poco("green_icon").click()
            sleep(1)
            # 判断升级按钮
            if self.poco("btn_upgrade").exists() or self.poco("UIPWeaponMachine").offspring("btn_upgrade").exists():
                self.poco("btn_upgrade").click()  # 点击升级按钮
                sleep(5)
                if self.poco(text="您的材料不足，无法对魔灵箭进行升级！").exists():
                    self.poco("btn_confirm").click()
                    sleep(1)
                    log("升级材料不足", snapshot=True)
                else:
                    sleep(1)
                    log("升级成功或失败", snapshot=True)
            else:
                log("已到达最高炮倍", snapshot=True)
            # 魔灵转换
            if self.poco("btn_switch").exists() or self.poco("UIPWeaponMachine").offspring("btn_switch").exists():
                self.poco("btn_switch").click()
                sleep(1)
                if self.poco(text="转化成功").exists():
                    super().dialog_confirm()
                    log("转化白金灵石成功", snapshot=True)
                else:
                    super().dialog_confirm()
                    log("魔灵不足，无法转化", snapshot=True)
            else:
                log("未找到'魔灵转换'按钮", snapshot=True)
            # 关闭魔灵箭升级弹窗；关闭锻造
            for i in range(2):
                super().close_button()
        else:
            log("炮倍不满足锻造按钮的出现", snapshot=True)

    # 技能
    def skill(self):
        skill_type_list = ["Auxiliary", "Specific", "Fighting"]
        try:
            self.poco("WidgetBtnSkill").wait_for_appearance(timeout=10)
            self.poco("WidgetBtnSkill").click()
            sleep(1)
            # 遍历技能
            for skill_type in skill_type_list:
                for skill in self.poco("UIPSkill").offspring(skill_type).child():
                    skill.click()
                    if self.poco("UIPSkillInfo").offspring("btn_close").exists():
                        self.poco("UIPSkillInfo").offspring("btn_close").click()
                    else:
                        log("技能未开放")
            # 单独处理元神
            self.poco("WidgetFightingSkill (4)").click()
            if self.poco("btn_activate").exists():
                self.poco("btn_activate").click()
                if self.poco(text="道具数量不足，无法激活元神").exists():
                    super().dialog_confirm()
                    if self.poco(texture="UIPSpiritGift_spirit_text").exists():
                        super().dialog_close()  # 关闭元神礼包弹窗
                else:
                    log("1.帐号宝鉴等级未达到开启元神，无法激活；2.成功激活元神", snapshot=True)
            else:
                log("1.帐号宝鉴等级未达到开启元神，无法激活；2.已激活元神", snapshot=True)
            super().dialog_close()  # 关闭元神技能详情弹窗
            # 单独处理雷鸣破
            self.poco("WidgetFightingSkill (5)").click()
            if self.poco("btn_activate").exists():
                self.poco("btn_activate").click()
                if self.poco(text="道具数量不足，无法激活雷鸣破").exists():
                    super().dialog_confirm()
                    if self.poco(texture="UIPThudnerGift_thunder_text").exists():
                        super().dialog_close()  # 关闭雷鸣破礼包弹窗
                else:
                    log("成功激活雷鸣破", snapshot=True)
            else:
                log("已激活雷鸣破", snapshot=True)
            super().dialog_close()  # 关闭雷鸣破技能详情弹窗
            # 关闭技能页面
            super().close_button()
        except Exception as e:
            log(e, desc="未找到'技能'按钮", snapshot=True)

    # 背包-安全中心
    def knapsack_security_center(self):
        # 用例列表
        pic_list = [
            r'modify_password.png',
            r'change_binding.png',
            r'secondary_password.png',
            r'trust_equipment.png'
        ]
        try:
            self.poco("WidgetBtnBag").wait_for_appearance(timeout=10)
            for pic in pic_list:
                self.poco("WidgetBtnBag").click()  # 点击背包按钮
                sleep(1)
                if self.poco("btn_sercurity_center").exists():
                    self.poco("btn_sercurity_center").click()  # 点击帐号安全中心
                else:
                    self.poco("UIPBag").offspring("btn_sercurity_center").click()
                sleep(1)
                # 滑动页面
                swipe((0.5 * self.position[0], 0.75 * self.position[1]), (0.5 * self.position[0], 0.45 * self.position[1]))
                sleep(1)
                if exists(Template(pic)):
                    touch(Template(pic))
                    sleep(1)
                    touch(Template(r'back.png'))
                    sleep(1)
                else:
                    log("该帐号未绑定信息", snapshot=True)
                    touch(Template(r'back.png'))
                    break
        except Exception as e:
            log(e, desc="未找到'背包'按钮", snapshot=True)
        sleep(2)

    # 背包-仓库
    def knapsack_storage(self):
        # 用例列表
        case_list = [
            ['10000000000', '妖灵不足'],
            ['200000000000', '妖灵不足'],
            ['0', '请求数据异常'],
            ['1234', '存取的妖灵不是100的整数倍'],
            ['1000', '存取成功']
        ]
        try:
            self.poco("WidgetBtnBag").wait_for_appearance(timeout=10)
            self.poco("WidgetBtnBag").click()
            sleep(2)
            # 点击仓库
            self.poco("btn_storage").wait_for_appearance(timeout=10)
            self.poco("btn_storage").click()
            sleep(1)
            self.poco("btn_save").click()  # 点击存取按钮
            sleep(1)
            super().input_text("SaveMoney", "input_password", "", "Dx123321")  # 输入二级密码
            sleep(1)
            super().input_text("SaveMoney", "input_save_money", "", "1000")  # 输入存入妖灵数
            sleep(1)
            self.poco(texture="store_text_cr").click()  # 点击存入
            sleep(1)
            if self.poco(text="VIP5及以上玩家才可操作仓库哦").exists():
                super().dialog_confirm()
                log("vip不足5级", snapshot=True)
            elif self.poco(text="本帐号已开启设备信任功能，请前往帐号安全中心信任当前设备才可使用仓库功能").exists():
                super().dialog_confirm()
                log("未开启信任设备", snapshot=True)
            else:
                if self.poco("btn_confirm").exists():
                    super().dialog_confirm()
                    log("请求数据失败，网络问题", snapshot=True)
                else:
                    log("存入妖灵成功", snapshot=True)
                # 单独处理输入错误二级密码
                self.poco("btn_save").click()
                sleep(1)
                super().input_text("SaveMoney", "input_password", "", "Dx123323")
                sleep(1)
                super().input_text("SaveMoney", "input_save_money", "", "1000")
                sleep(1)
                self.poco(texture="store_text_cr").click()
                sleep(1)
                super().dialog_confirm()
                log("二级密码错误", snapshot=True)
                # 存入测试
                for case in case_list:
                    if case[0] == '1000':
                        continue
                    self.poco("btn_save").click()
                    sleep(1)
                    super().input_text("SaveMoney", "input_password", "", "Dx123321")
                    sleep(1)
                    super().input_text("SaveMoney", "input_save_money", "", case[0])
                    sleep(1)
                    self.poco(texture="store_text_cr").click()
                    sleep(1)
                    log(case[1], snapshot=True)
                    if self.poco(text="妖灵数量必须是100的整数倍!").exists():
                        super().dialog_confirm()
                        super().dialog_close()
                    if self.poco(text="提示").exists():
                        super().dialog_confirm()
                # 取出测试
                for case in case_list:
                    if case[0] == '10000000000':
                        continue
                    self.poco("btn_save").click()
                    sleep(1)
                    super().input_text("SaveMoney", "input_password", "", "Dx123321")
                    sleep(1)
                    super().input_text("SaveMoney", "input_take_money", "", case[0])
                    sleep(1)
                    self.poco("btn_take").click()
                    sleep(1)
                    log(case[1], snapshot=True)
                    if self.poco(text="妖灵数量必须是100的整数倍!").exists():
                        super().dialog_confirm()
                        super().dialog_close()
                    if self.poco(text="提示").exists():
                        super().dialog_confirm()
            super().close_button()  # 关闭仓库
            super().close_button()  # 关闭背包
        except Exception as e:
            log(e, desc="未找到'背包'按钮", snapshot=True)

    # 背包-道具
    def knapsack_prop(self):
        self.poco("WidgetBtnBag").wait_for_appearance(timeout=10)
        self.poco("WidgetBtnBag").click()
        count = 0
        # 遍历背包中的道具
        for i in self.poco("UIPBag").offspring("Content").child():
            count += 1
            if count == 13:
                log("遍历结束", snapshot=True)
                break
                # swipe((0.65 * self.position[0], 0.7 * self.position[1]), (0.65 * self.position[0], 0.35 * self.position[1]))
            i.click()
            if self.poco("PropDetail").offspring("btn_close").exists():
                # 发送按钮
                if self.poco("btn_send").exists():
                    self.poco("btn_send").click()
                    if self.poco("txt_title").get_text() == "提示":
                        log("道具不满足数量条件", snapshot=True)
                        super().dialog_confirm()
                        continue
                    else:
                        super().input_text("GivePresent", "InputNickName", "", "凤凰火")
                        super().input_text("GivePresent", "input_password", "", "Dx123321")
                        super().confirm_button()
                        if self.poco(text="本帐号已开启设备信任功能，请前往帐号安全中心信任当前设备才可发送道具").exists():
                            log("本账号未开启信任设备", snapshot=True)
                        elif self.poco(text="请在帐号安全中心设置二级密码，才可使用发送功能哦").exists():
                            log("本账号未设置二级密码", snapshot=True)
                        else:
                            log("发送成功")
                        super().dialog_confirm()
                        continue
                # 分解按钮
                if self.poco("btn_decompose").exists():
                    self.poco("btn_decompose").click()
                    super().dialog_confirm()
                    if self.poco(text="已有道具数量不足，请重新登录后查看").exists():
                        log("道具不足，无法分解", snapshot=True)
                    else:
                        log("分解成功", snapshot=True)
                    super().dialog_confirm()
                    continue
                # 兑换按钮
                if self.poco("btn_exchange").exists():
                    self.poco("btn_exchange").click()
                    if self.poco("ExchangePage").offspring("btn_exchange").exists():
                        self.poco("ExchangePage").offspring("btn_exchange").click()
                    else:
                        log("未达到vip5", snapshot=True)
                        super().dialog_close()
                    super().dialog_confirm()
                    if self.poco(text="兑换成功").exists():
                        log("兑换成功", snapshot=True)
                    else:
                        log("兑换失败，勾玉不足", snapshot=True)
                    super().dialog_confirm()
                    super().dialog_close()
                    continue
                # 降级按钮
                if self.poco("btn_downgrade").exists():
                    self.poco("btn_downgrade").click()
                    super().dialog_confirm()
                    super().dialog_confirm()
                    log("降级成功", snapshot=True)
                    continue
                # 使用按钮
                if self.poco("btn_use").exists():
                    self.poco("btn_use").click()
                    super().dialog_confirm()
                    log("请在游戏内使用", snapshot=True)
                    continue
                # 装备按钮
                if self.poco("btn_equip").exists():
                    self.poco("btn_equip").click()
                    log("遍历结束", snapshot=True)
                    break
                super().dialog_close()
            else:
                log("遍历结束", snapshot=True)
                break
        super().close_button()

    # vip转盘
    def vip_turntable(self):
        # 点击大厅界面的vip转盘icon
        try:
            self.poco("WidgetBtnVipTurntable").wait_for_appearance(timeout=10)
            self.poco("WidgetBtnVipTurntable").click()
            # 等待转盘界面加载出来后，点击抽奖
            self.poco("btn_start").wait_for_appearance()
            self.poco("btn_start").click()
            # 弹出消耗妖灵提示，点击确定
            if self.poco("btn_confirm").exists() and self.poco("btn_cancel").exists():
                self.poco("txt_check_box").click()  # 勾选不在询问
                super().dialog_confirm()
                sleep(8)
                super().receive()
            elif self.poco(text="您今日VIP抽奖次数已用完，请明日再来").exists():
                super().dialog_confirm()
                log("抽奖次数已用完", snapshot=True)
            elif self.poco(text="您的妖灵不足").exists():
                super().dialog_confirm()
                log("妖灵不足", snapshot=True)
            elif self.poco(text="您的VIP等级不足，无法抽奖").exists():
                super().dialog_confirm()
                log("vip等级不足", snapshot=True)
            else:
                super().dialog_confirm()
            # 点击关闭vip转盘
            super().close_button()
        except Exception as e:
            log(e, desc="vip转盘入口不存在", snapshot=True)

    # 大厅界面-道友
    def guild(self):
        try:
            if self.poco("WidgetBtnGuild").exists():
                self.poco("WidgetBtnGuild").click()
            else:
                self.poco(texture="lobby_bottom_icon_guild").click()

        except Exception as e:
            log(e, "道友入口不存在")

    # 运行所有步骤
    def run_all(self):
        self.login()
        self.setup_nickname()
        self.announcement()
        self.service()
        self.setting()
        self.exchange_mall()
        self.cdkey()
        self.mail()
        self.forge()
        self.skill()
        self.knapsack_security_center()
        self.knapsack_storage()
        self.knapsack_prop()
        self.vip_turntable()
        log("测试结束", snapshot=True)


auto_setup(__file__)

# 初始化预处理操作对象
pre = Preprocessing()
pre.common_pre()

# 获取当前设备的分辨率和对应帐号
position = pre.get_position()
account = pre.get_account()

# 初始化大厅遍历操作对象
hall = Hall(position, account)
hall.run_all()

# 测试结束，杀进程
pre.stop_app()
