#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计模块 - 负责成绩统计、排名计算
作者：汪心雨
学号：2550204105
"""

from typing import List, Dict
from data_manager import DataManager


class Statistics:
    """成绩统计类"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def calculate_total(self, student: Dict) -> float:
        """计算单个学生总分"""
        scores = student.get("成绩", {})
        return sum(scores.values())
    
    def calculate_average(self, student: Dict) -> float:
        """计算单个学生平均分"""
        scores = student.get("成绩", {})
        if not scores:
            return 0.0
        return sum(scores.values()) / len(scores)
    
    def get_student_stats(self, student: Dict) -> Dict:
        """获取单个学生的完整统计信息"""
        total = self.calculate_total(student)
        average = self.calculate_average(student)
        return {
            **student,
            "总分": round(total, 2),
            "平均分": round(average, 2)
        }
    
    def get_all_rankings(self) -> List[Dict]:
        """获取所有学生排名（按平均分降序）"""
        stats_list = []
        for student in self.data_manager.get_all_students():
            stats_list.append(self.get_student_stats(student))
        
        # 按平均分降序排序
        stats_list.sort(key=lambda x: x["平均分"], reverse=True)
        
        # 添加排名
        for i, student in enumerate(stats_list, 1):
            student["排名"] = i
        
        return stats_list
    
    def get_class_stats(self) -> Dict:
        """获取班级整体统计"""
        all_students = self.data_manager.get_all_students()
        if not all_students:
            return {}
        
        all_averages = [self.calculate_average(s) for s in all_students]
        all_totals = [self.calculate_total(s) for s in all_students]
        
        return {
            "学生人数": len(all_students),
            "班级平均总分": round(sum(all_totals) / len(all_totals), 2),
            "班级平均平均分": round(sum(all_averages) / len(all_averages), 2),
            "最高平均分": round(max(all_averages), 2),
            "最低平均分": round(min(all_averages), 2)
        }
    
    def print_student_report(self, student: Dict) -> None:
        """打印单个学生成绩单"""
        stats = self.get_student_stats(student)
        print("\n" + "=" * 50)
        print(f"学号: {stats['学号']}")
        print(f"姓名: {stats['姓名']}")
        print("-" * 50)
        print("各科成绩:")
        for subject, score in stats['成绩'].items():
            print(f"  {subject}: {score}")
        print("-" * 50)
        print(f"总分: {stats['总分']}")
        print(f"平均分: {stats['平均分']}")
        print("=" * 50)
    
    def print_rankings(self) -> None:
        """打印所有学生排名"""
        rankings = self.get_all_rankings()
        
        if not rankings:
            print("暂无学生数据")
            return
        
        print("\n" + "=" * 70)
        print(f"{'排名':<6}{'学号':<12}{'姓名':<10}{'总分':<10}{'平均分':<10}")
        print("-" * 70)
        
        for student in rankings:
            print(f"{student['排名']:<6}{student['学号']:<12}{student['姓名']:<10}"
                  f"{student['总分']:<10}{student['平均分']:<10}")
        
        print("=" * 70)
        
        # 打印班级统计
        class_stats = self.get_class_stats()
        print(f"\n班级统计:")
        print(f"  学生人数: {class_stats['学生人数']}")
        print(f"  班级平均总分: {class_stats['班级平均总分']}")
        print(f"  班级平均平均分: {class_stats['班级平均平均分']}")
        print(f"  最高平均分: {class_stats['最高平均分']}")
        print(f"  最低平均分: {class_stats['最低平均分']}")
