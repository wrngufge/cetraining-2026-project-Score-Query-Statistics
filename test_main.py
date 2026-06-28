#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用例 - 验证核心功能
作者：汪心雨
学号：2550204105
"""

import os
import tempfile
from data_manager import DataManager
from statistics import Statistics


def test_add_and_query():
    """测试用例1：添加学生和查询功能"""
    print("\n" + "=" * 50)
    print("测试用例1：添加学生和查询")
    print("=" * 50)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        dm = DataManager(temp_file)
        
        # 添加学生
        dm.add_student("2024001", "张三", {"数学": 85, "英语": 90})
        dm.add_student("2024002", "李四", {"数学": 92, "英语": 88})
        
        # 按学号查询
        student = dm.find_by_id("2024001")
        assert student is not None, "按学号查询失败"
        assert student["姓名"] == "张三", "姓名不匹配"
        print("✓ 按学号查询成功")
        
        # 按姓名查询
        results = dm.find_by_name("张")
        assert len(results) == 1, "按姓名查询失败"
        print("✓ 按姓名模糊查询成功")
        
        # 验证数据持久化
        dm2 = DataManager(temp_file)
        assert len(dm2.get_all_students()) == 2, "数据持久化失败"
        print("✓ 数据持久化成功")
        
    finally:
        os.unlink(temp_file)
    
    print("测试用例1通过！\n")


def test_statistics():
    """测试用例2：统计计算功能"""
    print("=" * 50)
    print("测试用例2：统计计算")
    print("=" * 50)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        dm = DataManager(temp_file)
        stats = Statistics(dm)
        
        # 添加测试数据
        dm.add_student("2024001", "张三", {"数学": 80, "英语": 90})
        dm.add_student("2024002", "李四", {"数学": 90, "英语": 80})
        
        # 计算总分和平均分
        student = dm.find_by_id("2024001")
        total = stats.calculate_total(student)
        average = stats.calculate_average(student)
        
        assert total == 170, f"总分计算错误: {total}"
        assert average == 85.0, f"平均分计算错误: {average}"
        print("✓ 总分和平均分计算正确")
        
        # 排名测试
        rankings = stats.get_all_rankings()
        assert len(rankings) == 2, "排名数量错误"
        assert rankings[0]["学号"] == "2024001", "排名顺序错误"
        print("✓ 排名功能正常")
        
        # 班级统计
        class_stats = stats.get_class_stats()
        assert class_stats["学生人数"] == 2, "班级统计错误"
        print("✓ 班级统计功能正常")
        
    finally:
        os.unlink(temp_file)
    
    print("测试用例2通过！\n")


def test_import_export():
    """测试用例3：导入导出功能"""
    print("=" * 50)
    print("测试用例3：导入导出")
    print("=" * 50)
    
    # 创建临时导入文件
    import_content = "2024001,张三,数学:85,英语:90\n2024002,李四,数学:92,英语:88"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(import_content)
        import_file = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_db = f.name
    
    export_file = temp_db.replace('.json', '_export.json')
    
    try:
        dm = DataManager(temp_db)
        stats = Statistics(dm)
        
        # 导入
        result = dm.import_from_file(import_file)
        assert result, "导入失败"
        assert len(dm.get_all_students()) == 2, "导入数量错误"
        print("✓ 文件导入成功")
        
        # 导出
        rankings = stats.get_all_rankings()
        result = dm.export_results(export_file, rankings)
        assert result, "导出失败"
        assert os.path.exists(export_file), "导出文件不存在"
        
        with open(export_file, 'r', encoding='utf-8') as f:
            import json
            data = json.load(f)
        assert len(data) == 2, "导出数据数量错误"
        print("✓ 结果导出成功")
        
    finally:
        for f in [import_file, temp_db, export_file]:
            if os.path.exists(f):
                os.unlink(f)
    
    print("测试用例3通过！\n")


if __name__ == "__main__":
    print("开始运行测试...")
    test_add_and_query()
    test_statistics()
    test_import_export()
    print("=" * 50)
    print("所有测试用例通过！")
    print("=" * 50)
