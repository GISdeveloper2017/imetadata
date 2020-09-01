# imetadata
time and spatial meta data storage

# 提示
1. 系统运行命令
在iMetaData子目录下, 运行命令行
```
celery -A imetadata.ScheduleMng worker -B -l info
```

# RoadMap
1. 建立Celery运行框架

# 2020-06-08
1. 完成celery+rabbitmq运行框架的基础设计
1. 完成其中单队列运行的调试和运行工作
1. 配置ini信息, 改为配置对象


# 2020-06-02
1. 完成项目目录结构设计
1. 完成数据库操作基础框架的设计
1. 可以通过配置文件, 设置数据库的访问
1. 以工厂设计模式, 获取匹配的数据库, 实现postgresql数据库接口, 其他数据库接口未实现
1. 工厂为单例模式, 一次性初始化, 不再重复建立
