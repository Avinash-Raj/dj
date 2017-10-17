import os
import sys
import re
from .utils import Base
from subprocess import Popen, PIPE

try:
    import rest_framework
    REST = True
except:
    REST = False


class BaseMixin:
    def print_files_modified(self):
        sys.stdout.write(self.notice('Files Changed:\n'))
        for fil in self.files_modified:
            sys.stdout.write(self.warn('    {}\n'.format(fil)))

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
        return re.sub(r'(?m)(.|^)([A-Z])', lambda m: m.group(1) + '_' + m.group(2).lower() if m.group(1) else m.group(2).lower(), stri)


class CreateModelMixin(BaseMixin):
    def apply_model(self):
        with open(self.model_path, 'a') as f:
            f.write('''\nclass {}(models.Model):\n    pass\n'''.format(self.mv_name_arg))
        sys.stdout.write(self.success('New {} model created successfully!\n'.format(self.mv_name_arg)))
        # append models.py file path to modified_files
        self.files_modified.append(self.model_path)

    def create_model(self):
        self.model_path = self.get_mv_file_path('models')
        self.check_mv_name_already_exists_or_not(self.model_path, 'Model')
        self.apply_model()
        self.print_files_modified()


class CreateViewMixin(BaseMixin):
    def get_view_import_stmt(self):
        return 'from .{} import {}'.format(self.view_path.replace(self.app_path+os.path.sep, '').rstrip('.py').replace('/', '.'),self.mv_name_arg)

    def get_view_url_stmt(self):
        return "    url(r'^{name}/$', {class_name}.as_view(), name='{name}'),".format(name=self.camelcase_to_ucase(self.mv_name_arg), class_name=self.mv_name_arg)

    def create_view_urls(self):
        url_lines = [
                'from django.conf.urls import url',
                self.get_view_import_stmt(),
                '\n',
                'urlpatterns = [',
                self.get_view_url_stmt(),
                ']\n'
        ]

        with open(self.url_file_path, 'w') as w:
            w.write('\n'.join(url_lines))
        sys.stdout.write(self.success('New urls created successfully!\n'))

    def append_view_url(self):
        # Check import stmt for generic class exists or not
        cmd = """sed -i "/^\(from\|import\)/{{:a;n;/^$/!ba;s/.*/{}\\n/}};s~\]~{}\\n]~" {}""".format(
                            self.get_view_import_stmt(), self.get_view_url_stmt(), self.url_file_path)

        proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
        succ, err = proc.communicate()
        if err:
            sys.stderr.write(self.error(str(err)+'\n'))
            sys.exit(1)
        sys.stdout.write(self.success('URLs modified successfully!\n'))

    def identify_options(self):
        #if rest framework installed then use rest's import stmt
        # else use django's import stmt
        # stmts = []
        # if REST:
        #     # check for whether the CURD options specified or not
        #     if self.options:
        #         if len(self.options) == 5:
        pass


    def add_view_class(self):
        # TODO: add import stmt based upon the curd
        # is_import_stmt_exists = Base.check_import_stmt(self.view_path,'from django.views.generic import ')
        pass

    def apply_view(self):
        with open(self.view_path, 'a') as f:
            f.write('''\nclass {}(generics.View):\n    pass\n'''.format(self.mv_name_arg))
        sys.stdout.write(self.success('New {} View created successfully!\n'.format(self.mv_name_arg)))
        self.files_modified.append(self.view_path)
        # Append the url
        self.url_file_path = os.path.join(self.app_path, 'urls.py')
        if os.path.exists(os.path.join(self.url_file_path)):
            self.append_view_url()
        elif os.path.exists(os.path.join(self.app_path, 'urls', '__init__.py')):
            self.url_file_path = os.path.join(self.app_path, 'urls', '__init__.py')
            self.append_view_url()
        else:
            self.create_view_urls()
        self.files_modified.append(self.url_file_path)

    def create_view(self):
        self.rest = REST
        self.view_path = self.get_mv_file_path('views')
        self.check_mv_name_already_exists_or_not(self.view_path, 'View')
        self.apply_view()
        self.print_files_modified()
