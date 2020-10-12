# imetadata
时空数据入库管理引擎

# 运行与设置
## 系统运行命令
在iMetaData子目录下, 运行命令行
```
python.exe ScheduleCreator.py
python.exe ScheduleCreator.py -log /your_log_file_path
```

## 设置
### 全局设置
在iMetaData子目录下, 修改配置文件settings.py
1. 示例
```python
application = {
    'databases': [
        {'id': '0', 'type': 'postgresql',
         'host': '127.0.0.1', 'port': '5432', 'database': 'test', 'username': 'postgres', 'password': 'postgres'}
    ],
    'directory': {
        'work': ''
    },
    'metadata': {
        'directory': {
            'view': ''
        },
        'plugins': {
            'dir': [
                {'plugin': ['plugins_1000_dom_10', 'plugins_1000_dom_12'], 'keyword': 'dom'},
                {'plugin': ['plugins_1010_dem_10', 'plugins_1010_dem_12'], 'keyword': 'dem'}
            ]
        }
    }
}
```
1. databases
    * 数据库配置节点
    * 配置内容为数组, 可支持多个数据库同时连接
    * 每一个数据库的配置说明:
        * id: 数据库的标识, 配置后, 在代码中可以使用CFactory().give_me_db('[id]')来直接访问该数据库
        * type: 数据库类型, 目前支持postgresql和mysql
        * host: 数据库ip地址
        * port: 数据库访问端口号
        * database: 数据库名称
        * username: 用户名
        * password: 密码(暂时存储明文, 后期改为密文)
1. directory:
    * 目录配置
    * work: 工作路径, 为系统内置进行数据处理的临时目录, 建议大于20G
1. metadata:
    * 数据入库管理模块的专用配置
    * directory:
        * 数管的目录设置
        * view: 数管中用于存储空间数据快视图, 拇指图等文件的根目录, 存储空间自行根据每一个空间数据的元数据存储大小统计
    * plugins:
        * 自定义识别插件的配置
        * dir:
            * 目录识别插件的特定配置
            * 使用数组记录, 支持多个匹配模式
            * 每一个匹配模式的说明:
                * keyword: 
                    * 关键字, 目录必须等于关键词, 则目录下的文件, 按plugin中的设置顺序识别
                    * 注意: 如果关键字为空, 则所有子目录都优先按plugin中的插件顺序识别
                * plugin:
                    * 匹配关键字的目录下, 将按插件顺序识别
                    * 使用数组记录, 支持多个插件
                    * 识别顺序为从左到右
        * 自定义识别插件后, 仍然无法识别的数据, 系统将按内置的插件识别

### 其他配置
#### 数管
##### 自定义目录识别插件
1. 在目录下, 添加特定的标识文件, 用于管理和控制目录下的数据识别
1. 标识文件: metadata.rule
1. 标识文件的格式为xml
样例:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
    <type>DOM</type>
    <plugins>
        <file>
            <plugin>plugins_1000_dom_10</plugin>
            <plugin>plugins_1000_dom_12</plugin>
        </file>
        <dir>
            <plugin>plugins_1000_dom_10</plugin>
            <plugin>plugins_1000_dom_12</plugin>
        </dir>
    </plugins>
</root>
```
说明:
1. root: (*) 根节点, 不可修改和缺失
1. type: (*) 当前目录的业务类型, 等同于将目录名改为type节点中的名称, 不可修改和缺失
    * 示例中为dom, 则表明该目录将按dom类型进行数据识别
    * dom类型的识别, 参见全局设置中数管plugins的配置, 此类型等于keyword
1. plugins: (可选) 也可以在此文件中直接设置目录下识别的插件
    * 需要分别在file和dir子目录下设置文件和子目录的识别
    * 识别顺序为从上到下

    **注意: 在这里设置识别的插件后, 系统将忽略全局设置中的插件!!!**


# 说明
## 任务登记
1. 任务是指需要运行的并行或定时处理的工作, 包括一系列的判断, 处理, 操作目录和数据库等等(理解即可)
1. 任务的代码, 在一个特定类中编写, 这个类要依照特定的规范, 存储在特定的目录下(开发人员了解即可)
1. 任务的启动, 停止等管理, 在数据表sch_center_mission表中
1. 每一条记录, 是一个任务, 根据scmTrigger的不同, 可以分类为:
   * db_queue: 数据库队列, 特点: 从数据库队列中抢任务执行, 直至数据库队列中无任务
   * cron: 基于cron语法的时间调度, 特点: 如果任务时间长, 期间应执行的调度, 将被"消化"掉, 仅仅在任务执行完毕后的下一次运行
   * interval: 每隔x秒\分钟\小时\天\周\月, 指定的任务, 特点: 从上次任务结束后, 再过x单位时间, 下一次任务才执行
   * date: 指定时间运行一次的任务, 特点: 在规定的日期时间启动, 只运行一次
   * mem_queue: 后续会与rabbitmq, 或者redis等内存队列对接(暂未实现)
   * other: 其他(暂未实现)
1. 调度表sch_center_mission中的scmCommand和scmStatus配合, 完成并行的控制, 目前提供如下调度控制:
   * scmCommand=start&scmStatus=1: 启动调度
   * scmCommand=stop&scmStatus=1: 停止调度
     如果需要加速或减速, 只能停止调度->修改调度配置->启动调度
   * 当所有记录!!!的scmCommand=shutdown&scmStatus=0: 调度停止, 且调度系统关闭退出
1. sch_center_mission中可以登记的任务, 其处理算法为特定类, 该类存储在imetadata\job子目录下, 该子目录下子目录是任务触发的类型, 具体参见上面对
scmTrigger的描述, 字段scmAlgorithm就负责记录具体类型子目录下的类名称(不包含.py扩展名), 如:
   * db_queue类型下有job_dm_root_parser.py
     就可以在数据表中登记: 

     |scmTrigger|scmAlgorithm|说明|
     |  ----  | ----  | ----  |
     |db_queue|job_dm_root_parser|根目录扫描调度, 处理dm2_storage表队列, dsStatus:0->1->2->0|

1. scmParams是具体任务执行的参数, 格式为Json, 根据不同的scmTrigger, 参数可以进行自定义, 多个参数, 可以结合:

     |scmTrigger|scmParams|说明|样例|
     |  ----  | ----  | ----  | ----  |
     |interval|trigger.start_date|可选, 任务调度的有效开始时间|{"trigger": {"start_date": "2020-01-01 11:11:11"}}|
     |interval|trigger.end_date|可选, 任务调度的有效结束时间|{"trigger": {"end_date": "2020-01-20 11:11:11"}}|
     |interval|trigger.seconds|可选, 但是下面的时间间隔至少有一个!, 每隔x秒执行一次|{"trigger": {"seconds": 30}}|
     |interval|trigger.minutes|可选, 每隔x分钟执行一次|{"trigger": {"minutes": 30}}|
     |interval|trigger.hours|可选, 每隔x小时执行一次|{"trigger": {"hours": 2}}|
     |interval|trigger.days|可选, 每隔x小时执行一次|{"trigger": {"days": 2}}|
     |interval|trigger.weeks|可选, 每隔x星期执行一次|{"trigger": {"weeks": 2}}|
     |db_queue|job.db_server_id|数据库队列, 引用的数据库的标识, 该标识在settings.py中定义|{"job": {"db_server_id": 2}}|
     |db_queue|process.parallel_count|并行worker的个数|{"process": {"parallel_count": 1}}|


# 进度

## 插件
 |类型|名称|开发人|进度|说明|
 |  ----  |  ----  |  ----  | ----  | ----  |
 |卫星数据插件| GF1-PMS |赵宇飞|完成|高分一号PMS传感器|


## 调度
 |类型|进度|开发人|算法|说明|
 |  ----  |  ----  |  ----  | ----  | ----  |
 |db_queue| 已完成 |wangxy|job_dm_root_parser|根目录扫描调度, 处理dm2_storage表队列, dsStatus:0->1->2->0|
 |db_queue| 已完成 |zhaoyf, wangxy|job_dm_path2object|目录识别对象调度, 处理dm2_storage_directory表队列, dsScanStatus:0->1->2->0|
 |db_queue| 已完成 |zhaoyf, wangxy|job_dm_path_parser|目录下的子目录扫描调度, 处理dm2_storage_directory表队列, dsScanFileStatus:0->1->2->0|
 |db_queue| 已完成 |zhaoyf, wangxy|job_dm_file2object|目录识别对象调度, 处理dm2_storage_directory表队列, dsScanStatus:0->1->2->0|
 |db_queue| 进行中 |zhaoyf|job_dm_obj_tags|对象的标签自动识别|
 |db_queue| 进行中 |zhaoyf|job_dm_obj_detail|对象的附属文件解析|
 |db_queue| 进行中 |zhaoyf|job_dm_obj_metadata|对象的质检及元数据解析|

## 框架
 |进度|说明|
 | ---- | ---- |
 |已完成|支持在metadata.rule中设置当前目录下的文件的优先识别插件|
 |已完成|支持在应用程序配置中, 设置特定目录下的文件的优先识别插件|
  
# 设计
## 数管与其他支撑系统的边界设计
### 核心算法
1. 数管的对象中, 增加版本号, 该版本号为一个整数, 每一次修改, 该对象的版本号都将增加1
1. 数管的对象中, 有质检结果字段, 其中描述对象的各方面质量评价和结果, 具体分为通过, 警告和未通过三个状态
1. 数管向其他子系统输出数据(后称: 出库)时, 建立了规则库, 在规则库中登记的子系统, 将按规则定义收到数据
    1. 规则库中定义了哪些数据可以自动交付更新到子系统
    1. 规则库中定义了哪些数据可以手工审批更新到子系统
1. 数管的每一个数据对象入库后, 将启动规则出库, 届时, 将扫描规则库中的每一个规则:
    1. 对符合规则要求的数据, 将加入到自动交付列表中
    1. 对于符合手工审批更新出库的数据, 将加入到手动交付列表中

### 扩展的功能
1. 重新发布
    1. 在规则发生变化后, 往往需要重新发布
    1. 首先, 将所有已发布数据的状态改为未确认
    1. 其次, 重新计算所有对象, 将符合规则要求的对象更新到发布数据列表中, 如果该对象已经在列表中, 则将状态改为确认
    1. 再次, 所有未确认的数据对象删除

## 数据管理
### 元数据处理
#### 基本内容
1. 元数据处理的内容:
    1. 质检
    1. 提取并解析实体元数据
    1. 提取并解析业务元数据
    1. 提取并解析时间元数据
    1. 提取并解析空间元数据
    1. 优化空间元数据
    
#### 具体描述
##### 质检
###### 质检的定义
1. 质检是一个贯穿性的处理过程
    1. 比如: 在将实体解压缩时, 实体解压失败, 需要记录到质检中
    1. 比如: 实体解压成功后, 对解压缩后的元数据, 实体数据进行检验, 也需要记录到质检中
1. 质检是一个随时会被打断的过程
    1. 如果实体解压缩失败, 则后续的元数据提取, 影像数据可读性等质检过程都会中断
1. 质检是一个有层次的过程
    1. 实体解压缩成功, 才有后续的内容
    1. 实体元数据XML文件加载成功, 后续才能对元数据有效性进行检验

###### 质检的内容
1. 整体数据质检
    1. 整体数据可用性
        1. 数据是否可以打开
    1. 整体数据规范性
        1. 数据命名规范性
1. 数据实体质检
    1. 数据实体文件完整性
    1. 数据实体文件有效性
1. 元数据质检
    1. 业务元数据
        1. 元数据完整性
        1. 元数据文件有效性
        1. 元数据项合法性
    1. 数据元数据
        1. 数据实体格式合法性
        1. 数据元数据项合法性
        
###### 质检的结果
1. 质检的结果为xml格式文件
1. 质检的结果为分层次的节点


#### 卫星数据
##### 数据结构
1. 卫星数据压缩包, 一般数据压缩包以tar.gz, rar, zip等压缩包扩展名存储
1. 卫星数据解压缩后, 目录名与卫星数据主名相同, 一个目录中, 卫星的数据都在这个子目录下
1. 多个卫星数据解压缩在一个目录下, 目录名字没有规范, 但是这些卫星数据都在这一个目录下

#### 识别模式
1. 如果是目录
    1. 对目录名称进行关键字识别
    1. 对目录下的文件进行进一步识别
1. 如果是文件
    1. 如果文件扩展名是常用的压缩包
    1. 如果文件主名匹配特征码
    1. 将文件识别为对象

# 2020-09-18
## 数据管理并行处理算法
### 根目录扫描调度
1. 名称: job_dm_root_parser
1. 类型: db_queue
1. 算法:
   1. 抢占dm2_storage表中dstScanStatus=1的记录, 状态更新为2
   1. 检查dm2_storage_directory表中是否有对应的根目录, 加入到dm2_storage_directory表中, 注意设置如下状态:
        * dsd_directory_valid=1(待确认)
        * dsdScanFileStatus=1
        * scanStatus=1
   1. 将处理成功的记录, dm2_storage表dstScanStatus设置为0

### 目录识别调度
1. 名称: job_dm_path2object
1. 类型: db_queue
1. 算法:
   1. 抢占dm2_storage_directory表中dsdScanStatus=1的记录, 状态更新为2
   1. 检查目录是否存在
        1. 目录不存在:
            * 标记当前目录及以下的文件(递归)的dsfFileValid=0无效(为了高效处理)
                * dsfScanStatus=0
                * dsfFileValid=0
            * 标记当前目录及以下的子目录(递归)为dsd_directory_valid=0无效(为了高效处理)
                * dsdScanStatus=0
                * dsdScanFileStatus=0
                * dsdScanDirStatus=0
                * dsd_directory_valid=0
        1. 目录存在:
            * 检查并判断指定的元数据扫描规则文件是否与数据库中的记录相等(都是空也算相等)
                * 如果和记录中的不同
                    * 删除当前目录下的所有子目录, 文件 和对象
                    * 更新记录中的规则
                    * 设置子目录扫描状态为正常
                        * dsdScanFileStatus=1
                        * dsdScanDirStatus=1
                        * dsd_directory_valid=-1
                * 如果和记录中的相同
                    * 不处理
            * 设置当前目录的dsd_directory_valid=-1有效
            * 目录当前情况下是否是对象
                * 不知道是不是对象
                    * 开始判断是何种对象
                    * 更新对象字段
                * 是, 可能是, 不是
                    * 判断目录的最后修改时间和记录中的时间是否一致
                        * 如果无更新: 不再继续
                        * 如果有更新
                            * ***更新最后修改时间到记录中!!!(这里做, 因此, 在[目录扫描文件和子目录调度]中不能做!)***
                            * 删除旧的对象记录
                    * 开始判断是何种对象
                    * 更新对象字段
                * 识别后的结果:
                    * 不知道是不是对象
                        * dsdScanFileStatus=1
                        * dsdScanDirStatus=1
                        * dsd_directory_valid=-1
                    * 是, 可能是, 不是
                        * dsdScanFileStatus=0
                        * dsdScanDirStatus=0
                        * dsd_directory_valid=-1
   1. 将处理成功的dm2_storage_directory记录
        1. dsdScanStatus=0
   
### 目录扫描文件和子目录调度
1. 名称: job_dm_path_parser
1. 类型: db_queue
1. 算法:
   1. 抢占dm2_storage_directory表中dsdScanStatus=0&dsdScanFileStatus=1&dsd_directory_valid=-1(存在)的记录, 状态dsdScanFileStatus更新为2
   1. 将当前目录下的子目录的dsd_directory_valid改为1(待确认), 注意不是递归
   1. 将当前目录下的文件的dsfFileValid改为1(待确认), 注意不是递归
   1. 扫描目录下的文件和子目录:
        1. 黑白名单检化验
            1. 未通过
                1. 不处理, 进行下一个
            1. 通过
                1. 如果是子目录
                    1. 检查dm2_storage_directory中是否有匹配的记录
                        1. 如有对应记录
                            1. 检查目录最后修改时间, 与匹配的记录是否相同
                                1. 如果相同
                                    * dsdScanStatus=0
                                    * dsdScanFileStatus=0
                                    * dsd_directory_valid=-1 
                                1. 如果不同
                                    * ***这里不能更新记录的信息, 否则在对象识别调度中就无法判断时间有效性了!!!***
                                    * dsdScanStatus=1
                                    * dsdScanFileStatus=1
                                    * dsd_directory_valid=1 (这里是1或-1都无关系, 对象识别时, 还是要判断一下) 
                        1. 如果没有对应记录
                            1. 添加记录
                            1. 注意如下状态:
                               * dsdScanStatus=1
                               * dsdScanFileStatus=1
                               * dsd_directory_valid=-1 (这里是1或-1都无关系, 对象识别时, 还是要判断一下)
                1. 如果是文件
                    1. 检查dm2_storage_file中是否有匹配的记录
                        1. 如有对应记录
                            1. 检查文件的大小和最后修改时间, 与匹配的记录是否相同
                                1. 如果相同
                                    * dsfScanStatus=0
                                    * dsdFileValid=-1 
                                1. 如果不同
                                    * ***这里不能更新记录的信息, 否则在对象识别调度中就无法判断时间有效性了!!!***
                                    * dsdScanStatus=1
                                    * dsdFileValid=1 (这里是1或-1都无关系, 对象识别时, 还是要判断一下)
                        1. 如果没有对应记录
                            1. 添加记录
                            1. 注意如下状态:
                               * dsdScanStatus=1
                               * dsdFileValid=-1 (这里是1或-1都无关系, 对象识别时, 还是要判断一下)
   1. 将当前目录下的子目录的dsd_directory_valid=1(待确认)的, 都改为0(无效), 注意不是递归
   1. 将当前目录下的文件的dsfFileValid=1(待确认)的, 都改为0(无效), 注意不是递归
   1. 将处理成功的dm2_storage_directory记录
        1. dsdScanFileStatus=0
        1. dsdScanDirStatus=0

### 文件识别调度
1. 名称: job_dm_file2object
1. 类型: db_queue
1. 算法:
   1. 抢占dm2_storage_file表中dsfScanStatus=1的记录, 状态更新为2
   1. 检查文件是否存在
        1. 如果文件不存在:
            * 标记当前文件的dsfFileValid=0无效
        1. 文件存在:
            * 设置当前文件的dsfFileValid=-1有效
            * 文件当前情况下是否是对象
                * 不知道是不是对象
                    * 开始判断是何种对象
                    * 更新对象字段
                * 是, 可能是, 不是
                    * 判断文件的大小, 最后修改时间和记录中的是否一致
                        * 如果无更新: 不再继续
                        * 如果有更新
                            * ***更新最后修改时间到记录中!!!(这里做, 因此, 在[目录扫描文件和子目录调度]中不能做!)***
                            * 删除旧的对象记录
                    * 开始判断是何种对象
                    * 更新对象字段
   1. 将处理成功的dm2_storage_file记录
        1. dsfScanStatus=0

#### 对象标签处理调度
1. 名称: job_dm_obj_tags
1. 类型: db_queue
1. 算法:
   1. 抢占dm2_storage_object表中dsoTagsParserStatus=1的记录, 状态更新为2
   1. 根据对象类型, 解析对象的标签
        1. 业务标签
        1. 时间标签
        1. 空间标签
   1. 将处理成功的dm2_storage_object记录
        1. dsoTagsParserStatus=0

#### 对象详情处理调度
1. 名称: job_dm_obj_detail
1. 类型: db_queue
1. 算法:
   1. 抢占dm2_storage_object表中dsoDetailParserStatus=1的记录, 状态更新为2
   1. 根据对象类型, 清理对象的详情
   1. 根据对象类型, 重新注册对象的详情
   1. 将处理成功的dm2_storage_object记录
        1. dsoDetailParserStatus=0

#### 对象元数据处理调度
1. 名称: job_dm_obj_metadata
1. 类型: db_queue
1. 算法:
   1. 抢占dm2_storage_object表中dsoMetaDataParserStatus=1的记录, 状态更新为2
   1. 根据对象类型, 处理对象的元数据
        1. 创建虚拟内容对象
        1. 质检
        1. 提取并解析实体元数据
        1. 提取并解析业务元数据
        1. 提取并解析时间元数据
        1. 提取并解析空间元数据
        1. 优化空间元数据
        1. 清理虚拟内容对象
   1. 将处理成功的dm2_storage_object记录
        1. dsoMetaDataParserStatus=0

# 2020-09-05
扩展trigger的类型为
1. 数据库队列触发器
1. 时间触发器
   * 指定时间触发一次
   * 间隔指定秒数触发一次(注意:是从上次执行结束时间开始, 重新计时)
   * 根据cron语法, 定时触发(cron语法中有每隔n秒执行一次, 这里的计算, 将不考虑执行中所损耗的时间, 但中间积累的任务将被忽略)
1. 重新调整体系架构目录, 对重要的对象, 目录名称都进行了重新定义, 使结构更加清晰
1. 修改了数据表结构, 将数据库队列中的配置信息, 如并行个数等等, 都移到scmParams这个json字段中
调度执行器execute和调度工人job都可以访问这个参数, 进行个性化的处理
系统进行了基础测试, 主体架构基本成型.

# 2020-09-03
1. 不再使用Celery并行框架, 改为自己设计开发并行框架, 与原dm2数据库的并行架构思路统一, 以便平滑升级
1. 确定并行引擎为以scheduleBase基类派生的子类
   * 子类的类名称, 要求与其python文件名相同!!!
   * 子类必须放在imetadata\business子目录下!!!
1. 每一个子类, 处理一个并行, 具体模式参考样例sch_dm2_storage_parser.py
1. 调度表为: sch_center_mission, 每一条记录, 是一个并行, 根据scmTrigger的不同, 可以分类为:
   * db_queue: 数据表队列
   * cron: 基于cron语法的时间调度
   * interval: 基于每隔特定时间的时间调度
   * date: 基于特定时间启动一次的时间调度
   * mem_queue: 暂未实现, 后续可能会与rabbitmq, 或者redis等内存队列对接
   * other: 其他, 暂未扩展. 
1. 调度表sch_center_mission中的scmCommand和scmStatus配合, 完成并行的控制, 目前提供如下调度控制:
   * scmCommand=start&scmStatus=1: 启动调度
   * scmCommand=stop&scmStatus=1: 停止调度
   如果需要加速或减速, 只能停止调度->修改调度配置->启动调度
1. 调度表sch_center_mission中的scmCommand和scmStatus配合, 完成并行系统的退出:
   * 所有scmStatus=0&scmCommand=shutdown: 调度系统关闭退出

# 2020-06-02
1. 完成项目目录结构设计
1. 完成数据库操作基础框架的设计
1. 可以通过配置文件, 设置数据库的访问
1. 以工厂设计模式, 获取匹配的数据库, 实现postgresql数据库接口, 其他数据库接口未实现
1. 工厂为单例模式, 一次性初始化, 不再重复建立
