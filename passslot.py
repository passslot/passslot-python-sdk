import os.path, logging, sys, time

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json
try:        
    import requests
except ImportError:
    pass

__version_info__ = ('0', '1')
__version__ = '.'.join(__version_info__)

__allowed_images__ = ['icon', 'logo', 'strip', 'thumbnail', 'background', 'footer']


logger = logging.getLogger('passslot')

class PassSlot(object):

    app_key = None
    base_url = None
    debug = True
    
    __instance = None
    
    def __init__(self, app_key, base="https://api.passslot.com", version="v1", debug=False):
        
        self.base_url = "%s/%s" % (base, version)
        self.session = requests.session()
            
        if app_key is None and 'PASSSLOT_APPKEY' in os.environ :
            app_key = os.environ['PASSSLOT_APPKEY']
            
        if app_key is None: 
            raise PassSlotException('You must provide a PassSlot App Key')
        
        self.app_key = app_key
        self.debug = debug

    @classmethod
    def start(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = cls(*args, **kwargs)
        
        return cls.__instance
    
    
    def create_pass_from_template(self, templateId, values=None, images=None):
        resource = "/templates/%s/pass" % (templateId)
        return self.__create_pass(resource, values, images)
    
    def create_pass_from_template_with_name(self, templateName, values=None, images=None):
        resource = "/templates/names/%s/pass" % (requests.compat.quote(templateName))
        return self.__create_pass(resource, values, images)
    
    def __create_pass(self, resource, values, images):
        multipart = images != None and len(images) > 0
        
        if multipart:
            files = []
            for type in images:
                if type in __allowed_images__ or type + "2x" in __allowed_images__:
                    files.append((type, images[type]))
                else:
                    logger.warn('Image type %s not available. Image will be ignored.' % type)
                         
            files.append(('values', json.dumps(values)))
            content = files
        else:
            content = values            
        
        result = self.__call('post', resource, content, multipart)
        return Pass(self, **result)
    
    def download_pass(self, pspass):
        resource = "/passes/%s/%s" % (pspass.passTypeIdentifier, pspass.serialNumber)
        return self.__call('get', resource)
    
    def get_pass_url(self, pspass):
        if hasattr(pspass, 'url'):
            return pspass.url
        resource = "/passes/%s/%s/url" % (pspass.passTypeIdentifier, pspass.serialNumber)
        json = self.__call('get', resource)
        return json['url']
    
    def email_pass(self, pspass, email):
        resource = "/passes/%s/%s/email" % (pspass.passTypeIdentifier, pspass.serialNumber)
        content = {'email': email}
        self.__call('post', resource, content)
        return True
    
    def __call(self, method, resource, content=None, multipart=False):

        headers = {
            'User-Agent' : 'PassSlotSDK-Python/%s' % (__version__),
            'Accept': 'application/json, */*; q=0.01',
            'Authorization' : self.app_key
        }
        
        method = method.lower()
        
        kwargs = {}
        
        if method == 'post' or method == 'put':
            if multipart:
                kwargs['files'] = content
            else:
                headers['Content-Type']  = 'application/json';
                kwargs['data'] = json.dumps(content)
        
        if self.debug:
            logger.debug(('> %s %s%s' % (method.upper(), self.base_url, resource)) + ((': %s' % content) if content else '' ))

        response = self.session.request(method, self.base_url + resource, headers=headers, **kwargs)
        if self.debug:
            logger.debug('< %s: %s' % (response.status_code,
                                   response.text if response.headers['content-type'].startswith('application/json') 
                                                else '%s (%s bytes)' % (response.headers['content-type'], response.headers['content-length'])
                                ))
        
        if response.status_code == requests.codes.unprocessable:
            raise PassSlotApiValidationException(response.json())
        
        if response.status_code == requests.codes.unauthorized:
            raise PassSlotApiUnauthorizedException()
        
        if response.status_code < 200 or response.status_code >= 300:
            raise PassSlotApiException(response.status_code, response.content)
        
        if response.headers['content-type'].startswith('application/json'):
            return response.json()
        else:
            return response.content
    
    def log(self, *args, **kwargs):
        logger.log(self.level, *args, **kwargs)

    def __repr__(self):
        return '<PassSlot %s>' % self.app_key

class PassSlotObject(object):
    def __init__(self, engine, **entries):
        self.engine = engine
        self.__dict__.update(entries)

class Pass(PassSlotObject):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
    
    def download(self):
        self.data = self.engine.download_pass(self)
        return self.data
        
    def __repr__(self, *args, **kwargs):
        return '<Pass %s/%s>' % (self.passTypeIdentifier, self.serialNumber)
        

class PassSlotException(Exception):
    pass


class PassSlotApiException(PassSlotException):

    def __init__(self, status, msg=""):
        self.status = status
        self.msg = msg

    def __str__(self):
        return '[%s]: %s' % ( self.status, self.msg)
    
class PassSlotApiUnauthorizedException(PassSlotApiException):
    def __init__(self):
        super(self.__class__, self).__init__(401, "Unauthorized. Please check your app key and make sure it has access to the template and pass type id")
    
class PassSlotApiValidationException(PassSlotApiException):
    def __init__(self, response):
        msg = ''
        if response:
            msg = response['message']
            for error in response['errors']:
                msg += '; ' + error['field'] + ': ' + ', '.join(error['reasons'])
      
        
        super(self.__class__, self).__init__(422, msg)
