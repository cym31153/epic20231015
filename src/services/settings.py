# -*- coding: utf-8 -*-
# Time       : 2022/1/16 0:25
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import os
import random
import sys
import typing
from dataclasses import dataclass, field
from datetime import datetime
from os.path import join, dirname
from typing import Dict, Any, Optional

from services.utils import ToolBox

__all__ = [
    # ------------------------------
    # SETTINGS
    # ------------------------------
    "logger",
    "DIR_COOKIES",
    "DIR_USERS",
    "DIR_EXPLORER",
    "PATH_USR_COOKIES",
    "DIR_SCREENSHOT",
    "DIR_LOG",
    # ------------------------------
    # CONFIG
    # ------------------------------
    "EPIC_PASSWORD",
    "EPIC_EMAIL",
    "MESSAGE_PUSHER_SETTINGS",
    "PLAYER",
    "ACTIVE_PUSHERS",
    "ACTIVE_SERVERS",
    "SynergyTunnel",
]

"""
================================================ ʕ•ﻌ•ʔ ================================================
                                            (·▽·)欢迎嫖友入座
================================================ ʕ•ﻌ•ʔ ================================================
[√]核心配置 [※]边缘参数
"""
# ---------------------------------------------------
# [√]工程根目录定位
# ---------------------------------------------------
# 系统根目录
PROJECT_ROOT = dirname(dirname(__file__))
# 文件数据库目录
PROJECT_DATABASE = join(PROJECT_ROOT, "database")
# Cookie 工作目录
DIR_COOKIES = join(PROJECT_DATABASE, "cookies")
PATH_USR_COOKIES = join(DIR_COOKIES, "user_cookies.txt")
DIR_USERS = join(PROJECT_DATABASE, "users")
# FreeGame Mining Workspace
DIR_EXPLORER = join(PROJECT_DATABASE, "explorer")
# 服务日志目录
DIR_LOG = join(PROJECT_DATABASE, "logs")
DIR_SCREENSHOT = join(DIR_LOG, "screenshot")
# ---------------------------------------------------
# [√]服务器日志配置
# ---------------------------------------------------
logger = ToolBox.init_log(error=join(DIR_LOG, "error.log"), runtime=join(DIR_LOG, "runtime.log"))

# ---------------------------------------------------
# 路径补全
# ---------------------------------------------------
for _pending in [PROJECT_DATABASE, DIR_EXPLORER, DIR_COOKIES, DIR_USERS, DIR_LOG, DIR_SCREENSHOT]:
    os.makedirs(_pending, exist_ok=True)
"""
================================================== ʕ•ﻌ•ʔ ==================================================
                                  若您并非项目开发者 请勿修改以下变量的默认参数
================================================== ʕ•ﻌ•ʔ ==================================================

                                            Enjoy it -> ♂ main.py
"""


@dataclass
class MessagePusher:
    pushers: typing.Dict[str, str] = field(default_factory=dict)
    player: str = ""
    enable: bool = True

    # fmt:off
    CONVERTER = [
        "沫雯喂", "辰丽", "荪彦孜", "有坷唯", "郑姊祺", "弹蓶蓶", "王飛",
        "Makise Kurisu", "Rem", "Lacus Clyne", "Megumin", "Misaka Mikoto",
        "Yukino", "ゆずりは いのり", "Gokou Ruri", "がえん とおえ", "Yuuki Asuna",
    ]

    # fmt:on

    def __post_init__(self):
        self.player = (
                self.player
                or os.getenv("PLAYER", "")
                or f"{random.choice(self.CONVERTER)}({datetime.now().day})"
        )


@dataclass
class Config:
    epic_email: str = ""
    epic_password: str = ""
    message_pusher: MessagePusher = None
    config_yaml: typing.Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.message_pusher = self.message_pusher or MessagePusher()
        self.epic_email = (
                self.epic_email
                or os.getenv("EPIC_EMAIL")
        )
        self.epic_password = (
                self.epic_password
                or os.getenv("EPIC_PASSWORD")
        )


config_ = ToolBox.check_sample_yaml(
    path_output=join(dirname(dirname(__file__)), "config.yaml"),
    path_sample=join(dirname(dirname(__file__)), "config-sample.yaml"),
)
# --------------------------------
# [√] 账号信息
# --------------------------------
# 不建议在公有库上创建工作流运行项目，有仓库禁用风险
EPIC_EMAIL: Optional[str] = config_.get("EPΙC_EMAΙL") or config_.get("EPIC_EMAIL", "")
EPIC_PASSWORD: Optional[str] = config_.get("EPΙC_PASSWΟRD") or config_.get("EPIC_PASSWORD", "")
# --------------------------------
# [※] 消息推送配置
# --------------------------------
MESSAGE_PUSHER_SETTINGS: Optional[Dict[str, Any]] = config_.get("message_pusher_settings", {})
ENABLE_PUSHER = MESSAGE_PUSHER_SETTINGS.get("enable", False)
# Apprise Server 泛映射
PUSHER: Optional[Dict[str, Optional[str]]] = MESSAGE_PUSHER_SETTINGS.get("pusher", {})
# 匿名设置
PLAYER: Optional[str] = MESSAGE_PUSHER_SETTINGS.get("player", "")
# --------------------------------
# [※] 补全语法模板
# --------------------------------
if not EPIC_EMAIL:
    EPIC_EMAIL = os.getenv("EPΙC_EMAΙL") or os.getenv("EPIC_EMAIL", "")
if not EPIC_PASSWORD:
    EPIC_PASSWORD = os.getenv("EPΙC_PASSWΟRD") or os.getenv("EPIC_PASSWORD", "")

# feat: actions env
# 将平铺在配置文件中的非空 PUSHER_ 变量补充到 pusher 字典中
# 在 Actions 初始化阶段通过 echo 将 Secrets 写入到尚未创建的 config.yaml 中
for k_ in config_:
    if not config_[k_]:
        continue
    if k_.startswith("PUSHER_"):
        PUSHER[k_] = config_[k_]
    if k_.startswith("PLAYER"):
        PLAYER = config_[k_]
    if k_ == "ENABLE_PUSHER":
        ENABLE_PUSHER = True
MESSAGE_PUSHER_SETTINGS = {"player": PLAYER, "enable": ENABLE_PUSHER, "pusher": PUSHER}
try:
    for server in PUSHER:
        if not PUSHER[server]:
            PUSHER[server] = os.getenv(server, "")
except KeyError as e:
    print(f"[进程退出] 核心配置文件被篡改 error={e}")
    sys.exit()

# fmt:off
_CONVERTER = [
    "沫雯喂", "辰丽", "荪彦孜", "有坷唯", "郑姊祺", "弹蓶蓶", "王飛",
    "Makise Kurisu", "Rem", "Lacus Clyne", "Megumin", "Misaka Mikoto",
    "Yukino", "ゆずりは いのり", "Gokou Ruri", "がえん とおえ", "Yuuki Asuna",
]
# fmt:on
PLAYER = os.getenv("PLAYER", "") if not PLAYER else PLAYER
if PLAYER in ["", None]:
    PLAYER = f"{random.choice(_CONVERTER)}({datetime.now().day})"
# --------------------------------
# [√] 阻止缺省配置
# --------------------------------
if not all((EPIC_EMAIL, EPIC_PASSWORD)):
    print("[进程退出] 账号信息未配置或相关变量不合法")
    sys.exit()

# 检查激活的消息服务器
if not any(PUSHER.values()):
    MESSAGE_PUSHER_SETTINGS["enable"] = False
ACTIVE_PUSHERS = [_p[0] for _p in PUSHER.items() if _p[-1]]
ACTIVE_SERVERS = [_p[-1] for _p in PUSHER.items() if _p[-1]]

_0x1 = ["EPΙC_EMAΙL", "EPΙC_PASSWΟRD", "PLAYER"]
_0x1.extend(PUSHER)
for _k in _0x1:
    os.environ[_k] = "_0x1"


class SynergyTunnel:
    ARMOR = None
    _CHANNEL = {}

    LEAVES = []

    # 暂存任务促销
    url2name = {}

    @staticmethod
    def set_combat(k, v):
        SynergyTunnel._CHANNEL.update({k: v})

    @staticmethod
    def get_combat(k):
        return SynergyTunnel._CHANNEL.get(k)

    @staticmethod
    def is_convert() -> bool:
        return bool(SynergyTunnel.LEAVES)
