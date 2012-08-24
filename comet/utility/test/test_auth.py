from twisted.trial import unittest
from zope.interface import implementer

from ...log import log
from ...icomet import IAuthenticatable
from ..auth import CheckSignatureMixin
from ..auth import check_auth
from ..xml import xml_document
from ...test.support import DUMMY_VOEVENT
from ...test.gpg import GPGTestSupport

class DummyClass(CheckSignatureMixin):
    def __init__(self, must_auth, authenticated):
        self.must_auth = must_auth
        self.authenticated = authenticated

    @check_auth
    def test_function(self):
        return True

@implementer(IAuthenticatable)
class AuthenticatableDummyClass(DummyClass):
    pass

class CheckSignatureTestCase(GPGTestSupport):
    def setUp(self):
        GPGTestSupport.setUp(self)
        self.authenticator = DummyClass(True, False)

    def test_authenticate(self):
        self.assertFalse(self.authenticator.authenticated)
        doc = xml_document(DUMMY_VOEVENT)
        doc = self._sign_trusted(doc)
        doc.sign(self.PASSPHRASE, self.KEY_ID)
        d = self.authenticator.authenticate(doc)
        d.addCallback(lambda x: self.assertTrue(self.authenticator.authenticated))
        return d

class CheckAuthTestCase(unittest.TestCase):
    def test_bad_interface(self):
        dummy = DummyClass(False, False)
        self.assertEqual(dummy.test_function(), None)
        dummy = DummyClass(False, True)
        self.assertEqual(dummy.test_function(), None)
        dummy = DummyClass(True, True)
        self.assertEqual(dummy.test_function(), None)

    def test_no_auth_required(self):
        dummy = AuthenticatableDummyClass(False, False)
        self.assertEqual(dummy.test_function(), True)
        dummy = AuthenticatableDummyClass(False, True)
        self.assertEqual(dummy.test_function(), True)

    def test_auth_valid(self):
        dummy = AuthenticatableDummyClass(True, True)
        self.assertEqual(dummy.test_function(), True)

    def test_auth_invalid(self):
        dummy = AuthenticatableDummyClass(True, False)
        self.assertEqual(dummy.test_function(), None)