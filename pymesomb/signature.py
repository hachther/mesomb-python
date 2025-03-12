import hashlib
import hmac
import json
from urllib.parse import quote, urlparse, quote_plus

from pymesomb import mesomb


class Signature:
    """ """
    @staticmethod
    def sign_request(service, method, url, date, nonce, credentials, headers=None, body=None):
        """Method to use to compute signature used in MeSomb request

        Args:
          service: service to use can be payment, wallet ... (the list is provide by MeSomb)
          method: HTTP method (GET, POST, PUT, PATCH, DELETE...)
          url: the full url of the request with query element
          date: Datetime of the request
          nonce: Unique string generated for each request sent to MeSomb
          credentials: dict containing key => value for the credential provided by MeSOmb.
                {'access' => access_key, 'secret' => secret_key}
          headers: Extra HTTP header to use in the signature (Default value = None)
          body: The dict containing the body you send in your request body (Default value = None)

        Returns:
          Authorization to put in the header

        """
        algorithm = mesomb.algorithm
        parse = urlparse(url)
        canonical_query = parse.query
        if len(canonical_query) > 0:
            canonical_query = '&'.join([f"{quote_plus(c.split('=')[0])}={quote_plus(c.split('=')[1])}" for c in canonical_query.split('&')])

        timestamp = str(int(date.timestamp()))

        # CanonicalHeaders
        if headers is None:
            headers = {}
        headers['host'] = f'{parse.scheme}://{parse.netloc}'
        headers['x-mesomb-date'] = timestamp
        headers['x-mesomb-nonce'] = nonce
        canonical_headers = '\n'.join([f'{key.lower()}:{headers[key].strip()}' for key in sorted(headers)])

        if body is None:
            body = {}
        request_params = json.dumps(body, separators=(',', ':'))

        payload_hash = hashlib.sha1(request_params.encode('utf-8')).hexdigest()

        signed_headers = ';'.join(sorted(headers))

        canonical_request = f'{method}\n{quote(parse.path)}\n{canonical_query}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'

        scope = f"{date.strftime('%Y%m%d')}/{service}/mesomb_request"
        string_to_sign = f"{algorithm}\n{timestamp}\n{scope}\n{hashlib.sha1(canonical_request.encode('utf-8')).hexdigest()}"

        signature = hmac.new(credentials['secret_key'].encode(), string_to_sign.encode(), hashlib.sha1).hexdigest()

        authorization_header = f"{algorithm} Credential={credentials['access_key']}/{scope}, SignedHeaders={signed_headers}, Signature={signature}"

        return authorization_header
