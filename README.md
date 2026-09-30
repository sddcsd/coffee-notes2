# 咖啡小记

一个记录咖啡豆、手冲方案和口感的手机应用。

用 Capacitor 打包成 Android APK，由 GitHub Actions 自动构建。

## 目录说明

| 路径 | 说明 |
|---|---|
| `www/index.html` | **整个 app**（HTML + CSS + JS 全在这一个文件里） |
| `capacitor.config.json` | 打包配置（appId、桌面应用名、web 目录） |
| `package.json` | 依赖声明 |
| `.github/workflows/` | GitHub 自动构建脚本 |
| `android-build.gradle.template` | 原生构建脚本模板（引导时用一次） |
| `prepare_android.py` | 引导脚本（引导时用一次） |
| `android/` | 原生工程（由引导工作流生成后提交） |

## 怎么出 APK

见 `小白操作手册.md`。
