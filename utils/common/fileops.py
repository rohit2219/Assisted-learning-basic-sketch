from utils.common.functions import print_class

class fileops(object):

#    def __new__(self,file_name,file_mode):
#        ret_code = 0

    def __init__(self,file_object):
        self.file_object= file_object
        self.print_class=print_class()
        
    def file_close(self):
        ret_code=0
        try:

            self.file_object.close()
        except IOError as e:
            print_char = "I/O error({0}):"+ format(e.errno, e.strerror)
            self.print_class.print_char(print_char)
            ret_code = 99999
        return ret_code

    def file_write_line(self, content):
        ret_code = 0
        try:
            self.file_object.write(content)
        except IOError as e:
            print_char = "I/O error ({0}) while writing file:"+ self.file_object.name + format(e.errno, e.strerror)
            self.print_class.print_char(print_char)
            ret_code = 99999
        return ret_code

    def file_read_line(self):
        ret_line = "99999"
        try:
            ret_line = self.file_object.readline()
        except IOError as e:
            print_char = "I/O error({0}) while reading file :"+ self.file_object.name + format(e.errno, e.strerror)
            self.print_class.print_char(print_char)

        return ret_line
