DEV_SECRET = {
    'SECRET_KEY' : 'django-insecure-z)jm_*ue@qu&u*2n04@tefi3fo_)_*4d_^=9o)f3t*k)z^dn^6'
}

DEV_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'realtime_detection',
        'USER': 'admin',
        'PASSWORD': 'vmfhwprxm2xla!',
        'HOST': 'finalteam-db1.cwkyk5bf3ql5.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_ALL_TABLES',
        }
    }
}