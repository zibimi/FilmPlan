# 分类与导演们：重复影片清理及当前剩余清单

更新日期：2026-10-16（America/Los_Angeles）。路径复核完成时间：2026-10-16T12:01:23.210452-07:00。本文件替换初次只读审阅；下列“已执行”均有逐项日志和回读记录，“剩余候选”尚未删除。

## 已完成的清理与归位

原则：先比较文件体积、文件名中的明确质量标记及 MKV 格式，保留较好版本；条件接近时优先保留导演们。较好版本原在分类时，移到被替换影片原来的导演目录，保留较好版本文件名。体积相差不超过 15% 视为接近；质量线索冲突、剪辑不同、身份存疑时暂缓。质量判断依据用户指定的文件线索，并非逐片画面评测。

- 已删除重复或较差视频 **86 个**：分类 **71 个**、导演们 **15 个**。删除文件逻辑大小合计 **185.19 GiB**；实际释放空间受 NAS 回收站及快照影响。
- 已将分类中的较好版本 **15 个、46.78 GiB** 移回对应导演目录。首项做整文件 SHA-256，其余做覆盖全部字节的分块 SHA-256；全数校验一致后才删除分类源文件。
- 已逐项确认：86 个删除路径不存在、保留副本状态正常；15 个归位源路径不存在、目标大小和修改时间符合记录。无覆盖、无媒体删除失败。字幕、附件及目录未作清理；15 个归位源视频旁未发现同名外挂字幕。
- 初次清单另有 12 个分类旧路径，在本轮清理之前就已不存在，未计入这 86 项。

## 当前剩余范围

| 范围 | 候选组数 |
|---|---:|
| 两库之间 | 22 |
| 分类内部 | 62 |
| 导演们内部 | 7 |

当前按扩展名识别到分类 4,226 个、导演们 3,947 个媒体文件。扩展名包含 DAT/VCD 等，不等于电影部数；忽略隐藏目录、回收站和系统索引。目录枚举及候选路径复核错误均为 0。

这些分组按不同文件夹筛选，包含短片、多版本等资源；同一文件夹内的其他版本可能未计入。未做全库逐字节查重，无年份、异译名或光盘流文件仍可能漏检。候选不能直接作为删除清单。

## 剩余两库之间：22 组

### 1. 另一个女人（1988）

暂留原因：体积、格式或质量标记相互冲突。

- `/Volumes/分类/故事/另一个女人.Another.Woman.1988.rmvb` — 0.87 GiB
- `/Volumes/导演们/伍迪·艾伦/另一个女人.Another.Woman.1988.mkv` — 0.30 GiB

### 2. 哥伦布传1492（1992）

暂留原因：体积、格式或质量标记相互冲突。

- `/Volumes/分类/传记·一段历史/哥伦布传.1492.Conquest.of.Paradise.1992.rmvb` — 1.68 GiB
- `/Volumes/导演们/雷德利·斯科特/1492.征服天堂.1492.Conquest.of.Paradise.1992.BD.2Audio.MiniSD-TLF.mkv` — 0.98 GiB

### 3. 夜车（1959）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/惊悚·犯罪·动作/夜车.Night.Train.1959.DVDRip.XviD-MOC.mkv` — 0.36 GiB
- `/Volumes/导演们/耶尔齐·卡瓦莱罗维奇/夜车.Pociag.1959.DVDRip.XviD-MOC.mkv` — 0.68 GiB

### 4. 失衡生活（1983）

暂留原因：归位后分类仍留有另一份视频，本次未额外删除，待按质量规则复核。

- `/Volumes/导演们/高佛雷·雷吉奥/失衡生活.Koyaanisqatsi.1983.HDTV.MiniSD-TLF.mkv` — 0.54 GiB
- `/Volumes/分类/纪录/机械生活.Koyaanisqatsi.1983.DVD-Rip.Divx.720x416.Reggio.&amp.Philip.Glass.mkv` — 0.33 GiB

### 5. 弗朗德勒（2006）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/传记·一段历史/弗朗德勒.Flandres.2006.rmvb` — 0.43 GiB
- `/Volumes/导演们/布鲁诺·杜蒙/弗朗德勒.Flanders.2006.rmvb` — 0.43 GiB

### 6. 怪谈（1964）

暂留原因：剪辑或特殊版本标记，保留待核对。

- `/Volumes/分类/恐怖/怪谈.Kwaidan.未剪切版.1964.DVDrip.HALFCD.NOWYS.双面伊人.mkv` — 0.71 GiB
- `/Volumes/导演们/小林正树/怪谈.Kwaidan.1964.BluRay.CC.2Audio.MiniHD-TLF.mkv` — 2.26 GiB

### 7. 恋人曲（1974）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/喜剧/恋人曲.A.Lovers.Romance.1974.X264.mp4` — 1.37 GiB
- `/Volumes/导演们/安德烈·康查洛夫斯基/恋人曲.Romanca.O.Zakochanych.1974.X264.mp4` — 1.37 GiB

### 8. 恐怖角（1962）

暂留原因：导演归属或文件身份存疑。

- `/Volumes/分类/惊悚·犯罪·动作/恐怖角.Cape.Fear.1962.DVDRip.X264.MiniSD-TLF.mkv` — 0.68 GiB
- `/Volumes/导演们/马丁·斯科塞斯/恐怖角.Cape.Fear.1962.BD.MiniSD-TLF.mkv` — 0.78 GiB

### 9. 末路狂奔（1996）

暂留原因：体积、格式或质量标记相互冲突。

- `/Volumes/分类/惊悚·犯罪·动作/末路狂奔/末路狂奔.Pusher.1996.BD.MiniSD-TLF.mkv` — 0.77 GiB
- `/Volumes/导演们/尼古拉斯·温丁·雷弗恩/末路狂奔.Pusher.1996.720p.BluRay.x264.Chs-Phoenix.mp4` — 1.68 GiB

### 10. 末路狂奔2（2004）

暂留原因：体积、格式或质量标记相互冲突。

- `/Volumes/分类/惊悚·犯罪·动作/末路狂奔/末路狂奔2.Pusher.II.2004.BD.MiniSD-TLF.mkv` — 0.78 GiB
- `/Volumes/导演们/尼古拉斯·温丁·雷弗恩/末路狂奔2.Pusher.II.2004.mp4` — 1.97 GiB

### 11. 末路狂奔3（2005）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/惊悚·犯罪·动作/末路狂奔/末路狂奔3.Pusher.III.2005.BD.MiniSD-TLF.mkv` — 0.86 GiB
- `/Volumes/导演们/尼古拉斯·温丁·雷弗恩/末路狂奔3.Pusher.3.2005.720p.BluRay.x264.Chs-Phoenix.mp4` — 1.59 GiB

### 12. 狗脸的岁月（1985）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/青春·儿童/狗脸的岁月/狗脸的岁月.Mitt.Liv.som.Hund.1985.D9.MiniSD-TLF.mkv` — 0.75 GiB
- `/Volumes/导演们/拉斯·霍尔斯道姆/狗脸的岁月.My.Life.as.a.Dog.1985.CC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 8.58 GiB

### 13. 疾走天堂（2002）

暂留原因：导演归属或文件身份存疑。

- `/Volumes/分类/惊悚·犯罪·动作/疾走天堂.Heaven.2002.BD.MiniSD-TLF.mkv` — 0.85 GiB
- `/Volumes/导演们/克日什托夫·基耶斯洛夫斯基/天堂.Heaven.2002.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 4.48 GiB

### 14. 真情难诉（1924）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/故事/真情难诉.Harold.Llyod.Girl.Shy.1924.mkv` — 0.42 GiB
- `/Volumes/导演们/哈罗德·劳埃德/真情难诉.Girl.Shy.1924.mkv` — 0.54 GiB

### 15. 花（2011）

暂留原因：导演归属或文件身份存疑。

- `/Volumes/分类/华语世界/中国大陆/导演们/娄烨/花.Love.and.Bruises.2011.D9.MiniSD-TLF.mkv` — 1.09 GiB
- `/Volumes/导演们/彼得·格林纳威/花.Love.and.Bruises.2011.french.novembre.multi.720p.bluray.dts.x264-bix.avi` — 0.68 GiB

### 16. 苦恋（1965）

暂留原因：异常小文件。

- `/Volumes/分类/喜剧/苦恋.The.Loved.One.1965.mkv` — 0.00 GiB
- `/Volumes/导演们/托尼·理查德森/苦恋.The.Loved.One.1965.mkv` — 0.47 GiB

### 17. 蓝天使（1930）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/喜剧/蓝天使.Der.blaue.Engel.1930.BD.German.MiniSD-TLF.mkv` — 0.83 GiB
- `/Volumes/导演们/玛琳·黛德丽[演员]/蓝天使.The.Blue.Angel.1930.DVDrip.by.galmuchet.avi` — 0.66 GiB

### 18. 警察形容词（2009）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/惊悚·犯罪·动作/警察·形容词.Police.Adjective.2009.DVD-RMVB-人人影视.rmvb` — 0.51 GiB
- `/Volumes/导演们/柯内流·波蓝波宇/警察.形容词.Politist.Adjectiv.2009.DVDRip.x264-mafalda.mkv` — 1.87 GiB

### 19. 贪吃树（2000）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/动画片/贪吃树.Little.Otik.2000.DVDRip.LYMDG.mkv` — 0.55 GiB
- `/Volumes/导演们/杨·史云梅耶/贪吃树.Otesánek.2000.D5.MiniSD-TLF.mkv` — 0.95 GiB

### 20. 赫鲁斯塔廖夫开车（1998）

暂留原因：体积、格式或质量标记相互冲突。

- `/Volumes/分类/喜剧/赫鲁斯塔廖夫.开车.Khrustalyov.My.Car.1998.avi` — 1.32 GiB
- `/Volumes/导演们/阿列克谢·日尔曼/哈鲁斯坦洛夫.开车！.Khrustalyov.My.Car.1998.苏联.Aleksei.German.mkv` — 0.76 GiB

### 21. 足迹（2007）

暂留原因：导演归属或文件身份存疑。

- `/Volumes/分类/惊悚·犯罪·动作/足迹.Sleuth.2007.BD.2Audio.MiniSD-TLF.mkv` — 0.62 GiB
- `/Volumes/导演们/约瑟夫·L·曼凯维奇/足迹.Sleuth.2007.BD.2Audio.MiniSD-TLF.mkv` — 0.62 GiB

### 22. 野孩子（1970）

暂留原因：外文片名不完全一致，暂缓身份核对。

- `/Volumes/分类/青春·儿童/野孩子.The.Wild.Child.1970.D5.MiniSD-TLF.mkv` — 0.56 GiB
- `/Volumes/导演们/弗朗索瓦·特吕弗/野孩子.L.enfant.sauvage.1970.mp4` — 0.31 GiB

## 剩余分类内部：62 组

### 1. 不夜城（1948）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/黑色电影/不夜城.The.Naked.City.1948.mkv` — 0.44 GiB
- `/Volumes/分类/惊悚·犯罪·动作/不夜城/不夜城.The.Naked.City.1948.D9.MiniSD-TLF.mkv` — 0.68 GiB

### 2. 与我同行（1944）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/故事/与我同行.Going.My.Way.1944.720p.WEB-DL.MiniSD-TLF.mkv` — 0.68 GiB
- `/Volumes/分类/喜剧/与我同行.Going.My.Way.1944.Shout.Factory.BluRay.720p.x264.AC3.iNT-TLF.mkv` — 3.12 GiB

### 3. 关于格伦古尔德的三十二部短片（1993）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/短篇集/关于格伦古尔德的三十二部短片.Thirty.Two.Short.Films.About.Glenn.Gould.1993.mkv` — 0.36 GiB
- `/Volumes/分类/音乐/古尔德的32个短片.Thirty.Two.Short.Films.About.Glenn.Gould.1993.CC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 5.72 GiB

### 4. 冒一切风险的阶级（1960）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/故事/冒一切风险的阶级.The.Big.Risk.1960.avi` — 0.98 GiB
- `/Volumes/分类/惊悚·犯罪·动作/冒一切风险的阶级.Classe.Tous.Risques.1960.D9.MiniSD-TLF.mkv` — 0.77 GiB

### 5. 午后的迷惘（1943）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/CULT·实验/午后的迷惘.Meshes.of.the.Afternoon.1943.720p.BluRay.SILENT.x264-NCmt.mkv` — 0.85 GiB
- `/Volumes/分类/短篇集/午后的迷惘.Meshes.Of.The.Afternoon.1943.D9.MiniSD-TLF.mkv` — 0.10 GiB

### 6. 午宴之歌（2010）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/爱情/午宴之歌.The.Song.of.Lunch.2010.WEB-DL.MiniSD-TLF.mkv` — 0.23 GiB
- `/Volumes/分类/故事/午宴之歌.The.Song.of.Lunch.2010.mkv` — 0.18 GiB

### 7. 听到涛声（1993）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/动画片/听到涛声.Ocean.Waves.1993.BD.2Audio.MiniSD-TLF.mkv` — 0.53 GiB
- `/Volumes/分类/动画片/导演和大厂/吉卜力/听到涛声.Ocean.Waves.1993.BD.1920x1036.HEVC-10bit.OPUS.ASSx2.mkv` — 9.78 GiB

### 8. 告别昨日（1979）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/体育/告别昨日.Breaking.Away.1979.DVD2Rip.x264-AeroHut.mkv` — 0.67 GiB
- `/Volumes/分类/喜剧/突破.Breaking.Away.1979-AeroHut.mkv` — 0.67 GiB

### 9. 夜夜春宵（1944）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/故事/夜夜春宵.A.Canterbury.Tale.1944.DVDRip.XviD-DiMENSiON.mkv` — 0.48 GiB
- `/Volumes/分类/惊悚·犯罪·动作/夜夜春宵.A.Canterbury.Tale.1944.D9.MiniSD-TLF.with-commentary.mkv` — 0.97 GiB

### 10. 夜车（2007）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/导演们/刁亦男/夜车.Night.Train.2007.中国.XTM.DVD-HALFCD.mkv` — 0.31 GiB
- `/Volumes/分类/故事/夜车.Night.Train.2007.中国.XTM.DVD-HALFCD.mkv` — 0.31 GiB

### 11. 大市民（1990）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/喜剧/大市民.Metropolitan.1990.CC.BDRip.X264.iNT-TLF.mkv` — 2.73 GiB
- `/Volumes/分类/青春·儿童/大市民.Metropolitan.1990.mkv` — 0.38 GiB

### 12. 天书奇谭（1983）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/天书奇谭.The.Legend.of.Sealed.Book.1983.UHD.BluRay.2160p.x265.10bit.HDR.DTS.iNT-TLF.mkv` — 6.90 GiB
- `/Volumes/分类/动画片/天书奇谭.The.Legend.of.Sealed.Book.1983.DVD9.x264.AAC.miniSD-TLF.mkv` — 0.50 GiB

### 13. 天云山传奇（1981）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/天云山传奇.Legend.of.Tianyun.Monutain.1981.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 6.34 GiB
- `/Volumes/分类/华语世界/中国大陆/导演们/谢晋/天云山传奇.Legend.of.Tianyun.Monutain.1981.BluRay.1080p.x265.10bit.AC3-TLF.mkv` — 7.84 GiB

### 14. 女巫（1922）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/CULT·实验/女巫.Haexan.1922.D9.MiniSD-TLF.mkv` — 0.79 GiB
- `/Volumes/分类/CULT·实验/女巫.Witchcraft.Through.The.Ages.1922.68年重编版.D5.MiniSD-TLF.mkv` — 0.52 GiB
- `/Volumes/分类/恐怖/女巫.Haxan.1922.CC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 7.64 GiB

### 15. 山水情（1988）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/动画片/动画的世纪·100部作品/山水情.Te.Wei.1988.avi` — 0.19 GiB
- `/Volumes/分类/动画片/动画短片/山水情.Feeling.from.Mountain.and.Water.1988.flv` — 0.04 GiB

### 16. 岁月的童话（1991）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/动画片/导演和大厂/吉卜力/岁月的童话.Only.Yesterday.1991.BD.1920x1036.HEVC-10bit.OPUS.ASSx2.mkv` — 10.09 GiB
- `/Volumes/分类/故事/岁月的童话.Only.Yesterday.1991.DVD.X264.2Audio.AAC.HALFCD-NORM.mkv` — 0.50 GiB
- `/Volumes/分类/青春·儿童/岁月的童话.Only.Yesterday.1991.rmvb` — 0.51 GiB

### 17. 幽灵世界（2001）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/科幻·奇幻/幽灵世界.Ghost.World.2001.rmvb` — 0.54 GiB
- `/Volumes/分类/青春·儿童/幽灵世界.Ghost.World.2001.HDTV.MiniSD-TLF.mkv` — 0.81 GiB

### 18. 弗兰兹卡夫卡（1992）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/动画片/动画的世纪·100部作品/弗兰兹·卡夫卡.Franz.Kafka.Piotr.Dumala.1992.DVDRip.XviD-CiNEMAGROTESQUE.avi` — 0.18 GiB
- `/Volumes/分类/名著改编/卡夫卡电影作品集/弗兰兹·卡夫卡/弗兰兹·卡夫卡.Franz.Kafka.1992.DVDRip.XviD-CiNEMAGROTESQUE.avi` — 0.18 GiB

### 19. 情迷六月花（1990）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/传记·一段历史/情迷六月花.Henry.&.June.1990.D9.MiniSD-TLF.mkv` — 0.88 GiB
- `/Volumes/分类/情色/情迷六月花.Henry.&.June.1990.BD.MiniSD-TLF.mkv` — 1.90 GiB

### 20. 抢劫装甲车（1951）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/喜剧/抢劫装甲车.The.Lavender.Hill.Mob.1951.BD.MiniSD-TLF.mkv` — 0.60 GiB
- `/Volumes/分类/惊悚·犯罪·动作/拉凡德山的暴徒.The.Lavender.Hill.Mob.1951.DVDRip.X264.AAC.HALFCD-NORM.Christian.mkv` — 0.29 GiB

### 21. 攻壳机动队2无罪（2004）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/动画片/攻壳机动队2.无罪.Ghost.in.the.Shell.2.Innocence.2004.x264.10bit.1920x1036.FLAC.6.1.mkv` — 5.27 GiB
- `/Volumes/分类/动画片/攻壳机动队/攻壳机动队2-无罪.Ghost.In.The.Shell.2.Innocence.2004.BD.MiniSD-TLF.mkv` — 0.63 GiB

### 22. 无名（2023）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/无名.Hidden.Blade.2023.BD.MiniSD-TLF.mkv` — 0.66 GiB
- `/Volumes/分类/华语世界/中国大陆/导演们/程耳/无名.Hidden.Blade.2023.KOR.BluRay.1080p.HEVC.10bit.MiniFHD.mkv` — 8.06 GiB

### 23. 日烦夜烦（2001）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/恐怖/日烦夜烦.Trouble.Every.Day.2001.avi` — 0.68 GiB
- `/Volumes/分类/音乐/日烦夜烦.Trouble.Every.Day.2001.avi` — 0.68 GiB

### 24. 最后的舞者（2009）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/传记·一段历史/最后的舞者.Mao.s.Last.Dancer.2009.rmvb` — 0.48 GiB
- `/Volumes/分类/故事/最后的舞者.Maos.Last.Dancer.2009.BD.MiniSD-TLF.mkv` — 0.92 GiB

### 25. 月亮上的男人（1999）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/传记·一段历史/月亮上的男人.Man.On.The.Moon.1999.BD.MiniSD-TLF.mkv` — 0.88 GiB
- `/Volumes/分类/CULT·实验/月亮上的男人.Man.On.The.Moon.1999.DVDRip.XviD.AC3.mkv` — 0.44 GiB
- `/Volumes/分类/喜剧/月亮上的男人.Man.On.The.Moon.1999.BD.2Audio.MiniSD-TLF.mkv` — 0.93 GiB

### 26. 朱莉亚（1977）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/传记·一段历史/朱莉亚.Julia.1977.DVDRip.XviD-LOOK.mkv` — 0.53 GiB
- `/Volumes/分类/故事/朱莉亚.Julia.1977.BluRay.720p.x264.AC3.iNT-TLF.mkv` — 2.34 GiB

### 27. 杂耍班（1925）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/故事/杂耍班.Dupont.Variete.1925.mkv` — 0.30 GiB
- `/Volumes/分类/喜剧/杂耍班.Variete.1925.BD.German.MiniSD-TLF.mkv` — 0.81 GiB

### 28. 枪疯（1950）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/黑色电影/枪疯.Gun.Crazy.AKA.Deadly.Is.the.Female.1950.D5.2Audio.MiniSD-TLF.mkv` — 0.64 GiB
- `/Volumes/分类/黑色电影/枪疯.Gun.Crazy.1950.mkv` — 0.82 GiB
- `/Volumes/分类/惊悚·犯罪·动作/枪疯.Gun.Crazy.AKA.Deadly.Is.the.Female.1950.BD.2Audio.MiniSD-TLF.mkv` — 0.73 GiB

### 29. 桃色交易（1993）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/爱情/桃色交易.Indecent.Proposal.1993.REMASTERED.1080p.BluRay.x265.10bit.DTS.MultiAudio-TLF.mkv` — 10.00 GiB
- `/Volumes/分类/歌舞/桃色交易.Indecent.Proposal.1993.REMASTERED.1080p.BluRay.x265.10bit.DTS.MultiAudio-TLF.mkv` — 10.00 GiB

### 30. 棋王（1991）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/香港/导演们/徐克/棋王.King.of.Chess.1991.1080p.WEBRip.CHS-HAN@CHAOSPACE.mp4` — 2.51 GiB
- `/Volumes/分类/惊悚·犯罪·动作/棋王.King.Of.Chess.1991.DVD.X264.2Audio.AAC.HALFCD-NORM.mkv` — 0.42 GiB

### 31. 死吻（1955）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/黑色电影/死吻.Kiss.Me.Deadly.1955.DVDRip.by.Galmuchet.avi` — 0.98 GiB
- `/Volumes/分类/惊悚·犯罪·动作/死吻.Kiss.Me.Deadly.1955.BD.CC.MiniSD-TLF.mkv` — 0.84 GiB

### 32. 深夜止步（1975）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/恐怖/深夜止步.Deep.Red.1975.英语音轨.mp4` — 0.06 GiB
- `/Volumes/分类/惊悚·犯罪·动作/深夜止步.Deep.Red.1975.DC.BDRip.480p.AC3.2Audio.x264-CHD.mkv` — 2.05 GiB

### 33. 火之谜（2023）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/故事/火之谜.Riddle.of.Fire.2023.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 7.64 GiB
- `/Volumes/分类/青春·儿童/火之谜.Riddle.of.Fire.2023.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 7.64 GiB

### 34. 爸妈不在家（2013）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/东南亚/陈哲艺/爸妈不在家.Ilo.Ilo.2013.BDRip.X264.iNT-TLF.mkv` — 2.73 GiB
- `/Volumes/分类/故事/爸妈不在家.Ilo.Ilo.2013.rmvb` — 1.05 GiB

### 35. 牧马人（1982）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/牧马人.The.Herdsman.1982.BluRay.1080p.x265.10bit.AC3-TLF.mkv` — 7.24 GiB
- `/Volumes/分类/华语世界/中国大陆/导演们/谢晋/牧马人.The.Herdsman.1982.1080p.BluRay.x265.10bit.LPCM2.0-ParkHD.mkv` — 14.98 GiB

### 36. 狐狸与我（2007）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/故事/狐狸与我.The.Fox.And.The.Child.2007.BD.2Audio.MiniSD-TLF.mkv` — 0.64 GiB
- `/Volumes/分类/青春·儿童/狐狸与孩子.The.Fox.and.the.Child.2007.rmvb` — 0.45 GiB

### 37. 电影往事（2004）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/电影往事.Electric.Shadows.2004.D5.MiniSD-TLF.mkv` — 0.74 GiB
- `/Volumes/分类/华语世界/欧美华人/梦影童年.Electric.Shadows.2004.D5.HALFCD-TLF.mkv` — 0.00 GiB

### 38. 畸型人（1932）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/CULT·实验/畸型人.Freaks.1932.D9.MiniSD-TLF.mkv` — 0.45 GiB
- `/Volumes/分类/黑色电影/畸形人.Freaks.1932.Freaks.1932.avi` — 0.71 GiB

### 39. 登楼叹（2021）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/欧美华人/登楼叹.Ascension.2021.mp4` — 1.96 GiB
- `/Volumes/分类/华语世界/禁/登楼叹.Ascension.2021.mp4` — 1.96 GiB

### 40. 砂之女（1964）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/CULT·实验/砂之女.Woman.In.The.Dunes.D.C.1964.D9.MiniSD-TLF.mkv` — 0.94 GiB
- `/Volumes/分类/惊悚·犯罪·动作/砂之女.Woman.In.The.Dunes.1964.BluRay.1080p.LPCM1.0.x265.10bit-DreamHD.mkv` — 9.08 GiB

### 41. 稀有出口圣诞传说（2010）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/科幻·奇幻/稀有出口.圣诞传说.Rare.Exports.A.Christmas.Tale.2010.双语字幕.HR-HDTV.AC3.1024X576.x264-人人影视制作.mkv` — 1.26 GiB
- `/Volumes/分类/喜剧/稀有出口.圣诞传说.Rare.Exports.A.Christmas.Tale.2010.法国.DVD-HALFCD2.mp4` — 0.27 GiB

### 42. 突变第三型（1982）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/科幻·奇幻/突变第三型.The.Thing.1982.BDRip.MiniSD-TLF.mkv` — 0.72 GiB
- `/Volumes/分类/怪兽/怪形.The.Thing.1982.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 7.27 GiB

### 43. 第三个人（1949）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/黑色电影/第三个人.The.Third.Man.1949.mkv` — 0.64 GiB
- `/Volumes/分类/惊悚·犯罪·动作/第三人.The.Third.Man.1949.双语字幕.HR-HDTV.AC3.768X576.x264-人人影视制作.mkv` — 1.61 GiB

### 44. 罗小黑战记2（2025）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/罗小黑战记2.The.Legend.of.Hei.2.2025.BluRay.1080p.x265.10bit.EAC3.iNT-TLF.mkv` — 2.56 GiB
- `/Volumes/分类/动画片/罗小黑战记2.The.Legend.of.Hei.Ⅱ.2025.1080p.WEB-DL.H264.AAC-OurTV.mp4` — 5.92 GiB

### 45. 老井（1986）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/20世纪老电影/80/老井.Old.Well.1986.Bluray.1080p.LPCM1.0.x265.10bit-DreamHD.mkv` — 11.82 GiB
- `/Volumes/分类/华语世界/中国大陆/导演们/吴天明/老井.Old.Well.1986.WEB-DL.MiniHD-TLF.mkv` — 2.38 GiB

### 46. 肉体的恶魔（1986）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/CULT·实验/肉体的恶魔.Devil.In.The.Flesh.1986.DVDRip.XviD.mp4` — 0.45 GiB
- `/Volumes/分类/爱情/肉体的恶魔.Devil.in.the.Flesh.1986.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 9.13 GiB

### 47. 芙蓉镇（1986）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/导演们/谢晋/芙蓉镇.Hibiscus.Town.1986.BDRip.X264.iNT-TLF.mkv` — 2.99 GiB
- `/Volumes/分类/华语世界/中国大陆/导演们/谢晋/芙蓉镇/芙蓉镇‎.Hibiscus.Town.1986.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 13.98 GiB

### 48. 苏菲的抉择（1982）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/爱情/苏菲的抉择.Sophies.Choice.1982.BluRay.1080p.x265.10bit.DTS-TLF.mkv` — 12.08 GiB
- `/Volumes/分类/爱情/苏菲的抉择.Sophie's.Choice.1982.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 9.49 GiB
- `/Volumes/分类/故事/苏菲的抉择.Sophie's.Choice.1982.US.DVD.X264.2Audio.AAC.HALFCD-NOWYS.mmla.mkv` — 0.61 GiB

### 49. 蓝色构图（1935）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/动画片/蓝色构图.Komposition.in.blau.Oskar.Fischinger,.1935.avi` — 0.04 GiB
- `/Volumes/分类/动画片/动画的世纪·100部作品/Komposition.in.blau.Oskar.Fischinger.1935.avi` — 0.04 GiB

### 50. 蝴蝶（2002）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/喜剧/蝴蝶.The.Butterfly.2002.flv` — 0.01 GiB
- `/Volumes/分类/青春·儿童/蝴蝶.Le.Papilion.2002.D9.2Audio.MiniSD-TLF.mkv` — 0.54 GiB

### 51. 血与黑蕾丝（1964）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/黑色电影/血与黑蕾丝.Blood.And.Black.Lace.1964.D9.MiniSD-TLF.mkv` — 0.75 GiB
- `/Volumes/分类/惊悚·犯罪·动作/血与黑蕾丝.blood.and.black.lace.1964.d9.minisd-tlf.mkv` — 0.75 GiB

### 52. 血光鬼影夺命刀（1973）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/恐怖/血光鬼影夺命刀.Dont.Look.Now.1973.BD.MiniSD-TLF.mkv` — 0.81 GiB
- `/Volumes/分类/惊悚·犯罪·动作/威尼斯疑魂.Don't.Look.Now.1973.CC.BD.MiniSD-TLF.mkv` — 1.21 GiB

### 53. 进出口（2007）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/CULT·实验/进出口.Import.Export.2007.BD.MiniSD-TLF.mkv` — 1.05 GiB
- `/Volumes/分类/情色/进出口.Import.Export.2007.BluRay.720p.x264.AC3.iNT-TLF.mkv` — 3.32 GiB

### 54. 逍遥法外（2002）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/传记·一段历史/逍遥法外.Catch.Me.If.You.Can.2002.DVDRip.2Audio.HALFCD-NOWYS.netshow.mkv` — 0.55 GiB
- `/Volumes/分类/惊悚·犯罪·动作/逍遥法外.Catch.Me.If.You.Can.2002.DVD-RMVB.mkv` — 0.59 GiB

### 55. 遗情（2009）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/东南亚/遗情.woman.on.fire.looks.for.water.2009.woo.ming.jin.dvdrip.x264.ac3.2ch.allzine.mkv` — 1.09 GiB
- `/Volumes/分类/爱情/遗情.woman.on.fire.looks.for.water.2009.woo.ming.jin.dvdrip.x264.ac3.2ch.allzine.mkv` — 1.09 GiB

### 56. 邮差总按两次铃（1946）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/黑色电影/邮差总按两次铃.The.Postman.Always.Rings.Twice.1946.mkv` — 1.36 GiB
- `/Volumes/分类/惊悚·犯罪·动作/邮差总按两次铃.The.Postman.Always.Rings.Twice.1946.BD.MiniSD-TLF.mkv` — 0.84 GiB

### 57. 野花（2000）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/CULT·实验/野花.Kytice.2000.DVDRip.DivX.CZ-BiOGRa.mp4` — 0.31 GiB
- `/Volumes/分类/短篇集/野花.wild.flowers.2000.d5.minisd-tlf.mkv` — 0.72 GiB

### 58. 野蛮人入侵（2021）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/东南亚/野蛮人入侵.Barbarian.Invasion.2021.1080p.NF.WEB-DL.DDP5.1.x264.mkv` — 6.31 GiB
- `/Volumes/分类/喜剧/野蛮人入侵.Barbarian.Invasion.2021.mkv` — 0.34 GiB

### 59. 铁血战士杀戮之地（2025）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/科幻·奇幻/铁血战士.杀戮之地.Predator.Badlands.2025.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 3.07 GiB
- `/Volumes/分类/合集/铁血战士/铁血战士.杀戮之地.Predator.Badlands.2025.WEB-DL.MiniSD-TLF.mkv` — 0.53 GiB

### 60. 雄狮少年2（2024）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/雄狮少年2.I.Am.What.I.Am.2.2024.mp4` — 4.06 GiB
- `/Volumes/分类/动画片/雄狮少年2.I.Am.What.I.Am.2.2024.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 4.14 GiB

### 61. 香魂女（1993）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/华语世界/中国大陆/20世纪老电影/90/香魂女.Woman.Sesame.Oil.Maker.1993.rmvb` — 0.32 GiB
- `/Volumes/分类/故事/香魂女.Women.from.the.Lake.of.Scented.Souls.1993.rmvb` — 0.32 GiB

### 62. 高中课堂（2008）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/分类/故事/高中课堂.Entre.Les.Murs.2008.FRENCH.DVDRip.XviD-ZANBiC.mkv` — 0.48 GiB
- `/Volumes/分类/青春·儿童/墙壁之间.Entre.les.murs.2008.720p.BluRay.x264-CtrlHD.mkv` — 4.37 GiB

## 剩余导演们内部：7 组

### 1. 你知道你的楼梯很漂亮（1986）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/导演们/阿涅斯·瓦尔达/你知道.你的楼梯很漂亮.T.as.de.beaux.escaliers.tu.sais.1986.mkv` — 0.02 GiB
- `/Volumes/导演们/伊莎贝尔·阿佳妮作品集[演员]/你知道.你的楼梯很漂亮.T.as.de.beaux.escaliers.tu.sais.1986.mkv` — 0.01 GiB

### 2. 卢瓦河谷的木鞋匠（1956）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/导演们/阿涅斯·瓦尔达/南特的雅克德米/卢瓦河谷的木鞋匠.Le.Sabotier.du.Val.de.Loire.1956.D9.MiniSD-TLF.mkv` — 0.21 GiB
- `/Volumes/导演们/雅克·德米/卢瓦河谷的木鞋匠.Le.sabotier.du.Val.de.Loire.1956.mkv` — 0.09 GiB

### 3. 奥菲斯（1950）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/导演们/让·谷克多/奥菲斯/奥菲斯.Orphée.1950.D9.MiniSD-TLF.mkv` — 0.74 GiB
- `/Volumes/导演们/让·谷克多/奥菲斯的遗嘱/俄耳甫斯.Orphée.1950.BD.CC.MiniSD-TLF.mkv` — 0.84 GiB

### 4. 寻找小津（1985）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/导演们/小津安二郎/寻找小津.Tokyo-Ga.1985.mkv` — 0.36 GiB
- `/Volumes/导演们/维姆·文德斯/寻找小津.Tokyo.Ga.1985.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 8.94 GiB

### 5. 玩火（1975）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/导演们/阿兰·罗布-格里耶/玩火.Le.Jeu.avec.le.feu.1975.mkv` — 1.45 GiB
- `/Volumes/导演们/阿兰·罗布-格里耶/玩火/玩火.Le.Jeu.avec.le.feu.1975.D9.EngSub.MiniSD-TLF.mkv` — 1.68 GiB

### 6. 长夜漫漫路迢迢（1962）

片名、外文名、年份一致；尚未执行库内清理。

- `/Volumes/导演们/奥逊·威尔斯/长夜漫漫路迢迢.Long.Days.Journey.Into.Night.1962.BD.MiniSD-TLF.mkv` — 1.29 GiB
- `/Volumes/导演们/西德尼·吕美特/长夜漫漫路迢迢.Long.Days.Journey.into.Night.1962.mkv` — 0.66 GiB

### 7. 麦当劳桥上的未婚妻（1961）

片名或外文名及年份一致，待核对译名；尚未执行库内清理。

- `/Volumes/导演们/阿涅斯·瓦尔达/麦当劳桥上的未婚妻.Les.fiances.du.pont.Mac.Donald.1961.mkv` — 0.02 GiB
- `/Volumes/导演们/阿涅斯·瓦尔达/小心太阳眼镜/小心太阳眼镜.Les.fiances.du.pont.Mac.Donald.1961.mkv` — 0.03 GiB

## 15 个较好版本的归位记录

### 1. 乱世忠魂

- 移出：`/Volumes/分类/战争/乱世忠魂.From.Here.to.Eternity.1953.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/弗雷德·金尼曼/乱世忠魂.From.Here.to.Eternity.1953.BD.MiniSD-TLF.mkv` — 1.44 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 2. 乱世英豪

- 移出：`/Volumes/分类/故事/乱世英豪.Marketa.Lazarova.1967.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/法兰提塞·维拉席/乱世英豪.Marketa.Lazarova.1967.BD.MiniSD-TLF.mkv` — 1.22 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 3. 亚历山大涅夫斯基

- 移出：`/Volumes/分类/战争/亚历山大.涅夫斯基.Alexander.Nevsky.1938.mkv`
- 当前保留：`/Volumes/导演们/谢尔盖·爱森斯坦/亚历山大.涅夫斯基.Alexander.Nevsky.1938.mkv` — 1.43 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 4. 勾魂摄魄

- 移出：`/Volumes/分类/短篇集/勾魂摄魄.Spirits.of.the.Dead.1968.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 当前保留：`/Volumes/导演们/路易·马勒/勾魂摄魄.Spirits.of.the.Dead.1968.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 11.56 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 5. 唐祖凡尼

- 移出：`/Volumes/分类/音乐/唐祖凡尼.Don.Giovanni.1979.FRE.BD.EngSub.10bit.AC3.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/约瑟夫·罗西/唐祖凡尼.Don.Giovanni.1979.FRE.BD.EngSub.10bit.AC3.MiniSD-TLF.mkv` — 2.49 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 6. 大都会传奇

- 移出：`/Volumes/分类/短篇集/大都会传奇.New.York.Stories.1989.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/伍迪·艾伦/大都会传奇.New.York.Stories.1989.BD.MiniSD-TLF.mkv` — 0.92 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 7. 失衡生活

- 移出：`/Volumes/分类/纪录/失衡生活.Koyaanisqatsi.1983.HDTV.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/高佛雷·雷吉奥/失衡生活.Koyaanisqatsi.1983.HDTV.MiniSD-TLF.mkv` — 0.54 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 8. 尼斯印象

- 移出：`/Volumes/分类/短篇集/尼斯印象.A.propos.de.Nice.1930.BD.CC.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/让·维果/尼斯印象.A.propos.de.Nice.1930.BD.CC.MiniSD-TLF.mkv` — 0.33 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 9. 我嫁了个怪人

- 移出：`/Volumes/分类/动画片/我嫁了个怪人.I.Married.A.Strange.Person.1997.D5.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/比尔·普莱姆顿 & 罗伯特·克鲁伯/我嫁了个怪人.I.Married.A.Strange.Person.1997.D5.MiniSD-TLF.mkv` — 0.62 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 10. 斯托斯特姆桥

- 移出：`/Volumes/分类/短篇集/斯托斯特姆桥.Storstrømsbroen.1950.ChEn-Douban.mkv`
- 当前保留：`/Volumes/导演们/卡尔·西奥多·德莱叶/短片/斯托斯特姆桥.Storstrømsbroen.1950.ChEn-Douban.mkv` — 0.09 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 11. 有机体的秘密

- 移出：`/Volumes/分类/CULT·实验/有机体的秘密.WR.Mysteries.of.the.Organism.1971.mkv`
- 当前保留：`/Volumes/导演们/杜尚·马卡维耶夫/有机体的秘密.WR.Mysteries.of.the.Organism.1971.mkv` — 1.16 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 12. 杀人游戏

- 移出：`/Volumes/分类/CULT·实验/杀人游戏.Branded.to.Kill.1967.BD.CC.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/铃木清顺/杀人游戏.Branded.to.Kill.1967.BD.CC.MiniSD-TLF.mkv` — 0.53 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 13. 梦旅人

- 移出：`/Volumes/分类/青春·儿童/梦旅人.Picnic.1996.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/岩井俊二/梦旅人.Picnic.1996.BD.MiniSD-TLF.mkv` — 0.60 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 14. 正午

- 移出：`/Volumes/分类/西部/正午.High.Noon.1952.2160p.UHD.BluRay.x265.10bit.DV.DTS-HD.MA.2.0-SONYHD.mkv`
- 当前保留：`/Volumes/导演们/弗雷德·金尼曼/正午.High.Noon.1952.2160p.UHD.BluRay.x265.10bit.DV.DTS-HD.MA.2.0-SONYHD.mkv` — 18.83 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

### 15. 诚如神之所说

- 移出：`/Volumes/分类/动漫改真/诚如神之所说.As.the.Gods.Will.2014.BD1080P.X264.AAC.Japanese.CHS.Mp4Ba.mp4`
- 当前保留：`/Volumes/导演们/三池崇史/诚如神之所说.As.the.Gods.Will.2014.BD1080P.X264.AAC.Japanese.CHS.Mp4Ba.mp4` — 5.02 GiB
- 状态：归位完成、完整覆盖 SHA-256 校验一致。

## 86 项删除记录及最终保留位置

### quality-001 乱世忠魂（1953）

- 已删除：`/Volumes/导演们/弗雷德·金尼曼/乱世忠魂.From.Here.to.Eternity.1953.mkv`
- 当前保留：`/Volumes/导演们/弗雷德·金尼曼/乱世忠魂.From.Here.to.Eternity.1953.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-002 乱世英豪（1967）

- 已删除：`/Volumes/导演们/法兰提塞·维拉席/乱世英豪.Marketa.Lazarova.1967.DVDRip.XviD-MESS.mkv`
- 当前保留：`/Volumes/导演们/法兰提塞·维拉席/乱世英豪.Marketa.Lazarova.1967.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-003 亚历山大涅夫斯基（1938）

- 已删除：`/Volumes/导演们/谢尔盖·爱森斯坦/亚历山大.涅夫斯基.Alexander.Nevsky.1938.avi`
- 当前保留：`/Volumes/导演们/谢尔盖·爱森斯坦/亚历山大.涅夫斯基.Alexander.Nevsky.1938.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-004 亡命驾驶（2011）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/亡命驾驶.Drive.2011.V2.Bluray.2160p.DTS-HDMA5.1.DoVi.HDR.x265.10bit-DreamHD.mkv`
- 当前保留：`/Volumes/导演们/尼古拉斯·温丁·雷弗恩/亡命驾驶.Drive.2011.V2.Bluray.2160p.DTS-HDMA5.1.DoVi.HDR.x265.10bit-DreamHD.mkv`
- 依据：同等质量优先导演们。

### quality-005 人情纸风船（1937）

- 已删除：`/Volumes/分类/故事/人情纸风船.Humanity.and.Paper.Balloons.1937.D5.HalfCD-TLF.mkv`
- 当前保留：`/Volumes/导演们/山中贞雄/人情纸风船.Humanity.And.Paper.Balloons.1937.WEB-DL.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-006 人类之子（2006）

- 已删除：`/Volumes/分类/科幻·奇幻/人类之子.Children.of.Men.2006.HDRip.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/阿方索·卡隆/人类之子.Children.Of.Men.2006.BD.2Audio.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-007 传信人（1970）

- 已删除：`/Volumes/分类/爱情/传信人.The.Go-Between.1970.avi`
- 当前保留：`/Volumes/导演们/约瑟夫·罗西/幽情密使/幽情密使.The.Go.Between.1970.HDRip.push.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-008 传染病（2011）

- 已删除：`/Volumes/分类/科幻·奇幻/传染病.Contagion.2011.rmvb`
- 当前保留：`/Volumes/导演们/史蒂文·索德伯格/传染病.Contagion.2011.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-009 伸冤记（1956）

- 已删除：`/Volumes/分类/黑色电影/伸冤记.The.Wrong.Man.1956.WS.DVDRip.XviD-FRAGMENT.mkv`
- 当前保留：`/Volumes/导演们/阿尔弗雷德·希区柯克/伸冤记.The.Wrong.Man.1956.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-010 公路之王（1976）

- 已删除：`/Volumes/分类/公路/公路之王.Kings.of.the.Road.1976.BD.CC.MiniHD-TLF.mkv`
- 当前保留：`/Volumes/导演们/维姆·文德斯/公路之王.Kings.of.the.Road.1976.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-011 再不相见（1959）

- 已删除：`/Volumes/分类/短篇集/再不相见.Segodnya.Uvolneniya.Ne.Budet.1959.DVDRip.XviD.DivXForever.rmvb`
- 当前保留：`/Volumes/导演们/安德烈·塔尔科夫斯基/今天不离去.Segodnya.Uvolneniya.Ne.Budet.1959.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-012 勾魂摄魄（1968）

- 已删除：`/Volumes/导演们/路易·马勒/勾魂慑魄.Spirits.of.the.Dead.1968.rmvb`
- 当前保留：`/Volumes/导演们/路易·马勒/勾魂摄魄.Spirits.of.the.Dead.1968.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-013 卑微的人生（1997）

- 已删除：`/Volumes/分类/纪录/卑微的人生.A.Humble.Life.1997.mkv`
- 当前保留：`/Volumes/导演们/亚历山大·索科洛夫/卑微的人生.A.Humble.Life.1997.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-014 卡夫卡传（1991）

- 已删除：`/Volumes/分类/传记·一段历史/卡夫卡传.Kafka.1991.DVDRip.DivX-QiX.mkv`
- 当前保留：`/Volumes/导演们/史蒂文·索德伯格/卡夫卡.Kafka.1991.D5.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-015 变局（2012）

- 已删除：`/Volumes/分类/政法委/变局.Game.Change.2012.HDTV.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/杰伊·罗奇/变局.Game.Change.2012.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-016 启示录（2006）

- 已删除：`/Volumes/分类/传记·一段历史/启示录.Apocalypto.2006.BDRip.2Audio.miniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/梅尔·吉布森/启示.Apocalypto.2006.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-017 唐祖凡尼（1979）

- 已删除：`/Volumes/导演们/约瑟夫·罗西/唐璜.Don.Giovanni.1979.iTALiAN.BDRip.XviD-TRL.mkv`
- 当前保留：`/Volumes/导演们/约瑟夫·罗西/唐祖凡尼.Don.Giovanni.1979.FRE.BD.EngSub.10bit.AC3.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-018 喝彩（2015）

- 已删除：`/Volumes/分类/传记·一段历史/喝彩.Aferim.2015.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/拉杜·裘德/喝彩.Aferim.2015.BD.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-019 基督最后的诱惑（1988）

- 已删除：`/Volumes/分类/科幻·奇幻/基督最后的诱惑.The.Last.Temptation.of.Christ.1988.BD.CC.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/马丁·斯科塞斯/基督最后的诱惑.The.Last.Temptation.of.Christ.1988.BD.CC.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-020 大卫戈尔的一生（2003）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/大卫·戈尔的一生.The.Life.of.David.Gale.2003.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/艾伦·帕克/大卫·戈尔的一生.The.Life.of.David.Gale.2003.BD.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-021 大地儿女（1965）

- 已删除：`/Volumes/分类/华语世界/香港/导演们/胡金铨/大地儿女.Sons.of.Good.Earth.1965.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 当前保留：`/Volumes/导演们/胡金铨/大地儿女.Sons.of.Good.Earth.1965.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-022 大都会传奇（1989）

- 已删除：`/Volumes/导演们/伍迪·艾伦/纽约故事.New.York.Stories.1989.D5.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/伍迪·艾伦/大都会传奇.New.York.Stories.1989.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-023 天堂之日（1978）

- 已删除：`/Volumes/分类/故事/天堂之日.Days.of.Heaven.1978.mkv`
- 当前保留：`/Volumes/导演们/泰伦斯·马力克/天堂之日.Days.of.Heaven.1978.双语字幕.HR-HDTV.AC3.1024X576.x264-人人影视制作.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-024 失衡生活（1983）

- 已删除：`/Volumes/导演们/高佛雷·雷吉奥/机械世界.Koyaanisqatsi.1983.DVD-Rip.Divx.720x416.(Reggio.&amp.Philip.Glass).mkv`
- 当前保留：`/Volumes/导演们/高佛雷·雷吉奥/失衡生活.Koyaanisqatsi.1983.HDTV.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-025 好人寥寥（1992）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/好人寥寥.A.Few.Good.Men.1992.BD.MiniHD-TLF.mkv`
- 当前保留：`/Volumes/导演们/罗伯·莱纳/好人寥寥.A.Few.Good.Men.1992.BD.MiniHD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-026 妈咪（2014）

- 已删除：`/Volumes/分类/故事/妈咪.Mommy.2014.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/泽维尔·多兰/妈咪.Mommy.2014.BluRay.1080p.x265.10bit.DDP5.1-MiniHD.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-027 孤星血泪（1946）

- 已删除：`/Volumes/分类/爱情/孤星血泪.Great.Expectations.1946.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/大卫·里恩/孤星血泪.Great.Expectations.1946.BDRip.x.mkv`
- 依据：同等质量优先导演们。

### quality-028 安赫利卡奇事（2010）

- 已删除：`/Volumes/分类/故事/安赫利卡奇事.The.Strange.Case.of.Angelica.2010.rmvb`
- 当前保留：`/Volumes/导演们/曼努埃尔·德·奥利维拉/安吉里卡奇遇.The.Strange.Case.of.Angelica.2010.BDRip.X264.iNT-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-029 尼斯印象（1930）

- 已删除：`/Volumes/导演们/让·维果/尼斯的景象.A.Propos.De.Nice.1930.A.Propos.De.Nice.avi`
- 当前保留：`/Volumes/导演们/让·维果/尼斯印象.A.propos.de.Nice.1930.BD.CC.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-030 局内人（2006）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/局内人.Inside.Man.2006.rmvb`
- 当前保留：`/Volumes/导演们/斯派克·李/局内人.Inside.Man.2006.BD-R.1.40G.中英双字.迅雷.BT.rmvb`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-031 年少轻狂（1993）

- 已删除：`/Volumes/分类/青春·儿童/年少轻狂.Dazed.and.Confused.1993.rmvb`
- 当前保留：`/Volumes/导演们/理查德·林克莱特/年少轻狂.Dazed.and.Confused.1993.CC.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-032 当哈利遇到莎莉（1989）

- 已删除：`/Volumes/分类/爱情/当哈利遇到莎莉.When.Harry.Met.Sally.1989.2160p.UHD.BluRay.x265.10bit.DV.DTS-HD.MA.5.1.2Audio-SONYHD.mkv`
- 当前保留：`/Volumes/导演们/罗伯·莱纳/当哈利遇到莎莉.When.Harry.Met.Sally.1989.2160p.UHD.BluRay.x265.10bit.DV.DTS-HD.MA.5.1.2Audio-SONYHD.mkv`
- 依据：同等质量优先导演们。

### quality-033 彗星美人（1950）

- 已删除：`/Volumes/分类/传记·一段历史/彗星美人.All.About.Eve.1950.D9.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/约瑟夫·L·曼凯维奇/彗星美人.All.About.Eve.1950.D9.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-034 忠烈图（1974）

- 已删除：`/Volumes/分类/华语世界/香港/导演们/胡金铨/忠烈图.The.Valiant.Ones.1974.UHD.BluRay.2160p.x265.10bit.HDR.FLAC.iNT-TLF.mkv`
- 当前保留：`/Volumes/导演们/胡金铨/忠烈图.The.Valiant.Ones.1974.UHD.BluRay.2160p.x265.10bit.HDR.FLAC.iNT-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-035 忠犬八公的故事（2009）

- 已删除：`/Volumes/分类/故事/忠犬八公的故事.Hachiko.A.Dog's.Story.2009.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/拉斯·霍尔斯道姆/忠犬八公的故事.Hachiko.A.Dog's.Story.2009.BD.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-036 怒火风暴（1993）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/怒火风暴.Falling.Down.1993.BD.HALFCD-TLF.mkv`
- 当前保留：`/Volumes/导演们/乔·舒马赫/城市英雄.Falling.Down.1993.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-037 我嫁了个怪人（1997）

- 已删除：`/Volumes/导演们/比尔·普莱姆顿 & 罗伯特·克鲁伯/我嫁了个怪蜀黍.I.Married.a.Strange.Person.1997.DVDrip.by.Galmuchet.mkv`
- 当前保留：`/Volumes/导演们/比尔·普莱姆顿 & 罗伯特·克鲁伯/我嫁了个怪人.I.Married.A.Strange.Person.1997.D5.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-038 我的朋友伊万拉布辛（1984）

- 已删除：`/Volumes/分类/故事/我的朋友伊万.拉布辛.My.Friend.Ivan.Lapshin.1984.avi`
- 当前保留：`/Volumes/导演们/阿列克谢·日尔曼/我的朋友伊万·拉布辛.My.Friend.Ivan.Lapshin.1984.苏联.Aleksei.German.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-039 战争（2025）

- 已删除：`/Volumes/分类/战争/战·争.Warfare.2025.2160p.WEB-DL.DDP5.1.Atmos.H265-華堅馮力士原创中字.mkv`
- 当前保留：`/Volumes/导演们/亚历克斯·加兰/战争.Warfare.2025.USA.BluRay.Remux.UHD.DoVi.HDR10.2160p.Atmos.TrueHD7.1-CHD.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-040 房间里的女人（1983）

- 已删除：`/Volumes/分类/短篇集/房间里的女人.The.Woman.in.the.Room.1983.mkv`
- 当前保留：`/Volumes/导演们/弗兰克·德拉邦特/房间里的女人.The.Woman.in.the.Room.1983.mkv`
- 依据：同等质量优先导演们。

### quality-041 拯救大兵瑞恩（1998）

- 已删除：`/Volumes/分类/战争/拯救大兵瑞恩.Saving.Private.Ryan.1998.BD1080P.X264.2Audio.AAC.HALFCD-NORM.mkv`
- 当前保留：`/Volumes/导演们/史蒂文·斯皮尔伯格/拯救大兵瑞恩.Saving.Private.Ryan.1998.BD1080P.X264.2Audio.AAC.HALFCD-NORM.mkv`
- 依据：同等质量优先导演们。

### quality-042 摇滚万万岁（1984）

- 已删除：`/Volumes/分类/音乐/摇滚万万岁.This.Is.Spinal.Tap.1984.mkv`
- 当前保留：`/Volumes/导演们/罗伯·莱纳/摇滚万万岁.This.Is.Spinal.Tap.1984.CC.1080p.BluRay.x265.10bit.DTS-QuickIO.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-043 收藏家（1965）

- 已删除：`/Volumes/分类/科幻·奇幻/收藏家.The.Collector.1965.DVDRip.XviD-PARTICLE.mkv`
- 当前保留：`/Volumes/导演们/威廉·惠勒/收藏家.The.Collector.1965.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-044 改编剧本（2002）

- 已删除：`/Volumes/分类/故事/改编剧本.Adaptation.2002.HDRip.2Audio.HALFCD-NOWYS.mmla.mkv`
- 当前保留：`/Volumes/导演们/斯派克·琼斯/改编剧本.Adaptation.2002.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-045 斯托斯特姆桥（1950）

- 已删除：`/Volumes/导演们/卡尔·西奥多·德莱叶/短片/斯托斯特姆桥.Storstrømsbroen.1950.mkv`
- 当前保留：`/Volumes/导演们/卡尔·西奥多·德莱叶/短片/斯托斯特姆桥.Storstrømsbroen.1950.ChEn-Douban.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-046 无忧无虑（2008）

- 已删除：`/Volumes/分类/喜剧/无忧无虑.Happy.Go.Lucky.2008.DVD-RMVB.mkv`
- 当前保留：`/Volumes/导演们/迈克·李/无忧无虑.Happy.Go.Lucky.2008.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-047 最后安全（1923）

- 已删除：`/Volumes/分类/喜剧/最后安全.Safety.Last.1923.mkv`
- 当前保留：`/Volumes/导演们/哈罗德·劳埃德/最后安全.Safety.Last.1923.mkv`
- 依据：同等质量优先导演们。

### quality-048 月球旅行记彩色版（1902）

- 已删除：`/Volumes/分类/科幻·奇幻/月球旅行记.彩色版.A.Trip.to.the.Moon.1902.REMASTERED.Colorized.BluRay.1080p.x265.10bit.AC3.MultiAudio.iNT-TLF.mkv`
- 当前保留：`/Volumes/导演们/乔治·梅里爱/月球旅行记.彩色版.A.Trip.to.the.Moon.1902.REMASTERED.Colorized.BluRay.1080p.x265.10bit.AC3.MultiAudio.iNT-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-049 有机体的秘密（1971）

- 已删除：`/Volumes/导演们/杜尚·马卡维耶夫/有机体的秘密.WR-Mysteries.of.the.Organism.1971.D9.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/杜尚·马卡维耶夫/有机体的秘密.WR.Mysteries.of.the.Organism.1971.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-050 末世纪暴潮（1995）

- 已删除：`/Volumes/分类/科幻·奇幻/末世纪暴潮.Strange.Days.1995.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/凯瑟琳·毕格罗/末世纪暴潮.Strange.Days.1995.BD.2Audio.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-051 末路狂花（1991）

- 已删除：`/Volumes/分类/公路/末路狂花.Thelma.and.Louise.1991.mkv`
- 当前保留：`/Volumes/导演们/雷德利·斯科特/末路狂花.Thelma.And.Louise.1991.CC.2160p.UHD.BluRay.x265.10bit.DV.DTS-HD.MA.5.1.2Audio-SONYHD.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-052 杀人游戏（1967）

- 已删除：`/Volumes/导演们/铃木清顺/杀手烙印.Branded.to.Kill.1967.D5.MiniSD-.mkv`
- 当前保留：`/Volumes/导演们/铃木清顺/杀人游戏.Branded.to.Kill.1967.BD.CC.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-053 杀出个黎明（1996）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/杀出个黎明.From.Dusk.till.Dawn.1996.rmvb`
- 当前保留：`/Volumes/导演们/罗伯特·罗德里格兹/杀出个黎明.From.Dusk.Till.Dawn.1996.rmvb`
- 依据：同等质量优先导演们。

### quality-054 杀手悲歌（1992）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/杀手悲歌.El.Mariachi.1992.Dvdrip.Xvid.Mp3-NewMov.mkv`
- 当前保留：`/Volumes/导演们/罗伯特·罗德里格兹/杀手悲歌.El.Mariachi.1992.Dvdrip.Xvid.Mp3-NewMov.mkv`
- 依据：同等质量优先导演们。

### quality-055 梦旅人（1996）

- 已删除：`/Volumes/导演们/岩井俊二/梦旅人.picnic.1996.D5.TLF.mkv`
- 当前保留：`/Volumes/导演们/岩井俊二/梦旅人.Picnic.1996.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-056 梦醒人生（2001）

- 已删除：`/Volumes/分类/动画片/梦醒人生.Waking.Life.2001.美国.DVD-HALFCD2.mkv`
- 当前保留：`/Volumes/导演们/理查德·林克莱特/半梦半醒的人生.Waking.Life.2001.BD.4Audio.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-057 正午（1952）

- 已删除：`/Volumes/导演们/弗雷德·金尼曼/正午.High.Noon.1952.rmvb`
- 当前保留：`/Volumes/导演们/弗雷德·金尼曼/正午.High.Noon.1952.2160p.UHD.BluRay.x265.10bit.DV.DTS-HD.MA.2.0-SONYHD.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-058 没有过去的人（2002）

- 已删除：`/Volumes/分类/故事/没有过去的人.The.Man.Without.a.Past.2002.rmvb`
- 当前保留：`/Volumes/导演们/阿基·考里斯马基/没有过去的男人.The.Man.Without.a.Past.2002.rmvb`
- 依据：同等质量优先导演们。

### quality-059 爆裂鼓手（2014）

- 已删除：`/Volumes/分类/音乐/爆裂鼓手.Whiplash.2014.BD1280高清中英双字.rmvb`
- 当前保留：`/Volumes/导演们/达米恩·查泽雷/爆裂鼓手.Whiplash.2014.BD1280高清中英双字.rmvb`
- 依据：同等质量优先导演们。

### quality-060 爱丁顿（2025）

- 已删除：`/Volumes/分类/政法委/爱丁顿.Eddington.2025.1080p.MAX.WEB-DL.DDP5.1.H.264.mp4`
- 当前保留：`/Volumes/导演们/阿里·艾斯特/爱丁顿.Eddington.2025.2160p.AMZN.WEB-DL.DDP5.1.Atmos.H.265-BYNDR.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-061 爱乐之城（2016）

- 已删除：`/Volumes/分类/歌舞/爱乐之城.La.La.Land.2016.BluRay.1080p.x264.AC3.TriAudio-TLF.mkv`
- 当前保留：`/Volumes/导演们/达米恩·查泽雷/爱乐之城.La.La.Land.2016.V2.Bluray.2160p.TrueHD7.1.HDR.x265.10bit-DreamHD.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-062 玛戈王后（1954）

- 已删除：`/Volumes/分类/传记·一段历史/玛戈王后.La.Reine.Margot.1954.vhsrip.avi`
- 当前保留：`/Volumes/导演们/阿贝尔·冈斯/玛戈王后.La.Reine.Margot.1954.vhsrip.avi`
- 依据：同等质量优先导演们。

### quality-063 电影人生（2001）

- 已删除：`/Volumes/分类/故事/电影人生.The.Majestic.2001.HDTV.HALFCD-TLF.mkv`
- 当前保留：`/Volumes/导演们/弗兰克·德拉邦特/电影人生.The.Majestic.2001.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-064 男人的争斗（1955）

- 已删除：`/Volumes/分类/黑色电影/男人的争斗.Rififi.1955.2Audio.D9.MiniSD-.mkv`
- 当前保留：`/Volumes/导演们/朱尔斯·达辛/男人的斗争.Rififi.1955.CC.BDRip.X264.iNT-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-065 疯狂的麦克斯3（1985）

- 已删除：`/Volumes/分类/科幻·奇幻/疯狂的麦克斯3.Mad.Max.Beyond.Thunderdome.1985.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/乔治·米勒/疯狂的麦克斯3.Mad.Max.Beyond.Thunderdome.1985.BD.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-066 皮囊之下（2013）

- 已删除：`/Volumes/分类/科幻·奇幻/皮囊之下.Under.the.Skin.2013.rmvb`
- 当前保留：`/Volumes/导演们/乔纳森·格雷泽/皮囊之下.Under.The.Skin.2013.双语字幕.HR-HDTV.AC3.1024X554.x264.V2.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-067 神秘马戏团（2005）

- 已删除：`/Volumes/分类/恐怖/神秘马戏团.Strange.Circus.2005.rmvb`
- 当前保留：`/Volumes/导演们/园子温/神秘马戏团.Strange.Circus.2005.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-068 积木人生（1982）

- 已删除：`/Volumes/分类/CULT·实验/积木人生.The.Prefab.People.1982.repack.dvdrip.xvid-fico.mp4`
- 当前保留：`/Volumes/导演们/贝拉·塔尔/积木人生.The.Prefab.People.1982.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-069 精神病院（2002）

- 已删除：`/Volumes/分类/故事/精神病院,Dom.durakov.2002.DVDRip.avi`
- 当前保留：`/Volumes/导演们/安德烈·康查洛夫斯基/精神病院.Dom.durakov.2002.DVDRip.avi`
- 依据：同等质量优先导演们。

### quality-070 精英部队2大敌当前（2010）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/精英部队2.大敌当前.Elite.Squad.The.Enemy.Within.2010.rmvb`
- 当前保留：`/Volumes/导演们/何塞·帕迪里亚/精英部队2.大敌当前.Elite.Squad.The.Enemy.Within.2010.rmvb`
- 依据：同等质量优先导演们。

### quality-071 红菱艳（1948）

- 已删除：`/Volumes/分类/故事/红菱艳.The.Red.Shoes.1948.mkv`
- 当前保留：`/Volumes/导演们/迈克尔·鲍威尔/红菱艳.The.Red.Shoes.1948.mkv`
- 依据：同等质量优先导演们。

### quality-072 维拉德雷克（2004）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/维拉·德雷克.Vera.Drake.2004.LiMiTED.DVDRip.XviD-FTS.mkv`
- 当前保留：`/Volumes/导演们/迈克·李/维拉德雷克.Vera.Drake.2004.D9.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-073 肖申克的救赎（1994）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/肖申克的救赎.The.Shawshank.Redemption.1994.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 当前保留：`/Volumes/导演们/弗兰克·德拉邦特/肖申克的救赎.The.Shawshank.Redemption.1994.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-074 花与爱丽丝杀人事件（2015）

- 已删除：`/Volumes/分类/动画片/花与爱丽丝杀人事件.The.Murder.Case.of.Hana.&.Alice.2015.BD.HEVC.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/岩井俊二/花与爱丽丝杀人事件.The.Murder.Case.of.Hana.&.Alice.2015.BD.HEVC.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-075 角斗士（2000）

- 已删除：`/Volumes/分类/传记·一段历史/角斗士.Gladiator.2000.BDRip.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/雷德利·斯科特/角斗士.Gladiator.2000.BDRip.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-076 诚如神之所说（2014）

- 已删除：`/Volumes/导演们/三池崇史/诚如神之所说.As.the.Gods.Will.2014.rmvb`
- 当前保留：`/Volumes/导演们/三池崇史/诚如神之所说.As.the.Gods.Will.2014.BD1080P.X264.AAC.Japanese.CHS.Mp4Ba.mp4`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-077 贝隆夫人（1996）

- 已删除：`/Volumes/分类/传记·一段历史/贝隆夫人.Evita.1996.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/艾伦·帕克/贝隆夫人.Evita.1996.15th.BDRip.X264-YXY.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-078 这不是一部电影（2011）

- 已删除：`/Volumes/分类/纪录/这不是一部电影.This.Is.Not.a.Film.2011.D5.EngSUB.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/贾法·帕纳西/这不是一部电影.This.Is.Not.a.Film.2011.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-079 迷墙（1982）

- 已删除：`/Volumes/分类/音乐/迷墙.Pink.Floyd.The.Wall.1982.HDTV.MINISD-TLF.mkv`
- 当前保留：`/Volumes/导演们/艾伦·帕克/迷墙.Pink.Floyd.The.Wall.1982.HDTV.MINISD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-080 迷雾（2007）

- 已删除：`/Volumes/分类/科幻·奇幻/迷雾.The.Mist.2007.mkv`
- 当前保留：`/Volumes/导演们/弗兰克·德拉邦特/迷雾.The.Mist.2007.mkv`
- 依据：同等质量优先导演们。

### quality-081 透纳先生（2014）

- 已删除：`/Volumes/分类/传记·一段历史/透纳先生.Mr.Turner.2014.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/迈克·李/透纳先生.Mr.Turner.2014.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-082 遗传厄运（2018）

- 已删除：`/Volumes/分类/恐怖/遗传厄运.Hereditary.2018.V2.Bluray.2160p.DTS-HDMA5.1.DoVi.HDR.x265.10bit-NukeHD.mkv`
- 当前保留：`/Volumes/导演们/阿里·艾斯特/遗传厄运.Hereditary.2018.V2.Bluray.2160p.DTS-HDMA5.1.DoVi.HDR.x265.10bit-NukeHD.mkv`
- 依据：同等质量优先导演们。

### quality-083 隐秘（2006）

- 已删除：`/Volumes/分类/惊悚·犯罪·动作/隐秘.La.sconosciuta.2006.BD.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/朱塞佩·托纳多雷/隐秘.La.sconosciuta.2006.BD.3Audio.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-084 零点地带（1959）

- 已删除：`/Volumes/分类/战争/零点地带.Kapo.1959.D9.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/吉洛·彭泰科沃/零点地带.Kapo.1959.D9.MiniSD-TLF.mkv`
- 依据：同等质量优先导演们。

### quality-085 非洲女王号（1951）

- 已删除：`/Volumes/分类/战争/非洲女王号.The.African.Queen.1951.BDRip.MiniSD-TLF.mkv`
- 当前保留：`/Volumes/导演们/约翰.休斯顿/非洲女王号.The.African.Queen.1951.BD.2Audio.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

### quality-086 鸢之恋（1978）

- 已删除：`/Volumes/分类/爱情/鸢之恋-Furimukeba.ai.1978.D5.HALFCD-TLF.mkv`
- 当前保留：`/Volumes/导演们/山口百惠[演员]/鸢之恋.Furimukeba.ai.1978.BD.MiniSD-TLF.mkv`
- 依据：按体积、质量标记及MKV偏好保留占优版本。

## 排除与保留的特殊资源

《亡命大煞星》(1972) 的 The Getaway 与 Junior Bonner、《杀手》(1956) 的 The Killers 与 The Killing、《黑雨》(1989) 的 Black Rain 与 Kuroi ame、《米尔克/牛奶》(2008) 等存在片名或身份冲突，未作为普通同片副本处理。《卡尔·梅》(1974) 的 Part1/Part2，以及《玩家马布斯博士》(1922) 的 115 分钟版与 271 分钟修复分段版继续保留。花絮、访谈和解说资料不作为普通正片重复删除。
