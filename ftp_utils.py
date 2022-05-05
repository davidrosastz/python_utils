import ftplib
import pathlib

class NotLoggedInException(Exception):
    pass

class FtpUtils:
    ftp_host: str
    ftp_user: str
    ftp_password: str
    ftp: ftplib.FTP
    encoding: str

    def __init__(self, ftp_host: str, ftp_user: str, ftp_password: str, encoding: str='UTF-8') -> None:
        self.ftp_host = ftp_host
        self.ftp_user = ftp_user
        self.ftp_password = ftp_password
        self.encoding = encoding
        self.ftp_login()

    def ftp_login(self) -> None:
        self.ftp = ftplib.FTP(self.ftp_host, self.ftp_user, self.ftp_password)
        self.ftp.encoding = self.encoding

    def create_directory(self, directory: str) -> None:
        directories = pathlib.Path(directory).parts
        if len(directories) > 1:
            for dir in directories[1:]:
                try:
                    self.ftp.cwd(dir)

                except ftplib.error_perm as e:
                    self.ftp.mkd(dir)
                    self.ftp.cwd(dir)

    def change_directory(self, directory: str) -> None:
        self.ftp.cwd(directory)

    def upload_file(self, local_file_path: str, ftp_file_path: str='/') -> None:
        if not self.ftp:
            raise NotLoggedInException('No user logged in to the ftp server')

        self.create_directory(ftp_file_path)
        self.change_directory(ftp_file_path)
        with open(local_file_path, 'rb') as f:
            self.ftp.storbinary(f"STOR {local_file_path}", f)
