import os
import re
import sys

try:
    from django.core.management.color import color_style
except:
    sys.stdout.write('Please install django!')
    sys.exit(1)
from .utils import Base
from .mixins import CreateModelMixin, CreateViewMixin


class Dj(Base, CreateModelMixin, CreateViewMixin):
    def __init__(self):
        self.args = sys.argv
        self.args_len = len(self.args)
        self.basedir = os.getcwd()
        self.sub_command = 'help'
        self.commands = ['model', 'view']
        self.files_modified = []
        color = color_style()
        self.notice = color.NOTICE
        self.error = color.ERROR
        self.warn = color.WARNING
        self.success = color.SUCCESS

    def identify_arguments(self):
        if self.args_len == 2:
            # if first argument not of c or create
            self.check_func_arg(self.args[1])
            self.show_help()
        if self.args_len == 3:
            # if second argument not of view or model
            self.check_mv_arg(self.args[2])
            # show help for specific command
            self.sub_command = self.args[2]
            self.show_help()

        self.settings_path = self.get_settings_path()
        self.installed_apps = self.get_installed_apps()
        self.func_arg = self.check_func_arg(self.args[1])
        self.mv_arg = self.check_mv_arg(self.args[2])
        self.mv_name_arg = self.check_mv_name_arg(self.args[3])
        if self.args_len == 4:
            # if there was no app name then list all the
            # installed local apps
            sys.stderr.write(self.error('Please choose an appname!\n'))
            self.list_apps()
        if self.args_len == 5:
            self.app_name = self.args[4]
            if self.app_name not in self.installed_apps:
                sys.stderr.write(self.error("Given app name <{}> didn't get installed.\n".format(self.app_name)))
                self.list_apps()
            self.app_path = os.path.join(self.basedir, *self.app_name.split('.'))
            assert os.path.exists(self.app_path)
            if self.mv_arg in ['view', 'v']:
                self.create_view()
            else:
                self.create_model()

    def execute(self):
        if self.args_len == 1:
            self.show_help()
            return
        self.sub_command = self.args[1]
        self.identify_arguments()


def main():
    if 'manage.py' not in os.listdir('.'):
        sys.stderr.write('Please run this command inside the directory where manage.py exists!\n')
        sys.exit(1)
    utility = Dj()
    utility.execute()
