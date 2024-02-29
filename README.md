## QQMusicDownload ##  
本项目用于个人QQ音乐批量下载歌单的无损格式音乐  
（仅支持研究用途，严禁用于商业用途，请于24小时内删除通过本项目下载的音乐，有意向获取无损音乐请购买实体专辑）  

## 项目原理 ##
- 手机QQ音乐分享歌单或我的收藏链接到微信自己，通过浏览器打开获取歌单网址: https://i.y.qq.com/n2/m/share/details/taoge.html?id={id}&... 获取到歌单id  
- 通过qq音乐接口： get https://c.y.qq.com/v8/fcg-bin/fcg_v8_playlist_cp.fcg?id={id}&format=json 获取response为带歌单信息的json并保存为\cache\playlist.{id}.raw.json
- python解析\cache\playlist.{id}.raw.json为\cache\playlist.{id}.json
- (由于qq音乐接口已经升级，必须绿钻会员才能获取vkey下载完整歌曲, 本项目绕过这一步)  
  vkey获取接口：
  post https://u.y.qq.com/cgi-bin/musics.fcg?sign={sign}  
  body:
  {"comm":{"cv":4747474,"ct":24,"format":"json","inCharset":"utf-8","outCharset":"utf-8","notice":0,"platform":"yqq.json","needNewCode":1,"uin":0,"g_tk_new_20200303":5381,"g_tk":5381},"req_1":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"5556263040","songmid":["0004Fq5m1or8Sq"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}}}  
  songmid字段在上述 \cache\playlist.{id}.json 能查询到  
  具体sign计算方式请跳转至此链接查看：[https://gist.github.com/xyuanmu/9338af7dc3ac2d3a1c4cd067e7d51bc0](https://gist.github.com/xyuanmu/9338af7dc3ac2d3a1c4cd067e7d51bc0)  
  下载歌曲接口：http://dl.stream.qqmusic.qq.com/C400003iMNk90opPDm.m4a?vkey=50E1A39D9250BF152815E439B7C79C40ABF5095BAD722E832FEB9A54C2AE38018B7E2382F42118B295CCF3619DB78A8C715B826EA188F949&uin=0&guid=5556263040&fromtag=120032  
  以此URL为例，C400003iMNk90opPDm.m4a为文件名字，由 对应解析度(4Bytes)+songmid+对应解析度拓展名 构成，M800:320kmp3,M500:128kmp3,F000:flac,vkey为上述response获取。  
- 本项目使用网站：(https://flac.life/)[https://flac.life/]提供的服务获取音乐下载链接，由于网站限制，一次不能发送过多请求，否则可能会报错500或其他直到第二天重新可用。  
  此网站需要从公众号获取解锁码，通过https://api.itooi.cn/unlock/{unlockkey} 验证解锁码是否正确，每天0：00更新  
  通过 https://api.itooi.cn/tencent/search?type=song&format=1&keyword={keyword}&page=0&pageSize=20 搜索需要的歌曲并返回列表，本项目直接取第一条为结果，若不是你想要的音乐可以尝试修改sixyin.py中的搜索关键词。  
  通过 https://api.itooi.cn/tencent/url?id=XpCZeqOaG72UghOt7Qu29ioJbljtGBbx9RQ1o59kuWs=&quality=flac&isRedirect=0 (header: Unlockcode:{unlockkey})下载选中的音乐，id在上述搜索请求的response包含。  

## 使用步骤 ##  
由于时间原因，本项目并未设计图形界面或控制台界面，下载音乐需要修改源码中的一些字段，在代码中注释了具体的参数  
- 运行main.py 歌单信息和存储在 \cache\playlist.{id}.json ，可多次运行增量下载  
- 运行songs_proc.py 校验完整性以及导出歌单列表文件夹 \export  
- （如需要转换flac格式无损音乐至128k/320k MP3）下载ffmpeg runtime至 \ffmpeg，运行flac2mp3.py 直到转换完成  
