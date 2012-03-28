# -*- coding: utf-8 -*-
"""

    remoteobjects.http_requests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Http replacement object using Requests library as the underpinings.

    TODO: move file and replace http.

"""
import requests
from requests.auth import HTTPBasicAuth


DEFAULT_MAX_REDIRECTS=None


class Http(object):

    def __init__(self, cache=None, timeout=None,
                 proxy_info=None,
                 ca_certs=None, disable_ssl_certificate_validation=False):

        # Name/password
        self.credentials = None

        # Key/cert
        self.certificates = None

        # authorization objects
        self.authorizations = None

        self.timeout = timeout

    """ http object """
    def add_credentials(self, name, password, domain=""):
        """Add a name and password that will be used
        any time a request requires authentication."""
        self.credentials = HTTPBasicAuth(name, password)

    def add_certificate(self, key, cert, domain):
        """Add a key and cert that will be used
        any time a request requires authentication."""
        #self.certificates.add(key, cert, domain)

    def clear_credentials(self):
        """Remove all the names and passwords
        that are used for authentication"""
        del self.credentials
        self.credentials = None

    def request(self, uri, method="GET", body=None, headers=None,
                redirections=DEFAULT_MAX_REDIRECTS, connection_type=None):
        """ Performs a single HTTP request.

            :param uri: The 'uri' is the URI of the HTTP resource and can begin
with either 'http' or 'https'. The value of 'uri' must be an absolute URI.

The 'method' is the HTTP method to perform, such as GET, POST, DELETE, etc.
There is no restriction on the methods allowed.

The 'body' is the entity body to be sent with the request. It is a string
object.

Any extra headers that are to be sent with the request should be provided in the
'headers' dictionary.

The maximum number of redirect to follow before raising an
exception is 'redirections. The default is 5.

The return value is a tuple of (response, content), the first
being and instance of the 'Response' class, the second being
a string that contains the response entity body.
        """

        kwargs=dict( method=method,url=uri )

        if headers:
            kwargs['headers']=headers
        if data:
            kwargs['data']=body
        if redirections is not None and redirections > 0:
            kwargs['config']=dict(max_redirects=redirections)
            kwargs['allow_redirects']=True
        if timout:
            kwargs['timeout']=self.timeout
        if self.credentials:
            kwargs['auth']=self.credentials

        response = requests.request(**kwargs)

        # TODO this is the list of things that can be passed into request.  For
        # Now this is all I need, add the other ones as needed.

        # DONE       :param method: method for the new :class:`Request` object.
        # DONE       :param url: URL for the new :class:`Request` object.
        #        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        # DONE        :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
        # DONE       :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        #        :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
        #        :param files: (optional) Dictionary of 'name': file-like-objects (or {'name': ('filename', fileobj)}) for multipart encoding upload.
        #        :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        # DONE   :param timeout: (optional) Float describing the timeout of the request.
        #        :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.
        #        :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
        #        :param return_response: (optional) If False, an un-sent Request object will returned.
        #        :param session: (optional) A :class:`Session` object to be used for the request.
        #        :param config: (optional) A configuration dictionary.
        #        :param verify: (optional) if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        #        :param prefetch: (optional) if ``True``, the response content will be immediately downloaded.

        return (response, response.content)

