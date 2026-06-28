#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据管理模块 - 负责学生数据的增删改查和文件读写
作者：汪心雨
学号：2550204105
"""

import json
import os
from typing import List, Dict, Optional


class DataManager:
    """学生数据管理类"""
    
    def __init__(self, data_file: str = "students.json"):
        self.data_file = data_file
        self.students: List[Dict] = []
        self._load_data()
    
    def _load_data(self) -> None:
        """从文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.students = json.load(f)
            except Exception as e:
                print(f"加载数据失败: {e}")
                self.students = []
        else:
            self.students = []
    
    def save_data(self) -> None:
        """保存数据到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.students, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {self.data_file}")
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    def import_from_file(self, file_path: str) -> bool:
        """从外部文件导入学生成绩数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # 尝试 JSON 格式
            if file_path.endswith('.json'):
                data = json.loads(content)
            else:
                # 尝试解析文本格式: 学号,姓名,科目1,科目2,科目3...
                data = self._parse_text_format(content)
            
            if isinstance(data, list):
                self.students.extend(data)
            else:
                self.students.append(data)
            
            self.save_data()
            print(f"成功导入 {len(data) if isinstance(data, list) else 1} 条记录")
            return True
            
        except Exception as e:
            print(f"导入失败: {e}")
            return False
    
    def _parse_text_format(self, content: str) -> List[Dict]:
        """解析文本格式数据"""
        lines = content.strip().split('\n')
        students = []
        
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                student = {
                    "学号": parts[0].strip(),
                    "姓名": parts[1].strip(),
                    "成绩": {}
                }
                # 解析科目成绩
                for i in range(2, len(parts)):
                    subject_score = parts[i].strip().split(':')
                    if len(subject_score) == 2:
                        student["成绩"][subject_score[0].strip()] = float(subject_score[1].strip())
                    else:
                        # 默认科目名
                        student["成绩"][f"科目{i-1}"] = float(parts[i].strip())
                students.append(student)
        
        return students
    
    def add_student(self, student_id: str, name: str, scores: Dict[str, float]) -> bool:
        """添加学生"""
        # 检查学号是否已存在
        if self.find_by_id(student_id):
            print(f"学号 {student_id} 已存在！")
            return False
        
        student = {
            "学号": student_id,
            "姓名": name,
            "成绩": scores
        }
        self.students.append(student)
        self.save_data()
        print(f"成功添加学生: {name}")
        return True
    
    def delete_student(self, student_id: str) -> bool:
        """删除学生"""
        for i, student in enumerate(self.students):
            if student["学号"] == student_id:
                del self.students[i]
                self.save_data()
                print(f"已删除学号为 {student_id} 的学生")
                return True
        print(f"未找到学号 {student_id}")
        return False
    
    def update_student(self, student_id: str, name: str = None, scores: Dict[str, float] = None) -> bool:
        """修改学生信息"""
        student = self.find_by_id(student_id)
        if not student:
            print(f"未找到学号 {student_id}")
            return False
        
        if name:
            student["姓名"] = name
        if scores:
            student["成绩"].update(scores)
        
        self.save_data()
        print(f"已更新学号 {student_id} 的信息")
        return True
    
    def find_by_id(self, student_id: str) -> Optional[Dict]:
        """按学号查询"""
        for student in self.students:
            if student["学号"] == student_id:
                return student
        return None
    
    def find_by_name(self, name: str) -> List[Dict]:
        """按姓名查询（支持模糊匹配）"""
        results = []
        for student in self.students:
            if name in student["姓名"]:
                results.append(student)
        return results
    
    def get_all_students(self) -> List[Dict]:
        """获取所有学生"""
        return self.students
    
    def export_results(self, file_path: str, data: List[Dict]) -> bool:
        """导出统计结果到新文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"结果已导出到 {file_path}")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False
