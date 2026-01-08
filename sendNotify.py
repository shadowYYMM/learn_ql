import smtplib
from email.utils import formataddr as sync_formataddr
from email.header import Header as sync_Header
from email.mime.text import MIMEText as sync_MIMEText
import logging
from typing import Optional, Dict, Any

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 假设 push_config 是一个全局字典
push_config = {
    "SMTP_SERVICE": "",
    "SMTP_EMAIL": "",
    "SMTP_PASSWORD": "",
    "SMTP_NAME": "",
    "SMTP_SERVER": "",
    "SMTP_PORT": 465,
    "SMTP_SSL": True,
    "SMTP_TLS": False,
}


# 同步版本的 SMTP 通知函数（兼容性）
def smtp_notify_sync(text: str, desp: str) -> Optional[bool]:
    """
    使用 SMTP 邮件推送消息（同步版本）
    
    Args:
        text: 邮件标题
        desp: 邮件内容
        
    Returns:
        bool: 成功返回True，失败返回False，配置不完整返回None
    """
    smtp_email = push_config.get("SMTP_EMAIL")
    smtp_password = push_config.get("SMTP_PASSWORD")
    smtp_service = push_config.get("SMTP_SERVICE")
    smtp_name = push_config.get("SMTP_NAME", "")
    
    if not all([smtp_email, smtp_password, smtp_service]):
        logger.info("SMTP 配置不完整，跳过邮件推送")
        return None
    
    logger.info("SMTP 邮件服务启动（同步版本）")
    
    try:
        # 使用预设的常见服务
        if smtp_service.lower() == "qq":
            smtp_server = "smtp.qq.com"
            smtp_port = 465
            use_ssl = True
        elif smtp_service.lower() == "163":
            smtp_server = "smtp.163.com"
            smtp_port = 465
            use_ssl = True
        elif smtp_service.lower() == "gmail":
            smtp_server = "smtp.gmail.com"
            smtp_port = 465
            use_ssl = True
        else:
            # 通用配置
            smtp_server = push_config.get("SMTP_SERVER", "smtp.qq.com")
            smtp_port = int(push_config.get("SMTP_PORT", 465))
            use_ssl = push_config.get("SMTP_SSL", True)
        
        # 创建邮件
        html_content = desp.replace('\n', '<br/>')
        msg = sync_MIMEText(html_content, 'html', 'utf-8')
        
        if smtp_name:
            from_addr = sync_formataddr((sync_Header(smtp_name, 'utf-8').encode(), smtp_email))
        else:
            from_addr = smtp_email
        
        msg['From'] = from_addr
        msg['To'] = from_addr
        msg['Subject'] = sync_Header(text, 'utf-8')
        
        # 发送邮件
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, smtp_email, msg.as_string())
        server.quit()
        
        logger.info("SMTP 发送通知消息成功 🎉")
        return True
        
    except Exception as e:
        logger.error(f"SMTP 发送通知消息出现异常 😞: {str(e)}")
        logger.debug("详细错误信息:", exc_info=True)
        return False


# 如果需要同步运行
if __name__ == "__main__":
    # 同步版本测试
    result = smtp_notify_sync("同步测试", "这是同步版本测试")
    print(f"同步版本结果: {result}")
