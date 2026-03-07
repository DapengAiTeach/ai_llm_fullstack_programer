"""
提示词加载器模块
支持从文件加载系统提示词，并提供热更新功能
"""
import os
from pathlib import Path


class PromptLoader:
    """提示词加载器，支持缓存和热更新"""
    
    _instance = None
    _cache = {}
    _last_modified = {}
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化，设置提示词目录"""
        if not hasattr(self, '_initialized'):
            # 提示词目录相对于项目根目录
            self.prompts_dir = Path(__file__).parent.parent.parent / 'prompts'
            self._initialized = True
    
    def _get_file_path(self, name):
        """获取提示词文件路径"""
        file_path = self.prompts_dir / f'{name}.md'
        return file_path
    
    def _is_file_modified(self, name, file_path):
        """检查文件是否被修改"""
        if not file_path.exists():
            return False
        
        current_mtime = file_path.stat().st_mtime
        last_mtime = self._last_modified.get(name, 0)
        
        return current_mtime > last_mtime
    
    def load(self, name='system', force_reload=False):
        """
        加载提示词
        
        Args:
            name: 提示词文件名（不含扩展名）
            force_reload: 是否强制重新加载
            
        Returns:
            str: 提示词内容
            
        Raises:
            FileNotFoundError: 文件不存在
        """
        file_path = self._get_file_path(name)
        
        # 检查是否需要重新加载
        needs_reload = (
            force_reload or
            name not in self._cache or
            self._is_file_modified(name, file_path)
        )
        
        if needs_reload:
            if not file_path.exists():
                raise FileNotFoundError(f'提示词文件不存在: {file_path}')
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新缓存
            self._cache[name] = content
            self._last_modified[name] = file_path.stat().st_mtime
            
            print(f'[PromptLoader] 已加载提示词: {name}')
        
        return self._cache[name]
    
    def get_system_prompt(self, force_reload=False):
        """
        获取系统提示词（快捷方法）
        
        Args:
            force_reload: 是否强制重新加载
            
        Returns:
            str: 系统提示词内容
        """
        return self.load('system', force_reload=force_reload)
    
    def clear_cache(self, name=None):
        """
        清除缓存
        
        Args:
            name: 指定提示词名称，None 表示清除所有缓存
        """
        if name is None:
            self._cache.clear()
            self._last_modified.clear()
            print('[PromptLoader] 已清除所有缓存')
        else:
            self._cache.pop(name, None)
            self._last_modified.pop(name, None)
            print(f'[PromptLoader] 已清除缓存: {name}')
    
    def list_available(self):
        """
        列出可用的提示词文件
        
        Returns:
            list: 可用提示词名称列表
        """
        if not self.prompts_dir.exists():
            return []
        
        available = []
        for file_path in self.prompts_dir.glob('*.md'):
            available.append(file_path.stem)
        
        return sorted(available)


# 全局提示词加载器实例
_prompt_loader = None


def get_prompt_loader():
    """获取全局提示词加载器实例"""
    global _prompt_loader
    if _prompt_loader is None:
        _prompt_loader = PromptLoader()
    return _prompt_loader


def get_system_prompt(force_reload=False):
    """
    获取系统提示词的快捷函数
    
    Args:
        force_reload: 是否强制重新加载
        
    Returns:
        str: 系统提示词内容
    """
    loader = get_prompt_loader()
    return loader.get_system_prompt(force_reload=force_reload)
