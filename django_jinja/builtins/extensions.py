from jinja2.ext import Extension
from jinja2 import nodes
from jinja2 import Markup
from django.utils.safestring import mark_safe

import traceback

class CsrfExtension(Extension):
    tags = set(['csrf_token'])

    def __init__(self, environment):
        self.environment = environment

    def parse(self, parser):
        try:
            token = parser.stream.next()
            call_res = self.call_method('_render', [nodes.Name('csrf_token','load')])
            return nodes.Output([call_res]).set_lineno(token.lineno)
        except Exception:
            traceback.print_exc()

    def _render(self, csrf_token):
        if csrf_token:
            if csrf_token == 'NOTPROVIDED':
                return mark_safe(u"")

            return Markup(u"<div style='display:none'><input type='hidden'"
                          u" name='csrfmiddlewaretoken' value='%s' /></div>" % (csrf_token))

        from django.conf import settings
        if settings.DEBUG:
            import warnings
            warnings.warn("A {% csrf_token %} was used in a template, but the context"
                          "did not provide the value.  This is usually caused by not "
                          "using RequestContext.")
        return u''

        
#class LoadExtension(Extension):
#    """Changes auto escape rules for a scope."""
#    tags = set(['load'])
#
#    def parse(self, parser):
#        node = nodes.ExprStmt(lineno=next(parser.stream).lineno)
#
#        modules = []
#        while parser.stream.current.type != 'block_end':
#            lineno = parser.stream.current.lineno
#            if modules:
#                parser.stream.expect('comma')
#            expr = parser.parse_expression()
#            module = expr.as_const()
#            modules.append(module)
#
#        assignments = []
#        from djinja.template.defaultfunctions import Load
#        for m in modules:
#            target = nodes.Name(m,'store')
#            func = nodes.Call(nodes.Name('load', 'load'), [nodes.Const(m)],
#                              [], None, None)
#            assignments.append(nodes.Assign(target, func, lineno=lineno))
#                
#            for i in Load(m).globals.keys():
#                target = nodes.Name(i,'store')
#                f = nodes.Getattr(nodes.Name(m,'load'), i, 'load')
#            
#                assignments.append(nodes.Assign(target, f, lineno=lineno))
#
#        return assignments
