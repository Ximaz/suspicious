import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMailService:
    __server: smtplib.SMTP | None = None

    def __init__(self, host: str, port: int) -> None:
        self.__host = host
        self.__port = port

    def connect(self) -> None:
        self.__server = smtplib.SMTP(self.__host, self.__port)

    def __create_mail(
        self,
        subject: str,
        sender: str,
        recipient: str,
        html: str,
    ) -> str:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = str(recipient)
        msg["Subject"] = str(subject)

        # Attach the HTML content to the email
        msg.attach(MIMEText(html, "html"))

        return msg.as_string()

    def publish_email(
        self,
        subject: str,
        sender: str,
        recipient: str,
        html: str,
    ) -> None:
        if self.__server is None:
            raise Exception("The SMTP server is not connected.")

        message = self.__create_mail(
            subject=subject, sender=sender, recipient=recipient, html=html
        )

        self.__server.sendmail(sender, recipient, message)

    def close(self):
        if self.__server is None:
            raise Exception("The SMTP server is not connected.")

        self.__server.quit()
