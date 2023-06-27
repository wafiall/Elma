import json 
import mpyaes

key = mpyaes.generate_key(32)
IV = mpyaes.generate_IV(16)
cipher = mpyaes.new(key,mpyaes.MODE_CBC,IV)

data_json = {'pengirim' : 'vito',
        'pesan' : 'ini untuk di encrypt'}
data = json.dumps(data_json)
xxx = bytearray(data)
cipher.encrypt(xxx)

