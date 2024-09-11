import smtplib
import re
import os
import logging
from email.mime.text import MIMEText
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# 加载环境变量
load_dotenv()

# 从环境变量中读取配置
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')


class VerificationEmailSender:
    _smtp_server = 'smtp.163.com'  # 邮箱服务器地址
    _smtp_port = 25  # 使用非SSL的邮箱服务器端口（保持和有效代码一致）

    def __init__(self, recipient_email: str):
        if not self._validate_email(recipient_email):
            raise ValueError("Invalid email address format")
        self._recipient_email = recipient_email

    @staticmethod
    def _validate_email(email: str) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def send(self, verification_code: str) -> bool:
        # 设置邮件内容
        message = MIMEText(
            f'you\'re registering InubashiriLix blog, and vertification code is {verification_code}',  # 邮件正文内容
            'plain',  # 邮件格式
            'utf-8'  # 编码
        )

        message['From'] = SENDER_EMAIL  # 发件人
        message['To'] = self._recipient_email  # 收件人
        message['Subject'] = '【 Verification 】 InubashiriLix Blog Verification'

        try:
            # 使用 SMTP 而非 SMTP_SSL 来发送邮件
            with smtplib.SMTP(self._smtp_server, self._smtp_port) as smtp_connection:
                smtp_connection.login(SENDER_EMAIL, SENDER_PASSWORD)
                smtp_connection.sendmail(SENDER_EMAIL, [self._recipient_email], message.as_string())

            print("邮件发送成功！")
            return True

        except smtplib.SMTPException as e:
            logging.error("邮件发送失败：%s", e)
            print("邮件发送失败：", e)
            return False


def send_verification_email_async(recipient_email: str, verification_code: str) -> bool:
    sender = VerificationEmailSender(recipient_email)
    state_code_bool = sender.send(verification_code)
    return state_code_bool


def send_email_in_background(recipient_email: str, verification_code: str):
    # 使用线程池来异步发送邮件，测试专用函数
    with ThreadPoolExecutor() as executor:
        future = executor.submit(send_verification_email_async, recipient_email, verification_code)
        return future.result()


# 如果需要测试该脚本
if __name__ == '__main__':
    # 异步发送邮件
    send_email_in_background("13329001003@163.com", "137274")
