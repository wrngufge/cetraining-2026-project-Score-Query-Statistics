#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生成绩查询与统计工具 - 主程序入口
作者：汪心雨
学号：2550204105
"""

import os
from data_manager import DataManager
from statistics import Statistics


def show_menu():
    """显示主菜单"""
    print("\n" + "=" * 40)
    print("    学生成绩查询与统计工具")
    print("=" * 40)
    print("  1. 从文件导入学生成绩数据")
    print("  2. 按学号查询学生成绩")
    print("  3. 按姓名查询学生成绩")
    print("  4. 显示所有学生排名")
    print("  5. 添加学生成绩")
    print("  6. 修改学生成绩")
    print("  7. 删除学生成绩")
    print("  8. 导出统计结果")
    print("  0. 退出程序")
    print("=" * 40)


def main():
    """主程序"""
    dm = DataManager()
    stats = Statistics(dm)
    
    while True:
        show_menu()
        choice = input("\n请选择功能 (0-8): ").strip()
        
        if choice == "1":
            # 导入数据
            file_path = input("请输入要导入的文件路径: ").strip()
            if os.path.exists(file_path):
                dm.import_from_file(file_path)
            else:
                print("文件不存在！")
        
        elif choice == "2":
            # 按学号查询
            student_id = input("请输入学号: ").strip()
            student = dm.find_by_id(student_id)
            if student:
                stats.print_student_report(student)
            else:
                print("未找到该学生！")
        
        elif choice == "3":
            # 按姓名查询
            name = input("请输入姓名（支持模糊查询）: ").strip()
            results = dm.find_by_name(name)
            if results:
                print(f"\n找到 {len(results)} 条记录:")
                for student in results:
                    stats.print_student_report(student)
            else:
                print("未找到匹配的学生！")
        
        elif choice == "4":
            # 显示排名
            stats.print_rankings()
        
        elif choice == "5":
            # 添加学生
            student_id = input("请输入学号: ").strip()
            name = input("请输入姓名: ").strip()
            
            scores = {}
            print("请输入各科成绩（输入科目名:分数，输入 'done' 结束）:")
            while True:
                entry = input().strip()
                if entry.lower() == 'done':
                    break
                try:
                    subject, score = entry.split(':')
                    scores[subject.strip()] = float(score.strip())
                except ValueError:
                    print("格式错误，请使用 '科目名:分数' 格式")
            
            if scores:
                dm.add_student(student_id, name, scores)
            else:
                print("未输入任何成绩，添加取消")
        
        elif choice == "6":
            # 修改学生
            student_id = input("请输入要修改的学号: ").strip()
            student = dm.find_by_id(student_id)
            if not student:
                print("未找到该学生！")
                continue
            
            print(f"当前信息: {student['姓名']}")
            new_name = input("请输入新姓名（直接回车保持不变）: ").strip()
            name = new_name if new_name else None
            
            scores = {}
            print("请输入要修改的科目成绩（输入 'done' 结束）:")
            while True:
                entry = input().strip()
                if entry.lower() == 'done':
                    break
                try:
                    subject, score = entry.split(':')
                    scores[subject.strip()] = float(score.strip())
                except ValueError:
                    print("格式错误，请使用 '科目名:分数' 格式")
            
            dm.update_student(student_id, name, scores if scores else None)
        
        elif choice == "7":
            # 删除学生
            student_id = input("请输入要删除的学号: ").strip()
            confirm = input(f"确认删除学号 {student_id} 的学生? (y/n): ").strip().lower()
            if confirm == 'y':
                dm.delete_student(student_id)
            else:
                print("已取消删除")
        
        elif choice == "8":
            # 导出结果
            file_path = input("请输入导出文件路径（如: results.json）: ").strip()
            rankings = stats.get_all_rankings()
            if rankings:
                dm.export_results(file_path, rankings)
            else:
                print("暂无数据可导出")
        
        elif choice == "0":
            print("感谢使用，再见！")
            break
        
        else:
            print("无效选择，请重新输入！")


if __name__ == "__main__":
    main()
