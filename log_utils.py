import logging
import functools
import inspect
import os
from datetime import datetime
import traceback
import threading

# 添加一个线程本地存储，用于跟踪调用深度
_thread_local = threading.local()

def get_indent_level():
    if not hasattr(_thread_local, 'indent'):
        _thread_local.indent = 0
    return _thread_local.indent

def increase_indent():
    if not hasattr(_thread_local, 'indent'):
        _thread_local.indent = 0
    _thread_local.indent += 1

def decrease_indent():
    if not hasattr(_thread_local, 'indent'):
        _thread_local.indent = 0
    _thread_local.indent = max(0, _thread_local.indent - 1)

# 配置日志
def setup_logger():
    # 创建logs目录（如果不存在）
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 生成日志文件名，包含时间戳
    log_filename = f'logs/function_trace_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(message)s',
        datefmt='%H:%M:%S',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # 获取根日志记录器
    root_logger = logging.getLogger()
    
    # 设置PIL相关模块的日志级别为WARNING，以过滤掉DEBUG级别的日志
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('PngImagePlugin').setLevel(logging.WARNING)
    
    # 设置其他可能产生大量日志的模块级别
    logging.getLogger('PIL.Image').setLevel(logging.WARNING)
    logging.getLogger('PIL.ImageFile').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

logger = setup_logger()

def safe_str(obj):
    """安全地将对象转换为字符串"""
    try:
        return str(obj)
    except:
        return "<无法转换为字符串的对象>"

def format_log_message(caller_info, action, func_name, details):
    """格式化日志消息，使分隔符对齐"""
    # 获取当前缩进级别
    indent = get_indent_level()
    indent_str = '    ' * indent  # 使用4个空格作为一个缩进级别
    
    # 定义固定宽度
    caller_width = 50
    action_width = 15
    func_width = 40
    
    # 格式化各部分
    caller_part = f"{indent_str}来自: {caller_info}".ljust(caller_width + len(indent_str))
    action_part = f"{action}".ljust(action_width)
    func_part = f"{func_name}".ljust(func_width)
    
    # 组合消息
    return f"{caller_part} | {action_part} | {func_part} | {details}"

def trace_function(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # 获取函数所在文件、行号和函数名
            frame = inspect.currentframe()
            if frame is None:
                caller_info = "未知调用者"
            else:
                caller_frame = frame.f_back
                if caller_frame is None:
                    caller_info = "未知调用者"
                else:
                    filename = os.path.basename(caller_frame.f_code.co_filename)
                    line_number = caller_frame.f_lineno
                    caller_name = caller_frame.f_code.co_name
                    caller_info = f"{filename}:{line_number} - {caller_name}"

            # 安全地获取函数参数
            try:
                func_args = inspect.signature(func).bind(*args, **kwargs)
                func_args.apply_defaults()
                args_dict = {k: safe_str(v) for k, v in func_args.arguments.items()}
            except:
                args_dict = {"args": safe_str(args), "kwargs": safe_str(kwargs)}

            # 记录函数调用开始
            full_func_name = f"{func.__module__}.{func.__name__}"
            log_msg = format_log_message(
                caller_info, 
                "调用函数", 
                full_func_name, 
                f"参数: {args_dict}"
            )
            logger.debug(log_msg)
            
            # 增加缩进级别
            increase_indent()
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 减少缩进级别
            decrease_indent()

            # 安全地记录返回值
            try:
                result_str = safe_str(result)
            except:
                result_str = "<无法转换为字符串的返回值>"

            log_msg = format_log_message(
                caller_info, 
                "函数返回", 
                full_func_name, 
                f"返回值: {result_str}"
            )
            logger.debug(log_msg)

            return result

        except Exception as e:
            # 减少缩进级别（发生异常时也要确保缩进级别正确）
            decrease_indent()
            
            # 记录详细的异常信息
            full_func_name = f"{func.__module__}.{func.__name__}"
            error_details = f"异常类型: {type(e).__name__} | 异常信息: {str(e)} | 堆栈跟踪: {traceback.format_exc()}"
            
            log_msg = format_log_message(
                caller_info, 
                "函数异常", 
                full_func_name, 
                error_details
            )
            logger.error(log_msg)
            
            # 重新抛出异常，但不中断程序
            return None

    return wrapper 