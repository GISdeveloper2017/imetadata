# -*- coding: utf-8 -*- 
# @Time : 2021/1/7 18:02 
# @Author : 王西亚 
# @File : deploy.py
import argparse
import compileall
import datetime
import os
import py_compile
import shutil
from pathlib import Path

from imetadata.base.c_file import CFile
from imetadata.base.c_settings import CSettings
from imetadata.base.c_utils import CUtils

deploy_settings = CSettings(
    {
        'path': {
            'white_list': ['/imetadata*', ''],
            'black_list': None
        },
        'directory': {
            'white_list': None,
            'black_list': ['__pycache__']
        },
        'file': {
            'white_list': None,
            'black_list': ['*.pyc', '.ds_store', '.git*', '*.md', '*.sh', 'deploy.py']
        },
        'compile': {
            'path': {
                'white_list': None,
                'black_list': None
            },
            'file': {
                'white_list': ['c_*.py', '__init__.py'],
                'black_list': ['c_*plugins*.py']
            }
        }
    }
)


def deploy_match_pattern_list(text: str, jpath: str, match_result: bool, none_result: bool) -> bool:
    pattern_list = deploy_settings.xpath_one(jpath, None)
    if pattern_list is None:
        return none_result

    if CFile.file_match_list(text.lower(), pattern_list):
        return match_result
    else:
        return not match_result


def package(output_relation_dir):
    """
    编译根目录下的包括子目录里的所有py文件成pyc文件到新的文件夹下
    :param output_relation_dir: 需编译的目录
    :return:
    """
    output_relation_dir = CFile.unify(CUtils.any_2_str(output_relation_dir))

    application_dir = CFile.file_path(CFile.file_abs_path(__file__))
    output_dir = CFile.file_abs_path(CFile.join_file(application_dir, output_relation_dir))

    for each_directory, dir_name_list, file_name_without_path_list in os.walk(application_dir):
        directory_source = each_directory
        directory_name = CFile.file_name(directory_source)
        directory_relation = CFile.file_relation_path(each_directory, application_dir)
        directory_target = CFile.join_file(output_dir, directory_relation)

        path_deploy_enable = deploy_match_pattern_list(directory_relation, 'path.white_list', True, True)
        path_deploy_enable = path_deploy_enable and deploy_match_pattern_list(directory_relation, 'path.black_list',
                                                                              False, True)
        if path_deploy_enable:
            directory_deploy_enable = deploy_match_pattern_list(directory_name, 'directory.white_list', True, True)
            directory_deploy_enable = directory_deploy_enable and deploy_match_pattern_list(
                directory_name, 'directory.black_list',
                False, True
            )

            if directory_deploy_enable:
                for file_name_without_path in file_name_without_path_list:
                    file_deploy_enable = deploy_match_pattern_list(
                        file_name_without_path, 'file.white_list', True,
                        True
                    )
                    file_deploy_enable = file_deploy_enable and deploy_match_pattern_list(
                        file_name_without_path, 'file.black_list',
                        False, True
                    )

                    file_name_with_path_source = CFile.join_file(directory_source, file_name_without_path)
                    if file_deploy_enable:
                        file_compile_enable = deploy_match_pattern_list(
                            file_name_without_path, 'compile.file.white_list',
                            True, False
                        )
                        if file_compile_enable:
                            file_compile_enable = deploy_match_pattern_list(
                                file_name_without_path, 'compile.file.black_list',
                                False, False
                            )

                        file_name_without_path_target = CFile.change_file_ext(file_name_without_path, 'pyc')
                        file_name_with_path_target = CFile.join_file(directory_target, file_name_without_path_target)
                        CFile.check_and_create_directory_itself(directory_target)
                        if file_compile_enable:
                            py_compile.compile(file_name_with_path_source, cfile=file_name_with_path_target)
                            print('{0}-compile-success'.format(file_name_with_path_source))
                        else:
                            CFile.copy_file_to(file_name_with_path_source, directory_target)
                            print('{0}-no_compile'.format(file_name_with_path_source))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""
系统发布
作者：王西亚
日期：2021-01-07

说明：
-o: 系统输出目录
    """)
    parser.add_argument('-o', '--output', required=True, help='发布输出目录', dest='output')

    args = parser.parse_args()

    package(args.output)
    print('系统发布完毕! ')
