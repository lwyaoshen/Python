'''

当您使用Scrapy时，您需要声明您所使用的设定。这可以通过使用环境变量: SCRAPY_SETTINGS_MODULE 来完成。

SCRAPY_SETTINGS_MODULE 必须以Python路径语法编写, 如 myproject.settings 。 注意，设定模块应该在 Python import search path 中。

获取设定值(Populating the settings)
设定可以通过多种方式设置，每个方式具有不同的优先级。 下面以优先级降序的方式给出方式列表:

命令行选项(Command line Options)(最高优先级)
每个spider的设定
项目设定模块(Project settings module)
命令默认设定模块(Default settings per-command)
全局默认设定(Default global settings) (最低优先级)
这些设定(settings)由scrapy内部很好的进行了处理，不过您仍可以使用API调用来手动处理。 详情请参考 设置(Settings) API.

这些机制将在下面详细介绍。

1. 命令行选项(Command line options)
命令行传入的参数具有最高的优先级。 您可以使用command line 选项 -s (或 --set) 来覆盖一个(或更多)选项。

样例:

scrapy crawl myspider -s LOG_FILE=scrapy.log
2. Settings per-spider
Spiders (See the Spiders chapter for reference) can define their own settings that will take precedence and override the project ones. They can do so by setting their scrapy.spiders.Spider.custom_settings attribute.

3. 项目设定模块(Project settings module)
项目设定模块是您Scrapy项目的标准配置文件。 其是获取大多数设定的方法。例如:: myproject.settings 。

4. 命令默认设定(Default settings per-command)
每个 Scrapy tool 命令拥有其默认设定，并覆盖了全局默认的设定。 这些设定在命令的类的 default_settings 属性中指定。

5. 默认全局设定(Default global settings)
全局默认设定存储在 scrapy.settings.default_settings 模块， 并在 内置设定参考手册 部分有所记录。

如何访问设定(How to access settings)
设定可以通过Crawler的 scrapy.crawler.Crawler.settings 属性进行访问。其由插件及中间件的 from_crawler 方法所传入:

class MyExtension(object):

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        if settings['LOG_ENABLED']:
            print "log is enabled!"
另外，设定可以以字典方式进行访问。不过为了避免类型错误， 通常更希望返回需要的格式。 这可以通过 Settings API 提供的方法来实现。

设定名字的命名规则
设定的名字以要配置的组件作为前缀。 例如，一个robots.txt插件的合适设定应该为 ROBOTSTXT_ENABLED, ROBOTSTXT_OBEY, ROBOTSTXT_CACHEDIR 等等。

内置设定参考手册
这里以字母序给出了所有可用的Scrapy设定及其默认值和应用范围。

如果给出可用范围，并绑定了特定的组件，则说明了该设定使用的地方。 这种情况下将给出该组件的模块，通常来说是插件、中间件或pipeline。 同时也意味着为了使设定生效，该组件必须被启用。

AWS_ACCESS_KEY_ID
默认: None

连接 Amazon Web services 的AWS access key。 S3 feed storage backend 中使用.

AWS_SECRET_ACCESS_KEY
默认: None

连接 Amazon Web services 的AWS secret key。 S3 feed storage backend 中使用。

BOT_NAME
默认: 'scrapybot'

Scrapy项目实现的bot的名字(也未项目名称)。 这将用来构造默认 User-Agent，同时也用来log。

当您使用 startproject 命令创建项目时其也被自动赋值。

CONCURRENT_ITEMS
默认: 100

Item Processor(即 Item Pipeline) 同时处理(每个response的)item的最大值。

CONCURRENT_REQUESTS
默认: 16

Scrapy downloader 并发请求(concurrent requests)的最大值。

CONCURRENT_REQUESTS_PER_DOMAIN
默认: 8

对单个网站进行并发请求的最大值。

CONCURRENT_REQUESTS_PER_IP
默认: 0

对单个IP进行并发请求的最大值。如果非0，则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定， 使用该设定。 也就是说，并发限制将针对IP，而不是网站。

该设定也影响 DOWNLOAD_DELAY: 如果 CONCURRENT_REQUESTS_PER_IP 非0，下载延迟应用在IP而不是网站上。

DEFAULT_ITEM_CLASS
默认: 'scrapy.item.Item'

the Scrapy shell 中实例化item使用的默认类。

DEFAULT_REQUEST_HEADERS
默认:

{
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}
Scrapy HTTP Request使用的默认header。由 DefaultHeadersMiddleware 产生。

DEPTH_LIMIT
默认: 0

爬取网站最大允许的深度(depth)值。如果为0，则没有限制。

DEPTH_PRIORITY
默认: 0

整数值。用于根据深度调整request优先级。

如果为0，则不根据深度进行优先级调整。

DEPTH_STATS
默认: True

是否收集最大深度数据。

DEPTH_STATS_VERBOSE
默认: False

是否收集详细的深度数据。如果启用，每个深度的请求数将会被收集在数据中。

DNSCACHE_ENABLED
默认: True

是否启用DNS内存缓存(DNS in-memory cache)。

DNSCACHE_SIZE
Default: 10000

DNS in-memory cache size.

DNS_TIMEOUT
Default: 60

Timeout for processing of DNS queries in seconds. Float is supported.

DOWNLOADER
默认: 'scrapy.core.downloader.Downloader'

用于crawl的downloader.

DOWNLOADER_MIDDLEWARES
默认:: {}

保存项目中启用的下载中间件及其顺序的字典。 更多内容请查看 激活下载器中间件 。

DOWNLOADER_MIDDLEWARES_BASE
默认:

{
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}
包含Scrapy默认启用的下载中间件的字典。 永远不要在项目中修改该设定，而是修改 DOWNLOADER_MIDDLEWARES 。更多内容请参考 激活下载器中间件.

DOWNLOADER_STATS
默认: True

是否收集下载器数据。

DOWNLOAD_DELAY
默认: 0

下载器在下载同一个网站下一个页面前需要等待的时间。该选项可以用来限制爬取速度， 减轻服务器压力。同时也支持小数:

DOWNLOAD_DELAY = 0.25    # 250 ms of delay
该设定影响(默认启用的) RANDOMIZE_DOWNLOAD_DELAY 设定。 默认情况下，Scrapy在两个请求间不等待一个固定的值， 而是使用0.5到1.5之间的一个随机值 * DOWNLOAD_DELAY 的结果作为等待间隔。

当 CONCURRENT_REQUESTS_PER_IP 非0时，延迟针对的是每个ip而不是网站。

另外您可以通过spider的 download_delay 属性为每个spider设置该设定。

DOWNLOAD_HANDLERS
默认: {}

保存项目中启用的下载处理器(request downloader handler)的字典。 例子请查看 DOWNLOAD_HANDLERS_BASE 。

DOWNLOAD_HANDLERS_BASE
默认:

{
    'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
    'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
}
保存项目中默认启用的下载处理器(request downloader handler)的字典。 永远不要在项目中修改该设定，而是修改 DOWNLOADER_HANDLERS 。

如果需要关闭上面的下载处理器，您必须在项目中的 DOWNLOAD_HANDLERS 设定中设置该处理器，并为其赋值为 None 。 例如，关闭文件下载处理器:

DOWNLOAD_HANDLERS = {
    'file': None,
}
DOWNLOAD_TIMEOUT
默认: 180

下载器超时时间(单位: 秒)。

DOWNLOAD_MAXSIZE
Default: 1073741824 (1024MB)

The maximum response size (in bytes) that downloader will download.

If you want to disable it set to 0.

注解

This size can be set per spider using download_maxsize spider attribute and per-request using download_maxsize Request.meta key.

This feature needs Twisted >= 11.1.
DOWNLOAD_WARNSIZE
Default: 33554432 (32MB)

The response size (in bytes) that downloader will start to warn.

If you want to disable it set to 0.

注解

This size can be set per spider using download_warnsize spider attribute and per-request using download_warnsize Request.meta key.

This feature needs Twisted >= 11.1.
DUPEFILTER_CLASS
默认: 'scrapy.dupefilters.RFPDupeFilter'

用于检测过滤重复请求的类。

默认的 (RFPDupeFilter) 过滤器基于 scrapy.utils.request.request_fingerprint 函数生成的请求fingerprint(指纹)。 如果您需要修改检测的方式，您可以继承 RFPDupeFilter 并覆盖其 request_fingerprint 方法。 该方法接收 Request 对象并返回其fingerprint(一个字符串)。

DUPEFILTER_DEBUG
默认: False

默认情况下， RFPDupeFilter 只记录第一次重复的请求。 设置 DUPEFILTER_DEBUG 为 True 将会使其记录所有重复的requests。

EDITOR
默认: depends on the environment

执行 edit 命令编辑spider时使用的编辑器。 其默认为 EDITOR 环境变量。如果该变量未设置，其默认为 vi (Unix系统) 或者 IDLE编辑器(Windows)。

EXTENSIONS
默认:: {}

保存项目中启用的插件及其顺序的字典。

EXTENSIONS_BASE
默认:

{
    'scrapy.extensions.corestats.CoreStats': 0,
    'scrapy.telnet.TelnetConsole': 0,
    'scrapy.extensions.memusage.MemoryUsage': 0,
    'scrapy.extensions.memdebug.MemoryDebugger': 0,
    'scrapy.extensions.closespider.CloseSpider': 0,
    'scrapy.extensions.feedexport.FeedExporter': 0,
    'scrapy.extensions.logstats.LogStats': 0,
    'scrapy.extensions.spiderstate.SpiderState': 0,
    'scrapy.extensions.throttle.AutoThrottle': 0,
}
可用的插件列表。需要注意，有些插件需要通过设定来启用。默认情况下， 该设定包含所有稳定(stable)的内置插件。

更多内容请参考 extensions用户手册 及 所有可用的插件 。

ITEM_PIPELINES
默认: {}

保存项目中启用的pipeline及其顺序的字典。该字典默认为空，值(value)任意。 不过值(value)习惯设定在0-1000范围内。

为了兼容性，ITEM_PIPELINES 支持列表，不过已经被废弃了。

样例:

ITEM_PIPELINES = {
    'mybot.pipelines.validate.ValidateMyItem': 300,
    'mybot.pipelines.validate.StoreMyItem': 800,
}
ITEM_PIPELINES_BASE
默认: {}

保存项目中默认启用的pipeline的字典。 永远不要在项目中修改该设定，而是修改 ITEM_PIPELINES 。

LOG_ENABLED
默认: True

是否启用logging。

LOG_ENCODING
默认: 'utf-8'

logging使用的编码。

LOG_FILE
默认: None

logging输出的文件名。如果为None，则使用标准错误输出(standard error)。

LOG_FORMAT
Default: '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

String for formatting log messsages. Refer to the Python logging documentation for the whole list of available placeholders.

LOG_DATEFORMAT
Default: '%Y-%m-%d %H:%M:%S'

String for formatting date/time, expansion of the %(asctime)s placeholder in LOG_FORMAT. Refer to the Python datetime documentation for the whole list of available directives.

LOG_LEVEL
默认: 'DEBUG'

log的最低级别。可选的级别有: CRITICAL、 ERROR、WARNING、INFO、DEBUG。更多内容请查看 Logging 。

LOG_STDOUT
默认: False

如果为 True ，进程所有的标准输出(及错误)将会被重定向到log中。例如， 执行 print 'hello' ，其将会在Scrapy log中显示。

MEMDEBUG_ENABLED
默认: False

是否启用内存调试(memory debugging)。

MEMDEBUG_NOTIFY
默认: []

如果该设置不为空，当启用内存调试时将会发送一份内存报告到指定的地址；否则该报告将写到log中。

样例:

MEMDEBUG_NOTIFY = ['user@example.com']
MEMUSAGE_ENABLED
默认: False

Scope: scrapy.extensions.memusage

是否启用内存使用插件。当Scrapy进程占用的内存超出限制时，该插件将会关闭Scrapy进程， 同时发送email进行通知。

See 内存使用扩展(Memory usage extension).

MEMUSAGE_LIMIT_MB
默认: 0

Scope: scrapy.extensions.memusage

在关闭Scrapy之前所允许的最大内存数(单位: MB)(如果 MEMUSAGE_ENABLED为True)。 如果为0，将不做限制。

See 内存使用扩展(Memory usage extension).

MEMUSAGE_NOTIFY_MAIL
默认: False

Scope: scrapy.extensions.memusage

达到内存限制时通知的email列表。

Example:

MEMUSAGE_NOTIFY_MAIL = ['user@example.com']
See 内存使用扩展(Memory usage extension).

MEMUSAGE_REPORT
默认: False

Scope: scrapy.extensions.memusage

每个spider被关闭时是否发送内存使用报告。

查看 内存使用扩展(Memory usage extension).

MEMUSAGE_WARNING_MB
默认: 0

Scope: scrapy.extensions.memusage

在发送警告email前所允许的最大内存数(单位: MB)(如果 MEMUSAGE_ENABLED为True)。 如果为0，将不发送警告。

NEWSPIDER_MODULE
默认: ''

使用 genspider 命令创建新spider的模块。

样例:

NEWSPIDER_MODULE = 'mybot.spiders_dev'
RANDOMIZE_DOWNLOAD_DELAY
默认: True

如果启用，当从相同的网站获取数据时，Scrapy将会等待一个随机的值 (0.5到1.5之间的一个随机值 * DOWNLOAD_DELAY)。

该随机值降低了crawler被检测到(接着被block)的机会。某些网站会分析请求， 查找请求之间时间的相似性。

随机的策略与 wget --random-wait 选项的策略相同。

若 DOWNLOAD_DELAY 为0(默认值)，该选项将不起作用。

REACTOR_THREADPOOL_MAXSIZE
Default: 10

The maximum limit for Twisted Reactor thread pool size. This is common multi-purpose thread pool used by various Scrapy components. Threaded DNS Resolver, BlockingFeedStorage, S3FilesStore just to name a few. Increase this value if you’re experiencing problems with insufficient blocking IO.

REDIRECT_MAX_TIMES
默认: 20

定义request允许重定向的最大次数。超过该限制后该request直接返回获取到的结果。 对某些任务我们使用Firefox默认值。

REDIRECT_MAX_METAREFRESH_DELAY
默认: 100

有些网站使用 meta-refresh 重定向到session超时页面， 因此我们限制自动重定向到最大延迟(秒)。 =>有点不肯定:

REDIRECT_PRIORITY_ADJUST
默认: +2

修改重定向请求相对于原始请求的优先级。 负数意味着更多优先级。

ROBOTSTXT_OBEY
默认: False

Scope: scrapy.downloadermiddlewares.robotstxt

如果启用，Scrapy将会尊重 robots.txt策略。更多内容请查看 RobotsTxtMiddleware 。

SCHEDULER
默认: 'scrapy.core.scheduler.Scheduler'

用于爬取的调度器。

SPIDER_CONTRACTS
默认:: {}

保存项目中启用用于测试spider的scrapy contract及其顺序的字典。 更多内容请参考 Spiders Contracts 。

SPIDER_CONTRACTS_BASE
默认:

{
    'scrapy.contracts.default.UrlContract' : 1,
    'scrapy.contracts.default.ReturnsContract': 2,
    'scrapy.contracts.default.ScrapesContract': 3,
}
保存项目中默认启用的scrapy contract的字典。 永远不要在项目中修改该设定，而是修改 SPIDER_CONTRACTS 。更多内容请参考 Spiders Contracts 。

SPIDER_LOADER_CLASS
Default: 'scrapy.spiderloader.SpiderLoader'

The class that will be used for loading spiders, which must implement the SpiderLoader API.

SPIDER_MIDDLEWARES
默认:: {}

保存项目中启用的下载中间件及其顺序的字典。 更多内容请参考 激活spider中间件 。

SPIDER_MIDDLEWARES_BASE
默认:

{
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}
保存项目中默认启用的spider中间件的字典。 永远不要在项目中修改该设定，而是修改 SPIDER_MIDDLEWARES 。更多内容请参考 激活spider中间件.

SPIDER_MODULES
默认: []

Scrapy搜索spider的模块列表。

样例:

SPIDER_MODULES = ['mybot.spiders_prod', 'mybot.spiders_dev']
STATS_CLASS
默认: 'scrapy.statscollectors.MemoryStatsCollector'

收集数据的类。该类必须实现 状态收集器(Stats Collector) API.

STATS_DUMP
默认: True

当spider结束时dump Scrapy状态数据 (到Scrapy log中)。

更多内容请查看 数据收集(Stats Collection) 。

STATSMAILER_RCPTS
默认: [] (空list)

spider完成爬取后发送Scrapy数据。更多内容请查看 StatsMailer 。

TELNETCONSOLE_ENABLED
默认: True

表明 telnet 终端 (及其插件)是否启用的布尔值。

TELNETCONSOLE_PORT
默认: [6023, 6073]

telnet终端使用的端口范围。如果设置为 None 或 0 ， 则使用动态分配的端口。更多内容请查看 Telnet终端(Telnet Console) 。

TEMPLATES_DIR
默认: scrapy模块内部的 templates

使用 startproject 命令创建项目时查找模板的目录。

URLLENGTH_LIMIT
默认: 2083

Scope: spidermiddlewares.urllength

爬取URL的最大长度。更多关于该设定的默认值信息请查看: http://www.boutell.com/newfaq/misc/urllength.html

'''