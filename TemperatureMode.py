#from base_classes import *
import time, uuid, urllib, urllib2
import hmac, hashlib
from base64 import b64encode


class TemperatureMode:#(Mode):
    key = "TEMPERATURE"
    
    app_id = "saxTR9m9"
    consumer_key = "dj0yJmk9VldQQVduWEJoYWx0JmQ9WVdrOWMyRjRWRkk1YlRrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PWI3"
    consumer_secret = "a6c4f0725eee67133cb1985be8f00b00da3a962e"
    
    method = 'GET'
    url = "https://weather-ydn-yql.media.yahoo.com/forecastrss"
    concat = '&'
    
    #temp_min50_color = C(0, 0, 0)
    #temp_0_color = C(0, 0, 0)
    #temp_30_color = C(0, 0, 0)
    #temp_50_color = C(0, 0, 0)
    
    refresh_time = 120
    last_refresh = 0
    
    def loop(self, _leds):
        if last_refresh + refresh_time < time.time():
            tempForLeds([(0, 0)])
            
            last_refresh = time.time()
            
        return
      
    def tempForLeds(self, locations):#led):
        queries = [{
            'lat': str(lat),
            'lon': str(long),
            'format': 'json',
            'u': 'c'
        } for lat, long in locations]
        
        print(queries)
        
        
        
        for query in queries:
            
            oauth = {
                'oauth_consumer_key': self.consumer_key,
                'oauth_nonce': uuid.uuid4().hex,
                'oauth_signature_method': 'HMAC-SHA1',
                'oauth_timestamp': str(int(time.time())),
                'oauth_version': '1.0'
            }
            
            #Prepare signature string (merge all params and sort them)
            
            merged_params = query.copy()
            merged_params.update(oauth)
            sorted_params = [k + '=' + urllib.quote(merged_params[k], safe='') for k in sorted(merged_params.keys())]
            signature_base_str = self.method + self.concat + urllib.quote(self.url, safe='') + self.concat + urllib.quote(self.concat.join(sorted_params), safe='')
            
            #Generate Signature
            
            composite_key = urllib.quote(self.consumer_secret, safe='') + self.concat
            oauth_signature = b64encode(hmac.new(composite_key, signature_base_str, hashlib.sha1).digest())
            
            #Prepare Authorization header
            
            oauth['oauth_signature'] = oauth_signature
            auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(k,v) for k,v in oauth.iteritems()])

            #Send request
            
            url = self.url + '?' + urllib.urlencode(query)
            request = urllib2.Request(url)
            request.add_header('Authorization', auth_header)
            request.add_header('X-Yahoo-App-Id', self.app_id)
            response = urllib2.urlopen(request).read()
            print(response)
    

#led = Led("EUROPE", 53, 10)
tempMode = TemperatureMode()
tempMode.tempForLeds([(53, 10), (-30.8, 25.23), (64, -18)])
    