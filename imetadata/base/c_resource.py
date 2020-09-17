# -*- coding: utf-8 -*- 
# @Time : 2020/9/12 09:19 
# @Author : 王西亚 
# @File : c_resource.py

class CResource:
    Name_Application = 'imetadata'
    SYSTEM_NAME_MISSION_ID = '{system.mission.id}'

    NAME_CMD_COMMAND = 'cmd_command'
    NAME_CMD_ID = 'cmd_id'
    NAME_CMD_TITLE = 'cmd_title'
    NAME_CMD_TRIGGER = 'cmd_trigger'
    NAME_CMD_ALGORITHM = 'cmd_algorithm'
    NAME_CMD_PARAMS = 'cmd_params'

    CMD_START = 'start'
    CMD_STOP = 'stop'
    CMD_FORCE_STOP = 'force_stop'
    CMD_SHUTDOWN = 'shutdown'

    TRIGGER_TYPE_DB_QUEUE = 'db_queue'
    TRIGGER_TYPE_DATE = 'date'
    TRIGGER_TYPE_INTERVAL = 'interval'
    TRIGGER_TYPE_CRON = 'cron'
    TRIGGER_TYPE_QUEUE = 'queue'
    TRIGGER_TYPE_NONE = 'none'

    TRIGGER_Params = 'trigger'
    TRIGGER_Interval_Params_Seconds = 'seconds'

    NAME_JOB = 'job'
    NAME_PARAMS = 'params'
    NAME_STOP_EVENT = 'stop_event'
    NAME_SUBPROCESS_LIST = 'subprocess_list'

    Job_Params_DB_Server_ID = 'db_server_id'
    Name_Parallel_Count = 'parallel_count'
    Name_Process = 'process'

    Status_Finish = 0

    Name_White_List = 'white_list'
    Name_Black_List = 'black_list'

    Name_Filter = 'filter'
    Name_Directory = 'directory'
    Name_File = 'file'

    Dir_Type_Directory = 1
    Dir_Type_VirtualDirectory = 2
    Dir_Type_Root = 3

    FileName_MetaData_Rule = 'metadata.rule'

    Plugins_Target_Type_File = 'file'
    Plugins_Target_Type_Path = 'path'
    Plugins_Target_Type_Vector_Layer = 'vector_layer'

    Object_Confirm_IUnKnown = 0
    Object_Confirm_Maybe = 1
    Object_Confirm_IKnown = -1

    Name_Result = 'result'
    Name_Message = 'message'

    Success = -1
    Failure = 0
    Exception = 1

    Name_Business = 'business'
    Name_Plugins = 'plugins'

    FileExt_Py = 'py'
