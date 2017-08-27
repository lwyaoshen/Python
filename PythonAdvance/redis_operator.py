
import redis
PASSWORD = None
HOST = '127.0.0.1'
PORT = 6379
'''
redis 模块使用可以分类为：
连接方式
连接池
操作
String操作
Hash操作
List操作
Set操作
Sort Set操作
管道
发布订阅
'''
class RedisClient(object):
    def __init__(self, host=HOST, port=PORT,use_pool=True):
        if use_pool:
            pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
            self._db = redis.StrictRedis(connection_pool=pool)
            return;
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)


    '''
    string操作
    redis中的String在在内存中按照一个name对应一个value来存储的。
    set(name, value, ex=None, px=None, nx=False, xx=False)
    参数：
    ex，过期时间（秒）
    px，过期时间（毫秒）
    nx，如果设置为True，则只有name不存在时，当前set操作才执行
    xx，如果设置为True，则只有name存在时，岗前set操作才执行
    '''
    def set_str(self,key, value, ex=None, px=None, nx=False, xx=False):
        self._db.set(key, value, ex=None, px=None, nx=False, xx=False)

    '''
    setnx(name,value)
    设置值，只有name不存在时，执行设置操作（添加）
    '''
    def set_nx(self,name,value):
        self._db.setnx(name,value)
    '''
    setex(name,value,time)
    time，过期时间（数字秒 或 timedelta对象）
    '''
    def set_ex(self,name,value,time):
        self._db.setex(name,value,time)

    '''
    psetex(name,time_ms,value)
    time_ms，过期时间（数字毫秒 或 timedelta对象）
    '''
    def ps_set(self,name,time_ms,value):
        self._db.psset(name,time_ms,value)
    '''
    mset(*args, **kwargs)
    #批量设置值 
    #如：
    #mset(k1='v1', k2='v2')
    '''
    def m_set(self,*args, **kwargs):
        self._db.mset(*args, **kwargs)
    '''
    get(name)
    #获取值
    '''
    def get(self,key):
        return self._db.get(key)
    '''
    getrange(key, start, end)
    # 获取子序列（根据字节获取，非字符）
    # 参数：
    # name，Redis 的 name
    # start，起始位置（字节）
    # end，结束位置（字节）
    '''
    def get_range(self,key,start,end):
        return self._db.getrange(key.start,end)

    '''
    settrange(name,offset,value)
    # 修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加）
    # 参数：
    # offset，字符串的索引，字节（一个汉字三个字节）
    # value，要设置的值
    '''
    def set_trange(self,name,offset,value):
        self._db.settrange(name,offset,value)

    '''
    setbit(name,offset,value)
    # 对name对应值的二进制表示的位进行操作
    # 参数：
    # name，redis的name
    # offset，位的索引（将值变换成二进制后再进行索引）
    # value，值只能是 1 或 0  
    # 注：如果在Redis中有一个对应： n1 = "foo"，
    #那么字符串foo的二进制表示为：01100110 01101111 01101111
    #所以，如果执行 setbit('n1', 7, 1)，则就会将第7位设置为1，
    #那么最终二进制则变成 01100111 01101111 01101111，即："goo"
    # 扩展，转换二进制表示：# source = "武沛齐"
    '''
    def set_bit(self,name,offset,value):
        self._db.setbit(name,offset,value)
    '''
    getbit(name,offset)
    # 获取name对应的值的二进制表示中的某位的值 （0或1）
    '''
    def get_bit(self,name,offset):
        return self._db.getbit(name,offset)
    '''
    bitcount(key,start=None,end=None)
    # 获取name对应的值的二进制表示中 1 的个数
    # 参数：
    # key，Redis的name
    # start，位起始位置
    # end，位结束位置
    '''
    def bit_count(self,key,start=None,end=None):
        return self._db.bitcount(key,start,end)
    '''
    bitop(operation,dest,*keys)
    # 获取多个值，并将值做位运算，将最后的结果保存至新的name对应的值
    # 参数：
    # operation,AND（并） 、 OR（或） 、 NOT（非） 、 XOR（异或）
    # dest, 新的Redis的name
    # *keys,要查找的Redis的name
    # 如：
    bitop("AND", 'new_name', 'n1', 'n2', 'n3')
    # 获取Redis中n1,n2,n3对应的值，然后讲所有的值做位运算（求并集），然后将结果保存 new_name 对应的值中
    '''
    def bit_top(self,operation,dest,*keys):
        return self._db.bitop(operation,dest,*keys)
    '''
    strlen(name)
    # 返回name对应值的字节长度（一个汉字3个字节）
    '''

    def str_len(self,name):
        return self._db.strlen(name)
    '''
    incr(self, name, amount = 1)
    # 自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
    # 参数：
    # name,Redis的name
    # amount,自增数（必须是整数）
    # 注：同incrby
    '''
    def in_cr(self, name, amount = 1):
        return self._db.incr(name,amount)

    '''
    incrbyfloat(self,name,amount=1.0)
    # 自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
    # 参数：
    # name,Redis的name
    # amount,自增数（浮点型）
    '''
    def incr_byfloat(self,name,amount=1.0):
        return self._db.incrbyfloat(name,amount=1.0)
    '''
    decr(self, name, amount=1)
    # 自减 name对应的值，当name不存在时，则创建name＝amount，否则，则自减。
    # 参数：
    # name,Redis的name
    # amount,自减数（整数）
    '''
    def de_cr(self,name,amount=1):
        return self._db.decr(name,amount)
    '''
    append(key,value)
    # 在redis name对应的值后面追加内容
    # 参数：
    key, redis的name
    value, 要追加的字符串
    '''
    def append(self,key,value):
        return self._db.append(key,value)
    '''
    hset(name,key,value)
    # name对应的hash中设置一个键值对（不存在，则创建；否则，修改）
    # 参数：
    # name，redis的name
    # key，name对应的hash中的key
    # value，name对应的hash中的value
    # 注：
    # hsetnx(name, key, value),当name对应的hash中不存在当前key时则创建（相当于添加）
    '''
    def h_set(self,name,key,value):
        self._db.hset(name,key,value)
    '''
    hmset(name,mapping)
    # 在name对应的hash中批量设置键值对
    # 参数：
    # name，redis的name
    # mapping，字典，如：{'k1':'v1', 'k2': 'v2'}
    # 如：
    # r.hmset('xx', {'k1':'v1', 'k2': 'v2'})
    '''
    def hm_set(self,name,mapping):
        self._db.hmset(name,mapping)
    '''
    hget(name,key)
    # 在name对应的hash中获取根据key获取value
    '''
    def h_get(self,name,key):
        self._db.hmset(name,key)
    '''
    hmget(name,keys,*args)
    # 在name对应的hash中获取多个key的值
    # 参数：
    # name，reids对应的name
    # keys，要获取key集合，如：['k1', 'k2', 'k3']
    # *args，要获取的key，如：k1,k2,k3
    # 如：
    # r.mget('xx', ['k1', 'k2'])
    # 或
    # print r.hmget('xx', 'k1', 'k2')
    '''
    def hm_get(self,name,keys,*args):
        return self._db.hmget(name,keys,*args)
    '''
    hgetall(name)
    #获取name对应hash的所有键值
    '''
    def h_getall(self, name):
        return self._db.hgetall(name)

    '''
    hlen(name)
    # 获取name对应的hash中键值对的个数
    '''
    def h_len(self, name):
        return self._db.hlen(name)
    '''
    hkeys(name)
    # 获取name对应的hash中所有的key的值
    '''
    def h_keys(self, name):
        return self._db.hkeys(name)

    '''
    hvals(name)
    # 获取name对应的hash中所有的value的值
    '''
    def h_vals(self, name):
        return self._db.hvals(name)

    '''
    hexists(name,key)
    # 检查name对应的hash是否存在当前传入的key
    '''
    def h_exists(self, name,key):
        return self._db.hexists(name,key)
    '''
    hdel(name,*key)
    # 将name对应的hash中指定key的键值对删除
    '''
    def h_del(self, name,*key):
        return self._db.hdel(name,*key)
    '''
    hincrby(name,key,amount=1)
    # 自增name对应的hash中的指定key的值，不存在则创建key=amount
    # 参数：
    # name，redis中的name
    # key， hash对应的key
    #amount，自增数（整数）
    '''
    def h_incrby(self, name,key,amount=1):
        return self._db.hincrby(name,key,amount)
    '''
    hincrbyfloat(name,key,amount=1.0)
    # 自增name对应的hash中的指定key的值，不存在则创建key=amount
    # 参数：
    # name，redis中的name
    # key， hash对应的key
    # amount，自增数（浮点数）
    # 自增name对应的hash中的指定key的值，不存在则创建key=amount
    '''
    def h_incrbyfloat(self, name,key,amount=1.0):
        return self._db.hincrbyfloat(name,key,amount)
    '''
    hscan(name,cursor=0,match=None,count=None)
    # 增量式迭代获取，对于数据大的数据非常有用，hscan可以实现分片的获取数据，   
    #并非一次       性将数据全部获取完，从而放置内存被撑爆
    # 参数：
    # name，redis的name
    # cursor，游标（基于游标分批取获取数据）
    # match，匹配指定key，默认None 表示所有的key
    # count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
 
    # 如：
    # 第一次：cursor1, data1 = r.hscan('xx', cursor=0, match=None, count=None)
    # 第二次：cursor2, data1 = r.hscan('xx', cursor=cursor1, match=None, count=None)
    # ...
    # 直到返回值cursor的值为0时，表示数据已经通过分片获取完毕
    '''
    def h_scan(self, name,cursor=0,match=None,count=None):
        return self._db.hscan(name,cursor,match,count)
    '''
    hscan_iter(name,match=None,count=None)
    # 利用yield封装hscan创建生成器，实现分批去redis中获取数据
    # 参数：
    # match，匹配指定key，默认None 表示所有的key
    # count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
    # 如：
    # for item in r.hscan_iter('xx'):
    #     print item
    '''
    def hscan_iter(self, name,match=None,count=None):
        return self._db.hscan_iter(name,match,count)
    '''
    lpush(name,values)
    # 在name对应的list中添加元素，每个新的元素都添加到列表的最左边
 
    # 如：
    # r.lpush('oo', 11,22,33)
    # 保存顺序为: 33,22,11
    # 扩展：
    # rpush(name, values) 表示从右向左操作
    '''
    def lpush(self, name,values):
        return self._db.lpush(name,values)
    '''
    lpushx(name,value)
    # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边
    # 更多：
    # rpushx(name, value) 表示从右向左操作
    '''
    def l_pushx(self, name,values):
        return self._db.lpushx(name,values)
    '''
    llen(name)
    # name对应的list元素的个数
    '''
    def l_len(self, name):
        return self._db.llen(name)
    '''
    linsert(name,where,refvalue,value)
    # 在name对应的列表的某一个值前或后插入一个新值
    # 参数：
    # name，redis的name
    # where，BEFORE或AFTER    
    # refvalue，标杆值，即：在它前后插入数据
    # value，要插入的数据
    '''
    def l_insert(self, name,where,refvalue,value):
        return self._db.llen(name,where,refvalue,value)
    '''
    r.lset(name,index,value)
    # 对name对应的list中的某一个索引位置重新赋值
 
    # 参数：
    # name，redis的name
    # index，list的索引位置
    # value，要设置的值
    '''
    def l_set(self, name,index,value):
        return self._db.lset(name,index,value)
    '''
    r.lrem(name,value,num)
    在name对应的list中删除指定的值
 
    # 参数：
    # name，redis的name
    # value，要删除的值
    # num，  num=0，删除列表中所有的指定值；
    # num=2,从前到后，删除2个；
    # num=-2,从后向前，删除2个;
    '''
    def l_rem(self, name,value,num):
        return self._db.lrem(name,value,num)
    '''
    lpop(name)
    # 在name对应的列表的左侧获取第一个元素并在列表中移除，返回值则是第一个元素
    # 更多：
    # rpop(name) 表示从右向左操作
    '''
    def l_pop(self, name):
        return self._db.l_pop(name)
    '''
    lindex(name,index)
    #在name对应的列表中根据索引获取列表元素
    '''
    def l_index(self, name,index):
        return self._db.lindex(name,index)
    '''
    ltrim(name,start,end)
    #在name对应的列表中移除没有在start-end索引之间的值
    # 参数：
    # name，redis的name
    # start，索引的起始位置
    # end，索引结束位置
    '''
    def l_trim(self, name,start,end):
        return self._db.ltrim(name,start,end)

    '''
    lrange(name,start,end)
    # 在name对应的列表分片获取数据
    # 参数：
    # name，redis的name
    # start，索引的起始位置
    # end，索引结束位置
    '''
    def l_range(self, name,start,end):
        return self._db.lrange(name,start,end)
    '''
    rpoplpush(src,dst)
    # 从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边
    # 参数：
    # src，要取数据的列表的name
    # dst，要添加数据的列表的name
    '''
    def r_poplpush(self, src,dst):
        return self._db.rpoplpush(src,dst)
    '''
    blpop(keys,timeout)
    # 将多个列表排列，按照从左到右去pop对应列表的元素
    # 参数：
    # keys，redis的name的集合
    # timeout，超时时间，当元素所有列表的元素获取完之后， 
    阻塞等待列表内有数据的时间（秒）, 0 表示永远阻塞
    # 更多：
    # r.brpop(keys, timeout)，从右向左获取数据
    '''
    def b_lpop(self, keys,timeout):
        return self._db.blpop(keys,timeout)
    '''
    brpoplpush(src,dst,timeout=0)
    # 从一个列表的右侧移除一个元素并将其添加到另一个列表的左侧
    # 参数：
    # src，取出并要移除元素的列表对应的name
    # dst，要插入元素的列表对应的name
    # timeout，当src对应的列表中没有数据时，阻塞等待其有数据的超时时间（秒），0 表示永远阻塞
    自定义增量迭代
    # 由于redis类库中没有提供对列表元素的增量迭代，如果想要循环name对应的列表的所有元素，那么就需要：
    # 1、获取name对应的所有列表
    # 2、循环列表
    # 但是，如果列表非常大，那么就有可能在第一步时就将程序的内容撑爆，
    所有有必要自定义一个增量迭代的功能：
 
    def list_iter(name):
    """
    自定义redis列表增量迭代
    :param name: redis中的name，即：迭代name对应的列表
    :return: yield 返回 列表元素
    """
    '''
    def b_rpoplpush(self, src,dst,timeout=0):
        return self._db.brpoplpush(src,dst,timeout)
    '''
    sadd(name,values)
    # name对应的集合中添加元素
    '''
    def s_add(self, name,values):
        return self._db.sadd(name,values)
    '''
    scard(name)
    #获取name对应的集合中元素个数
    '''
    def s_card(self, name):
        return self._db.scard(name)
    '''
    sdiff(keys,*args)
    #在第一个name对应的集合中且不在其他name对应的集合的元素集合
    '''
    def s_diff(self, keys,*args):
        return self._db.sdiff(keys,*args)
    '''
    sdiffstore(dest,keys,*args)
    # 获取第一个name对应的集合中且不在其他name对应的集合，再将其新加入到dest对应的集合中
    '''
    def s_diffstore(self, dest,keys,*args):
        return self._db.sdiffstore(dest,keys,*args)
    '''
    sinter(keys,*args)
    # 获取多一个name对应集合的并集
    '''
    def s_inter(self, keys,*args):
        return self._db.sinter(keys,*args)
    '''
    sinterstore(dest,keys.*args)
    # 获取多一个name对应集合的并集，再讲其加入到dest对应的集合中 
    '''
    def s_interstore(self, dest,keys,*args):
        return self._db.sinterstore(dest,keys,*args)
    '''
    sismember(name,value)
    # 检查value是否是name对应的集合的成员
    '''
    def s_ismember(self, name,value):
        return self._db.sismember(name,value)
    '''
    smembers(name)
    # 获取name对应的集合的所有成员
    '''
    def s_members(self, name):
        return self._db.smembers(name)
    '''
    smove(src,dst,value)
    # 将某个成员从一个集合中移动到另外一个集合
    '''
    def s_move(self, src,dst,value):
        return self._db.smove(src,dst,value)
    '''
    spop(name)
    # 从集合的右侧（尾部）移除一个成员，并将其返回
    '''
    def s_pop(self, name):
        return self._db.spop(name)
    '''
    srandmember(name,numbers)
    # 从name对应的集合中随机获取 numbers 个元素
    '''
    def s_randmember(self, name,numbers):
        return self._db.srandmember(name,numbers)
    '''
    srem(name,values)
    # 在name对应的集合中删除某些值
    '''
    def s_rem(self, name,values):
        return self._db.srem(name,values)
    '''
    sunion(keys,*args)
    # 获取多一个name对应的集合的并集
    '''
    def s_union(self, keys,*args):
        return self._db.sunion(keys,*args)
    '''
    sunionstore(dest,keys,*args)
    # 获取多一个name对应的集合的并集，并将结果保存到dest对应的集合中
    '''
    def s_unionstore(self, dest,keys,*args):
        return self._db.sunionstore(dest,keys,*args)
    '''
    sscan(name,cursor=0,match=None,count=None)
    # 同字符串的操作，用于增量迭代分批获取元素，避免内存消耗太大
    '''
    def s_scan(self, name,cursor=0,match=None,count=None):
        return self._db.sscan(name,cursor,match,count)
    '''
    sscan_iter(name,match=None,count=None)
    # 同字符串的操作，用于增量迭代分批获取元素，避免内存消耗太大
    '''
    def sscan_iter(self, name,match=None,count=None):
        return self._db.sscan_iter(name,match,count)
    '''
    zadd(name,*args,**kwargs)
    # 在name对应的有序集合中添加元素
    # 如：   
    # zadd('zz', 'n1', 1, 'n2', 2)
    # 或
    # zadd('zz', n1=11, n2=22)
    '''
    def z_add(self, name,*args,**kwargs):
        return self._db.zadd(name,*args,**kwargs)
    '''
    zcard(name)
    # 获取name对应的有序集合元素的数量
    '''
    def z_card(self, name):
        return self._db.zcard(name)
    '''
    zcount(name,min,max)
    # 获取name对应的有序集合中分数 在 [min,max] 之间的个数
    '''
    def z_count(self, name,min,max):
        return self._db.zcount(name,min,max)
    '''
    zincrby(name,value,amount)
    # 自增name对应的有序集合的 name 对应的分数
    '''
    def z_incrby(self, name,value,amount):
        return self._db.zincrby(name,value,amount)
    '''
    r.zrange(name, start, end, desc=False, withscores=Flase, score_cast_func=float)
    # 按照索引范围获取name对应的有序集合的元素
    # 参数：
    # name，redis的name
    # start，有序集合索引起始位置（非分数）
    # end，有序集合索引结束位置（非分数）
    # desc，排序规则，默认按照分数从小到大排序
    # withscores，是否获取元素的分数，默认只获取元素的值
    # score_cast_func，对分数进行数据转换的函数
    # 更多：
    # 从大到小排序
    # zrevrange(name, start, end, withscores=False, score_cast_func=float)
    # 按照分数范围获取name对应的有序集合的元素
    # zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float)
    # 从大到小排序
    # zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=float)
    '''
    def z_range(self, name, start, end, desc=False, withscores=False, score_cast_func=float):
        return self._db.zrange(name, start, end, desc, withscores, score_cast_func)
    '''
    zrank(name, value)
    # 获取某个值在 name对应的有序集合中的排行（从 0 开始）
    '''
    def z_rank(self, name, value):
        return self._db.zrank(name, value)
    '''
    zrangebylex(name, min, max, start=None, num=None)
    # 当有序集合的所有成员都具有相同的分值时，有序集合的元素会根据成员的 值
    #（lexicographical ordering）来进行排序，而这个命令则可以返回给定的有序集合键
    # key 中， 元素的值介于 min 和 max 之间的成员
    # 对集合中的每个成员进行逐个字节的对比（byte-by-byte compare）， 并按照从低到高的顺序， 返回排序后的集合成员。 如果两个字符串有一部分内容是相同的话， 那么命令会认为较长的字符串比较短的字符串要大
    # 参数：
    # name，redis的name
    # min，左区间（值）。 + 表示正无限； - 表示负无限； ( 表示开区间； [ 则表示闭区间
    # min，右区间（值）
    # start，对结果进行分片处理，索引位置
    # num，对结果进行分片处理，索引后面的num个元素
    # 如：
    # ZADD myzset 0 aa 0 ba 0 ca 0 da 0 ea 0 fa 0 ga
    # r.zrangebylex('myzset', "-", "[ca") 结果为：['aa', 'ba', 'ca']
    # 更多：
    # 从大到小排序
    # zrevrangebylex(name, max, min, start=None, num=None)
    '''
    def z_rangebylex(self, name, min, max, start=None, num=None):
        return self._db.zrangebylex(name, min, max, start, num)
    '''
    zrem(name, values)
    # 删除name对应的有序集合中值是values的成员
    # 如：zrem('zz', ['s1', 's2'])
    '''
    def z_rem(self, name, values):
        return self._db.zrem(name, values)
    '''
    zremrangebyrank(name, min, max)
    # 根据排行范围删除
    '''
    def z_remrangebyrank(self, name, min, max):
        return self._db.zremrangebyrank(name, min, max)
    '''
    zremrangebyscore(name, min, max)
    # 根据分数范围删除
    '''
    def z_remrangebyscore(self, name, min, max):
        return self._db.zremrangebyscore(name, min, max)
    '''
    zremrangebylex(name, min, max)
    # 根据值返回删除
    '''
    def z_remrangebylex(self, name, min, max):
        return self._db.zremrangebylex(name, min, max)
    '''
    zscore(name, values)
    # 获取name对应有序集合中 value 对应的分数
    '''
    def z_score(self, name, values):
        return self._db.zscore(name, values)
    '''
    zinterstore(dest, keys, aggregate=None)
    # 获取两个有序集合的交集，如果遇到相同值不同分数，则按照aggregate进行操作
    # aggregate的值为:  SUM  MIN  MAX
    '''
    def z_interstore(self, dest, keys, aggregate=None):
        return self._db.zinterstore(dest, keys, aggregate)
    '''
    zunionstore(dest, keys, aggregate=None)
    # 获取两个有序集合的并集，如果遇到相同值不同分数，则按照aggregate进行操作
    # aggregate的值为:  SUM  MIN  MAX
    '''
    def z_unionstore(self, dest, keys, aggregate=None):
        return self._db.zunionstore(dest, keys, aggregate)
    '''
    zscan(name, cursor=0, match=None, count=None, score_cast_func=float)
    #  同字符串相似，相较于字符串新增score_cast_func，用来对分数进行操作
    '''
    def z_scan(self, name, cursor=0, match=None, count=None, score_cast_func=float):
        return self._db.zscan(name, cursor, match, count, score_cast_func)

    '''
    zscan_iter(name, match=None, count=None,score_cast_func=float)
    # 同字符串相似，相较于字符串新增score_cast_func，用来对分数进行操作 
    '''
    def zscan_iter(self,name, match=None, count=None,score_cast_func=float):
        return self._db.zscan_iter(name, match, count,score_cast_func)
    '''
    delete(*name)
    # 根据删除redis中的任意数据类型
    '''
    def delete(self,*name):
        return self._db.delete(*name)
    '''
    exists(name)
    # 检测redis的name是否存在
    '''
    def exists(self,name):
        return self._db.exists(name)
    '''
    keys(pattern='*')
    # 根据模型获取redis的name
 
    # 更多：
    # KEYS * 匹配数据库中所有 key 。
    # KEYS h?llo 匹配 hello ， hallo 和 hxllo 等。
    # KEYS h*llo 匹配 hllo 和 heeeeello 等。
    # KEYS h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo
    '''
    def keys(self,pattern='*'):
        return self._db.keys(pattern)
    '''
    expire(name,time)
    # 为某个redis的某个name设置超时时间
    '''
    def expire(self,name,time):
        return self._db.expire(name,time)
    '''
    rename(src, dst)
    # 对redis的name重命名为
    '''
    def rename(self,src, dst):
        return self._db.rename(src, dst)
    '''
    move(name,db)
    # 将redis的某个值移动到指定的db下
    '''
    def move(self,name,db):
        return self._db.move(name,db)
    '''
    randomkey()
    # 随机获取一个redis的name（不删除）
    '''
    def randomkey(self):
        return self._db.randomkey()
    '''
    type(name)
    # 获取name对应值的类型
    '''
    def type(self,name):
        return self._db.type(name)
    '''
    scan(cursor=0,match=None,count=None)
    # 同字符串操作，用于增量迭代获取key
    '''
    def scan(self,cursor=0,match=None,count=None):
        return self._db.scan(cursor,match,count)

    '''
    scan_iter(match=None,count=None)
    # 同字符串操作，用于增量迭代获取key
    '''
    def scan_iter(self,match=None,count=None):
        return self._db.scan_iter(match,count)
    '''
    redis默认在执行每次请求都会创建（连接池申请链接）和断开（归还连接池）一次连接操作，如果想要再一次请求中指定多个命令，则可以使用pipline实现一次请求指定多个命令，并且默认情况下一次pipline是原子性操作。
    '''
    def get_pipeline(self):
        pipe = self._db.pipeline(transaction=True)
        return pipe
if __name__=='__main__':
    r = RedisClient()
    r.set_str('name','yangsheng')

'''
import redis
class RedisHelper:
    #类
    def __init__(self):
        #链接
        self.__conn = redis.Redis(host='0.0.0.0')
        self.chan_sub = 'fm104.5'
        #创建频道
        self.chan_pub = 'fm104.5'
 
    def public(self,info):
        #公共的
        self.__conn.publish(self.chan_pub,info)
        #将内容发布到频道
        return True
 
    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub
        
        
发布者
from redis_demo.demo import RedisHelper
#实例化
obj = RedisHelper()
#把内容发布到频道
obj.public('python')
        
'''
'''
订阅者
from redis_demo.demo import RedisHelper
 
obj = RedisHelper()
redis_sub = obj.subscribe()
 
while True:
    msg= redis_sub.parse_response()
    print (msg)
    print(type(msg))
'''