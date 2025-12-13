[app]
title = EKG Registration
package.name = ekgregistration
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.main = ekg_registration_kivy.py

version = 0.1

# ИСПРАВЛЕНО: убираем точные версии, используем совместимые
requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_path = 
android.sdk_path = 
android.accept_sdk_license = True
android.arch = armeabi-v7a
android.release = False

[buildozer]
log_level = 2
warn_on_root = 0
