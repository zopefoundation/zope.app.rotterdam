##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Custom Widgets for the rotterdam layer.
"""
__docformat__ = 'restructuredtext'

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.formlib.interfaces import IInputWidget
from zope.formlib.widget import escape
from zope.formlib.widget import renderElement
from zope.formlib.widgets import TextAreaWidget
from zope.interface import implementer


@implementer(IInputWidget)
class SimpleEditingWidget(TextAreaWidget):
    """Improved textarea editing, with async saving using JavaScript.


    Multi-line text (unicode) input.

    >>> from zope.publisher.browser import TestRequest
    >>> from zope.schema import Text
    >>> field = Text(__name__='foo', title=u'on')
    >>> request = TestRequest(form={'field.foo': u'Hello\\r\\nworld!'})
    >>> widget = SimpleEditingWidget(field, request)
    >>> widget.style = ''
    >>> widget.hasInput()
    True
    >>> widget.getInputValue()
    u'Hello\\nworld!'

    >>> def normalize(s):
    ...   return '\\n  '.join(filter(None, s.split(' ')))

    >>> print(normalize( widget() ))
    <textarea
      cols="60"
      id="field.foo"
      name="field.foo"
      rows="15"
      >Hello\r
    world!</textarea>

    >>> print(normalize( widget.hidden() ))
    <input
      class="hiddenType"
      id="field.foo"
      name="field.foo"
      type="hidden"
      value="Hello&#13;&#10;world!"
      />

    Calling `setRenderedValue` will change what gets output:

    >>> widget.setRenderedValue("Hey\\ndude!")
    >>> print(normalize( widget() ))
    <textarea
      cols="60"
      id="field.foo"
      name="field.foo"
      rows="15"
      >Hey\r
    dude!</textarea>

    Check that HTML is correctly encoded and decoded:

    >>> request = TestRequest(
    ...     form={'field.foo': u'<h1>&copy;</h1>'})
    >>> widget = SimpleEditingWidget(field, request)
    >>> widget.style = ''
    >>> widget.getInputValue()
    u'<h1>&copy;</h1>'

    >>> print(normalize( widget() ))
    <textarea
      cols="60"
      id="field.foo"
      name="field.foo"
      rows="15"
      >&lt;h1&gt;&amp;copy;&lt;/h1&gt;</textarea>
    """

    default = ""
    width = 60
    height = 15
    extra = ""
    style = "width: 98%; font-family: monospace;"
    rowTemplate = ViewPageTemplateFile("simpleeditingrow.pt")
    rowFragment = ViewPageTemplateFile("simpleeditingrowfragment.pt")

    def _toFieldValue(self, value):
        if self.context.min_length and not value:  # pragma: no cover
            return None
        return super()._toFieldValue(value)

    def __call__(self):
        return renderElement("textarea",
                             name=self.name,
                             id=self.name,
                             cssClass=self.cssClass,
                             rows=self.height,
                             cols=self.width,
                             style=self.style,
                             contents=escape(self._getFormValue()),
                             extra=self.extra)

    def contents(self):  # pragma: no cover
        """Make the contents available to the template"""
        return self._getFormData()
