import sys
import os
import re
from django.core.management.color import color_style


class Base(object):
    def __init__(self):
        pass

    def unknown_command(self, command):
        sys.stderr.write(self.error('Unknown command {}\n'.format(command)))
        # sys.exit(1)

    def show_help(self):
        usage = [color_style().NOTICE('[dj]')]
        if self.sub_command == 'help':
            usage.append('    create')
            usage.append('    list')
        elif self.sub_command in ['v', 'view']:
            usage.append('    create view <view_name> <app_name>')
        elif self.sub_command in ['m', 'model']:
            usage.append('    create model <model_name> <app_name>')
        else:
            for com in self.commands:
                usage.append('    create {}'.format(com))

        for txt in usage:
            sys.stdout.write(txt+'\n')
        sys.exit(1)

    def get_settings_path(self):
        """Get the path where settings.py wasactually loated!"""
        settings_path = None
        with open(os.path.join(self.basedir, 'manage.py')) as f:
            settings_path = re.search(r'os\.environ\.setdefault\("DJANGO_SETTINGS_MODULE",\s*"([^\'"]+)', f.read()).group(1)
        return os.path.join(*settings_path.split('.')) + '.py'

    def list_apps(self):
        usage = [self.notice('Installed Apps:')]
        for app in self.installed_apps:
            usage.append(self.success('    {}'.format(app)))
        for txt in usage:
            sys.stdout.write(txt+'\n')
        sys.exit(1)

    def check_func_arg(self, arg):
        if arg not in ['c', 'create']:
            self.unknown_command(arg)
            self.show_help()
            sys.exit(1)
        return arg

    def check_mv_arg(self, arg):
        if arg not in self.commands + ['m', 'v']:
            self.unknown_command(arg)
            self.show_help()
            sys.exit(1)
        return arg

    def check_mv_name_arg(self, arg):
        if not arg.isalpha():
            sys.stderr.write(self.error('View or model name must contain only alphabets.\n'))
            sys.exit(1)
        if not arg[0].isupper():
            sys.stderr.write(self.warn('View or model name should startswith a capital letter.\n'))
            sys.exit(1)
        return arg

    def get_installed_apps(self):
        """List all the installed local apps."""
        apps = []
        with open(self.settings_path) as f:
            apps_str = re.search(r'(?s)INSTALLED_APPS\s+=\s+[(\[]\s*(.+?)\s*[)\]]', f.read()).group(1).strip()
            for app in apps_str.split(','):
                if 'django.contrib' in app or "'" not in app:
                    continue
                app_name = app.split("'")[1]
                if os.path.exists(os.path.join(self.basedir, app_name.split('.')[0])):
                    apps.append(app_name)
        return apps

    def get_and_list_installed_apps(self):
        self.settings_path = self.get_settings_path()
        self.installed_apps = self.get_installed_apps()
        self.list_apps()
