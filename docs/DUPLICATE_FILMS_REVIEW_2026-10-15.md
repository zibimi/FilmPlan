# 分类与导演们：内部重复清理结果

更新日期：2026-10-16（America/Los_Angeles）。最终路径核验时间：2026-10-16T13:52:07.156184-07:00。本轮以用户手动整理后的全新扫描为基准，清理两个大文件夹内部的重复；没有按旧报告盲目执行。

## 本轮已完成

- 处理 **95 部作品、96 个同版本分组**，删除 **100 个**重复或较差视频，逻辑文件大小合计 **123.70 GiB**。
- 分类删除 **64 个**；导演们删除 **36 个**。
- 已将保留版本归档移动 **28 个**：分类内 **25 个**，导演库内 **3 个**。全部为同一共享目录内部移动，无跨共享复制、无覆盖。
- 每项执行前核对大小、修改时间及保留视频容器头和尾部可读性；移动前后核对首尾数据摘要。执行后核验删除路径不存在、最终保留文件大小和修改时间一致。没有整片解码或画面评测。
- 最终目录成员与预期一致；无失败、无意外缺失或新增。字幕、附件、分集、分段和特殊版本不随普通视频副本删除；本轮归档视频未发现同名外挂字幕需要移动。文件逻辑大小不代表NAS实际释放空间。

## 选择与归档规则

体积明显更大优先；15%以内视为接近，按MKV/MP4 > AVI > RMVB比较，再比较字节大小。特殊版本/分段/资料保留。 体积与格式优劣直接冲突时保留两份待复核。

分类选择依据在线类型资料和剧情梗概，落入现有目录体系。华语或华人文化题材沿用华语世界优先规则；动画、短篇集、系列、导演子目录在适用时保留。只有剧情时阅读梗概并选择明确的家庭、宗教、体育等主题；无法细分的使用现有故事类。下面每部分类影片均附核对来源，归档位置是本次采用的主位置。

## 当前还需要判断的内部候选

本轮保留 **11 组**真正需再核对的内部候选。其中体积与格式冲突 **6 组**；其余涉及剪辑、声轨或异常小文件。另有 **13 组**不同短片、不同版本或正片附加资料已明确保留，不应算作多余副本。分集、分段和合集粗筛误报另行排除。

### 千禧曼波（2001）

资料列119分钟与DVD101分钟，需核对实际时长区分剪辑

- `/Volumes/分类/华语世界/台湾/侯孝贤/千禧曼波.Millenium.Mambo.2001.D9.MiniSD-TLF.mkv` — 0.69 GiB
- `/Volumes/分类/华语世界/台湾/侯孝贤/千禧曼波.Millennium.Mambo.2001.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 8.92 GiB

### 午后的迷惘（1943）

含附加资料、特殊音轨或剪辑，不作为普通副本删除

- `/Volumes/分类/CULT·实验/午后的迷惘.Meshes.of.the.Afternoon.1943.720p.BluRay.SILENT.x264-NCmt.mkv` — 0.85 GiB
- `/Volumes/分类/短篇集/午后的迷惘.Meshes.Of.The.Afternoon.1943.D9.MiniSD-TLF.mkv` — 0.10 GiB

### 电影往事（2004）

含异常小文件，需要先核对是否为有效媒体

- `/Volumes/分类/华语世界/中国大陆/电影往事.Electric.Shadows.2004.D5.MiniSD-TLF.mkv` — 0.74 GiB
- `/Volumes/分类/华语世界/欧美华人/梦影童年.Electric.Shadows.2004.D5.HALFCD-TLF.mkv` — 0.00 GiB

### 砂之女（1964）

存在明确不同剪辑/黑白版标记

- `/Volumes/分类/CULT·实验/砂之女.Woman.In.The.Dunes.D.C.1964.D9.MiniSD-TLF.mkv` — 0.94 GiB
- `/Volumes/分类/惊悚·犯罪·动作/砂之女.Woman.In.The.Dunes.1964.BluRay.1080p.LPCM1.0.x265.10bit-DreamHD.mkv` — 9.08 GiB

### 闪灵（1980）

存在明确不同剪辑/黑白版标记

- `/Volumes/导演们/斯坦利·库布里克/闪灵/闪灵.The.Shining.1980.2160p.iTunes.WEB-DL.DD5.1.DV.HDR.H.265-BATWEB.mkv` — 25.40 GiB
- `/Volumes/导演们/斯坦利·库布里克/闪灵/闪灵.The.Shining.1980.REMASTERED.US.DC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 8.59 GiB

### 丑闻笔记（2006）

较大文件为AVI/RMVB，另一份为更优容器MKV：体积与格式偏好冲突，暂留两份

- `/Volumes/分类/惊悚·犯罪·动作/丑闻笔记.Notes.on.a.Scandal.2006.rmvb` — 0.97 GiB
- `/Volumes/分类/惊悚·犯罪·动作/丑闻笔记.Notes.On.A.Scandal.2006.BD.2Audio.MiniSD-TLF.mkv` — 0.73 GiB

### 四十五周年45（2015）

较大文件为AVI/RMVB，另一份为更优容器MKV：体积与格式偏好冲突，暂留两份

- `/Volumes/分类/爱情/45周年.45.Years.2015.rmvb` — 0.97 GiB
- `/Volumes/分类/爱情/四十五周年.45.Years.2015.LIMITED.BD.MiniSD-TLF.mkv` — 0.68 GiB

### 我们仍未知道那天所看见的花的名字剧场版（2013）

较大文件为AVI/RMVB，另一份为更优容器MKV：体积与格式偏好冲突，暂留两份

- `/Volumes/分类/动画片/未闻花名.Anohana.the.Movie.The.Flower.We.Saw.That.Day.2013.rmvb` — 1.05 GiB
- `/Volumes/分类/动画片/我们仍未知道那天所看见的花的名字.剧场版.Anohana.The.Movie.The.Flower.We.Saw.That.Day.2013.BD.MiniSD-TLF.mkv` — 0.55 GiB

### 死吻（1955）

较大文件为AVI/RMVB，另一份为更优容器MKV：体积与格式偏好冲突，暂留两份

- `/Volumes/分类/黑色电影/死吻.Kiss.Me.Deadly.1955.DVDRip.by.Galmuchet.avi` — 0.98 GiB
- `/Volumes/分类/惊悚·犯罪·动作/死吻.Kiss.Me.Deadly.1955.BD.CC.MiniSD-TLF.mkv` — 0.84 GiB

### 畸型人（1932）

较大文件为AVI/RMVB，另一份为更优容器MKV：体积与格式偏好冲突，暂留两份

- `/Volumes/分类/黑色电影/畸形人.Freaks.1932.Freaks.1932.avi` — 0.71 GiB
- `/Volumes/分类/CULT·实验/畸型人.Freaks.1932.D9.MiniSD-TLF.mkv` — 0.45 GiB

### 上帝愤怒的人（1981）

较大文件为AVI/RMVB，另一份为更优容器MKV：体积与格式偏好冲突，暂留两份

- `/Volumes/导演们/沃纳·赫尔佐格/上帝愤怒的人.Gods.Angry.Man.1981.avi` — 0.34 GiB
- `/Volumes/导演们/沃纳·赫尔佐格/上帝愤怒的人.Gods.Angry.Man.1981.mkv` — 0.17 GiB

## 明确保留的特殊资源

- **Louis Aimé Augustin Le Prince - 1988 - Roundhay Garden Scene.mp4（1988）**：不同早期短片，误报，不应合并。
- **刺客聂隐娘（2015）**：明确不同剪辑、呈现或解说版本，继续保留。
- **吴清源（2006）**：正片与附加资料，不按普通重复删除。
- **深夜止步（1975）**：正片与附加资料，不按普通重复删除。
- **金刚狼3（2017）**：明确不同剪辑、呈现或解说版本，继续保留。
- **两生花（1991）**：正片与附加资料，不按普通重复删除。
- **大学新生（1925）**：完整正片与解说音轨版，分别保留。
- **敲诈配音版（1929）**：明确不同剪辑、呈现或解说版本，继续保留。
- **残酷的游戏（1983）**：正片与附加资料，不按普通重复删除。
- **追随（1998）**：明确不同剪辑、呈现或解说版本，继续保留。
- **闹鬼（1920）**：明确不同剪辑、呈现或解说版本，继续保留。
- **飞毛腿（1928）**：明确不同剪辑、呈现或解说版本，继续保留。
- **饲养乌鸦（1976）**：正片与附加资料，不按普通重复删除。

《女巫》1922原版与1968年重编版分别去重后，各保留一份；两种版本互不替代。

## 尚存跨库候选：3 组

本轮按请求处理库内重复，下列跨库身份或导演归属问题未扩展执行。

### 疾走天堂（2002）

- `/Volumes/分类/惊悚·犯罪·动作/疾走天堂.Heaven.2002.BD.MiniSD-TLF.mkv` — 0.85 GiB
- `/Volumes/导演们/克日什托夫·基耶斯洛夫斯基/天堂.Heaven.2002.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 4.48 GiB

### 花（2011）

- `/Volumes/分类/华语世界/中国大陆/导演们/娄烨/花.Love.and.Bruises.2011.D9.MiniSD-TLF.mkv` — 1.09 GiB
- `/Volumes/导演们/彼得·格林纳威/花.Love.and.Bruises.2011.french.novembre.multi.720p.bluray.dts.x264-bix.avi` — 0.68 GiB

### 蓝天使（1930）

- `/Volumes/分类/喜剧/蓝天使.Der.blaue.Engel.1930.BD.German.MiniSD-TLF.mkv` — 0.83 GiB
- `/Volumes/导演们/玛琳·黛德丽[演员]/蓝天使.The.Blue.Angel.1930.DVDrip.by.galmuchet.avi` — 0.66 GiB

## 本轮逐项执行记录

### /Volumes/分类

#### internal-002 修女艾达（2013，普通正片）

- 最终保留：`/Volumes/分类/宗教/修女艾达.Ida.2013.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 6.33 GiB
- 已删除：`/Volumes/分类/宗教/修女艾达.Ida.2013.BD.MiniSD-TLF.mkv` — 0.96 GiB
- 归档依据：修女誓愿、信仰与身世是故事核心，保留宗教题材类
- [类型或身份资料](https://www.imdb.com/title/tt2718492/)

#### internal-003 借着雨点说爱你（2004，普通正片）

- 最终保留：`/Volumes/分类/爱情/借着雨点说爱你.Be.with.You.2004.BD.MiniSD-TLF.mkv` — 0.67 GiB
- 移出原位置：`/Volumes/分类/科幻·奇幻/借着雨点说爱你.Be.with.You.2004.BD.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/科幻·奇幻/大约在雨季.Be.with.You.2004.rmvb` — 0.63 GiB
- 归档依据：IMDb剧情/奇幻/爱情；爱情为核心，采用爱情类
- [类型或身份资料](https://www.imdb.com/title/tt0442268/)

#### internal-004 华盛顿城堡的圣徒（1993，普通正片）

- 最终保留：`/Volumes/分类/故事/华盛顿城堡的圣徒.The.Saint.of.Fort.Washington.1993.D5.MiniSD-TLF.mkv` — 0.52 GiB
- 已删除：`/Volumes/分类/故事/燃烧华盛顿.The.Saint.of.Fort.Washington.1993.mkv` — 0.36 GiB
- 归档依据：IMDb心理剧情/剧情，流浪者生活题材，保留故事兜底
- [类型或身份资料](https://www.imdb.com/title/tt0108026)

#### internal-005 吉尔达（1946，普通正片）

- 最终保留：`/Volumes/分类/黑色电影/吉尔达.Gilda.1946.BD.MiniSD-TLF.mkv` — 1.36 GiB
- 已删除：`/Volumes/分类/黑色电影/吉尔达.Gilda.1946.avi` — 0.66 GiB
- 归档依据：IMDb Film Noir，Criterion亦认定黑色电影
- [类型或身份资料](https://www.imdb.com/title/tt0038559)
- [类型或身份资料](https://www.criterion.com/films/27909-gilda)

#### internal-007 女巫（1922，1922原版）

- 最终保留：`/Volumes/分类/恐怖/女巫.Haxan.1922.CC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 7.64 GiB
- 已删除：`/Volumes/分类/CULT·实验/女巫.Haexan.1922.D9.MiniSD-TLF.mkv` — 0.79 GiB
- 归档依据：Criterion证实1922原版及1968年76分钟重编版为不同版本；分别去重，重编版必须保留一份
- [类型或身份资料](https://www.criterion.com/films/352-haxan)
- [类型或身份资料](https://www.criterion.com/current/posts/6634-haxan-let-her-suffering-begin)

#### internal-008 女巫（1922，1968重编版）

- 最终保留：`/Volumes/分类/恐怖/女巫.Witchcraft.Through.The.Ages.1922.68年重编版.D5.MiniSD-TLF.mkv` — 0.52 GiB
- 已删除：`/Volumes/分类/CULT·实验/女巫.Witchcraft.Through.The.Ages.1922.68年重编版.D5.MiniSD-TLF.mkv` — 0.52 GiB
- 归档依据：Criterion证实1922原版及1968年76分钟重编版为不同版本；分别去重，重编版必须保留一份
- [类型或身份资料](https://www.criterion.com/films/352-haxan)
- [类型或身份资料](https://www.criterion.com/current/posts/6634-haxan-let-her-suffering-begin)

#### internal-009 尼罗河上的惨案（1978，普通正片）

- 最终保留：`/Volumes/分类/惊悚·犯罪·动作/尼罗河上的惨案.Death.on.the.Nile.1978.BD.2Audio.MiniSD-TLF.mkv` — 1.29 GiB
- 已删除：`/Volumes/分类/惊悚·犯罪·动作/译制经典尼罗河上的惨案.Death.on.the.Nile.1978.DVDrip.X264.2Audio.AAC.HALFCD-NORMTEAM.hoson.mkv` — 0.49 GiB
- 归档依据：IMDb犯罪/悬疑推理
- [类型或身份资料](https://www.imdb.com/title/tt0077413/)

#### internal-010 岁月的童话（1991，普通正片）

- 最终保留：`/Volumes/分类/动画片/导演和大厂/吉卜力/岁月的童话.Only.Yesterday.1991.BD.1920x1036.HEVC-10bit.OPUS.ASSx2.mkv` — 10.09 GiB
- 已删除：`/Volumes/分类/故事/岁月的童话.Only.Yesterday.1991.DVD.X264.2Audio.AAC.HALFCD-NORM.mkv` — 0.50 GiB
- 已删除：`/Volumes/分类/青春·儿童/岁月的童话.Only.Yesterday.1991.rmvb` — 0.51 GiB
- 归档依据：动画长片；保留原吉卜力子目录
- [类型或身份资料](https://www.imdb.com/title/tt0102587/)
- [类型或身份资料](https://www.douban.com/doulist/148800689/?playable=0&sort=seq&start=100&sub_type=)

#### internal-011 幽灵世界（2001，普通正片）

- 最终保留：`/Volumes/分类/喜剧/幽灵世界.Ghost.World.2001.HDTV.MiniSD-TLF.mkv` — 0.81 GiB
- 移出原位置：`/Volumes/分类/青春·儿童/幽灵世界.Ghost.World.2001.HDTV.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/科幻·奇幻/幽灵世界.Ghost.World.2001.rmvb` — 0.54 GiB
- 归档依据：IMDb Comedy/Drama，成长题材黑色喜剧，采用喜剧主类
- [类型或身份资料](https://www.imdb.com/title/tt0162346/)

#### internal-012 弗兰兹卡夫卡（1992，普通正片）

- 最终保留：`/Volumes/分类/动画片/动画的世纪·100部作品/弗兰兹·卡夫卡.Franz.Kafka.Piotr.Dumala.1992.DVDRip.XviD-CiNEMAGROTESQUE.avi` — 0.18 GiB
- 已删除：`/Volumes/分类/名著改编/卡夫卡电影作品集/弗兰兹·卡夫卡/弗兰兹·卡夫卡.Franz.Kafka.1992.DVDRip.XviD-CiNEMAGROTESQUE.avi` — 0.18 GiB
- 归档依据：波兰文化机构确认Dumala的动画短片；资料记1991，原文件记1992，本轮不改名
- [类型或身份资料](https://culture.pl/pl/dzielo/franz-kafka)

#### internal-013 情迷六月花（1990，普通正片）

- 最终保留：`/Volumes/分类/情色/情迷六月花.Henry.&.June.1990.BD.MiniSD-TLF.mkv` — 1.90 GiB
- 已删除：`/Volumes/分类/传记·一段历史/情迷六月花.Henry.&.June.1990.D9.MiniSD-TLF.mkv` — 0.88 GiB
- 归档依据：豆瓣剧情/传记/情色，采用更具体的情色分类
- [类型或身份资料](https://www.douban.com/doulist/1691871/)
- [类型或身份资料](https://www.imdb.com/title/tt0099762/fullcredits/)

#### internal-015 抢劫装甲车（1951，普通正片）

- 最终保留：`/Volumes/分类/喜剧/抢劫装甲车.The.Lavender.Hill.Mob.1951.BD.MiniSD-TLF.mkv` — 0.60 GiB
- 已删除：`/Volumes/分类/惊悚·犯罪·动作/拉凡德山的暴徒.The.Lavender.Hill.Mob.1951.DVDRip.X264.AAC.HALFCD-NORM.Christian.mkv` — 0.29 GiB
- 归档依据：IMDb喜剧/犯罪，Ealing劫案喜剧
- [类型或身份资料](https://www.imdb.com/title/tt0044829/)
- [类型或身份资料](https://player.bfi.org.uk/rentals/film/watch-the-lavender-hill-mob-1951-online)

#### internal-016 攻壳机动队2无罪（2004，普通正片）

- 最终保留：`/Volumes/分类/动画片/攻壳机动队/攻壳机动队2.无罪.Ghost.in.the.Shell.2.Innocence.2004.x264.10bit.1920x1036.FLAC.6.1.mkv` — 5.27 GiB
- 移出原位置：`/Volumes/分类/动画片/攻壳机动队2.无罪.Ghost.in.the.Shell.2.Innocence.2004.x264.10bit.1920x1036.FLAC.6.1.mkv`
- 已删除：`/Volumes/分类/动画片/攻壳机动队/攻壳机动队2-无罪.Ghost.In.The.Shell.2.Innocence.2004.BD.MiniSD-TLF.mkv` — 0.63 GiB
- 归档依据：IMDb日本动画/科幻，保留已存在的攻壳机动队系列目录
- [类型或身份资料](https://www.imdb.com/title/tt0347246/)

#### internal-017 无名（2023，普通正片）

- 最终保留：`/Volumes/分类/华语世界/中国大陆/导演们/程耳/无名.Hidden.Blade.2023.KOR.BluRay.1080p.HEVC.10bit.MiniFHD.mkv` — 8.06 GiB
- 已删除：`/Volumes/分类/华语世界/中国大陆/无名.Hidden.Blade.2023.BD.MiniSD-TLF.mkv` — 0.66 GiB
- 归档依据：豆瓣中国大陆悬疑历史剧情；两份均为BD来源，保留程耳导演子目录
- [类型或身份资料](https://movie.douban.com/subject/35372742/)

#### internal-018 日烦夜烦（2001，普通正片）

- 最终保留：`/Volumes/分类/恐怖/日烦夜烦.Trouble.Every.Day.2001.avi` — 0.68 GiB
- 已删除：`/Volumes/分类/音乐/日烦夜烦.Trouble.Every.Day.2001.avi` — 0.68 GiB
- 归档依据：IMDb剧情/恐怖/惊悚，不是音乐片
- [类型或身份资料](https://www.imdb.com/title/tt0204700/)

#### internal-019 最后的舞者（2009，普通正片）

- 最终保留：`/Volumes/分类/华语世界/欧美华人/最后的舞者.Maos.Last.Dancer.2009.BD.MiniSD-TLF.mkv` — 0.92 GiB
- 移出原位置：`/Volumes/分类/故事/最后的舞者.Maos.Last.Dancer.2009.BD.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/传记·一段历史/最后的舞者.Mao.s.Last.Dancer.2009.rmvb` — 0.48 GiB
- 归档依据：李存信生平传记；中英双语、华人移民文化题材，按华语世界既有优先规则归入欧美华人
- [类型或身份资料](https://www.imdb.com/title/tt1071812/)

#### internal-020 月亮上的男人（1999，普通正片）

- 最终保留：`/Volumes/分类/传记·一段历史/月亮上的男人.Man.On.The.Moon.1999.BD.2Audio.MiniSD-TLF.mkv` — 0.93 GiB
- 移出原位置：`/Volumes/分类/喜剧/月亮上的男人.Man.On.The.Moon.1999.BD.2Audio.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/传记·一段历史/月亮上的男人.Man.On.The.Moon.1999.BD.MiniSD-TLF.mkv` — 0.88 GiB
- 已删除：`/Volumes/分类/CULT·实验/月亮上的男人.Man.On.The.Moon.1999.DVDRip.XviD.AC3.mkv` — 0.44 GiB
- 归档依据：安迪考夫曼生平传记喜剧，采用传记主类
- [类型或身份资料](https://www.imdb.com/title/tt0125664/)
- [类型或身份资料](https://www.universalpicturesathome.com/movies/man-on-the-moon)

#### internal-021 朱莉亚（1977，普通正片）

- 最终保留：`/Volumes/分类/传记·一段历史/朱莉亚.Julia.1977.BluRay.720p.x264.AC3.iNT-TLF.mkv` — 2.34 GiB
- 移出原位置：`/Volumes/分类/故事/朱莉亚.Julia.1977.BluRay.720p.x264.AC3.iNT-TLF.mkv`
- 已删除：`/Volumes/分类/传记·一段历史/朱莉亚.Julia.1977.DVDRip.XviD-LOOK.mkv` — 0.53 GiB
- 归档依据：Lillian Hellman回忆改编的历史剧情，保留既有传记归属
- [类型或身份资料](https://www.imdb.com/title/tt0076245/)

#### internal-022 杀人者（1946，普通正片）

- 最终保留：`/Volumes/分类/黑色电影/绣巾蒙面盗.The.Killers.1946.BD.MiniSD-TLF.mkv` — 0.98 GiB
- 已删除：`/Volumes/分类/黑色电影/杀人者.The.Killers.1946.D9.MiniSD-TLF.mkv` — 0.80 GiB
- 归档依据：Criterion确认The Killers为Robert Siodmak黑色电影
- [类型或身份资料](https://www.criterion.com/films/724-the-killers)

#### internal-023 杂耍班（1925，普通正片）

- 最终保留：`/Volumes/分类/爱情/杂耍班.Variete.1925.BD.German.MiniSD-TLF.mkv` — 0.81 GiB
- 移出原位置：`/Volumes/分类/喜剧/杂耍班.Variete.1925.BD.German.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/故事/杂耍班.Dupont.Variete.1925.mkv` — 0.30 GiB
- 归档依据：Dupont导演，爱情嫉妒悲剧；IMDb Crime/Drama/Romance，非喜剧
- [类型或身份资料](https://www.imdb.com/es/title/tt0016481/)
- [类型或身份资料](https://catalogue.bnf.fr/ark%3A/12148/cb14661599h)

#### internal-024 枪疯（1950，普通正片）

- 最终保留：`/Volumes/分类/黑色电影/枪疯.Gun.Crazy.1950.mkv` — 0.82 GiB
- 已删除：`/Volumes/分类/黑色电影/枪疯.Gun.Crazy.AKA.Deadly.Is.the.Female.1950.D5.2Audio.MiniSD-TLF.mkv` — 0.64 GiB
- 已删除：`/Volumes/分类/惊悚·犯罪·动作/枪疯.Gun.Crazy.AKA.Deadly.Is.the.Female.1950.BD.2Audio.MiniSD-TLF.mkv` — 0.73 GiB
- 归档依据：同名Gun Crazy与AKA Deadly Is the Female，经典黑色犯罪片
- [类型或身份资料](https://www.imdb.com/title/tt0042530/plotsummary/)
- [类型或身份资料](https://www.imdb.com/name/nm0197982/)

#### internal-025 树（2010，普通正片）

- 最终保留：`/Volumes/分类/家庭/树.The.Tree.2010.BD.MiniSD-TLF.mkv` — 0.75 GiB
- 移出原位置：`/Volumes/分类/故事/树.The.Tree.2010.BD.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/故事/树上的父亲.The.Tree.2010.rmvb` — 0.39 GiB
- 归档依据：IMDb剧情概要为丧父后母女及家庭生活，采用家庭题材
- [类型或身份资料](https://www.imdb.com/title/tt1496005/plotsummary/)

#### internal-026 桃色交易（1993，普通正片）

- 最终保留：`/Volumes/分类/爱情/桃色交易.Indecent.Proposal.1993.REMASTERED.1080p.BluRay.x265.10bit.DTS.MultiAudio-TLF.mkv` — 10.00 GiB
- 已删除：`/Volumes/分类/歌舞/桃色交易.Indecent.Proposal.1993.REMASTERED.1080p.BluRay.x265.10bit.DTS.MultiAudio-TLF.mkv` — 10.00 GiB
- 归档依据：IMDb Drama/Romance，婚姻与情感题材
- [类型或身份资料](https://www.imdb.com/title/tt0107211)

#### internal-027 棋王（1991，普通正片）

- 最终保留：`/Volumes/分类/华语世界/香港/导演们/徐克/棋王.King.of.Chess.1991.1080p.WEBRip.CHS-HAN@CHAOSPACE.mp4` — 2.51 GiB
- 已删除：`/Volumes/分类/惊悚·犯罪·动作/棋王.King.Of.Chess.1991.DVD.X264.2Audio.AAC.HALFCD-NORM.mkv` — 0.42 GiB
- 归档依据：IMDb中国香港华语剧情，保留原有导演子目录
- [类型或身份资料](https://www.imdb.com/title/tt0095450/)
- [类型或身份资料](https://en.wikipedia.org/wiki/King_of_Chess_(1991_film))

#### internal-029 漫长夏日（1966，普通正片）

- 最终保留：`/Volumes/分类/体育/无尽之夏.The.Endless.Summer.1966.BluRay.a720.x264.DD51.MySiLU.mkv` — 2.05 GiB
- 移出原位置：`/Volumes/分类/纪录/无尽之夏.The.Endless.Summer.1966.BluRay.a720.x264.DD51.MySiLU.mkv`
- 已删除：`/Volumes/分类/纪录/漫长夏日.The.Endless.Summer.1966.BD.MiniSD-TLF.mkv` — 0.68 GiB
- 归档依据：IMDb Sports Documentary，冲浪运动纪录片，采用体育题材
- [类型或身份资料](https://www.imdb.com/title/tt0060371)

#### internal-030 火之谜（2023，普通正片）

- 最终保留：`/Volumes/分类/冒险·灾难/火之谜.Riddle.of.Fire.2023.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 7.64 GiB
- 移出原位置：`/Volumes/分类/故事/火之谜.Riddle.of.Fire.2023.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 已删除：`/Volumes/分类/青春·儿童/火之谜.Riddle.of.Fire.2023.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 7.64 GiB
- 归档依据：IMDb Adventure/Fantasy，儿童林间冒险故事，采用既有冒险分类
- [类型或身份资料](https://www.imdb.com/title/tt7575046/)

#### internal-031 爱到天堂（1945，普通正片）

- 最终保留：`/Volumes/分类/黑色电影/爱到天堂.Leave.Her.to.Heaven.1945.CC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 4.28 GiB
- 已删除：`/Volumes/分类/黑色电影/狂恋.Leave.Her.to.Heaven.1945.mkv` — 0.46 GiB
- 归档依据：IMDb Film Noir，Criterion亦确认黑色电影
- [类型或身份资料](https://www.imdb.com/title/tt0037865)
- [类型或身份资料](https://www.criterion.com/films/29602-leave-her-to-heaven)

#### internal-032 爸妈不在家（2013，普通正片）

- 最终保留：`/Volumes/分类/华语世界/东南亚/陈哲艺/爸妈不在家.Ilo.Ilo.2013.BDRip.X264.iNT-TLF.mkv` — 2.73 GiB
- 已删除：`/Volumes/分类/故事/爸妈不在家.Ilo.Ilo.2013.rmvb` — 1.05 GiB
- 归档依据：新加坡华语家庭剧情，保留原陈哲艺子目录
- [类型或身份资料](https://www.imdb.com/title/tt2901736/)

#### internal-033 牧马人（1982，普通正片）

- 最终保留：`/Volumes/分类/华语世界/中国大陆/导演们/谢晋/牧马人.The.Herdsman.1982.1080p.BluRay.x265.10bit.LPCM2.0-ParkHD.mkv` — 14.98 GiB
- 已删除：`/Volumes/分类/华语世界/中国大陆/牧马人.The.Herdsman.1982.BluRay.1080p.x265.10bit.AC3-TLF.mkv` — 7.24 GiB
- 归档依据：豆瓣中国大陆剧情/爱情，保留谢晋导演子目录
- [类型或身份资料](https://movie.douban.com/subject/1308038/comments?status=P)

#### internal-034 牯岭街少年杀人事件（1991，普通正片）

- 最终保留：`/Volumes/分类/华语世界/台湾/杨德昌/牯岭街少年杀人事件.A.Brighter.Summer.Day.1991.BD.CC.2Audio.MiniSD&MiniHD-TLF/牯岭街少年杀人事件.A.Brighter.Summer.Day.1991.BD.CC.2Audio.MiniHD-TLF.mkv` — 3.93 GiB
- 已删除：`/Volumes/分类/华语世界/台湾/杨德昌/牯岭街少年杀人事件.A.Brighter.Summer.Day.1991.BD.CC.2Audio.MiniSD&MiniHD-TLF/牯岭街少年杀人事件.A.Brighter.Summer.Day.1991.BD.CC.2Audio.MiniSD-TLF.mkv` — 2.62 GiB
- 归档依据：台湾华语剧情，现杨德昌电影子目录内，保留较好版本位置
- [类型或身份资料](https://www.imdb.com/title/tt0101985/)
- [类型或身份资料](https://www.criterion.com/films/28596-a-brighter-summer-day)

#### internal-035 狐狸与我（2007，普通正片）

- 最终保留：`/Volumes/分类/青春·儿童/狐狸与我.The.Fox.And.The.Child.2007.BD.2Audio.MiniSD-TLF.mkv` — 0.64 GiB
- 移出原位置：`/Volumes/分类/故事/狐狸与我.The.Fox.And.The.Child.2007.BD.2Audio.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/青春·儿童/狐狸与孩子.The.Fox.and.the.Child.2007.rmvb` — 0.45 GiB
- 归档依据：IMDb动物冒险/剧情/家庭，女孩与狐狸的故事
- [类型或身份资料](https://www.imdb.com/title/tt0756648/)

#### internal-036 玛德莲堕落少女（2002，普通正片）

- 最终保留：`/Volumes/分类/宗教/玛德莲堕落少女.The.Magdalene.Sisters.2002.WEB-DL.MiniSD-TLF.mkv` — 1.31 GiB
- 移出原位置：`/Volumes/分类/故事/玛德莲堕落少女.The.Magdalene.Sisters.2002.WEB-DL.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/故事/青楼姊妹花.The.Magdalene.Sisters.2002.mkv` — 0.94 GiB
- 归档依据：IMDb剧情概要为教会收容所内女性受压迫，采用宗教题材
- [类型或身份资料](https://www.imdb.com/title/tt0318411)

#### internal-038 登楼叹（2021，普通正片）

- 最终保留：`/Volumes/分类/华语世界/欧美华人/登楼叹.Ascension.2021.mp4` — 1.96 GiB
- 已删除：`/Volumes/分类/华语世界/禁/登楼叹.Ascension.2021.mp4` — 1.96 GiB
- 归档依据：Tribeca确认美国制作、汉语纪录片，按华语文化优先保留欧美华人类
- [类型或身份资料](https://tribecafilm.com/festival/archive/ascension-2021)
- [类型或身份资料](https://www.imdb.com/title/tt14505430/)

#### internal-039 神奇星球（1973，普通正片）

- 最终保留：`/Volumes/分类/动画片/奇幻星球.Fantastic.Planet.1973.480p.bdrip.x264.ac3-CHD.mkv` — 1.36 GiB
- 已删除：`/Volumes/分类/动画片/神奇星球.Fantastic.Planet.1973.BD.MiniSD-TLF.mkv` — 0.53 GiB
- 归档依据：IMDb Animation/Sci-Fi，Criterion确认为动画电影
- [类型或身份资料](https://www.imdb.com/title/tt0070544)
- [类型或身份资料](https://www.criterion.com/films/28636)

#### internal-040 稀有出口圣诞传说（2010，普通正片）

- 最终保留：`/Volumes/分类/恐怖/稀有出口.圣诞传说.Rare.Exports.A.Christmas.Tale.2010.双语字幕.HR-HDTV.AC3.1024X576.x264-人人影视制作.mkv` — 1.26 GiB
- 移出原位置：`/Volumes/分类/科幻·奇幻/稀有出口.圣诞传说.Rare.Exports.A.Christmas.Tale.2010.双语字幕.HR-HDTV.AC3.1024X576.x264-人人影视制作.mkv`
- 已删除：`/Volumes/分类/喜剧/稀有出口.圣诞传说.Rare.Exports.A.Christmas.Tale.2010.法国.DVD-HALFCD2.mp4` — 0.27 GiB
- 归档依据：奇幻恐怖题材，非普通喜剧
- [类型或身份资料](https://www.imdb.com/title/tt1401143/)

#### internal-041 突变第三型（1982，普通正片）

- 最终保留：`/Volumes/分类/怪兽/怪形.The.Thing.1982.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 7.27 GiB
- 已删除：`/Volumes/分类/科幻·奇幻/突变第三型.The.Thing.1982.BDRip.MiniSD-TLF.mkv` — 0.72 GiB
- 归档依据：IMDb明确Monster Horror/Body Horror，采用现有怪兽类
- [类型或身份资料](https://www.imdb.com/title/tt0084787/)

#### internal-042 第三个人（1949，普通正片）

- 最终保留：`/Volumes/分类/黑色电影/第三人.The.Third.Man.1949.双语字幕.HR-HDTV.AC3.768X576.x264-人人影视制作.mkv` — 1.61 GiB
- 移出原位置：`/Volumes/分类/惊悚·犯罪·动作/第三人.The.Third.Man.1949.双语字幕.HR-HDTV.AC3.768X576.x264-人人影视制作.mkv`
- 已删除：`/Volumes/分类/黑色电影/第三个人.The.Third.Man.1949.mkv` — 0.64 GiB
- 归档依据：IMDb明确Film Noir
- [类型或身份资料](https://www.imdb.com/title/tt0041959/)

#### internal-043 罗小黑战记2（2025，普通正片）

- 最终保留：`/Volumes/分类/华语世界/中国大陆/罗小黑战记2.The.Legend.of.Hei.Ⅱ.2025.1080p.WEB-DL.H264.AAC-OurTV.mp4` — 5.92 GiB
- 移出原位置：`/Volumes/分类/动画片/罗小黑战记2.The.Legend.of.Hei.Ⅱ.2025.1080p.WEB-DL.H264.AAC-OurTV.mp4`
- 已删除：`/Volumes/分类/华语世界/中国大陆/罗小黑战记2.The.Legend.of.Hei.2.2025.BluRay.1080p.x265.10bit.EAC3.iNT-TLF.mkv` — 2.56 GiB
- 归档依据：国产动画/奇幻/冒险，按华语世界既有地域优先规则集中到中国大陆
- [类型或身份资料](https://movie.douban.com/coming?sequence=)

#### internal-044 老井（1986，普通正片）

- 最终保留：`/Volumes/分类/华语世界/中国大陆/导演们/吴天明/老井.Old.Well.1986.Bluray.1080p.LPCM1.0.x265.10bit-DreamHD.mkv` — 11.82 GiB
- 移出原位置：`/Volumes/分类/华语世界/中国大陆/20世纪老电影/80/老井.Old.Well.1986.Bluray.1080p.LPCM1.0.x265.10bit-DreamHD.mkv`
- 已删除：`/Volumes/分类/华语世界/中国大陆/导演们/吴天明/老井.Old.Well.1986.WEB-DL.MiniHD-TLF.mkv` — 2.38 GiB
- 归档依据：IMDb中国大陆剧情/爱情、吴天明导演；资料记1987，原文件1986，本轮不改名
- [类型或身份资料](https://www.imdb.com/title/tt0091377/)

#### internal-045 肉体的恶魔（1986，普通正片）

- 最终保留：`/Volumes/分类/爱情/肉体的恶魔.Devil.in.the.Flesh.1986.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 9.13 GiB
- 已删除：`/Volumes/分类/CULT·实验/肉体的恶魔.Devil.In.The.Flesh.1986.DVDRip.XviD.mp4` — 0.45 GiB
- 归档依据：IMDb Drama/Romance，采用爱情主类
- [类型或身份资料](https://www.imdb.com/title/tt0090944/)

#### internal-046 芙蓉镇（1986，普通正片）

- 最终保留：`/Volumes/分类/华语世界/中国大陆/导演们/谢晋/芙蓉镇/芙蓉镇‎.Hibiscus.Town.1986.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 13.98 GiB
- 已删除：`/Volumes/分类/华语世界/中国大陆/导演们/谢晋/芙蓉镇.Hibiscus.Town.1986.BDRip.X264.iNT-TLF.mkv` — 2.99 GiB
- 归档依据：IMDb中国大陆剧情/历史/爱情，保留谢晋电影文件夹，不动旁边Extras
- [类型或身份资料](https://www.imdb.com/title/tt0087301/maindetails)

#### internal-047 芭贝特的盛宴（1987，普通正片）

- 最终保留：`/Volumes/分类/宗教/巴贝特之宴.Babette.s.Feast.1987.D5.MiniSD-TLF.mkv` — 0.67 GiB
- 移出原位置：`/Volumes/分类/故事/巴贝特之宴.Babette.s.Feast.1987.D5.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/故事/芭贝特的盛宴.Babette's.Feast.1987.BD.MiniSD-TLF.mkv` — 0.57 GiB
- 归档依据：IMDb剧情与宗教社区、牧师家庭为核心设定，采用宗教题材
- [类型或身份资料](https://www.imdb.com/title/tt0092603/)

#### internal-048 苏菲的抉择（1982，普通正片）

- 最终保留：`/Volumes/分类/爱情/苏菲的抉择.Sophies.Choice.1982.BluRay.1080p.x265.10bit.DTS-TLF.mkv` — 12.08 GiB
- 已删除：`/Volumes/分类/爱情/苏菲的抉择.Sophie's.Choice.1982.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 9.49 GiB
- 已删除：`/Volumes/分类/故事/苏菲的抉择.Sophie's.Choice.1982.US.DVD.X264.2Audio.AAC.HALFCD-NOWYS.mmla.mkv` — 0.61 GiB
- 归档依据：IMDb Drama/Romance，保留爱情主类
- [类型或身份资料](https://www.imdb.com/fr/title/tt0084707/)

#### internal-049 蓝色构图（1935，普通正片）

- 最终保留：`/Volumes/分类/动画片/动画的世纪·100部作品/Komposition.in.blau.Oskar.Fischinger.1935.avi` — 0.04 GiB
- 已删除：`/Volumes/分类/动画片/蓝色构图.Komposition.in.blau.Oskar.Fischinger,.1935.avi` — 0.04 GiB
- 归档依据：IMDb抽象定格动画短片，保留原动画选集子目录
- [类型或身份资料](https://www.imdb.com/title/tt0026580/)

#### internal-050 蝴蝶（2002，普通正片）

- 最终保留：`/Volumes/分类/青春·儿童/蝴蝶.Le.Papilion.2002.D9.2Audio.MiniSD-TLF.mkv` — 0.54 GiB
- 已删除：`/Volumes/分类/喜剧/蝴蝶.The.Butterfly.2002.flv` — 0.01 GiB
- 归档依据：IMDb冒险/喜剧/剧情，儿童与老人的山间旅程，保留青春儿童主题归属
- [类型或身份资料](https://www.imdb.com/title/tt0329485/)

#### internal-051 血与黑蕾丝（1964，普通正片）

- 最终保留：`/Volumes/分类/恐怖/血与黑蕾丝.Blood.And.Black.Lace.1964.D9.MiniSD-TLF.mkv` — 0.75 GiB
- 移出原位置：`/Volumes/分类/黑色电影/血与黑蕾丝.Blood.And.Black.Lace.1964.D9.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/惊悚·犯罪·动作/血与黑蕾丝.blood.and.black.lace.1964.d9.minisd-tlf.mkv` — 0.75 GiB
- 归档依据：意大利Giallo恐怖/悬疑犯罪片
- [类型或身份资料](https://www.imdb.com/video/vi414908697/)
- [类型或身份资料](https://www.imdb.com/title/tt0058567/plotsummary/)

#### internal-052 血光鬼影夺命刀（1973，普通正片）

- 最终保留：`/Volumes/分类/恐怖/威尼斯疑魂.Don't.Look.Now.1973.CC.BD.MiniSD-TLF.mkv` — 1.21 GiB
- 移出原位置：`/Volumes/分类/惊悚·犯罪·动作/威尼斯疑魂.Don't.Look.Now.1973.CC.BD.MiniSD-TLF.mkv`
- 已删除：`/Volumes/分类/恐怖/血光鬼影夺命刀.Dont.Look.Now.1973.BD.MiniSD-TLF.mkv` — 0.81 GiB
- 归档依据：IMDb明确Horror/心理恐怖
- [类型或身份资料](https://www.imdb.com/title/tt0069995/)

#### internal-053 袒露（2026，普通正片）

- 最终保留：`/Volumes/分类/故事/袒露.Truly.Naked.2026.1080p.中文字幕.mp4` — 8.76 GiB
- 移出原位置：`/Volumes/分类/情色/袒露.Truly.Naked.2026.1080p.中文字幕.mp4`
- 已删除：`/Volumes/分类/情色/袒露.Truly.Naked.2026.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 4.14 GiB
- 归档依据：IMDb Drama，成长与家庭关系题材，未被标为情色类型，采用故事类
- [类型或身份资料](https://www.imdb.com/title/tt8760666)

#### internal-054 进出口（2007，普通正片）

- 最终保留：`/Volumes/分类/故事/进出口.Import.Export.2007.BluRay.720p.x264.AC3.iNT-TLF.mkv` — 3.32 GiB
- 移出原位置：`/Volumes/分类/情色/进出口.Import.Export.2007.BluRay.720p.x264.AC3.iNT-TLF.mkv`
- 已删除：`/Volumes/分类/CULT·实验/进出口.Import.Export.2007.BD.MiniSD-TLF.mkv` — 1.05 GiB
- 归档依据：IMDb只有心理剧情，移民与劳工生活；剧情兜底，非情色主类
- [类型或身份资料](https://www.imdb.com/title/tt0459102/)
- [类型或身份资料](https://cineuropa.org/en/film/74057/)

#### internal-055 逍遥法外（2002，普通正片）

- 最终保留：`/Volumes/分类/传记·一段历史/逍遥法外.Catch.Me.If.You.Can.2002.DVD-RMVB.mkv` — 0.59 GiB
- 移出原位置：`/Volumes/分类/惊悚·犯罪·动作/逍遥法外.Catch.Me.If.You.Can.2002.DVD-RMVB.mkv`
- 已删除：`/Volumes/分类/传记·一段历史/逍遥法外.Catch.Me.If.You.Can.2002.DVDRip.2Audio.HALFCD-NOWYS.netshow.mkv` — 0.55 GiB
- 归档依据：IMDb Biography/Crime，采用已有传记类
- [类型或身份资料](https://www.imdb.com/title/tt0264464/)

#### internal-056 遗情（2009，普通正片）

- 最终保留：`/Volumes/分类/华语世界/东南亚/遗情.woman.on.fire.looks.for.water.2009.woo.ming.jin.dvdrip.x264.ac3.2ch.allzine.mkv` — 1.09 GiB
- 已删除：`/Volumes/分类/爱情/遗情.woman.on.fire.looks.for.water.2009.woo.ming.jin.dvdrip.x264.ac3.2ch.allzine.mkv` — 1.09 GiB
- 归档依据：马来西亚华语剧情；IMDb确认Woo Ming Jin与原文片名
- [类型或身份资料](https://www.imdb.com/title/tt1493296/)

#### internal-057 邮差总按两次铃（1946，普通正片）

- 最终保留：`/Volumes/分类/黑色电影/邮差总按两次铃.The.Postman.Always.Rings.Twice.1946.mkv` — 1.36 GiB
- 已删除：`/Volumes/分类/惊悚·犯罪·动作/邮差总按两次铃.The.Postman.Always.Rings.Twice.1946.BD.MiniSD-TLF.mkv` — 0.84 GiB
- 归档依据：IMDb明确Film Noir
- [类型或身份资料](https://www.imdb.com/title/tt0038854/)

#### internal-058 野花（2000，普通正片）

- 最终保留：`/Volumes/分类/短篇集/野花.wild.flowers.2000.d5.minisd-tlf.mkv` — 0.72 GiB
- 已删除：`/Volumes/分类/CULT·实验/野花.Kytice.2000.DVDRip.DivX.CZ-BiOGRa.mp4` — 0.31 GiB
- 归档依据：七个捷克民间故事组成的恐怖奇幻短篇集，保留形式分类
- [类型或身份资料](https://www.imdb.com/pt/title/tt0239102/)

#### internal-059 野蛮人入侵（2021，普通正片）

- 最终保留：`/Volumes/分类/华语世界/东南亚/野蛮人入侵.Barbarian.Invasion.2021.1080p.NF.WEB-DL.DDP5.1.x264.mkv` — 6.31 GiB
- 已删除：`/Volumes/分类/喜剧/野蛮人入侵.Barbarian.Invasion.2021.mkv` — 0.34 GiB
- 归档依据：马来西亚华语动作剧情；原喜剧位置不合适
- [类型或身份资料](https://www.imdb.com/title/tt14760842/)

#### internal-060 铁血战士杀戮之地（2025，普通正片）

- 最终保留：`/Volumes/分类/合集/铁血战士/铁血战士.杀戮之地.Predator.Badlands.2025.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 3.07 GiB
- 移出原位置：`/Volumes/分类/科幻·奇幻/铁血战士.杀戮之地.Predator.Badlands.2025.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 已删除：`/Volumes/分类/合集/铁血战士/铁血战士.杀戮之地.Predator.Badlands.2025.WEB-DL.MiniSD-TLF.mkv` — 0.53 GiB
- 归档依据：IMDb科幻/动作/冒险；保留现有铁血战士系列组织，将较好版本归入系列目录
- [类型或身份资料](https://www.imdb.com/title/tt31227572)

#### internal-061 雄狮少年2（2024，普通正片）

- 最终保留：`/Volumes/分类/华语世界/中国大陆/雄狮少年2.I.Am.What.I.Am.2.2024.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 4.14 GiB
- 移出原位置：`/Volumes/分类/动画片/雄狮少年2.I.Am.What.I.Am.2.2024.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 已删除：`/Volumes/分类/华语世界/中国大陆/雄狮少年2.I.Am.What.I.Am.2.2024.mp4` — 4.06 GiB
- 归档依据：豆瓣喜剧/动作/动画；按华语世界既有地域优先规则集中到中国大陆
- [类型或身份资料](https://movie.douban.com/subject/35883131/)
- [类型或身份资料](https://www.imdb.com/title/tt32439604/releaseinfo/)

#### internal-062 香魂女（1993，普通正片）

- 最终保留：`/Volumes/分类/华语世界/中国大陆/20世纪老电影/90/香魂女.Woman.Sesame.Oil.Maker.1993.rmvb` — 0.32 GiB
- 已删除：`/Volumes/分类/故事/香魂女.Women.from.the.Lake.of.Scented.Souls.1993.rmvb` — 0.32 GiB
- 归档依据：IMDb与发行方确认谢飞、中国普通话剧情；两种英文名指同片，保留已有年代目录
- [类型或身份资料](https://www.imdb.com/title/tt0108608/)
- [类型或身份资料](https://films.yilisoo.com/index.php/woman-sesame-oil-maker/)

#### internal-063 驯马手莫兰特（1980，普通正片）

- 最终保留：`/Volumes/分类/战争/驯马手莫兰特.Breaker.Morant.1980.CC.BD.HEVC.10bit.MiniHD-TLF.mkv` — 3.39 GiB
- 已删除：`/Volumes/分类/战争/烈血焚城.Breaker.Morant.1980.BDRip.X264.iNT-TLF.A165F64E.mkv` — 1.37 GiB
- 归档依据：Criterion确认布尔战争期间军法审判故事，保留战争题材
- [类型或身份资料](https://www.criterion.com/films/27766-breaker-morant)

#### internal-064 高中课堂（2008，普通正片）

- 最终保留：`/Volumes/分类/青春·儿童/墙壁之间.Entre.les.murs.2008.720p.BluRay.x264-CtrlHD.mkv` — 4.37 GiB
- 已删除：`/Volumes/分类/故事/高中课堂.Entre.Les.Murs.2008.FRENCH.DVDRip.XviD-ZANBiC.mkv` — 0.48 GiB
- 归档依据：IMDb剧情概要为巴黎青少年班级的一个学年，采用既有青春校园主题类
- [类型或身份资料](https://www.imdb.com/title/tt1068646/plotsummary/)

#### internal-065 魔光血影（1960，普通正片）

- 最终保留：`/Volumes/分类/恐怖/偷窥狂.Peeping.Tom.1960.CC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 10.81 GiB
- 移出原位置：`/Volumes/分类/惊悚·犯罪·动作/偷窥狂.Peeping.Tom.1960.CC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv`
- 已删除：`/Volumes/分类/惊悚·犯罪·动作/魔光血影.Peeping.Tom.1960.D9.MiniSD-TLF.mkv` — 0.73 GiB
- 归档依据：IMDb Horror/Thriller，Criterion亦确认心理恐怖
- [类型或身份资料](https://www.imdb.com/title/tt0054167/)
- [类型或身份资料](https://www.criterion.com/films/235-peeping-tom)

### /Volumes/导演们

#### internal-066 一诺千金（1996，普通正片）

- 最终保留：`/Volumes/导演们/达内兄弟/一诺千金/一诺千金.La.promesse.1996.CC.BDRip.X264.iNT-TLF.mkv` — 2.34 GiB
- 已删除：`/Volumes/导演们/达内兄弟/一诺千金/一诺千金.La.Promesse.1996.DVDRip.DivX-QiX.mkv` — 0.35 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-067 万尼亚在42街口（1994，普通正片）

- 最终保留：`/Volumes/导演们/路易·马勒/万尼亚在42街口.Vanya.On.42nd.Street.1994.CC.Bluray.x264-10bit.MiniHD-TLF.mkv` — 1.42 GiB
- 已删除：`/Volumes/导演们/路易·马勒/泛雅在42街.Vanya.on.42nd.Street.1994.rmvb` — 1.19 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-069 不伦之恋（1981，普通正片）

- 最终保留：`/Volumes/导演们/贝特朗·布里叶/不伦之恋.Beau.Pere.1981.D5.MiniSD-TLF.mkv` — 0.81 GiB
- 已删除：`/Volumes/导演们/贝特朗·布里叶/不伦之恋.Beau-pere.1981.DVDRip.DivX.Fr.mkv` — 0.46 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-070 与君别（1933，普通正片）

- 最终保留：`/Volumes/导演们/成濑巳喜男/与君别.Apart.from.You.1933.avi` — 1.22 GiB
- 已删除：`/Volumes/导演们/成濑巳喜男/除了你.Apart.from.You.1933.avi` — 1.22 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-071 东风（1970，普通正片）

- 最终保留：`/Volumes/导演们/让·吕克.戈达尔/东风.Le.Vent.D'est.1970.BD.EngSub.MiniSD-TLF.mkv` — 0.79 GiB
- 已删除：`/Volumes/导演们/让·吕克.戈达尔/东风.Groupe.Dziga.Vertov.-.Le.vent.d'est.1970.mkv` — 0.34 GiB
- 归档依据：导演库内保留较好版本及其现有位置
- [类型或身份资料](https://www.imdb.com/title/tt0065173/)

#### internal-072 乡愁（1983，普通正片）

- 最终保留：`/Volumes/导演们/安德烈·塔尔科夫斯基/乡愁.Nostalghia.1983.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 13.79 GiB
- 已删除：`/Volumes/导演们/安德烈·塔尔科夫斯基/乡愁.Nostalghia.1983.mkv` — 0.61 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-073 乱世儿女（1975，普通正片）

- 最终保留：`/Volumes/导演们/斯坦利·库布里克/巴里.林登.Barry.Lyndon.1975.CC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 15.46 GiB
- 已删除：`/Volumes/导演们/斯坦利·库布里克/乱世儿女.Barry.Lyndon.1975.HDTV.MiniSD-TLF.mkv` — 1.18 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-074 伸冤记（1956，普通正片）

- 最终保留：`/Volumes/导演们/阿尔弗雷德·希区柯克/伸冤记.The.Wrong.Man.1956.BD.MiniSD-TLF.mkv` — 2.18 GiB
- 已删除：`/Volumes/导演们/阿尔弗雷德·希区柯克/伸冤记.The.Wrong.Man.1956.HDTV.MiniSD-TLF.mkv` — 0.79 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-075 你知道你的楼梯很漂亮（1986，普通正片）

- 最终保留：`/Volumes/导演们/阿涅斯·瓦尔达/你知道.你的楼梯很漂亮.T.as.de.beaux.escaliers.tu.sais.1986.mkv` — 0.02 GiB
- 已删除：`/Volumes/导演们/伊莎贝尔·阿佳妮作品集[演员]/你知道.你的楼梯很漂亮.T.as.de.beaux.escaliers.tu.sais.1986.mkv` — 0.01 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-076 八月狂想曲（1991，普通正片）

- 最终保留：`/Volumes/导演们/黑泽明/留芳颂.Rhapsody.in.August.1991.mkv` — 0.88 GiB
- 已删除：`/Volumes/导演们/黑泽明/八月狂想曲.Rhapsody.in.August.1991.D5.MiniSD-TLF.mkv` — 0.67 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-077 冷酷祭典（1995，普通正片）

- 最终保留：`/Volumes/导演们/克劳德·夏布洛尔/冷酷祭典.La.Ceremonie.1995.BD.MiniSD-TLF(1).mkv` — 0.65 GiB
- 已删除：`/Volumes/导演们/克劳德·夏布洛尔/仪式.La.Ceremonie.1995.mkv` — 0.37 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-078 单车少年（2011，普通正片）

- 最终保留：`/Volumes/导演们/达内兄弟/单车少年.The.Kid.with.a.Bike.2011.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 4.40 GiB
- 已删除：`/Volumes/导演们/达内兄弟/单车少年.The.Kid.with.a.Bike.2011.rmvb` — 0.33 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-079 卢瓦河谷的木鞋匠（1956，普通正片）

- 最终保留：`/Volumes/导演们/雅克·德米/卢瓦河谷的木鞋匠.Le.Sabotier.du.Val.de.Loire.1956.D9.MiniSD-TLF.mkv` — 0.21 GiB
- 移出原位置：`/Volumes/导演们/阿涅斯·瓦尔达/南特的雅克德米/卢瓦河谷的木鞋匠.Le.Sabotier.du.Val.de.Loire.1956.D9.MiniSD-TLF.mkv`
- 已删除：`/Volumes/导演们/雅克·德米/卢瓦河谷的木鞋匠.Le.sabotier.du.Val.de.Loire.1956.mkv` — 0.09 GiB
- 归档依据：依据导演署名把较好版本归回对应导演/影片目录
- [类型或身份资料](https://cine-tamaris.fr/jacques-demy/le-sabotier-du-val-de-loire-1955/)

#### internal-080 坏血（1986，普通正片）

- 最终保留：`/Volumes/导演们/莱奥·卡拉克斯/坏血.Mauvais.Sang.1986.D9.MiniSD-TLF.mkv` — 0.84 GiB
- 已删除：`/Volumes/导演们/莱奥·卡拉克斯/坏血.Bad.Blood.1986.INTERNAL.DVDRip.XviD-RiZZ.CN.mkv` — 0.44 GiB
- 归档依据：导演库内保留较好版本及其现有位置
- [类型或身份资料](https://www.imdb.com/title/tt0091497/)

#### internal-081 天涯沦落两心知（1991，普通正片）

- 最终保留：`/Volumes/导演们/吉列姆/天涯沦落两心知.The.Fisher.King.1991.BD.MiniSD-TLF.mkv` — 1.02 GiB
- 已删除：`/Volumes/导演们/吉列姆/渔王.The.Fisher.King.1991.avi` — 0.93 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-082 奥菲斯（1950，普通正片）

- 最终保留：`/Volumes/导演们/让·谷克多/奥菲斯/俄耳甫斯.Orphée.1950.BD.CC.MiniSD-TLF.mkv` — 0.84 GiB
- 移出原位置：`/Volumes/导演们/让·谷克多/奥菲斯的遗嘱/俄耳甫斯.Orphée.1950.BD.CC.MiniSD-TLF.mkv`
- 已删除：`/Volumes/导演们/让·谷克多/奥菲斯/奥菲斯.Orphée.1950.D9.MiniSD-TLF.mkv` — 0.74 GiB
- 归档依据：依据导演署名把较好版本归回对应导演/影片目录
- [类型或身份资料](https://www.criterion.com/films/610-orpheus)

#### internal-083 对话（1974，普通正片）

- 最终保留：`/Volumes/导演们/弗朗西斯·福特·科波拉/对话.The.Conversation.1974.HDTV.MiniSD-TLF.mkv` — 0.72 GiB
- 已删除：`/Volumes/导演们/弗朗西斯·福特·科波拉/窃听大阴谋.The.Conversation.1974.DVD.2Auido.NOWYS.双面伊人.mkv` — 0.56 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-084 寻找小津（1985，普通正片）

- 最终保留：`/Volumes/导演们/维姆·文德斯/寻找小津.Tokyo.Ga.1985.REMASTERED.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 8.94 GiB
- 已删除：`/Volumes/导演们/小津安二郎/寻找小津.Tokyo-Ga.1985.mkv` — 0.36 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-085 影子大亨（1994，普通正片）

- 最终保留：`/Volumes/导演们/科恩兄弟/金钱帝国.The.Hudsucker.Proxy.1994.D9.MiniSD-TLF.mkv` — 0.69 GiB
- 已删除：`/Volumes/导演们/科恩兄弟/影子大亨.The.Hudsucker.Proxy.1994.美国.mkv` — 0.38 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-086 待嫁女儿心（1969，普通正片）

- 最终保留：`/Volumes/导演们/罗伯特·奥尔特曼/待嫁女儿心.That.Cold.Day.in.the.Park.1969.1080p.BluRay.H264.AAC-RARBG.mkv` — 2.04 GiB
- 已删除：`/Volumes/导演们/罗伯特·奥尔特曼/待嫁女儿心.That.Cold.Day.in.the.Park.1969.BD.MiniSD-TLF.mkv` — 0.83 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-087 我雇了一名合约杀手（1990，普通正片）

- 最终保留：`/Volumes/导演们/阿基·考里斯马基/我雇了一名合约杀手.I.Hired.a.Contract.Killer.1990.mkv` — 0.51 GiB
- 已删除：`/Volumes/导演们/阿基·考里斯马基/我聘请了职业杀手.I.Hired.a.Contract.Killer.1990.mkv` — 0.29 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-088 无耻混蛋（2009，普通正片）

- 最终保留：`/Volumes/导演们/昆汀·塔伦蒂诺/无耻混蛋.Inglourious.Basterds.2009.UHD.BluRay.2160p.2Audio.DTS-HD.MA.5.1.x265.10bit.HDR-ALT.mkv` — 26.53 GiB
- 已删除：`/Volumes/导演们/昆汀·塔伦蒂诺/无耻混蛋.Inglourious.Basterds.2009.rmvb` — 0.60 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-089 暗堡里的三恶人（1958，普通正片）

- 最终保留：`/Volumes/导演们/黑泽明/战国英豪.The.Hidden.Fortress.1958.D9.Min.mkv` — 0.88 GiB
- 已删除：`/Volumes/导演们/黑泽明/暗堡里的三恶人.The.Hidden.Fortress.1958.BD.MiniSD-TLF.mkv` — 0.84 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-090 月球旅行记彩色版（1902，普通正片）

- 最终保留：`/Volumes/导演们/乔治·梅里爱/月球旅行记.彩色版.A.Trip.to.the.Moon.1902.REMASTERED.Colorized.BluRay.1080p.x265.10bit.AC3.MultiAudio.iNT-TLF.mkv` — 0.93 GiB
- 已删除：`/Volumes/导演们/乔治·梅里爱/月球旅行记.A.Trip.to.the.Moon.1902.REMASTERED.Colorized.BluRay.1080p.x265.10bit.AC3.MultiAudio.iNT-TLF.mkv` — 0.93 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-091 柏蒂娜的苦泪（1972，普通正片）

- 最终保留：`/Volumes/导演们/法斯宾德/柏蒂娜的苦泪.The.Bitter.Tears.of.Petra.von.Kant.1972.CC.BD.MiniSD-TLF.mkv` — 1.16 GiB
- 已删除：`/Volumes/导演们/法斯宾德/柏蒂娜的苦泪.Die.bitteren.Tranen.der.Petra.von.Kant.1972.D9.2Audio.MiniSD-TLF.mkv` — 0.71 GiB
- 归档依据：导演库内保留较好版本及其现有位置
- [类型或身份资料](https://www.imdb.com/title/tt0068278/)

#### internal-092 满城风雨（1974，普通正片）

- 最终保留：`/Volumes/导演们/比利·怀尔德/满城风雨/满城风雨.The.Front.Page.1974.DVDRip.XviD-SAPHiRE.mkv` — 0.42 GiB
- 已删除：`/Volumes/导演们/比利·怀尔德/满城风雨/满城风雨.The.Front.Page.1974.DVDRip.XviD-SAPHiRE.mp4` — 0.41 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-093 爱在黎明破晓前（1995，普通正片）

- 最终保留：`/Volumes/导演们/理查德·林克莱特/爱在黎明破晓前.Before.Sunrise.1995.CC.BD.2Audio.MiniSD-TLF.mkv` — 0.80 GiB
- 已删除：`/Volumes/导演们/理查德·林克莱特/爱在黎明破晓前.Before.Sunrise.1995.mkv` — 0.45 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-094 玩火（1975，普通正片）

- 最终保留：`/Volumes/导演们/阿兰·罗布-格里耶/玩火/玩火.Le.Jeu.avec.le.feu.1975.D9.EngSub.MiniSD-TLF.mkv` — 1.68 GiB
- 已删除：`/Volumes/导演们/阿兰·罗布-格里耶/玩火.Le.Jeu.avec.le.feu.1975.mkv` — 1.45 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-095 简单挽歌（1990，普通正片）

- 最终保留：`/Volumes/导演们/亚历山大·索科洛夫/简单挽歌.A.Simple.Elegy.1990.avi` — 0.22 GiB
- 已删除：`/Volumes/导演们/亚历山大·索科洛夫/简单挽歌.Prostaya.elegiya.Elegia.Semplice.1990.avi` — 0.14 GiB
- 归档依据：导演库内保留较好版本及其现有位置
- [类型或身份资料](https://sokurov.spb.ru/isle_en/documentaries.html?num=59)

#### internal-096 赤裸裸（1993，普通正片）

- 最终保留：`/Volumes/导演们/迈克·李/赤裸裸.Naked.1993.D9.MiniSD-TLF.mkv` — 1.00 GiB
- 已删除：`/Volumes/导演们/迈克·李/赤裸裸.Naked.1993.BD.MiniSD-TLF.mkv` — 0.98 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-097 远方（2002，普通正片）

- 最终保留：`/Volumes/导演们/努里·比格·锡兰/远方.Distant.2002.1080p.BluRay.x265.10bit.DTS-SONYHD.mkv` — 8.52 GiB
- 已删除：`/Volumes/导演们/努里·比格·锡兰/乌扎克.Distant.2002.土耳其.XTM.DVD-HALFCD2.mkv` — 0.36 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-098 银色性男女（1993，普通正片）

- 最终保留：`/Volumes/导演们/罗伯特·奥尔特曼/银色.性.男女.Short.Cuts.1993.DVDrip.XviD.AC3.iNT-alaundo.mkv` — 2.05 GiB
- 已删除：`/Volumes/导演们/罗伯特·奥尔特曼/人生交叉点.Short.Cuts.1993.CC.BD.MiniSD-TLF.mkv` — 0.91 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-099 长夜漫漫路迢迢（1962，普通正片）

- 最终保留：`/Volumes/导演们/西德尼·吕美特/长夜漫漫路迢迢.Long.Days.Journey.Into.Night.1962.BD.MiniSD-TLF.mkv` — 1.29 GiB
- 移出原位置：`/Volumes/导演们/奥逊·威尔斯/长夜漫漫路迢迢.Long.Days.Journey.Into.Night.1962.BD.MiniSD-TLF.mkv`
- 已删除：`/Volumes/导演们/西德尼·吕美特/长夜漫漫路迢迢.Long.Days.Journey.into.Night.1962.mkv` — 0.66 GiB
- 归档依据：依据导演署名把较好版本归回对应导演/影片目录
- [类型或身份资料](https://www.festival-cannes.com/en/f/long-day-s-journey-into-night/)

#### internal-100 雪国列车（2013，普通正片）

- 最终保留：`/Volumes/导演们/奉俊昊/雪国列车.Snowpiercer.2013.2160p.UHD.Blu-ray.HEVC.Atmos.TrueHD7.1-DiY@HDHome.mkv` — 76.99 GiB
- 已删除：`/Volumes/导演们/奉俊昊/雪国列车.Snowpiercer.2013.BluRay.1080p.DTS-HDMA7.1.x265.10bit-DreamHD.mkv` — 12.16 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-101 面孔（1958，普通正片）

- 最终保留：`/Volumes/导演们/英格玛·伯格曼/面孔.The.Magician.1958.CC.BluRay.1080p.x265.10bit.AC3.iNT-TLF.mkv` — 8.21 GiB
- 已删除：`/Volumes/导演们/英格玛·伯格曼/魔术师.The.Magician.1958.720p.Bluray.X264-DIMENSION.mkv` — 4.37 GiB
- 归档依据：导演库内保留较好版本及其现有位置

#### internal-102 麦当劳桥上的未婚妻（1961，普通正片）

- 最终保留：`/Volumes/导演们/阿涅斯·瓦尔达/小心太阳眼镜/小心太阳眼镜.Les.fiances.du.pont.Mac.Donald.1961.mkv` — 0.03 GiB
- 已删除：`/Volumes/导演们/阿涅斯·瓦尔达/麦当劳桥上的未婚妻.Les.fiances.du.pont.Mac.Donald.1961.mkv` — 0.02 GiB
- 归档依据：导演库内保留较好版本及其现有位置

## 历史与核验范围

上轮跨库清理已删除86个视频，并把15个较好版本移回对应导演目录；详细历史见本仓库提交 `6b246fb` 及本地执行日志。此后用户继续手动整理，本轮重新扫描相对旧快照新增8个路径、缺失40个路径，这些不是本轮100项删除的执行结果。

当前按扩展名识别的媒体文件：分类 4,129 个，导演们 3,912 个；文件数包含短片、分集和光盘流，不等于电影部数。忽略隐藏目录、回收站和系统索引。无年份、译名完全不同或光盘结构中的同片仍可能漏检。原始粗筛不会直接变成删除清单。
