from ctypes import CDLL

dll = CDLL("./bin/Debug/MyLib.dll")
dll.mylib_function()
