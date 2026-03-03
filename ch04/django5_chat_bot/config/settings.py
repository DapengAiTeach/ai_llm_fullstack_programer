from pathlib import Path

# 项目的根目录
BASE_DIR = Path(__file__).resolve().parent.parent
# 安全密钥，随机生成，很重要
SECRET_KEY = 'django-insecure-y*=r_#ln3rq-29)*%ka!=!dsy9vfjd1w0k_rnk-4)t9aixfr2('
# 是否开启调试，部署的时候一定要关闭
DEBUG = True
# 允许访问网站的的域名
# 开发的时候，可以用 * 表示所有
# 部署的时候，只能用自己访问的域名，否则会有安全问题
ALLOWED_HOSTS = ["*"]
# 根路由配置，一般不会手动修改
ROOT_URLCONF = 'config.urls'
# WSGI应用配置，一般不会手动修改
WSGI_APPLICATION = 'config.wsgi.application'
# 语言和时区配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 安装的app，包含Django内置的APP以及我们后续自己开发的APP
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 自定义的APP
    'apps.chatbot',
    'apps.home',
]

# 中间件，顺序不能乱，且非常重要
# 后续我们可能开发自己的中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 数据库配置，Django默认支持SQlite，也支持MySQL、PostgreSQL、Oracle、SQL Server
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# 默认数据库主键类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 密码验证器
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 静态文件配置
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
