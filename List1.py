#coding=utf-8
import wx
from wxpy import *
import wx  
import re

#import MySQLdb
#import pymysql
import pymysql
#pymysql.install_as_MySQLdb()

import _thread
import time

pause = 0 #讀取微信時暫停檢查資料庫
content=0 #內容未更新前暫停檢查資料庫

def print_time( threadName, delay):
   while 1:
      time.sleep(delay)
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

def create(parent):
  global pause
  global content 
  return Frame1(parent)
# assign ID numbers
[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, wxID_FRAME1LISTBOX1, 
] = [wx.NewId() for _init_ctrls in range(4)]
class Frame1(wx.Frame):


  def check_act(self,threadName, delay):
   global pause 
   global conten
   while 1:
    if(pause==0 and content==1):
      #print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
      time.sleep(delay)
      try:
        cur.execute("SELECT * FROM contact WHERE Active > %s" , '0')  #执行sql
        cxn.commit()   
        #rs=cur.fetchone()  #获取一行记录
        #print(rs)
        #rs=cur.fetchmany(2) #获取余下记录中的2行记录
        #print(rs)
        ars=cur.fetchall()  #获取剩下的所有记录
        for rs in ars:
          mess = self.txtCtrl1.GetValue()

          if(rs[2]!=''):
            mess=rs[2]

          self.bot.file_helper.send(rs[0]+":"+mess)
          self.my_friend = self.bot.friends().search(rs[0])[0]
          self.my_friend.send(mess)  


          print(rs)
          sql = "UPDATE contact SET Active='0',Message='' WHERE Name='%s'" %rs[0]
          cur.execute(sql)
          sql = "UPDATE contact SET Message='' WHERE Name='%s'" %rs[0]
          cur.execute(sql)

          self.SetTitle(rs[0]+":"+mess)

          #sel=self.listBox1.FindString(rs[0])
          self.listBox1.SetStringSelection(rs[0])

        cxn.commit()
      except Exception as e:
        print("Error to select:",e)


  def _init_ctrls(self, prnt):
    # BOA generated methods
    wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
       pos=wx.Point(358, 184), size=wx.Size(299, 387),
       style=wx.DEFAULT_FRAME_STYLE, title=u'微信')
    self.SetClientSize(wx.Size(291, 347))
    self.SetBackgroundColour(wx.Colour(0, 128, 0))
    self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label=u'連接手機微信號',
       name='button1', parent=self, pos=wx.Point(8, 8), size=wx.Size(176,
       28), style=0)
    self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
       id=wxID_FRAME1BUTTON1)
    self.listBox1 = wx.ListBox(choices=[], id=wxID_FRAME1LISTBOX1,
       name='listBox1', parent=self, pos=wx.Point(8, 48),
       size=wx.Size(276, 224), style=0)
    self.listBox1.SetBackgroundColour(wx.Colour(255, 255, 128))
    self.listBox1.Bind(wx.EVT_LISTBOX, self.OnListBox1Listbox,
       id=wxID_FRAME1LISTBOX1)
    self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label=u'發送',
       name='button2', parent=self, pos=wx.Point(104, 312),
       size=wx.Size(87, 28), style=0)
    self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
       id=wxID_FRAME1BUTTON2)

    self.txtCtrl1 = wx.TextCtrl(self, pos=(8,280), size =(276, 20), style = wx.TE_CENTER)
    self.txtCtrl1.SetValue('產線生產警示，請即時關注!')
    try:
      _thread.start_new_thread( self.check_act, ("Thread-1", 5, ) )
      #_thread.start_new_thread( print_time, ("Thread-2", 5, ) )
    except:
      print ("Error: unable to start thread")



  def __init__(self, parent):
    self._init_ctrls(parent)

  def OnButton1Button(self, event):
    '''
    click button to load the listbox with names
    '''
    global pause
    global content 

    pause=1
    #print(pause)
    try:
    #建立与数据库的连接
      print ("Clear to python.contact ....")
      cur.execute("TRUNCATE TABLE contact")    #清除Table
      cxn.commit()           
    except:
      print ("Could not connect to MySQL server.")
      exit( 0 )

          
     

    self.SetTitle("Select a name ...")
    self.listBox1.Clear()
    self.bot = Bot()
    friendlist=self.bot.friends()
    
    j=0
    for i in friendlist:
      if(j>0):
        s = str(i).replace('Friend: ','').strip('<>')
        self.listBox1.Append(s)

        values = [s,0,""]
        cur.execute("INSERT INTO contact VALUES(%s, %s, %s)" ,values)          #新增一筆
        cxn.commit()                #向数据库提交数据
      j=j+1
    
    pause=0  
    content=1

  def OnListBox1Listbox(self, event):
    '''
    click list item and display the selected string in frame's title
    '''
    selName = self.listBox1.GetStringSelection()
    self.SetTitle(selName)

  def OnButton2Button(self, event):
    '''
    click button to clear the listbox items
    '''
    fri = self.listBox1.GetStringSelection()
    if(fri!=''):
      mess = self.txtCtrl1.GetValue()
      self.bot.file_helper.send(fri+":"+mess)
      self.my_friend = self.bot.friends().search(fri)[0]
      self.my_friend.send(mess)  
#--------------- end of class Frame1 --------------------
# program entry point ...
if __name__ == '__main__':

  app = wx.App()
  wx.InitAllImageHandlers()
  frame = create(None)
  frame.Show()
  try:
  #建立与数据库的连接
    print ("Connecting to MySQL server....")
    cxn = pymysql.connect(host='10.97.60.214', user='root', passwd='00000000', db='LES',charset = 'utf8mb4')
    #cxn = MySQLdb.connect(host='localhost', user='root', passwd='00000000', db='python')
  except:
    print ("Could not connect to MySQL server.")
    exit( 0 )
  print ("Connected to host='10.97.60.214', user='root', passwd='00000000', db='LES' MySQL server.")
  cur=cxn.cursor()         # 使用cursor()方法获取操作游标
    #conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='t1')

  
  app.MainLoop()