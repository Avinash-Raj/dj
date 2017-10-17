import re
import os


class UrlClass:
    """Functions which helps to build urls"""
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
