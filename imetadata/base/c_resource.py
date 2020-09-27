# -*- coding: utf-8 -*- 
# @Time : 2020/9/12 09:19 
# @Author : 王西亚 
# @File : c_resource.py

class CResource:
    OS_Windows = 'windows'
    OS_Linux = 'linux'

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
    Name_FileName = 'filename'

    Name_Total = 'total'
    Name_Data = 'data'
    Name_Item = 'item'
    Name_Items = 'items'
    Name_Records = 'records'
    Name_Record = 'record'

    Dir_Type_Directory = 1
    Dir_Type_VirtualDirectory = 2
    Dir_Type_Root = 3

    FileName_MetaData_Rule = 'metadata.rule'

    Object_Confirm_IUnKnown = 0
    Object_Confirm_Maybe = 1
    Object_Confirm_IKnown = -1
    Object_Confirm_IKnown_Not = 2

    Name_Result = 'result'
    Name_Message = 'message'

    Success = -1
    Failure = 0
    Exception = 1

    Name_MetaData = 'metadata'
    Name_Plugins = 'plugins'
    Name_WorkDir = 'workdir'
    Name_Business = 'business'

    FileExt_Py = 'py'

    FileType_Unknown = 'none'
    FileType_File = 'file'
    FileType_Dir = 'dir'

    File_Status_Valid = -1
    File_Status_Invalid = 0
    File_Status_Unknown = 1

    Name_ID = 'id'
    Name_Name = 'name'
    Name_Code = 'code'
    Name_Catalog = 'catalog'
    Name_Title = 'title'
    Name_Type = 'type'

    Name_XPath = 'xpath'
    Name_Attr_Name = 'attr_name'
    Name_List = 'list'

    Name_Root = 'root'

    Path_MD_Rule_Type = '/root/type'

    TextMatchType_Common = 'common'
    TextMatchType_Regex = 'regex'

    DB_True = -1
    DB_False = 0

    MetaDataFormat_Text = 0
    MetaDataFormat_Json = 1
    MetaDataFormat_XML = 2

    MetaDataEngine_Raster = 'raster'
    MetaDataEngine_Vector = 'vector'
    MetaDataEngine_Document = 'document'
    MetaDataEngine_21AT_MBTiles = '21at_mbtiles'
    MetaDataEngine_Custom = 'custom'

    DetailEngine_Same_File_Main_Name = 'same_file_main_name'
    DetailEngine_File_Of_Same_Dir = 'file_of_same_dir'
    DetailEngine_All_File_Of_Same_Dir = 'all_file_of_same_dir'
    DetailEngine_File_Of_Dir = 'file_of_dir'
    DetailEngine_All_File_Of_Dir = 'all_file_of_dir'

    TagEngine_Global_Dim_In_RelationPath = 'global_dim_in_relation_path'
    TagEngine_Global_Dim_In_MainName = 'global_dim_in_main_name'

    QualityAudit_Type_Pass = 'pass'
    QualityAudit_Type_Warn = 'warn'
    QualityAudit_Type_Error = 'error'

    QualityAudit_FileExist = 'file_exist'
    QualityAudit_XML_Value = 'xml_value'
