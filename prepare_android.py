#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prepare_android.py —— 引导阶段使用

把 android-build.gradle.template 里的占位符替换掉，写入
android/app/build.gradle，并把桌面应用名改对。

用法（在仓库根目录）：
    python3 prepare_android.py
"""
import io
import json
import os
import re
import sys

TPL = 'android-build.gradle.template'
TARGET = 'android/app/build.gradle'
STRINGS = 'android/app/src/main/res/values/strings.xml'
PLACEHOLDER = 'APP_ID_PLACEHOLDER'

# 桌面图标名。app 内部显示名是用户可自定义的（设置 → 应用名称），
# 两者是独立的两件事，不要互相覆盖。
LAUNCHER_NAME = '咖啡小记'


def main():
    if not os.path.exists(TPL):
        print('缺少 %s，请先把它放到仓库根目录' % TPL)
        return 1
    if not os.path.exists(TARGET):
        print('找不到 %s，请先执行 npx cap add android' % TARGET)
        return 1

    cfg = {}
    if os.path.exists('capacitor.config.json'):
        # 用 utf-8-sig 读取：Windows 上编辑器常给 JSON 加上 BOM
        cfg = json.load(io.open('capacitor.config.json', encoding='utf-8-sig'))
    app_id = cfg.get('appId') or 'com.coffee.notes'
    # 桌面图标名固定用 LAUNCHER_NAME，不要用 appName。
    # appName 是「默认显示名」，只在用户没有自定义时生效；
    # 用户可以在 app 设置里自定义界面显示名（settings.appName），
    # 那个值存在用户数据里，与桌面名无关。
    launcher_name = LAUNCHER_NAME

    tpl = io.open(TPL, encoding='utf-8').read()
    out = tpl.replace(PLACEHOLDER, app_id)

    # 自检
    if PLACEHOLDER in out:
        print('appId 占位符替换失败')
        return 2
    if 'signingConfigs' not in out:
        print('模板缺少 signingConfigs 段')
        return 2
    if 'versionCode' not in out:
        print('模板缺少 versionCode')
        return 2

    io.open(TARGET, 'w', encoding='utf-8', newline='').write(out)
    print('已写入 %s' % TARGET)
    print('  applicationId = %s' % app_id)

    if os.path.exists(STRINGS):
        s = io.open(STRINGS, encoding='utf-8').read()
        s = re.sub(r'<string name="app_name">[^<]*</string>',
                   '<string name="app_name">%s</string>' % launcher_name, s)
        s = re.sub(r'<string name="title_activity_main">[^<]*</string>',
                   '<string name="title_activity_main">%s</string>' % launcher_name, s)
        io.open(STRINGS, 'w', encoding='utf-8', newline='').write(s)
        print('  桌面应用名(launcher) = %s' % launcher_name)
        print('  注意：app 内显示名由用户在设置里自定义，与此无关')
    else:
        print('警告：找不到 %s' % STRINGS)

    print('自检通过')
    return 0


if __name__ == '__main__':
    sys.exit(main())
