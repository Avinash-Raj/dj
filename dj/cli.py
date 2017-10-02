import os
import sys

try:
    from django.core.management.color import color_style
except:
    sys.stdout.write('Please install django!')
    sys.exit(1)
# from django.core.management import ManagementUtility


class Dj:
    def __init__(self):
        self.args = sys.argv
        self.args_len = len(self.args)
        self.cwd = self.args[0]
        self.sub_command = 'help'
        self.commands = ['model', 'view']

    def unknown_command(self, command):
        sys.stderr.write('Unknown command {}\n'.format(command))
        # sys.exit(1)

    def show_help(self):
        usage = [color_style().NOTICE('[dj]')]
        if self.sub_command == 'help':
            usage.append('    create')
        elif self.sub_command in ['v', 'view']:
            usage.append('    create view <view_name> <app_name>')
        elif self.sub_command in ['m', 'model']:
            usage.append('    create model <model_name> <app_name>')
        else:
            for com in self.commands:
                usage.append('    create {}'.format(com))

        for txt in usage:
            sys.stdout.write(txt+'\n')

    def identify_arguments(self):
        if self.args_len == 2:
            # if first argument not of c or create
            if self.args[1] not in ['c', 'create']:
                self.unknown_command(self.args[1])
            self.show_help()
            return
        elif self.args_len == 3:
            # if second argument not of view or model
            if self.args[2] not in self.commands + ['m', 'v']:
                self.unknown_command(self.args[2])
                self.show_help()
            # show help for specific command
            else:
                self.sub_command = self.args[2]
                self.show_help()

    def execute(self):
        if self.args_len == 1:
            self.show_help()
            return
        self.sub_command = self.args[1]
        self.identify_arguments()


def main():
    utility = Dj()
    utility.execute()
