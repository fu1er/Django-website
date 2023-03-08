# 视频网站爬虫、查询与数据分析实验

## 访问网站

浏览器中输入`http://101.43.196.108:8000/videopage/`

## 运行

```bash
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```
* ### 项目设计

  1. 系统功能以及实现方法

     整个项目分为爬虫和网站建设两部分

     * 爬虫

       爬虫部分爬取的是 Bilibili 若干分区八月份的热门视频。因为该网站的网页都是动态网页，为此使用了 selenium 库来模拟浏览器的访问以动态获取到当前页面的源码。在使用该模块之前，爬虫项目使用的是 python 自带的 reques 去请求网页源码，但是请求到的源码没有包含需要的信息，后来使用了 selenium 库才成功解决这个问题。

       ```python
       from selenium import webdriver
       from selenium.webdriver.common.keys import Keys
       from selenium.webdriver.chrome.options import Options
       
       chrome_options = Options()
       chrome_options.add_argument('--headless')
       chrome_options.add_argument('--disable-gpu')
       browser = webdriver.Chrome(options=chrome_options)
       ```

       由于 selenium 库是直接操控浏览器去访问网页，所以在爬取信息的时候总是会打开新的浏览器窗口，因此项目中用上述代码实现浏览器在后台运行，使得爬取数据时界面比较清爽。

       ```python
       while dat_total < dat_need:
           page = browser.page_source
           # 用BS解析网页源码
           BS_page = BeautifulSoup(page, 'html.parser')
           # 匹配资源
           AREA = BS_page.find('div', class_='l-con')
           area = AREA.find('div', class_="vd-list-cnt")
           videolst = area.find_all('div', class_="r")
           for video in videolst:
               dat_total += 1
               url = 'https:'+video.find('a').get('href')# .strip('//')
               try:
                   '''option'''
                   page_option.op_func(url, dat_total)
                   '''finish'''
               except:
                   dat_total -= 1
                   continue
           page_num += 1
           browser.find_element_by_xpath('//*[@id="videolist_box"]/div[2]/div[2]/div/input').send_keys(page_num)
           browser.find_element_by_xpath('//*[@id="videolist_box"]/div[2]/div[2]/div/input').send_keys(Keys.ENTER)
           time.sleep(1)
       ```

       接下来就是爬取数据的部分了，首先是输入 URL ，为需要爬取的视频分区的网址，然后是 所需要的数据量和当前已经爬取的数据量，以及当前网页的分页数。用两个变量分别存储已经爬取的数据总量和需要爬取的数据量，在数据不够时进行循环。

       接下来用 selenium 库里的函数获取当前浏览器页面的源码，这样成功得到了包含所需信息的网页源码。之后应用 bs4 库里的 BeautifSoup 对得到的源码进行解析，根据分区网页的 HTML 代码的标签定位到网页中视频排行榜里所有的视频的URL，并对其进行格式化。

       然后调用另一个操作函数，传入该 URL ，操作是进入到具体的视频详情页面去爬取所需要的视频信息以及作者信息，并写入具体的文件里。如果爬取时出现错误，就直接跳过该视频的爬取。主要是应对作者删除视频但是平台没有及时更新的情况，此前没有加上这个逻辑时，曾出现作者已经删除了视频，但是排行榜上仍有该视频的排行，访问该视频的    URL 得到的是一个空页面导致程序异常终止。

       每次成功爬取一个视频对应的信息都会使得当前爬取的信息总数增加一。爬取完一页之后页码加一然后让浏览器在跳转框里输入对应的页码并按下回车键，用来模拟翻页的操作，进行下一页的爬取。

       以下是操作函数中部分内容：

       ```python
       def op_func(url, total):
           chrome_options = Options()
           chrome_options.add_argument('--headless')
           chrome_options.add_argument('--disable-gpu')
           browser = webdriver.Chrome(options=chrome_options)
           browser.get(url)
           time.sleep(3)
           js = "var q=document.documentElement.scrollTop=2000"
           browser.execute_script(js)
           time.sleep(2)
           page = browser.page_source
       ```

       函数开启新的浏览器，并向传入的 URL 发送 get 请求，请求到视频详情页的内容。在这里让程序等待了 3s 才进行下一步操作，是因为由于网速不足可能导致页面渲染慢，影响后续的操作。经过等待基本上网页已经加载好了，又因为BIlibili的评论区是动态加载的，只有下滑到评论区才会动态去请求评论区的内容。所以在这里程序模拟了一个下拉滚动条到评论区的操作，然后等待 2s 让评论充分加载。后面就是获取源码，用bf4解析源码，写入文件的操作了。

       ![image-20210910184911204](/Users/fu1er/Library/Application Support/typora-user-images/image-20210910184911204.png)

       ![image-20210910184930263](/Users/fu1er/Library/Application Support/typora-user-images/image-20210910184930263.png)

       ![image-20210910185023052](/Users/fu1er/Library/Application Support/typora-user-images/image-20210910185023052.png)

       数据和图片按照分区储存方便查看，程序最终爬取了共5106个视频对应的信息。

     * 网站

       网站的搭建使用的是 Django 框架，在处理数据的问题上，用的是 python 自带的 SQLite 库。

       在 Django 项目的模型里建立两个类，分别对应作者和视频，用于调用数据库里的数据，并且两者应该是一对多的关系，每个视频都有对应的作者：

       ```python
       from django.db import models
       
       class Author(models.Model):
           name = models.CharField(max_length=100)
           describe = models.TextField()
           followers = models.CharField(max_length=200)
           photo = models.CharField(max_length=200)
           def __str__(self):
               return self.name
       
       class Videoinfo(models.Model):
           video_name = models.CharField(max_length = 200)
           video_view = models.CharField(max_length = 200)
           publish_date = models.CharField(max_length = 200)
           likes = models.CharField(max_length = 200)
           coins = models.CharField(max_length = 200)
           collects = models.CharField(max_length = 200)
           brief = models.CharField(max_length = 500)
           comment = models.CharField(max_length = 1000)
           url = models.CharField(max_length = 200)
           cover = models.CharField(max_length=200)
           author = models.ForeignKey(Author, on_delete=models.CASCADE)
           def __str__(self):
               return self.video_name
       
       ```

       接下来做的是写一个脚本把爬取的数据导入到数据库里，具体做法是用爬到的信息创建 Author 和 Videoinfo 实例，然后保存到数据库里。特殊的是要先建立所有作者的数据表，然后在创建Videoinfo 实例的时候要先找到该视频对应的作者用来给 author 变量赋值，绑定好关系。建立好模型以及导入数据可以很大程度上简化后面网页建设处理数据访问的问题。

       接下来就是视图层的编写了。view.py 文件里包含了项目需要用到的所有请求的响应方法，有主页，作者页，搜索页，对应的搜索结果页等等。

       实现视频和作者等信息的分页展示我是使用了 Django 自带的 Paginator 模块，很简单地实现了分页设计。

       实现网页中搜索视频和作者的操作也使用了Django自带的数据查询功能，在模版里定义的两个数据的类都有 filter 方法，并且在搜索里支持用 __contains= 的方法来查询文本是否包含某一字段。查询时还利用了 Q 对象，使得查询能够支持 or 的并列查询。

       ```python
       result = Author.objects.all().filter(Q(name__contains=word)| Q(describe__contains=word))
       result = Videoinfo.objects.all().filter(Q(video_name__contains=word)| Q(brief__contains=word))
       ```

       这样的查询效率还不错。

       网页的顶端是一个导航栏，点击相应按钮可以跳转到对应的页面：

       ![image-20210910232133752](/Users/fu1er/Library/Application Support/typora-user-images/image-20210910232133752.png)

       搜索页面在没有匹配的结果时也会返回对应的信息提示没有结果。

* ### 数据分析

  1. 数据处理

     在数据处理这方面，直接对存储视频信息的 csv 文件进行一个读取

     ```python
     with open(file_name) as f:
         reader = csv.reader(f)
         for row in reader:
             vname.append(row[0])
             vview.append(row[1])
             vdate.append(row[2])
             vlike.append(row[3])
             vcoin.append(row[4])
             vcoll.append(row[5])
             vbrief.append(row[6])
             vcomment.append(row[7])
     ```

     将读取的结果放到建好的列表中方便使用。然后需要做的是对信息的格式的处理，因为读入的时候是以字符串的形式读入，且数据中会混有中文，所以先进行一些格式上的操作：

     ```python
     hours = []
     for date in vdate:
         hours.append(int(date[11:13]))
     views = []
     for view in vview[1:]:
         if view[-3] == '万':
             views.append(float(view[:-3])*10000)
         else:
             views.append(float(view[:-3]))
     likes = []
     for like in vlike[1:]:
         if like[-1] == '万':
             likes.append(float(like[:-1])*10000)
         else:
             likes.append(float(like))
     ```

     由此得到了视频发布的时间（精确到小时），播放量和点赞数。

  2. 结论1：作者上传视频的时间大多在下午和晚上，可能是由于这两个时间段活跃用户更多；舞蹈区的视频作者在00:00～06:00发布视频的比例多于知识区和游戏区，可能是由于观众群体活跃时间存在差异。

     对得到的视频发布时间绘制一个饼状图。

     ```python
     newlst = []
     add_time = 0
     for i in range(0, 6):
         add_time += time_list[0][i]
     newlst.append(add_time)
     add_time = 0
     for i in range(6, 12):
         add_time += time_list[0][i]
     newlst.append(add_time)
     add_time = 0
     for i in range(12, 18):
         add_time += time_list[0][i]
     newlst.append(add_time)
     add_time = 0
     for i in range(18, 24):
         add_time += time_list[0][i]
     newlst.append(add_time)
     add_time = 0
     
     plt.figure()
     plt.pie(x = newlst, labels = ['0~6','6_12','12~18','18~24'])
     plt.xlabel("publish time")
     plt.show()
     ```

     这里先对时间进行了一个简单的分段，因为对于时间来说分析较长一段时间的效果更好。

     <img src="/Users/fu1er/Library/Application Support/typora-user-images/image-20210910235340943.png" alt="image-20210910235340943" style="zoom:33%;" /><img src="/Users/fu1er/Library/Application Support/typora-user-images/image-20210910235431584.png" alt="image-20210910235431584" style="zoom:33%;" /><img src="/Users/fu1er/Library/Application Support/typora-user-images/image-20210910235552812.png" alt="image-20210910235552812" style="zoom:33%;" />

     可以看到，知识区、舞蹈区、游戏区的热门视频的发布时间是有差异的。其中舞蹈区的视频在0～6点这个时间段的比例明显大于其他两个分区，这有可能是由于观众群体不同造成的。另外，发布视频最集中的时间段是下午及晚上，因为这两个时间段活跃用户更多。

  3. 结论2:白嫖的人很多，但是舞蹈区的观众白嫖率【更低】。

     绘制点赞数和播放量之间的散点图：

     ```python
     plt.figure()
     plt.scatter(likes, views, s=3)
     plt.xlabel("likes")
     plt.ylabel("views")
     plt.show()
     ```

     <img src="/Users/fu1er/Library/Application Support/typora-user-images/image-20210911000607500.png" alt="image-20210911000607500" style="zoom:25%;" /><img src="/Users/fu1er/Library/Application Support/typora-user-images/image-20210911000720120.png" alt="image-20210911000720120" style="zoom:25%;" /><img src="/Users/fu1er/Library/Application Support/typora-user-images/image-20210911000811858.png" alt="image-20210911000811858" style="zoom:25%;" />

     由于游戏区八月份热门视频出现了一个两千多万播放量的现象级作品，导致散点图左下角过于密集，考虑到该点基本处于对角线上，先剔除该数据，即对数据进行一个切片后再生成图片，这样三个分区的播放量基本保持在同一量级上。：

     ```python
     for view in vview[1:]:
         if view[-3] == '万':
             views.append(float(view[:-3])*10000)
         else:
             views.append(float(view[:-3]))
     likes = []
     for like in vlike[1:]:
         if like[-1] == '万':
             likes.append(float(like[:-1])*10000)
         else:
             likes.append(float(like))
     ```

     ![image-20210911001153449](/Users/fu1er/Library/Application Support/typora-user-images/image-20210911001153449.png)

     

     横向比较，首先，三个分区的播放量和点赞数基本成正比，这是符合预期的，但是知识区和游戏区的观众明显更爱白嫖。在图的左侧出现了很多点，说明很多观众看完视频却连一个免费的赞都不愿意点。再看舞蹈区的散点图，左侧的点明显少于另外两个区，由此可见舞蹈区的观众白嫖率更低。

  4. 结论3: 11:00~13:00和18:00~20:00这两个时间段里发布的视频播放量显著高于其他时间段发布的视频的播放量。

     通过对数据的操作得到在每个小时的时间段里发布的视频的平均播放量：

     ```python
     time_list = np.zeros((1, 24))
     view_list = np.zeros((1, 24))
     for i in range(len(hours)):
         for t in range(1, 25):
             if hours[i] < t:
                 time_list[0][t-1] += 1
                 view_list[0][t-1] += views[i]
                 break
     for i in range(0, 24):
         if (time_list[0][i] != 0):
             view_list[0][i] = view_list[0][i]/time_list[0][i]
     X = np.linspace(1, 24, 24)
     Y = time_list[0]
     plt.figure()
     plt.bar(X, Y, 0.35,)
     plt.xlim(0, 25)
     plt.xlabel("publish time")
     plt.ylabel("views")
     plt.xticks(np.arange(0,25,1))
     plt.show()
     ```

     time_list 储存每个小时发布的视频总数， view_list 储存每个小时发布的视频的总播放量的和，最后求平均然后绘制图像：

     <img src="/Users/fu1er/Library/Application Support/typora-user-images/image-20210911002355683.png" alt="image-20210911002355683" style="zoom:25%;" /><img src="/Users/fu1er/Library/Application Support/typora-user-images/image-20210911002436856.png" alt="image-20210911002436856" style="zoom:25%;" /><img src="/Users/fu1er/Library/Application Support/typora-user-images/image-20210911002521282.png" alt="image-20210911002521282" style="zoom:25%;" />

     可以明显地看出无论是哪个分区，图像上都有两个峰值，对应的时间段是人们的休息时间，大家显然更多是在休息时间选择用看视频的方式打发时间。

