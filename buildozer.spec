[app]
title = EKG Registration
package.name = ekgregistration
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.main = ekg_registration_kivy.py

version = 0.1
requirements = python3==3.9.10,kivy==2.1.0

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a
android.release = False

[buildozer]
log_level = 2
warn_on_root = 0
