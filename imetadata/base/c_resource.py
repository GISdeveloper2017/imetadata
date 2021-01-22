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

    Name_WKT = 'wkt'
    Name_Srid = 'srid'
    Name_Description = 'description'
    Name_Period = 'period'

    Name_Text = 'text'

    Name_Password = 'password'
    Name_UserName = 'username'
    Port_Postgresql_Default = 5432
    Name_Port = 'port'
    Name_Host = 'host'
    Host_LocalHost = '127.0.0.1'
    OS_Windows = 'windows'
    OS_Linux = 'linux'
    OS_MacOS = 'Darwin'

    Scan_Period_Minute = 'minute'
    Scan_Period_Hour = 'hour'
    Scan_Period_Day = 'day'
    Scan_Period_Week = 'week'
    Scan_Period_Month = 'month'
    Scan_Period_Year = 'year'

    Application_Name = 'imetadata'
    Name_IMetaData = 'imetadata'
    SYSTEM_NAME_MISSION_ID = '{system.mission.id}'

    NAME_CMD_COMMAND = 'cmd_command'
    NAME_CMD_ID = 'cmd_id'
    NAME_CMD_TITLE = 'cmd_title'
    NAME_CMD_TRIGGER = 'cmd_trigger'
    NAME_CMD_ALGORITHM = 'cmd_algorithm'
    NAME_CMD_PARAMS = 'cmd_params'
    NAME_CMD_SETTINGS = 'cmd_settings'

    Name_Application = 'application'
    Name_Debug = 'debug'

    Name_Browse = 'browse'
    Name_Thumb = 'thumb'
    Name_Browse_GeoTiff = 'browse_geotiff'

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
    Job_Params_Abnormal_Job_Retry_Times = 'abnormal_job_retry_times'
    Default_Abnormal_Job_Retry_Times = 3

    Name_Parallel_Count = 'parallel_count'
    Name_Process = 'process'

    DB_Type_Postgresql = 'postgresql'

    DB_Server_ID_Default = '0'
    DB_Server_ID_Distribution = '0'  # 同步的目标数据库（如ap3_product_rsp_***）标识，可能与数管dm2的数据库不在同一个库

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
    Name_Schema = 'schema'
    Name_Public = 'public'
    Name_DataBases = 'databases'
    Name_Item = 'item'
    Name_Items = 'items'
    Name_Records = 'records'
    Name_Record = 'record'

    Name_Source = 'source'
    Name_Encoding = 'encoding'
    Name_Format = 'format'
    Name_Size = 'size'
    Name_Length = 'length'
    Name_Range = 'range'
    Name_Time = 'time'
    Name_Start_Time = 'start_time'
    Name_End_Time = 'end_time'
    Name_Time_Native = 'time_native'
    Name_Start_Time_Native = 'start_time_native'
    Name_End_Time_Native = 'end_time_native'

    Name_Time_Date = 'time_date'  # 时间日期部分
    Name_Time_Time = 'time_time'  # 时间时间部分

    Name_Default = 'default'

    Dir_Type_Directory = 1
    Dir_Type_VirtualDirectory = 2
    Dir_Type_Root = 3

    FileName_MetaData_Rule = 'metadata.rule'
    FileName_MetaData_Bus_21AT = 'metadata.21at'
    FileName_MetaData = 'metadata.json'
    FileName_MetaData_Bus = 'metadata_bus.xml'

    TableName_DM_Object = 'dm2_storage_object'

    Object_Confirm_IUnKnown = 0
    Object_Confirm_Maybe = 1
    Object_Confirm_IKnown = -1
    Object_Confirm_IKnown_Not = 2

    Name_Result = 'result'
    Name_Message = 'message'

    Name_Layer = 'layer'
    Name_Layers = 'layers'

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
    Name_Notify = 'notify'
    Name_Audit = 'audit'
    Name_System = 'system'
    Name_User = 'user'
    Name_Distribution = 'distribution'

    FileExt_Py = 'py'
    FileExt_Mbtiles = 'mbtiles'

    FileType_Unknown = 'none'
    FileType_File = 'file'
    FileType_Dir = 'dir'
    FileType_Layer = 'layer'

    File_Status_Valid = -1
    File_Status_Invalid = 0
    File_Status_Unknown = 1

    Storage_Type_Core = 'core'
    Storage_Type_InBound = 'inbound'
    Storage_Type_Mix = 'mix'

    IB_Bus_Status_InBound = 'inbound'
    IB_Bus_Status_Not_InBound = 'not_inbound'
    IB_Bus_Status_Online = 'online'

    Name_ID = 'id'
    Name_Name = 'name'
    Name_Code = 'code'
    Name_Catalog = 'catalog'
    Name_Title = 'title'
    Name_Level = 'level'
    Name_Group = 'group'
    Name_Type = 'type'
    Name_Common = 'common'
    Name_Access = 'access'
    Name_Quality = 'quality'
    Name_Tag = 'tag'
    Name_Tags = 'tags'
    Name_Table = 'table'
    Name_Vector = 'vector'
    Name_Vector_DataSet = 'vector_dataset'
    Name_Query = 'query'
    Name_ShapeFile = 'shapefile'
    Name_Pipe = 'pipe'
    Name_Geometry = 'geometry'
    Name_Option = 'option'
    Name_Data_Sample = 'data_sample'
    Name_Separator = 'separator'
    Name_Enable = 'enable'
    Name_Fuzzy_Matching = 'fuzzy_matching'
    Name_Field = 'field'
    Name_InBound = 'inbound'
    Name_OutBound = 'outbound'
    Name_Map = 'map'

    Name_Columns = 'columns'
    Name_PrimaryKey = 'primarykey'
    Name_DataType = 'datatype'
    Name_Width = 'width'
    Name_Number = 'number'
    Name_SQL = 'sql'
    Name_NotNull = 'notnull'
    Name_Null = 'null'
    Name_Target = 'target'
    Name_Value = 'value'
    Name_Array = 'array'
    Name_Get = 'get'
    Name_Set = 'set'
    Name_Set_Method = 'set_method'
    DB_Column_Set_Method_Param = 'param'
    DB_Column_Set_Method_Geometry = 'geometry'
    DB_Column_Set_Method_Function = 'function'
    DB_Column_Set_Method_Stream = 'stream'
    DB_Column_Set_Method_Exchange = 'exchange'

    Name_XPath = 'xpath'
    Name_NameSpaceMap = 'namespacemap'
    Name_Custom_Item = 'custom_item'
    Name_Attr_Name = 'attr_name'
    Name_List = 'list'
    Name_Not_List = 'not_list'
    Name_Custom = 'custom'
    Name_Root = 'root'
    Name_Binary = 'binary'
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
    Name_Test = 'test'

    Name_Dir = 'dir'
    Name_Rule = 'rule'
    Name_Mode = 'mode'

    Name_Server = 'server'
    Name_Client = 'client'
    Name_Url = 'url'
    Name_Timeout = 'timeout'
    Name_Parser = 'parser'

    Switch_Inbound_After_QI_Immediately_Of_IB_Storage = 'inbound_after_qi_immediately_of_ib_storage'
    Switch_Inbound_After_QI_Immediately_Of_MIX_Storage = 'inbound_after_qi_immediately_of_mix_storage'

    Path_MD_Rule_Type = '/root/type'
    Path_MD_Rule_Plugins_Dir = '/root/plugins/dir/plugin'
    Path_MD_Rule_Plugins_File = '/root/plugins/file/plugin'

    Path_Setting_Application = Name_Application
    Path_Setting_Application_Dir = '{0}.{1}'.format(Path_Setting_Application, Name_Directory)
    Path_Setting_Application_ID = '{0}.{1}'.format(Path_Setting_Application, Name_ID)
    Path_Setting_Application_Name = '{0}.{1}'.format(Path_Setting_Application, Name_Name)

    Path_Setting_Spatial = 'spatial'
    Path_Setting_Spatial_Srid = '{0}.srid'.format(Path_Setting_Spatial)

    Path_Setting_Dir = Name_Directory
    Path_Setting_Dir_WorkDir = '{0}.{1}'.format(Path_Setting_Dir, Name_Work)
    Path_Setting_Dir_Test = '{0}.{1}'.format(Path_Setting_Dir, Name_Test)
    Path_Setting_Dir_Test_Data = '{0}.{1}'.format(Path_Setting_Dir_Test, Name_Data)

    Path_Setting_Dependence = 'dependence'

    Path_Setting_Dependence_Tika = '{0}.tika'.format(Path_Setting_Dependence)
    Path_Setting_Dependence_Tika_Enable = '{0}.{1}'.format(Path_Setting_Dependence_Tika, Name_Enable)
    Path_Setting_Dependence_Tika_Mode = '{0}.{1}'.format(Path_Setting_Dependence_Tika_Enable, Name_Mode)
    Path_Setting_Dependence_Tika_Server = '{0}.{1}'.format(Path_Setting_Dependence_Tika, Name_Server)
    Path_Setting_Dependence_Tika_Server_Url = '{0}.{1}'.format(Path_Setting_Dependence_Tika_Server, Name_Url)
    Path_Setting_Dependence_Tika_Server_Timeout = '{0}.{1}'.format(Path_Setting_Dependence_Tika_Server, Name_Timeout)
    Path_Setting_Dependence_Tika_Client = '{0}.{1}'.format(Path_Setting_Dependence_Tika, Name_Client)
    Path_Setting_Dependence_Tika_Client_App = '{0}.{1}'.format(Path_Setting_Dependence_Tika_Client, Name_Application)

    Path_Setting_Dependence_Arcpy = '{0}.arcpy'.format(Path_Setting_Dependence)
    Path_Setting_Dependence_Arcpy_Enable = '{0}.{1}'.format(Path_Setting_Dependence_Arcpy, Name_Enable)

    Path_Setting_MetaData = 'metadata'

    Path_Setting_MetaData_Dir = '{0}.{1}'.format(Path_Setting_MetaData, Name_Directory)
    Path_Setting_MetaData_Dir_View = '{0}.{1}'.format(Path_Setting_MetaData_Dir, Name_View)

    Path_Setting_MetaData_Plugins = '{0}.{1}'.format(Path_Setting_MetaData, Name_Plugins)
    Path_Setting_MetaData_Plugins_Dir = '{0}.{1}'.format(Path_Setting_MetaData_Plugins, Name_Dir)

    Path_Setting_MetaData_Time = '{0}.{1}'.format(Path_Setting_MetaData, Name_Time)
    Path_Setting_MetaData_Time_Query = '{0}.{1}'.format(Path_Setting_MetaData_Time, Name_Query)
    Path_Setting_MetaData_Time_Server = '{0}.{1}'.format(Path_Setting_MetaData_Time, Name_Server)

    Path_Setting_MetaData_Tags = '{0}.{1}'.format(Path_Setting_MetaData, Name_Tags)
    Path_Setting_MetaData_Tags_Rule = '{0}.{1}'.format(Path_Setting_MetaData_Tags, Name_Rule)

    Path_Setting_MetaData_InBound = '{0}.{1}'.format(Path_Setting_MetaData, Name_InBound)

    Path_Setting_MetaData_InBound_ignore = '{0}.ignore'.format(Path_Setting_MetaData_InBound)
    Path_Setting_MetaData_InBound_ignore_file = '{0}.file'.format(Path_Setting_MetaData_InBound_ignore)
    Path_Setting_MetaData_InBound_ignore_dir = '{0}.dir'.format(Path_Setting_MetaData_InBound_ignore)

    Path_Setting_MetaData_InBound_Schema = '{0}.schema'.format(Path_Setting_MetaData_InBound)
    Path_Setting_MetaData_InBound_Schema_Default = '{0}.default'.format(Path_Setting_MetaData_InBound_Schema)
    Path_Setting_MetaData_InBound_Schema_Special = '{0}.special'.format(Path_Setting_MetaData_InBound_Schema)

    Path_Setting_MetaData_InBound_Switch = '{0}.{1}'.format(Path_Setting_MetaData_InBound, Name_Switch)

    Path_Setting_MetaData_InBound_Parser = '{0}.{1}'.format(Path_Setting_MetaData_InBound, Name_Parser)
    Path_Setting_MetaData_InBound_Parser_MetaData = '{0}.{1}'.format(Path_Setting_MetaData_InBound_Parser,
                                                                     Name_MetaData)
    Name_Retry_Times = 'retry_times'
    Path_Setting_MetaData_InBound_Parser_MetaData_Retry_Times = '{0}.{1}'.format(
        Path_Setting_MetaData_InBound_Parser_MetaData, Name_Retry_Times)

    Name_QI = 'qi'
    Path_Setting_MetaData_QI = '{0}.{1}'.format(Path_Setting_MetaData, Name_QI)
    Path_Setting_MetaData_QI_Switch = '{0}.{1}'.format(Path_Setting_MetaData_QI, Name_Switch)

    Path_Storage_Option_Inbound = 'inbound'
    Path_SO_Inbound_Filter = '{0}.{1}'.format(Path_Storage_Option_Inbound, Name_Filter)
    Path_SO_Inbound_Filter_Dir = '{0}.{1}'.format(Path_SO_Inbound_Filter, Name_Directory)
    Path_SO_Inbound_Filter_Dir_BlackList = '{0}.{1}'.format(Path_SO_Inbound_Filter_Dir, Name_Black_List)
    Path_SO_Inbound_Filter_Dir_WhiteList = '{0}.{1}'.format(Path_SO_Inbound_Filter_Dir, Name_White_List)
    Path_SO_Inbound_Filter_File = '{0}.{1}'.format(Path_SO_Inbound_Filter, Name_File)
    Path_SO_Inbound_Filter_File_BlackList = '{0}.{1}'.format(Path_SO_Inbound_Filter_File, Name_Black_List)
    Path_SO_Inbound_Filter_File_WhiteList = '{0}.{1}'.format(Path_SO_Inbound_Filter_File, Name_White_List)

    Path_IB_Opt_Notify = Name_Notify
    Path_IB_Opt_Notify_module = '{0}.{1}'.format(Path_IB_Opt_Notify, Name_Module)

    TextMatchType_Common = 'common'
    TextMatchType_Regex = 'regex'

    DB_True = -1
    DB_False = 0

    Engine_Custom = Name_Custom

    MetaDataEngine_Raster = 'raster'
    MetaDataEngine_Vector = 'vector'
    MetaDataEngine_Document = 'document'
    # MetaDataEngine_Document_Tika 是 MetaDataEngine_Document 的一种实现
    MetaDataEngine_Document_Tika = 'document_tika'
    MetaDataEngine_Spatial_Layer = 'spatial_layer'
    MetaDataEngine_Attached_File = 'attached_file'  # 加给元数据为附属的文本文件的数据用，目前有切片

    BrowseEngine_Raster = 'raster'
    BrowseEngine_Vector = 'vector'
    BrowseEngine_Document = 'document'

    DetailEngine_Same_File_Main_Name = 'same_file_main_name'
    DetailEngine_File_Itself = 'file_itself'
    DetailEngine_Directory_Itself = 'directory_itself'
    DetailEngine_File_Of_Same_Dir = 'file_of_same_dir'
    DetailEngine_All_File_Of_Same_Dir = 'all_file_of_same_dir'
    DetailEngine_File_Of_Dir = 'file_of_dir'
    DetailEngine_All_File_Of_Dir = 'all_file_of_dir'
    DetailEngine_Fuzzy_File_Main_Name = 'fuzzy_file_main_name'  # 匹配以主文件主名开头的文件
    DetailEngine_Busdataset = 'busdataset'  # 用于入数据集的附属文件metadata.21at

    Tag_DataSample_RelationPath = 'relation_path'
    Tag_DataSample_MainName = 'main_name'
    Tag_DataSample_RelationMainName = 'relation_main_name'

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
    Encoding_GB2312 = 'GB2312'

    value_type_string = 'string'  # 文本类型
    value_type_date = 'date'  # 日期类型
    value_type_date_nosep = 'date_nosep'  # 日期类型(没有‘-’or‘/’)
    value_type_date_month_nosep = 'date_month_nosep'  # 日期类型(只包含YYYYMM日期类型，并且没有‘-’or‘/’)
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

    IB_Status_QI_InQueue = 1
    IB_Status_QI_Dir_Scan_Creating = 2
    IB_Status_QI_Error = 21
    IB_Status_QI_Processing = 3
    IB_Status_QI_Finished = 4
    IB_Status_IB_InQueue = 5
    IB_Status_IB_Processing = 6
    IB_Status_IB_Error = 61
    IB_Status_IB_Wait_Audit = 8

    ProcType_New = 'new'
    ProcType_Delete = 'delete'
    ProcType_Update = 'update'
    ProcType_Same = 'same'

    InBound_Storage_Match_Mode_Auto = 'auto'
    InBound_Storage_Match_Mode_Set = 'set'

    DataAccess_Pass = 'pass'
    DataAccess_Wait = 'wait'
    DataAccess_Forbid = 'forbid'
    DataAccess_Unknown = 'unknown'

    Path_21AT_MD_Content_ProductType = '/root/ProductType'
    Path_21AT_MD_Content_ProductName = '/root/DSName'

    DataGroup_Sat_raster = 'sat_raster'  # 卫星的不能只能GF1 GF2...
    DataGroup_Industry_Land_Data = 'land_data'
    DataGroup_Industry_Land_DataSet = 'land_dataset'
    DataGroup_Document = 'document'
    DataGroup_Raster = 'raster'
    DataGroup_Raster_DataSet = 'raster_dataset'
    DataGroup_Vector = 'vector'
    DataGroup_Vector_DataSet = 'vector_dataset'

    DataCatalog_Land = 'land'  # 国土行业
    DataCatalog_Sat = 'sat'  # 原始数据（卫星）
    DataCatalog_Common = 'common'  # 通用数据

    DataType_String = 1
    DataType_DateTime = 2
    DataType_Numeric = 3
    DataType_Bool = 4
    DataType_Integer = 5

    DataType_Text = 21
    DataType_Binary = 22

    DataType_Geometry = 30
    DataType_Point = 31
    DataType_PolyLine = 32
    # ...

    DataType_Other = 40
    DataType_XML = 41
    DataType_Json = 42
    DataType_Array = 43
    DataType_Array_Char = 431
    # ...

    DataValueType_Value = 1
    DataValueType_File = 2
    DataValueType_SQL = 3

    # 在数据同步时用到下面参数以及上面三个参数
    DataValueType_Array = 4

    FileFormat_XML = 'xml'
    FileFormat_Json = 'json'
    FileFormat_TXT = 'txt'
    FileFormat_Binary = 'bin'

    Path_IB_Control = 'control'
    Path_IB_Switch = '{0}.switch'.format(Path_IB_Control)
    Path_IB_Switch_CheckFileLocked = '{0}.check_file_locked'.format(Path_IB_Switch)

    def data_group_title(self, group_name: str):
        if group_name.lower() == self.DataGroup_Industry_Land_Data:
            return '国土数据'
        elif group_name.lower() == self.DataGroup_Industry_Land_DataSet:
            return '国土数据集'
        elif group_name.lower() == self.DataGroup_Raster:
            return '影像'
        elif group_name.lower() == self.DataGroup_Raster_DataSet:
            return '影像数据集'
        elif group_name.lower() == self.DataGroup_Vector:
            return '矢量'
        elif group_name.lower() == self.DataGroup_Vector_DataSet:
            return '矢量数据集'
        elif group_name.lower() == self.DataGroup_Document:
            return '文档'
        else:
            return '卫星影像'

    def data_catalog_title(self, catalog_name: str):
        if catalog_name.lower() == self.DataCatalog_Land:
            return '国土行业'
        elif catalog_name.lower() == self.DataCatalog_Sat:
            return '原始数据'
        elif catalog_name.lower() == self.DataCatalog_Common:
            return '通用数据'
        else:
            return None

    def path_switch(self, path_prefix, switch_name: str) -> str:
        return '{0}.{1}'.format(path_prefix, switch_name)

    # Object_Def_Catalog_Common = 'object'  # 普通文件
    # Object_Def_Catalog_Object = 'object'  # 独立对象类型
    Object_Def_Catalog_Dataset = 'dataset'  # 普通数据集类型（gdb数据）
    Object_Def_Catalog_Object_Common = 'object_common'  # 普通文件(文档、图片等)
    Object_Def_Catalog_Object_Vector = 'object_vector'  # 普通矢量文件
    Object_Def_Catalog_Object_Raster = 'object_raster'  # 普通影像文件
    Object_Def_Catalog_Object_Sat = 'object_sat'  # 卫星类型
    Object_Def_Catalog_Object_Tiles = 'object_tiles'  # 切片类型
    Object_Def_Catalog_Object_Business = 'object_bus'  # 业务对象类型（如即时服务）
    Object_Def_Catalog_Dataset_Business = 'dataset_bus'  # 业务数据集类型（如即时服务）

    # 通用类型
    Object_Def_Type_Raster = 'raster'
    Object_Def_Type_Vector = 'vector'

    # 即时服务独立对象类型
    Object_Def_Type_DOM = 'dom'
    Object_Def_Type_DEM = 'dem'
    Object_Def_Type_DEM_NoFrame = 'dem_noframe'  # dem非分幅
    Object_Def_Type_Ortho = 'ortho'  # 单景正射
    Object_Def_Type_Mosaic = 'mosaic'  # 镶嵌影像
    Object_Def_Type_Third_Survey = 'third_survey'  # 三调影像
    Object_Def_Type_Guoqing_Scene = 'guoqing_scene'  # 国情影像-整景纠正
    Object_Def_Type_Guoqing_Frame = 'guoqing_frame'  # 国情影像-分幅影像
    Object_Def_Type_Custom = 'custom'  # 自定义影像

    # 即时服务数据集类型
    Object_Def_Type_DataSet_DOM = 'business_dataset_dom'  # dom数据集
    Object_Def_Type_DataSet_DEM = 'business_dataset_dem'  # dem数据集
    Object_Def_Type_DataSet_DEM_Frame = 'business_dataset_dem_frame'  # dem分幅数据集
    Object_Def_Type_DataSet_DEM_NoFrame = 'business_dataset_dem_noframe'  # dem非分幅数据集
    Object_Def_Type_DataSet_Ortho = 'business_dataset_ortho'  # 单景正射数据集
    Object_Def_Type_DataSet_Mosaic = 'business_dataset_mosaic'  # 镶嵌影像数据集
    Object_Def_Type_DataSet_Third_Survey = 'business_dataset_third_survey'  # 三调影像数据集
    Object_Def_Type_DataSet_Guoqing = 'business_dataset_guoqing'  # 国情影像数据集
    Object_Def_Type_DataSet_Guoqing_Scene = 'business_dataset_guoqing_scene'  # 国情影像-整景纠正数据集
    Object_Def_Type_DataSet_Guoqing_Frame = 'business_dataset_guoqing_frame'  # 国情影像-分幅影像数据集
    Object_Def_Type_DataSet_Custom = 'business_dataset_custom'  # 自定义影像数据集

    Plugins_Info_Module_Distribute_Engine = 'module.distribute.engine'
    Plugins_Info_Child_Layer_Plugins_Name = 'child_layer_plugins_name'
    Plugins_Info_Child_Layer_Data_Type = 'child_layer_data_type'

    # 配置 入库插件的测试用例用
    Name_Test_File_Type = 'test_file_type'
    Name_Test_file_path = 'test_Name_Test_file_path'
    Name_Test_object_confirm = 'test_object_confirm'
    Name_Test_object_name = 'test_object_name'
