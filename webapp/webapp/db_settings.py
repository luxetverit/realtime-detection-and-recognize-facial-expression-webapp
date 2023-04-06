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



AWS_SECRET = {
    'EMAIL_BACKEND': 'django_ses.SESBackend',
    'AWS_SES_REGION_NAME': 'ap-northeast-2',
    'AWS_SES_REGION_ENDPOINT': 'email-smtp.ap-northeast-2.amazonaws.com',
    'AWS_ACCESS_KEY_ID':'AKIAY67IOZYVWY3THHOD',
    'AWS_SECRET_ACCESS_KEY': 'BGU7+SaRupwNzKYk9hWxRczzUK35s00w8wN5PY4UBqDl'
}