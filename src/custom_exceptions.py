import traceback
import sys

class CustomException(Exception):
    def __init__(self, 
                 error_message, 
                 error_detail: sys,
                 *args):
        super().__init__(error_message, *args)
        self.error_message = self.__get_detailed_error_message(error_message, error_detail)
    
    @staticmethod
    def __get_detailed_error_message(self, error_message):
        _, _, exc_traceback = traceback.sys.exc_info()
        exc_filename = exc_traceback.tb_frame.f_code.co_filename
        exc_lineno = exc_traceback.tb_lineno

        return f"Error Occured In {exc_filename}, line: {exc_lineno}, \n Error : {error_message}"
    
    def __str__(self):
        return self.error_message