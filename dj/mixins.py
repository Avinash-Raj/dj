import os
import sys
import re
from subprocess import Popen, PIPE


class BaseMixin:
    def get_mv_file_path(self, arg):
        m_file = os.path.join(self.app_path, '{}.py'.format(arg))
        m_directory = os.path.join(self.app_path, arg)
        if os.path.exists(m_file) and os.path.isfile(m_file):
            return m_file
        if os.path.exists(m_directory) and os.path.isdir(m_directory):
            return os.path.join(m_directory, '__init__.py')
        sys.stderr.write(self.error('No {} file or folder exists.\n'.format(arg)))
        sys.exit(1)

    def check_mv_name_already_exists_or_not(self, mv_path, class_name):
        with open(mv_path) as f:
            is_exists = re.search(r'(?m)^class {}[:(]'.format(self.mv_name_arg), f.read())
            if not is_exists:
                return None
            sys.stderr.write(self.error('{} with the name {} already exists!\n'.format(class_name, self.mv_name_arg)))
            sys.exit(1)

    def camelcase_to_ucase(self, stri):
        return re.sub(r'(?m)(.|^)([A-Z])', lambda m: '_' + m.group(2).lower() if m.group(1) else m.group(2).lower(), stri)


class CreateModelMixin(BaseMixin):
    def create_model_urls(self):
        url_lines = [
                'from django.conf.urls import url',
                'from .{} import {}'.format(self.model_path.replace(self.app_path+os.path.sep, '').rstrip('.py').replace('/', '.'), self.mv_name_arg),
                '\n',
                'urlpatterns = [',
                "    url(r'^{name}/$', {class_name}.as_view(), name='{name}'),".format(name=self.camelcase_to_ucase(self.mv_name_arg), class_name=self.mv_name_arg),
                ']\n'
        ]

        with open(self.url_file_path, 'w') as w:
            w.write('\n'.join(url_lines))
        sys.stdout.write(self.success('{} created successfully!\n'.format(self.url_file_path)))

    def apply_model(self):
        with open(self.model_path, 'a') as f:
            f.write('''\nclass {}(models.Model):\n    pass\n'''.format(self.mv_name_arg))
        sys.stdout.write(self.success('New {} model created successfully!\n'.format(self.mv_name_arg)))
        # TODO: make changes in urls.py
        # check urls.py exists or not
        self.url_file_path = os.path.join(self.app_path, 'urls.py')
        if os.path.exists(os.path.join(self.url_file_path)):
            # self.url_file_path = 
            pass
        elif os.path.exists(os.path.join(self.app_path, 'urls', '__init__.py')):
            self.url_file_path = os.path.join(self.app_path, 'urls', '__init__.py')
        else:
            self.create_model_urls()
        # proc = Popen('ls -l', shell=True, stdout=PIPE, stderr=PIPE)
        # succ, err = proc.communicate()

    def create_model(self):
        self.model_path = self.get_mv_file_path('models')
        # self.url_path = self.get_mv_file_path('urls')
        self.check_mv_name_already_exists_or_not(self.model_path, 'Model')
        self.apply_model()


class CreateViewMixin(BaseMixin):
    def apply_view(self):
        # TODO: fill this
        pass

    def create_view(self):
        self.view_path = self.get_mv_file_path('views')
        self.check_mv_name_already_exists_or_not(self.model_path, 'View')
        self.apply_view()
