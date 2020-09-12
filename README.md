# imetadata
时空数据入库管理引擎

# 提示
1. 系统运行命令
在iMetaData子目录下, 运行命令行
```
python.exe ScheduleCreator.py
python.exe ScheduleCreator.py -log /your_log_file_path
```

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


# RoadMap
1. 完成

     |进度|开发人|类型|算法|说明|
     |  ----  |  ----  |  ----  | ----  | ----  |
     | 已完成 |wangxy|db_queue|job_dm_root_parser|根目录扫描调度, 处理dm2_storage表队列, dsStatus:0->1->2->0|
     | 建设中 |wangxy|db_queue|job_dm_path2object|目录识别对象调度, 处理dm2_storage_directory表队列, dsScanStatus:0->1->2->0|
     | 建设中 |zhaoyf|db_queue|job_dm_path_parser|目录下的子目录扫描调度, 处理dm2_storage_directory表队列, dsScanFileStatus:0->1->2->0|


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
