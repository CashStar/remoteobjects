from __future__ import with_statement

import unittest
import logging
import sys
from datetime import datetime

from remoteobjects import tests, fields, remote


class TestLinks(unittest.TestCase):

    def testBasic(self):

        class What(remote.RemoteObject):
            what = fields.Something()

        class Linky(remote.RemoteObject):
            name  = fields.Something()
            stuff = remote.Link(r'asf', fields.Object(What))

        l = Linky(name='awesome')

        self.assertRaises(ValueError, l.stuff)

        l._id = 'http://example.com/dwar'

        self.assert_(callable(l.stuff), "Linky instance's stuff is a method")

        content = """{ "what": "what!" }"""
        headers = { 'accept': 'application/json' }
        with tests.MockedHttp('http://example.com/asf', content, headers=headers) as h:
            w = l.stuff(http=h)
        self.assert_(isinstance(w, What), 'stuff method gave us a What')
        self.assertEquals(w.what, 'what!', "stuff's What seems viable")
        self.assertEquals(w._id, 'http://example.com/asf', "stuff's What knows its _id")


    def testCallable(self):

        class What(remote.RemoteObject):
            what = fields.Something()

        class Linky(remote.RemoteObject):
            meh   = fields.Something()
            stuff = remote.Link(lambda o: o.meh, fields.Object(What))

        l = Linky(meh='http://example.com/bwuh')

        content = """{ "what": "wha-hay?" }"""
        headers = { 'accept': 'application/json' }
        with tests.MockedHttp('http://example.com/bwuh', content, headers=headers) as h:
            w = l.stuff(http=h)
        self.assert_(w)
        self.assertEquals(w.what, 'wha-hay?')
        self.assertEquals(w._id, 'http://example.com/bwuh')


if __name__ == '__main__':
    tests.log()
    unittest.main()