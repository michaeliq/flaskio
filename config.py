import os

secret_key = "abhjlk-hkljhadja_adjkhakdhlakd_akdhlkahl"
PWD = os.path.abspath(os.curdir)

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///message_app.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False