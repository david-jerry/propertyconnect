"""
Base settings to build other settings files upon.
"""
from datetime import timedelta
from pathlib import Path


def gettext_noop(s):
    return s

import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# afriproperty/
APPS_DIR = ROOT_DIR / "afriproperty"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Africa/Lagos"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("af", gettext_noop("Afrikaans")),
    ("ar", gettext_noop("Arabic")),
    ("en", gettext_noop("English")),
    ("es", gettext_noop("Spanish")),
    ("fr", gettext_noop("French")),
    ("ig", gettext_noop("Igbo")),
]

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = ["he", "ar", "ar-dz", "fa", "ur"]

# Settings for language cookie
LANGUAGE_COOKIE_NAME = "django_language"
LANGUAGE_COOKIE_AGE = None
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = "/"
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SAMESITE = True

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]
DEFAULT_CHARSET = "utf-8"

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_ADMIN = [
    "tinymce",
    'filebrowser',
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "dal",
    "dal_select2",
    "admin_honeypot",
]

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # Handy template tags
    "django.forms",
]

THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    # Cookie consent
    "cookielaw",
    "category",
    # requand are only installed when someone else desires to use our repository after we push to github only for local use and not production ired for serving swagger api documentation
    "drf_yasg",
    # google translation
    'google_translate',
    # Shell commands with imports to all necessary models
    "shell_plus",
    # comments app
    "comment",
]

IPLOCATION_APIKEY = env(
    "IPLOCATION_APIKEY",
)

LOCAL_APPS = [
    "afriproperty.users.apps.UsersConfig",
    "afriproperty.property.apps.PropertyConfig",
    "afriproperty.tips.apps.TipsConfig",
    "afriproperty.core.apps.CoreConfig",
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_ADMIN + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "afriproperty.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"
LOGOUT_URL = "account_logout"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
DEFAULT_HASHING_ALGORITHM = "sha256"
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    # HTML Minification
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
    # Django default security middlewares
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE_CLASSES = MIDDLEWARE

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"
ADMIN_MEDIA_PREFIX = "/admin/media/"
# Maximum size, in bytes, of a request before it will be streamed to the
# file system instead of into memory.
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400  # i.e. 25.0 MB

# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400  # i.e. 2.5 MB

# Maximum number of GET/POST parameters that will be read before a
# SuspiciousOperation (TooManyFieldsSent) is raised.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000


# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "afriproperty.utils.context_processors.settings_context",
            ],
        },
    }
]

# Decimal separator symbol
DECIMAL_SEPARATOR = "."

# Boolean that sets whether to add thousand separator when formatting numbers
USE_THOUSAND_SEPARATOR = True
# Thousand separator symbol
THOUSAND_SEPARATOR = ","

# Number of digits that will be together, when splitting them by
# THOUSAND_SEPARATOR. 0 means no grouping, 3 means splitting by thousands...
NUMBER_GROUPING = 3

# Default primary key field type.
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "SAMEORIGIN"
# USE_X_FORWARDED_HOST = True

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 500

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "dashboard/"
ADMIN_DOC_URL = "dashboard/doc/"
ADMIN_FILEBROWSER_URL = "dashboard/filebrowser/"

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Jeremiah David (Darkcodr Codes)""", "server@darkcodr.codes")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"




# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 2
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
# login attempts security
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 600
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "afriproperty.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "afriproperty.users.adapters.SocialAccountAdapter"

# Allauth Custom forms
ACCOUNT_FORMS = {
    # "add_email": "allauth.account.forms.AddEmailForm",
    # "change_password": "allauth.account.forms.ChangePasswordForm",
    # "disconnect": "allauth.socialaccount.forms.DisconnectForm",
    # "login": "allauth.account.forms.LoginForm",
    # "reset_password": "allauth.account.forms.ResetPasswordForm",
    # "reset_password_from_key": "allauth.account.forms.ResetPasswordKeyForm",
    # "set_password": "allauth.account.forms.SetPasswordForm",
    "signup": "afriproperty.users.forms.UserCreationForm",
    # "signup": "allauth.socialaccount.forms.SignupForm",
}


# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Add Auth Token eg. [Bearer] [Paste JWT Token]": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
    "VALIDATOR_URL": [
        "http://127.0.0.1:3000",
        "http://192.168.99.101",
        "http://0.0.0.0:3000",
        "http://afriproperty.ng",
    ],
    "USE_SESSION_AUTH": True,
    "LOGIN_URL": LOGIN_URL,
    "LOGOUT_URL": LOGOUT_URL,
    "DOC_EXPANSION": None,
    "APIS_SORTER": None,
    "OPERATIONS_SORTER": None,
    "JSON_EDITOR": True,
    "SHOW_REQUEST_HEADERS": True,
    "SUPPORTED_SUBMIT_METHODS": ["get", "post", "put", "delete", "patch"],
    "ACCEPT_HEADER_VERSION": None,  # e.g. '1.0'
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=4),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"




# Your stuff...
# ------------------------------------------------------------------------------
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "JPEG"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"JPEG": ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True


JET_DEFAULT_THEME = "light-blue"
JET_SIDE_MENU_COMPACT = True
JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE = str(ROOT_DIR / "client_secrets.json")



PROFILE_APP_NAME = 'afriproperty.users'
PROFILE_MODEL_NAME = 'User'
COMMENT_SHOW_FLAGGED=True
COMMENT_FLAGS_ALLOWED=3
COMMENT_ALLOW_BLOCKING_USER=True
SCOMMENT_ALLOW_MODERATOR_TO_BLOCK=True


HTML_MINIFY = True
EXCLUDE_FROM_MINIFYING = ("/admin/*", "/jet/*", "/jet/dashboard/*")
KEEP_COMMENTS_ON_MINIFYING = True

# TINYMCE_JS_URL = str(APPS_DIR / "static/tinymce/tinymce.min.js") # "https://bizwallet-bucket.s3.amazonaws.com/static/tinymce/tinymce.min.js" #str(APPS_DIR / "/static/tinymce/tinymce.min.js")
# TINYMCE_JS_ROOT = str(APPS_DIR / "static/tinymce")  # "https://bizwallet-bucket.s3.amazonaws.com/static/tinymce" #str(APPS_DIR / "/static/tinymce")
# TINYMCE_JS_URL = "https://cdnjs.cloudflare.com/ajax/libs/tinymce/5.9.2/tinymce.min.js" #str(APPS_DIR / "/static/tinymce/tinymce.min.js")
# TINYMCE_JS_ROOT = str(ROOT_DIR / "staticfiles/tinymce") #cdnjs.cloudflare.com/ajax/libs/tinymce/4.5.1/" #str(APPS_DIR / "/static/js/")
# TINYMCE_DEFAULT_CONFIG = {
#     "theme": "silver",
#     "width": "100%",
#     'relative_urls': False,
#     "height": 500,
#     "menubar": False,
#     "statusbar": True,
#     "selector": "textarea",
#     "content_css": "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
#     "plugins": "a11ychecker,advcode,advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
#     "searchreplace,visualblocks,code,fullpage,fullscreen,insertdatetime,media,table,tabfocus,paste,"
#     "code,help,wordcount",
#     "toolbar": "undo redo | formatselect | code"
#     "bold italic backcolor | alignleft aligncenter "
#     "alignright alignjustify | bullist numlist outdent indent | "
#     "removeformat | help",
#     "menubar":"tools",
#     "custom_undo_redo_levels": 10,
#     "fullpage_default_doctype": '<!DOCTYPE html>',
#     "fullpage_default_encoding": 'UTF-8'
# }
# TINYMCE_SPELLCHECKER = True
# TINYMCE_COMPRESSOR = True

# Whether to append trailing slashes to URLs.
APPEND_SLASH = True
# COOKIE_CONSENT_NAME = "bizwallet_cookie_consent"
# COOKIE_CONSENT_DECLINE = 0
# COOKIE_CONSENT_ENABLED = lambda r: DEBUG or (r.user.is_authenticated() and r.user.is_field_worker and r.user.is_staff)
# PAYSTACK_PUB_API_KEY = ""
# PAYSTACK_SEC_API_KEY = ""
PAYSTACK_SECRET_KEY = env("PAYSTACK_SECRET_KEY")
GOOGLE_API_KEY = env("GOOGLE_API_KEY")
# API_KEY = env("API_KEY")
