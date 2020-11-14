# -*- coding: utf-8 -*- 
# @Time : 2020/9/12 09:19 
# @Author : 王西亚 
# @File : c_resource.py

class CResource:
    SRID_WGS84 = 4326

    Spatial_MetaData_Type_Native_Center = 11
    Spatial_MetaData_Type_Native_BBox = 12
    Spatial_MetaData_Type_Native_Geom = 13
    Spatial_MetaData_Type_Wgs84_Center = 21
    Spatial_MetaData_Type_Wgs84_BBox = 22
    Spatial_MetaData_Type_Wgs84_Geom = 23

    Spatial_MetaData_Type_Prj_Wkt = 24
    Spatial_MetaData_Type_Prj_Proj4 = 25
    Spatial_MetaData_Type_Prj_Project = 26
    Spatial_MetaData_Type_Prj_Coordinate = 27
    Spatial_MetaData_Type_Prj_Degree = 28
    Spatial_MetaData_Type_Prj_Zone = 29
    Spatial_MetaData_Type_Prj_Source = 30

    View_MetaData_Type_Browse = 11
    View_MetaData_Type_Thumb = 12

    Name_Native_Center = 'native_center'
    Name_Native_BBox = 'native_bbox'
    Name_Native_Geom = 'native_geom'
    Name_Wgs84_Center = 'wgs84_center'
    Name_Wgs84_BBox = 'wgs84_bbox'
    Name_Wgs84_Geom = 'wgs84_geom'
    Name_Prj_Wkt = 'prj_wkt'
    Name_Prj_Proj4 = 'prj_proj4'
    Name_Prj_Project = 'prj_project'
    Name_Prj_Coordinate = 'prj_coordinate'
    Name_Prj_Degree = 'prj_degree'
    Name_Prj_Zone = 'prj_zone'
    Name_Prj_Source = 'prj_source'

    Name_Password = 'password'
    Name_UserName = 'username'
    Port_Postgresql_Default = 5432
    Name_Port = 'port'
    Name_Host = 'host'
    Host_LocalHost = '127.0.0.1'
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

    Name_Browse = 'browse'
    Name_Thumb = 'thumb'

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

    DB_Type_Postgresql = 'postgresql'

    DB_Server_ID_Default = '0'

    Name_ON = 'on'
    Name_OFF = 'off'

    Status_Finish = 0

    Name_White_List = 'white_list'
    Name_Black_List = 'black_list'

    Name_Filter = 'filter'
    Name_Directory = 'directory'
    Name_File = 'file'
    Name_FileName = 'filename'

    Name_Total = 'total'
    Name_Data = 'data'
    Name_DataBase = 'database'
    Name_DataBases = 'databases'
    Name_Item = 'item'
    Name_Items = 'items'
    Name_Records = 'records'
    Name_Record = 'record'

    Name_Source = 'source'

    Name_Format = 'format'
    Name_Size = 'size'
    Name_Length = 'length'
    Name_Range = 'range'
    Name_Time = 'time'
    Name_Start_Time = 'start_time'
    Name_End_Time = 'end_time'

    Name_Default = 'default'

    Dir_Type_Directory = 1
    Dir_Type_VirtualDirectory = 2
    Dir_Type_Root = 3

    FileName_MetaData_Rule = 'metadata.rule'
    FileName_Ready_21AT = 'ready.21at'
    FileName_MetaData_Bus_21AT = 'metadata.21at'
    FileName_MetaData = 'metadata.json'
    FileName_MetaData_Bus = 'metadata_bus.xml'

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
    Name_Plugin = 'plugin'
    Name_Work = 'work'
    Name_Business = 'business'
    Name_View = 'view'
    Name_DataAccess = 'dataaccess'
    Name_Modules = 'modules'
    Name_Module = 'module'
    Name_Audit = 'audit'
    Name_System = 'system'
    Name_User = 'user'
    Name_Distribution = 'distribution'

    FileExt_Py = 'py'

    FileType_Unknown = 'none'
    FileType_File = 'file'
    FileType_Dir = 'dir'

    File_Status_Valid = -1
    File_Status_Invalid = 0
    File_Status_Unknown = 1

    Storage_Type_Core = 'core'
    Storage_Type_InBound = 'inbound'

    Name_ID = 'id'
    Name_Name = 'name'
    Name_Code = 'code'
    Name_Catalog = 'catalog'
    Name_Title = 'title'
    Name_Level = 'level'
    Name_Group = 'group'
    Name_Type = 'type'
    Name_Access = 'access'
    Name_Quality = 'quality'

    Name_InBound = 'inbound'
    Name_OutBound = 'outbound'

    Name_DataType = 'datatype'
    Name_Width = 'width'
    Name_SQL = 'sql'
    Name_NotNull = 'notnull'

    Name_XPath = 'xpath'
    Name_Attr_Name = 'attr_name'
    Name_List = 'list'
    Name_Custom = 'custom'
    Name_Root = 'root'

    Name_Keyword = 'keyword'

    Name_Img = 'img'
    Name_Ige = 'ige'
    Name_rrd = 'rrd'
    Name_rde = 'rde'
    Name_Tif = 'tif'
    Name_Tiff = 'tiff'
    Name_Bil = 'bil'
    Name_Shp = 'shp'

    Name_Switch = 'switch'

    Switch_Use_Ready_Flag_File_Name = 'use_ready_flag_file_name'

    Path_MD_Rule_Type = '/root/type'
    Path_MD_Rule_Plugins_Dir = '/root/plugins/dir/plugin'
    Path_MD_Rule_Plugins_File = '/root/plugins/file/plugin'

    Path_Setting_MetaData = 'metadata'
    Path_Setting_MetaData_Plugins_Dir = '{0}.plugins.dir'.format(Path_Setting_MetaData)
    Path_Setting_MetaData_InBound = '{0}.inbound'.format(Path_Setting_MetaData)
    Path_Setting_MetaData_InBound_ignore = '{0}.ignore'.format(Path_Setting_MetaData_InBound)
    Path_Setting_MetaData_InBound_ignore_file = '{0}.file'.format(Path_Setting_MetaData_InBound_ignore)
    Path_Setting_MetaData_InBound_ignore_dir = '{0}.dir'.format(Path_Setting_MetaData_InBound_ignore)
    Path_Setting_MetaData_InBound_Schema = '{0}.schema'.format(Path_Setting_MetaData_InBound)
    Path_Setting_MetaData_InBound_Schema_Default = '{0}.default'.format(Path_Setting_MetaData_InBound_Schema)
    Path_Setting_MetaData_InBound_Schema_Special = '{0}.special'.format(Path_Setting_MetaData_InBound_Schema)
    Path_Setting_MetaData_InBound_Switch = '{0}.{1}'.format(Path_Setting_MetaData_InBound, Name_Switch)

    Path_Storage_Option_Inbound = 'inbound'
    Path_SO_Inbound_Filter = '{0}.{1}'.format(Path_Storage_Option_Inbound, Name_Filter)
    Path_SO_Inbound_Filter_Dir = '{0}.{1}'.format(Path_SO_Inbound_Filter, Name_Directory)
    Path_SO_Inbound_Filter_Dir_BlackList = '{0}.{1}'.format(Path_SO_Inbound_Filter_Dir, Name_Black_List)
    Path_SO_Inbound_Filter_Dir_WhiteList = '{0}.{1}'.format(Path_SO_Inbound_Filter_Dir, Name_White_List)
    Path_SO_Inbound_Filter_File = '{0}.{1}'.format(Path_SO_Inbound_Filter, Name_File)
    Path_SO_Inbound_Filter_File_BlackList = '{0}.{1}'.format(Path_SO_Inbound_Filter_File, Name_Black_List)
    Path_SO_Inbound_Filter_File_WhiteList = '{0}.{1}'.format(Path_SO_Inbound_Filter_File, Name_White_List)

    TextMatchType_Common = 'common'
    TextMatchType_Regex = 'regex'

    DB_True = -1
    DB_False = 0

    Engine_Custom = Name_Custom

    MetaDataEngine_Raster = 'raster'
    MetaDataEngine_Vector = 'vector'
    MetaDataEngine_Document = 'document'

    BrowseEngine_Raster = 'raster'
    BrowseEngine_Vector = 'vector'
    BrowseEngine_Document = 'document'

    DetailEngine_Same_File_Main_Name = 'same_file_main_name'
    DetailEngine_File_Of_Same_Dir = 'file_of_same_dir'
    DetailEngine_All_File_Of_Same_Dir = 'all_file_of_same_dir'
    DetailEngine_File_Of_Dir = 'file_of_dir'
    DetailEngine_All_File_Of_Dir = 'all_file_of_dir'

    TagEngine_Global_Dim_In_RelationPath = 'global_dim_in_relation_path'
    TagEngine_Global_Dim_In_MainName = 'global_dim_in_main_name'

    QA_Result_Pass = 'pass'
    QA_Result_Warn = 'warn'
    QA_Result_Error = 'error'

    QA_Type_FileExist = 'file_exist'
    QA_Type_XML_Node_Exist = 'xml_node_exist'

    Name_Min = 'min'
    Name_Max = 'max'

    ModuleName_MetaData = 'module_metadata'
    ModuleName_Distribution = 'module_distribution'
    ModuleName_DataMining = 'module_datamining'
    ModuleName_Data2Service = 'module_data2service'

    # 投影坐标信息来源; 1-数据;2-业务元数据;9-人工指定
    Prj_Source_Data = 1
    Prj_Source_BusMetaData = 2
    Prj_Source_Custom = 9

    # 质检-分组-数据完整性
    QA_Group_Data_Integrity = 'di'

    MetaDataFormat_Text = 0
    MetaDataFormat_Json = 1
    MetaDataFormat_XML = 2
    DataFormat_Vector_File = 3  # 矢量文件
    DataFormat_Vector_Dataset = 4  # 矢量数据集
    DataFormat_Raster_File = 5  # 影像文件

    Transformer_DOM_MDB = 'mdb'
    Transformer_DOM_MAT = 'mat'
    Transformer_DOM_XLS = 'xls'
    Transformer_DOM_XLSX = 'xlsx'

    Transformer_XML = 'xml'
    Transformer_Json = 'json'
    Transformer_TXT = 'txt'

    Seq_Type_AutoInc = 1
    Seq_Type_Date_AutoInc = 2

    Encoding_UTF8 = 'UTF-8'
    Encoding_GBK = 'GBK'
    Encoding_GBK2312 = 'GBK2312'

    value_type_string = 'string'  # 文本类型
    value_type_date = 'date'  # 日期类型
    value_type_datetime = 'datetime'  # 日期时间类型
    value_type_date_or_datetime = 'date_or_datetime'  # 日期类型或日期时间类型
    value_type_decimal = 'decimal'  # 小数（包含负数）
    value_type_integer = 'integer'  # 整数（包含负整数）
    value_type_decimal_or_integer = 'decimal_or_integer'  # 小数或整数（包含负数）
    value_type_decimal_or_integer_positive = 'positive_decimal_or_integer'  # 正小数或整数（不包含负数）

    ProcStatus_Finished = 0
    ProcStatus_InQueue = 1
    ProcStatus_Processing = 2
    ProcStatus_Error = 3
    ProcStatus_WaitConfirm = 9

    InBound_Storage_Match_Mode_Auto = 'auto'
    InBound_Storage_Match_Mode_Set = 'set'

    DataAccess_Pass = 'pass'
    DataAccess_Wait = 'wait'
    DataAccess_Forbid = 'forbid'
    DataAccess_Unknown = 'unknown'

    Path_21AT_MD_Content_ProductType = '/root/ProductType'
    Path_21AT_MD_Content_ProductName = '/root/DSName'

    DataGroup_Sat_raster = 'sat_raster'
    DataGroup_Industry_Data = 'industry_data'
    DataGroup_Industry_DataSet = 'industry_dataset'
    DataGroup_Raster = 'raster'
    DataGroup_Raster_DataSet = 'raster_dataset'
    DataGroup_Vector = 'vector'
    DataGroup_Vector_DataSet = 'vector_dataset'

    def data_group_title(self, group_name: str):
        if group_name.lower() == self.DataGroup_Sat_raster:
            return '卫星影像'
        elif group_name.lower() == self.DataGroup_Industry_Data:
            return '行业数据'
        elif group_name.lower() == self.DataGroup_Industry_DataSet:
            return '行业数据集'
        elif group_name.lower() == self.DataGroup_Raster:
            return '影像'
        elif group_name.lower() == self.DataGroup_Raster_DataSet:
            return '影像数据集'
        elif group_name.lower() == self.DataGroup_Vector:
            return '矢量'
        elif group_name.lower() == self.DataGroup_Vector_DataSet:
            return '矢量数据集'
        else:
            return None

    def path_switch(self, path_prefix, switch_name: str) -> str:
        return '{0}.{1}'.format(path_prefix, switch_name)
