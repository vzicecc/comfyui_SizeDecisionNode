import torch
from torch import nn

import comfy

# 注册节点到ComfyUI系统
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

class SizeDecisionNode:
    """
    尺寸决策节点
    功能：根据输入尺寸自动判断方向并返回预设尺寸组合
    - 横向（宽>高+阈值）：返回横向预设
    - 竖向（高>宽+阈值）：返回竖向预设
    - 正方形（差值<=阈值）：返回正方形预设
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义输入参数"""
        return {
            "required": {
                "原始宽度": ("INT", {"default": 512, "min": 1}),  # 原始尺寸输入
                "原始高度": ("INT", {"default": 512, "min": 1}),
                "正方形阈值": ("INT", {"default": 64, "min": 0}),  # 正方形判断容差
                
                # 各方向预设尺寸
                "横向宽度": ("INT", {"default": 1024, "min": 1}),
                "横向高度": ("INT", {"default": 768, "min": 1}),
                "竖向宽度": ("INT", {"default": 768, "min": 1}),
                "竖向高度": ("INT", {"default": 1024, "min": 1}),
                "正方形宽度": ("INT", {"default": 1024, "min": 1}),
                "正方形高度": ("INT", {"default": 1024, "min": 1}),
            }
        }

    RETURN_TYPES = ("INT", "INT")  # 输出宽高
    RETURN_NAMES = ("输出宽度", "输出高度")
    FUNCTION = "decide_size"      # 主处理函数
    CATEGORY = "AI绘图/工具"       # 节点分类

    def decide_size(self, 原始宽度, 原始高度, 正方形阈值, 
                  横向宽度, 横向高度, 竖向宽度, 竖向高度,
                  正方形宽度, 正方形高度):
        """尺寸决策逻辑"""
        delta = abs(原始宽度 - 原始高度)
        
        # 正方形判断（包含阈值）
        if delta <= 正方形阈值:
            return (正方形宽度, 正方形高度)
            
        # 横向判断
        elif 原始宽度 > 原始高度:
            return (横向宽度, 横向高度)
            
        # 竖向判断
        else:
            return (竖向宽度, 竖向高度)

# 注册节点
NODE_CLASS_MAPPINGS["SizeDecisionNode"] = SizeDecisionNode
NODE_DISPLAY_NAME_MAPPINGS["SizeDecisionNode"] = "智能尺寸决策器"

# 导出配置（供ComfyUI加载）
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']