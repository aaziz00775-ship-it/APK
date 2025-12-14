[app]
title = Test App
package.name = testapp
package.domain = org.test

source.dir = .
source.include_exts = py
source.main = main.py

version = 0.1
requirements = python3==3.9.19,kivy==2.2.1

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = armeabi-v7a
android.skip_update = False
android.gradle_dependencies =

[buildozer]
log_level = 2
warn_on_root = 0
