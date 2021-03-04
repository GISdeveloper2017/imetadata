import os
import traceback

import paramiko

from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_time import CTime
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_timeJob import CTimeJob
import settings

class job_d2s_storage_monitor(CTimeJob):
    def execute(self) -> str:
        dm2_storage_list = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            '''
SELECT
	dstid,
	dsttitle,
	dstunipath,
	dstscanlasttime,
	dstlastmodifytime,
	dstotheroption,
	dstotheroption -> 'mount' ->> 'username' AS dm2_username,
	dstotheroption -> 'mount' ->> 'password' AS dm2_password 
FROM
	dm2_storage 
WHERE
	dstscanstatus = 0 
	AND ( dsttype = 'mix' OR dsttype = 'core' )
            '''
        )
        gis_server_list = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            '''
            select dgsid, dgstitle, dgslastmodifytime
            from dp_gis_server
            '''
        )
        if dm2_storage_list.is_empty():
            return CResult.merge_result(CResult.Success, '本次没有需要检查的入库存储！')
        if gis_server_list.is_empty():
            return CResult.merge_result(CResult.Success, '本次没有需要检查的服务！')
        hostname = settings.application.xpath_one('data2service.system.connect.host', None)
        port = settings.application.xpath_one('data2service.system.connect.port', None)
        username = settings.application.xpath_one('data2service.system.connect.username', None)
        password = settings.application.xpath_one('data2service.system.connect.password', None)
        for data_index in range(dm2_storage_list.size()):
            storage_id = dm2_storage_list.value_by_name(data_index, 'dstid', '')
            storage_title = dm2_storage_list.value_by_name(data_index, 'dsttitle', '')
            storage_dstscanlasttime = dm2_storage_list.value_by_name(data_index, 'dstscanlasttime', None)
            storage_dstunipath = dm2_storage_list.value_by_name(data_index, 'dstunipath', '')
            storage_username = dm2_storage_list.value_by_name(data_index, 'dm2_username', '')
            storage_password = dm2_storage_list.value_by_name(data_index, 'dm2_password', '')
            CLogger().debug('正在检查和启动存储[{0}.{1}]的定时扫描...'.format(storage_id, storage_title))

            for data_index in range(gis_server_list.size()):
                server_id = gis_server_list.value_by_name(data_index, 'dgsid', '')
                server_title = gis_server_list.value_by_name(data_index, 'dgstitle', '')
                server_dgslastmodifytime = gis_server_list.value_by_name(data_index, 'dgslastmodifytime', '')
                CLogger().debug('正在检查和启动存储[{0}.{1}]的定时扫描...'.format(server_id, server_title))

                if storage_dstscanlasttime is not None:
                    gis_storage_list = CFactory().give_me_db(self.get_mission_db_id()).all_row(
                        '''
                        select dgsid, dgsserverid, dgsstorageid, dgsstoragelastcfgtime
                        from dp_gis_storage
                        where dgsstorageid = :storage_id and dgsserverid = :server_id
                        ''',
                            {'storage_id': storage_id, 'server_id': server_id}
                    )
                    gis_storage_id = gis_storage_list.value_by_name(data_index, 'dgsid', '')
                    # gis_storage_server_id = gis_storage_list.value_by_name(data_index, 'dgsserverid', '')
                    # gis_storage_storage_id = gis_storage_list.value_by_name(data_index, 'dgsstorageid', '')
                    gis_storage_dgslastmodifytime = gis_storage_list.value_by_name(data_index, 'dgslastmodifytime', '')
                    if gis_storage_list.is_empty():
                        gis_storage_id = CUtils.one_id()
                        database = CFactory().give_me_db(self.get_mission_db_id())
                        database.execute(
                            '''
                            insert into dp_gis_storage(
                            dgsid, 
                            dgsserverid, 
                            dgsstorageid, 
                            dgsstoragelastcfgtime, 
                            dgsstatus, 
                            dgsmountprocid, 
                            dgsmounturl, 
                            dgsmountmemo, 
                            dgsmemo,
                            dgsdefinetype,
                            dgsdefine,
                            dgslastmodifytime
                            ) 
                            VALUES(
                            :dgsid, 
                            :dgsserverid, 
                            :dgsstorageid, 
                            :dgsstoragelastcfgtime, 
                            :dgsstatus, 
                            :dgsmountprocid, 
                            :dgsmounturl, 
                            :dgsmountmemo, 
                            :dgsmemo,
                            :dgsdefinetype,
                            :dgsdefine,
                            :dgslastmodifytime
                            ) 
                            ''',
                            {
                                'dgsid': gis_storage_id,
                                'dgsserverid': server_id,
                                'dgsstorageid': storage_id,
                                'dgsstoragelastcfgtime': None,
                                'dgsstatus': 2,
                                'dgsmountprocid': None,
                                'dgsmounturl': None,
                                'dgsmountmemo': None,
                                'dgsmemo': None,
                                'dgsdefinetype': None,
                                'dgsdefine': None,
                                'dgslastmodifytime': None
                            }
                        )

                        CLogger().info("--------------begin mount---------------")
                        try:
                            mountcmd = "mount -t cifs {0} {1} -o username={2},password={3} "  # 挂接
                            fstab_line = "echo '{0}  {1}  cifs  defaults,username={2},password={3}  0  0' >> /etc/fstab"  # 挂接
                            client = paramiko.SSHClient()  # 启动ssh客户端
                            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            # 连接linux服务器
                            client.connect(hostname=hostname, port=port, username=username, password=password)
                            # 创建挂载点
                            win_path = storage_dstunipath.replace('\\', '/')
                            linux_path = '/mnt/store_' + storage_id
                            if not os.path.exists(linux_path):
                                CLogger().info("to make dir " + linux_path)
                                cmdin, cmdout, cmderr = client.exec_command("mkdir " + linux_path)
                                if cmderr != None:
                                    error_msg = cmderr.read().decode('utf-8')
                                    if len(error_msg) > 1:
                                        CLogger().error(error_msg)
                            # check if the linux_path mounted 看是否挂接
                            CLogger().info("check if the linux_path mounted " + linux_path)
                            cmdin, cmdout, cmderr = client.exec_command('mount')
                            if cmdout != None:
                                mount_info = cmdout.read().decode('utf-8')
                                if linux_path in mount_info:
                                    CLogger().info("the linux_path mounted " + linux_path)
                                    continue

                            CLogger().info("to " + mountcmd.format(win_path, linux_path, storage_username, storage_password))
                            # 开始挂接
                            cmdin, cmdout, cmderr = client.exec_command(
                                mountcmd.format(win_path, linux_path, storage_username, storage_password))
                            if cmderr != None:
                                error_msg = cmderr.read().decode('utf-8')
                                if len(error_msg) > 1:
                                    CLogger().error(error_msg)
                                    message = error_msg
                            # echo into fstab
                            CLogger().info(fstab_line.format(win_path, linux_path, username, password))
                            # 向fstab中写配置文件
                            cmdin, cmdout, cmderr = client.exec_command(
                                fstab_line.format(win_path, linux_path, username, password))
                            message = 'mount success'
                            CLogger().info('mount success')
                            # 更新挂接状态
                            lastmodifytime = CTime.now()
                            CFactory().give_me_db(self.get_mission_db_id()).execute(
                                '''
                                update dp_gis_storage 
                                set dgsstatus = 1,
                                dgsserverid = :server_id,
                                dgsmounturl = :linux_path,
                                dgslastmodifytime = :lastmodifytime,
                                dgsmountmemo = :message
                                where dgsid = :gis_storage_id
                                ''',
                                {'server_id': server_id, 'linux_path': linux_path, 'gis_storage_id': gis_storage_id,
                                 'lastmodifytime': lastmodifytime, 'message': message}
                            )
                            CFactory().give_me_db(self.get_mission_db_id()).execute(
                                '''
                                update dm2_storage 
                                set 
                                dstlastmodifytime = :lastmodifytime
                                where dstid = :storage_id
                                ''',
                                {'storage_id': storage_id, 'lastmodifytime': lastmodifytime}
                            )
                        except Exception as error:
                            message = 'mount服务[{0}.{1}]的状态过程出现异常! 错误信息为: {2}'.format(server_id, server_title,
                                                                              error.__str__())
                            CFactory().give_me_db(self.get_mission_db_id()).execute(
                                '''
                                update dp_gis_storage 
                                set dgsstatus = 3,
                                dgsmountmemo = :message
                                where dgsid = :gis_storage_id
                                ''',
                                {'gis_storage_id': gis_storage_id, 'message': message}
                            )
                            CLogger().error(message)

                    else:
                        if server_dgslastmodifytime is not None:
                            if CUtils.equal_ignore_case(storage_dstscanlasttime, gis_storage_dgslastmodifytime):
                                pass
                            else:
                                CFactory().give_me_db(self.get_mission_db_id()).execute(
                                    '''
                                    update dp_gis_storage 
                                    set dgsstatus = 2
                                    where dgsid = :gis_storage_id
                                    ''',
                                    {'gis_storage_id': gis_storage_id}
                                )
                                try:
                                    mountcmd = "mount -t cifs {0} {1} -o username={2},password={3} "  # 挂接
                                    fstab_line = "echo '{0}  {1}  cifs  defaults,username={2},password={3}  0  0' >> /etc/fstab"  # 挂接
                                    client = paramiko.SSHClient()  # 启动ssh客户端
                                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                    # 连接linux服务器
                                    client.connect(hostname=hostname, port=port, username=username, password=password)
                                    # 创建挂载点
                                    win_path = storage_dstunipath.replace('\\', '/')
                                    linux_path = '/mnt/store_' + storage_id
                                    if not os.path.exists(linux_path):
                                        CLogger().info("to make dir " + linux_path)
                                        cmdin, cmdout, cmderr = client.exec_command("mkdir " + linux_path)
                                        if cmderr != None:
                                            error_msg = cmderr.read().decode('utf-8')
                                            if len(error_msg) > 1:
                                                CLogger().debug(error_msg)
                                                # self.report_error(start_response, error_msg)
                                    # check if the linux_path mounted 看是否挂接
                                    CLogger().info("check if the linux_path mounted " + linux_path)
                                    cmdin, cmdout, cmderr = client.exec_command('mount')
                                    if cmdout != None:
                                        mount_info = cmdout.read().decode('utf-8')
                                        if linux_path in mount_info:
                                            CLogger().info("the linux_path mounted " + linux_path)
                                            continue
                                    CLogger().info("to " + mountcmd.format(win_path, linux_path, storage_username, storage_password))
                                    # 开始挂接
                                    cmdin, cmdout, cmderr = client.exec_command(
                                        mountcmd.format(win_path, linux_path, storage_username, storage_password))
                                    if cmderr != None:
                                        error_msg = cmderr.read().decode('utf-8')
                                        if len(error_msg) > 1:
                                            CLogger().error(error_msg)
                                    # echo into fstab
                                    CLogger().info(fstab_line.format(win_path, linux_path, username, password))
                                    # 向fstab中写配置文件
                                    cmdin, cmdout, cmderr = client.exec_command(
                                        fstab_line.format(win_path, linux_path, username, password))
                                    message = 'mount success'
                                    # 更新挂接状态
                                    lastmodifytime = CTime.now()
                                    CFactory().give_me_db(self.get_mission_db_id()).execute(
                                        '''
                                        update dp_gis_storage 
                                        set dgsstatus = 1,
                                        dgsserverid = :server_id,
                                        dgsmounturl = :linux_path,
                                        dgslastmodifytime = :lastmodifytime,
                                        dgsmountmemo = :message
                                        where dgsid = :gis_storage_id
                                        ''',
                                        {'server_id': server_id, 'linux_path': linux_path,
                                         'gis_storage_id': gis_storage_id,
                                         'lastmodifytime': lastmodifytime,
                                         'message': message}
                                    )
                                    CFactory().give_me_db(self.get_mission_db_id()).execute(
                                        '''
                                        update dm2_storage 
                                        set 
                                        dstlastmodifytime = :lastmodifytime
                                        where dstid = :storage_id
                                        ''',
                                        {'storage_id': storage_id, 'lastmodifytime': lastmodifytime}
                                    )
                                    CLogger().info(message)
                                except Exception as error:
                                    message = 'mount服务[{0}.{1}]的状态过程出现异常! 错误信息为: {2}'.format(server_id, server_title,
                                                                                             error.__str__())
                                    CFactory().give_me_db(self.get_mission_db_id()).execute(
                                        '''
                                        update dp_gis_storage 
                                        set dgsstatus = 3,
                                        dgsmountmemo = :message
                                        where dgsid = :gis_storage_id
                                        ''',
                                        {'gis_storage_id': gis_storage_id, 'message': message}
                                    )
                                    CLogger().debug(message)
        return CResult.merge_result(CResult.Success, '服务mount监控任务执行成功结束！')

if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_d2s_storage_monitor('', '').execute()