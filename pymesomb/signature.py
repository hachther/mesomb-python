import hashlib
import hmac
import json
from urllib.parse import quote, urlparse

from pymesomb import mesomb


class Signature:
    @staticmethod
    def sign_request(service, method, url, date, nonce, credentials, headers=None, body=None):
        """
    Method to use to compute signature used in MeSomb request

    :param service: service to use can be payment, wallet ... (the list is provide by MeSomb)
    :param method: HTTP method (GET, POST, PUT, PATCH, DELETE...)
    :param url: the full url of the request with query element https://mesomb.hachther.com/path/to/ressource?highlight=params#url-parsing
    :param date: Datetime of the request
    :param nonce: Unique string generated for each request sent to MeSomb
    :param credentials: dict containing key => value for the credential provided by MeSOmb. {'access' => access_key, 'secret' => secret_key}
    :param headers: Extra HTTP header to use in the signature
    :param body: The dict containing the body you send in your request body
    :return: Authorization to put in the header
    """
        algorithm = mesomb.algorithm
        parse = urlparse(url)
        canonical_query = parse.query

        timestamp = str(int(date.timestamp()))

        # CanonicalHeaders
        if headers is None:
            headers = {}
        headers['host'] = '{}://{}'.format(parse.scheme, parse.netloc)
        headers['x-mesomb-date'] = timestamp
        headers['x-mesomb-nonce'] = nonce
        canonical_headers = '\n'.join(['{}:{}'.format(key.lower(), headers[key].strip()) for key in sorted(headers)])

        if body is None:
            body = {}
        request_params = json.dumps(body, separators=(',', ':'))

        payload_hash = hashlib.sha1(request_params.encode('utf-8')).hexdigest()

        signed_headers = ';'.join(sorted(headers))

        canonical_request = '{}\n{}\n{}\n{}\n{}\n{}'.format(method, quote(parse.path), canonical_query,
                                                            canonical_headers,
                                                            signed_headers, payload_hash)

        scope = '{}/{}/mesomb_request'.format(date.strftime('%Y%m%d'), service)
        string_to_sign = '{}\n{}\n{}\n{}'.format(algorithm, timestamp, scope,
                                                 hashlib.sha1(canonical_request.encode('utf-8')).hexdigest())

        signature = hmac.new(credentials['secret_key'].encode(), string_to_sign.encode(), hashlib.sha1).hexdigest()

        authorization_header = '{} Credential={}/{}, SignedHeaders={}, Signature={}'.format(algorithm,
                                                                                            credentials['access_key'],
                                                                                            scope,
                                                                                            signed_headers, signature)

        return authorization_header
