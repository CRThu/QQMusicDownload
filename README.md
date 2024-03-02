## QQMusicDownload ##  
本项目用于个人QQ音乐批量下载歌单的无损格式音乐  

⚠: 仅支持研究用途，严禁用于商业用途，请于24小时内删除通过本项目下载的音乐，有意向获取无损音乐请购买实体专辑。

## 项目原理 ##

- 手机QQ音乐分享歌单或我的收藏链接到微信自己，通过浏览器打开获取歌单网址: `https://i.y.qq.com/n2/m/share/details/taoge.html?id={id}&...` 获取到歌单id 
- 通过QQ音乐接口，获取response中带歌单信息的json。
   接口URL：`https://c.y.qq.com/v8/fcg-bin/fcg_v8_playlist_cp.fcg?id={id}&format=json`  
   保存路径：`\cache\playlist.{id}.raw.json`
- Python解析文件为：`\cache\playlist.{id}.raw.json为\cache\playlist.{id}.json`
- (由于qq音乐接口已经升级，必须绿钻会员才能获取vkey下载完整歌曲, 本项目绕过这一步)  
  vkey获取接口：
  `post https://u.y.qq.com/cgi-bin/musics.fcg?sign={sign}`
  body示例:
  ```
  {
     "comm": {
       "cv": 4747474,
       "ct": 24,
       "format": "json",
       "inCharset": "utf-8",
       "outCharset": "utf-8",
       "notice": 0,
       "platform": "yqq.json",
       "needNewCode": 1,
       "uin": 0,
       "g_tk_new_20200303": 5381,
       "g_tk": 5381
     },
     "req_1": {
       "module": "vkey.GetVkeyServer",
       "method": "CgiGetVkey",
       "param": {
         "guid": "5556263040",
         "songmid": ["0004Fq5m1or8Sq"],
         "songtype": [0],
         "uin": "0",
         "loginflag": 1,
         "platform": "20"
       }
     }
   }
  ```

  `songmid`字段在 `\cache\playlist.{id}.json`文件中找到。  
  具体sign计算方式请跳转至此链接查看：[Python版QQ音乐sign加密](https://gist.github.com/xyuanmu/9338af7dc3ac2d3a1c4cd067e7d51bc0)  

  下载歌曲接口：`http://dl.stream.qqmusic.qq.com/C400003iMNk90opPDm.m4a?vkey=50E1A39D9250BF152815E439B7C79C40ABF5095BAD722E832FEB9A54C2AE38018B7E2382F42118B295CCF3619DB78A8C715B826EA188F949&uin=0&guid=5556263040&fromtag=120032`
  
  在此示例中，`C400003iMNk90opPDm.m4a` 是文件名，由对应的解析度前缀（4字节）、`songmid`和对应的文件扩展名组成。例如，`M800`表示320k的MP3格式，`M500`表示128k的MP3格式，`F000`表示FLAC格式。`vkey`通过上述接口的响应获得。

- 本项使用[Flac.life](https://flac.life/)网站提供的服务来获取音乐下载链接。由于网站限制，不能发送过多请求，否则可能会导致500等报错信息，需等到第二天重置。
  
  **获取音乐流程**
    1. 解锁码获取：首先从Flac.life公众号获取解锁码，然后通过 `https://api.itooi.cn/unlock/{unlockkey}` 验证解锁码是否正确。解锁码每天0:00更新。
    2. 搜索歌曲：使用接口 `https://api.itooi.cn/tencent/search?type=song&format=1&keyword={keyword}&page=0&pageSize=20` 来搜索歌曲，并返回列表。默认情况下，项目会使用列表中的第一条结果。如果结果不符合预期，可以在 `sixyin.py` 中修改搜索关键词。
    3. 下载音乐：通过 `https://api.itooi.cn/tencent/url?id={id}&quality=flac&isRedirect=0` （需要在header中包含`Unlockcode:{unlockkey}`）下载选中的音乐。歌曲的`id`可以从搜索接口的响应中获得。
    4. 请根据需要调整请求参数，以符合项目需求。


## 使用步骤 ##  
由于时间原因，本项目并未设计图形界面或控制台界面。用户需直接修改源码中的特定字段来下载音乐，具体参数已在代码注释中说明。

- **下载歌单**：运行 `main.py` 以下载歌单信息，信息将被保存在 `\cache\playlist.{id}.json` 文件中。该脚本支持增量下载，可以多次运行。
- **处理歌曲**：运行 `songs_proc.py` 以校验歌曲完整性并导出歌单到 `\export` 文件夹。
- **格式转换（可选）**：若需将FLAC格式无损音乐转换为128k或320k的MP3格式，首先下载 `ffmpeg runtime` 到 `\ffmpeg` 目录，然后运行 `flac2mp3.py` 直至转换完成。
