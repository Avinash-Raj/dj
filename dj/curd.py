import re
from .urls import UrlClass


class CURDViewClas(UrlClass):
    def get_rest_import_stmts(self):
        """Detrieve import stmts"""
        if self.rest and set(self.options) == set('CURDL'):
            return ['from rest_framework.viewsets import ModelViewSet']
        smts = {
          'C': 'Create{}View'.format('API' if self.rest else ''),
          'U': 'Update{}View'.format('API' if self.rest else ''),
          'D': '{}View'.format('DestroyAPI' if self.rest else 'Delete'),
          'L': 'List{}View'.format('API' if self.rest else ''),
          'R': '{}View'.format('RetrieveAPI' if self.rest else 'Detail')
        }
        return ['from rest_framework.generics import {}'.format(smts[opt]) if self.rest else 'from django.views.generic import {}'.format(smts[opt]) for opt in self.options]

    def _get_django_view_stmts(self, view_stmts):
        """Build django view statements."""
        view_classes = []
        template = ['class {}({}):',
                    '    model = None',
                    '    form_class = None',
                    "    template_name = 'none.html'"]
        for stmt in view_stmts:
            # if Delete in view stmt then remove form_class and template_name attrib
            if 'Delete' in stmt:
                view_classes.append('\n'.join(template[:2]).format(self.mv_name_arg+stmt, stmt))
                continue
            view_classes.append('\n'.join(template).format(self.mv_name_arg+stmt, stmt))

        return '\n\n'.join(view_classes)

    def _get_viewset_stmts(self):
        template = ['class {}ViewSet(ModelViewSet):'.format(self.mv_name_arg),
                    '    queryset = None',
                    '    serializer_class = None',
                    '    permission_classes = ()']
        return '\n'.join(template)

    def _get_rest_framework_view_stmts(self, view_stmts):
        """Build DRF view statements."""
        if set(self.options) == set('CURDL'):
            return self._get_viewset_stmts()

        view_classes = []
        template = ['class {}({}):',
                    '    queryset = None',
                    '    serializer_class = None',
                    "    permission_classes = ()"]

        if 'C' in self.options:
            view_cls_stmt = [template[0].format(self.mv_name_arg + 'View', 'CreateAPIView')]
            if 'L' in self.options:
                view_cls_stmt = [template[0].format(self.mv_name_arg + 'View', ', '.join([i for i in view_stmts if re.search(r'^[LC]', i)]))]
            view_classes.append('\n'.join(view_cls_stmt + template[1:]))
        if any(i in 'URD' for i in self.options):
            view_cls_stmt = [template[0].format(self.mv_name_arg + 'UpdateView', ', '.join([i for i in view_stmts if re.search(r'^[URD]', i)]))]
            view_classes.append('\n'.join(view_cls_stmt + template[1:]))

        return '\n\n'.join(view_classes)

    def check_and_import_stmts(self, stmts):
        """Check and import stmts which are not imported."""
        stmts_to_import = []
        view_content = None
        with open(self.view_path) as f:
            view_content = f.read()
            for stm in stmts:
                if stm in view_content:
                    continue
                stmts_to_import.append(stm)
        # add the import stmts
        view_content = re.sub(r'(?m)^((?:import|from).*)(?=\n\n)', r'\1\n{}'.format('\n'.join(stmts_to_import)), view_content, 1)
        # Get the last word
        stmts = [i.split()[-1] for i in stmts]
        # create view
        if not self.rest:
            view_stmts = self._get_django_view_stmts(stmts)
        else:
            view_stmts = self._get_rest_framework_view_stmts(stmts)

        view_content += view_stmts
        with open(self.view_path, 'w') as w:
            w.write(view_content)

    def create_curdl_view(self):
        rest_stmts = self.get_rest_import_stmts()
        self.check_and_import_stmts(rest_stmts)
