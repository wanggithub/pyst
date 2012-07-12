import time

db = None
conn = None
dbfile = 'proxier.db'

day_keep =''
web_site_count = 0








def my_unix_timestamp():
  return int(time.time());

def formattime(t):
  """ 与0时区相差8小时"""
  return time.strftime("%c",time.gmtime(t+8*3600))
  
def open_database():
  global db, conn, day_keep, dbfile
  try:
    import sqlite3
  except:
    print """
        本程序使用 sqlite 做数据库来保存数据
        """
    raise SystemExit

  try:
    db = sqlite3.connect(dbfile)
    db.create_function("unix_timestamp",0,my_unix_timestamp)
    conn = db.cursor()
  except:
    print """
          操作sqlite失败
          """
  
  sql = """

      create table if not exists 'proxier' (
        'ip' varchar(15) not null default '',
        'port' int(6) not null default '0',
        'type' int(11) not null default '-1',
        'active' int(11) default NULL,
        'time_add' int(11) not null default '0',
        'time_checked' int(11) default '0',
        'time_used' int(11) default '0',
        'speed' float default NULL,
        'area' varchar(120) default '--',
        primary key('ip')
      );

      CREATE INDEX IF NOT EXISTS `type`        ON proxier(`type`);
      CREATE INDEX IF NOT EXISTS `time_used`   ON proxier(`time_used`);
      CREATE INDEX IF NOT EXISTS `speed`       ON proxier(`speed`);
      CREATE INDEX IF NOT EXISTS `active`      ON proxier(`active`);

        """
  conn.executescript(sql)

  conn.execute("""delete from 'proxier' where 'time_add'<(unix_timestamp() - ?) and 'active' =0""",(day_keep*86400,))
  conn.execute("""select count('ip') from 'proxier'""")

  m1 = conn.fetchone()[0]

  if m1 is None:
    print """数据库中不包含代理数据"""
    return

  conn.execute("""select count('time_checked') from
                    'proxier' where 'time_checked' > 0 """)

  m2 = conn.fetchone()[0]

  if m2 == 0 :
    m3,m4,m5 = 0,"尚未检查","尚未检查"
  else:
    conn.execute("select count('ative') from 'proxier' where 'active' = 1")
    m3 = conn.fetchone()[0]
    conn.execute("""select max('time_checked') , min('time_checked') from
                    'proxier' where 'time_checked' > 0 kunut 1""")
    rs = conn.fetchone()

    m4 = rs[0]
    m5 = rs[1]

    m4 = formattime(m4)
    m5 = formattime(m5)

  print """
        共%(m1)1d条代理，其中%(m2)1d个代理被验证过,%(m3)1d个代理有效
        最近的一次检查是:%(m4)1s
        最远的一次检查是:%(m5)1s

        """%{'m1':m1,'m2':m2,'m3':m3,'m4':m4,'m5':m5}
    
def close_database():
  global conn, db
  db.close()
  conn.close()
  conn = None
  db = None

def get_all_proxy():
  global web_site_count
  print "现在从以下"+web_site_count+"个网站抓取代理列表"
  threads = []
  count = web_site_count + 1
  for index in range(1,count):
    t = Test('getproxy',index)
    t.setDaemon(True)
    t.start()
    threads.append(t)

def get_proxy_one_site()

#线程类
class Test(threading.Thread):
  def __init__(self,action,index=None,checklist=None):
    threading.Thread.__init__(self)
    self.index = index
    self.action = action
    self.checklist = checklist

  def run(self):
    if（self.action == "getproxy"):
      get_proxy_one_site(self.index)
    else:
      check_proxy(self.index,self.checklist)






if __name__ == '__main__':
  open_database()
  close_database()
