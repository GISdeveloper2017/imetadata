# imetadata
时空数据入库管理引擎

# 提示
1. 系统运行命令
在iMetaData子目录下, 运行命令行
```
python.exe ScheduleCreator.py
python.exe ScheduleCreator.py -log /your_log_file_path
```

# RoadMap
1. 调试db_queue和cron的Trigger模式
1. 测试完成sch_dm2_storage_parser和sch_dm2_storage_directory_parser

# 2020-09-03
1. 不再使用Celery并行框架, 改为自己设计开发并行框架, 与原dm2数据库的并行架构思路统一, 以便平滑升级
1. 确定并行引擎为以scheduleBase基类派生的子类
   * 子类的类名称, 要求与其python文件名相同!!!
   * 子类必须放在imetadata\business子目录下!!!
1. 每一个子类, 处理一个并行, 具体模式参考样例sch_dm2_storage_parser.py
1. 调度表为: sch_center_mission, 每一条记录, 是一个并行, 根据scmTrigger的不同, 可以分类为:
   * db_queue: 数据表队列
   * cron: 基于cron语法的时间调度
   * mem_queue: 暂未实现, 后续可能会与rabbitmq, 或者redis等内存队列对接
   * other: 其他, 暂未扩展. 
1. 调度表sch_center_mission中的scmCommand和scmStatus配合, 完成并行的控制, 目前提供如下调度控制:
   * scmCommand=start&scmStatus=1: 启动调度
   * scmCommand=stop&scmStatus=1: 停止调度
   如果需要加速或减速, 只能停止调度->修改调度配置->启动调度
1. 调度表sch_center_mission中的scmParallelCount和scmStatus配合, 完成并行系统的退出:
   * scmStatus=0&scmParallelCount=0: 调度系统关闭退出


# 2020-06-02
1. 完成项目目录结构设计
1. 完成数据库操作基础框架的设计
1. 可以通过配置文件, 设置数据库的访问
1. 以工厂设计模式, 获取匹配的数据库, 实现postgresql数据库接口, 其他数据库接口未实现
1. 工厂为单例模式, 一次性初始化, 不再重复建立
