__author__ = 'DarkWing'

import win32gui
import win32ui
import win32con
import win32api

hdesktop = win32gui.GetDesktopWindow()

width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSVREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSVREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSVREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSVREEN)

desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

mem_dc = img_dc.CreateCompatibleDC()

screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc,width,height)
mem_dc.SelectObject(screenshot)

mem_dc.BitBlt((0,0),(width,height),img_dc,(left,top),win32con.SRCCOPY)

screenshot.SaveBitmapFile(mem_dc,"screenshot.bmp")

mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())

