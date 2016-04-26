# coding=utf-8
import threading
import time
import urllib2


class UploadFile:
    def __init__(self):
        pass

    @staticmethod
    def upload(file_path, filename, type='img', timeout=10):
        boundary = '----------%s' % hex(int(time.time() * 1000))
        data = ['--%s' % boundary]

        fr = open(file_path, 'rb')
        data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('file', filename))
        if type == 'img':
            data.append('Content-Type: %s\r\n' % 'image/*')
        elif type == 'file':
            data.append('Content-Type: %s\r\n' % 'text/*')
        elif type == 'json':
            data.append('Content-Type: %s\r\n' % 'application/json')
        data.append(fr.read())
        fr.close()
        data.append('--%s--\r\n' % boundary)

        http_url = 'http://uiauto.beta.qunar.com/upload/file'
        http_body = '\r\n'.join(data)
        try:
            req = urllib2.Request(http_url, data=http_body)
            req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
            req.add_header('User-Agent', 'Mozilla/5.0')
            resp = urllib2.urlopen(req, timeout=timeout)
            print resp.read()
        except Exception, e:
            print 'upload fail'
            print e

    @staticmethod
    def upload_backgroud(file_path, filename, type='img', timeout=30):
        upload_thread = threading.Thread(target=UploadFile.upload, args=(file_path, filename, type, timeout))
        upload_thread.start()
        upload_thread.join()


if __name__ == '__main__':
    # UploadFile.upload('pic.png','pic.png')
    # UploadFile.upload('pc_beta_last.log','pc_beta_last.log')
    UploadFile.upload('report.html', 'report.html')
