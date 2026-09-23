#!/usr/bin/env python3
"""
Movie filename cleanup helper for NAS movie folders.

Current rules:
- Work only on files under /Volumes/看 by default.
- Exclude /Volumes/看/剧.
- Do not infer movie titles from folder names.
- Use dot-separated names: 中文名.English.Title.年份.剩余部分.ext
- /Volumes/导演们 has separate rules:
  - 导演文件夹: /Volumes/导演们/<导演名>
  - 单一电影文件: video files directly inside a director folder.
  - 单一电影文件夹: subfolders inside a director folder; handle separately.
  - 单一电影文件夹 itself should be named with the Chinese movie title only.
  - If a folder is "(年份)中文名 外语名", use it as authoritative metadata:
    folder -> 中文名; files -> 中文名.外语名.年份.ext.
  - If a movie folder name is a clear Chinese movie title, files inside that
    folder may use it as the Chinese title. Category folders such as 默片,
    有声片, 短片, 花絮, 字幕, 资料, 合集 are not movie titles.
  - If one folder contains A/B, CD1/CD2, Disc1/Disc2, Part1/Part2, or episode
    markers, skip/ignore the whole group first; user plans to replace many
    split resources with complete sources later.
  - Extras/interviews/commentaries/trailers/featurettes/archive material are
    skipped. If clearly tied to one movie, they may later be moved into a
    花絮 subfolder under that movie folder.
  - Collections/series/short-film collections, especially old-film sets, keep
    their original names and are not normalized as individual feature films.
  - If a movie folder contains exactly one video file and no other real files,
    rename that video, move it to the director folder, then delete the empty
    movie folder.
  - When a file inside a movie folder glues the folder's Chinese title directly
    to a foreign title or CD marker, the folder name may be used as the split
    point, e.g. 侦探Les.espions -> 侦探.Les.espions.
  - If reliable lookup sources do not provide a Chinese title, keep the
    foreign/original title plus year instead of inventing a Chinese title.
  - Foreign titles can stay in their original language; do not translate them
    to English just for naming.
  - 巴斯特·基顿 short-film collection is ignored by user request.
  - 乔治·梅里爱 First Wizard of Cinema collection volumes are ignored.
  - 哈罗德·劳埃德 files may remove D1./D2. style disc prefixes first.
- Subtitle archives:
  - Extract only subtitle files from pure subtitle archives.
  - After successful extraction, rename subtitles to match the same-directory
    movie stem, using .chs/.cht/.eng when language can be inferred.
  - Delete the original subtitle archive only after its extracted subtitle
    files have been matched/planned safely.
- Generate preview CSVs and shell scripts; only execute shell scripts after review.

Source lookup priority for researched fixes:
1. Douban: search Chinese title first; if missing, search foreign title with
   dots replaced by spaces, optionally adding director.
2. TMDb: useful for multilingual titles, years, and media-library matching.
3. IMDb: verify original title, year, director, and same-title ambiguity.
4. Google/web search: combine Chinese title, foreign title, director, and year;
   use Letterboxd, Wikipedia, MUBI, BFI, Criterion, etc. as cross-checks.
5. Specialist sources: HKMDB for Hong Kong films, Taiwan film databases for
   Taiwanese films, Bangumi/TheTVDB for animation and series.

JSON workflow:
- Keep three long-lived JSON files in FilmNamingPlan:
  导演们文件快照.json as immutable backup, and 导演们_改名计划.json as the
  editable sync plan, and 导演们_多段资源清单.json as the replacement backlog.
- Multi-part/split/episode resources are tracked separately in
  导演们_多段资源清单.json and are not applied to NAS by apply-json.
- Send temporary analysis/validation output to /tmp.
- If reliable sources do not provide a Chinese title, do not invent one; keep
  the foreign/original title and year.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shlex
import shutil
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path


DEFAULT_ROOT = Path("/Volumes/看")
DIRECTORS_ROOT = Path("/Volumes/导演们")
DEFAULT_OUTPUT_DIR = Path(os.environ.get("MOVIE_TOOL_OUTPUT_DIR", "/Users/milou/Movies/FilmNamingPlan"))
DEFAULT_EXCLUDES = {"剧", "#recycle"}
VIDEO_EXTS = {".mkv", ".mp4", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg", ".mkv1", ".mov", ".m4v", ".wmv", ".flv", ".ts", ".webm"}
SUBTITLE_EXTS = {".srt", ".ass", ".ssa"}
SUBTITLE_ARCHIVE_EXTS = SUBTITLE_EXTS | {".sub", ".idx"}
SUPPORTED_EXTS = VIDEO_EXTS | SUBTITLE_EXTS
ARCHIVE_EXTS = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz", ".tbz2", ".sit", ".sitx", ".ace", ".cab", ".iso"}
ARCHIVE_PART_RE = re.compile(r"(?i)(part\d+|\.r\d{2,3}$|\.z\d{2,3}$|\.00\d$)")
YEAR_TOKEN_RE = re.compile(r"(?:^|[. _\-(])((?:18|19|20)\d{2})(?:$|[. _\-)])")
DOT_YEAR_RE = re.compile(r"\.(?:18|19|20)\d{2}(?:\.|$)")
FOREIGN_CHAR_RE = re.compile(r"[A-Za-z\u3040-\u30ff\u0400-\u04ff\u0370-\u03ff\u0590-\u05ff\u0600-\u06ff\u0900-\u097f\u0e00-\u0e7f]")
CD_PART_RE = re.compile(r"(?i)(^|[._ -])(cd|disc|disk|part|pt)[._ -]*\d+(?=$|[._ -])")
AB_PART_RE = re.compile(r"(?i)(^|[._ -])(?:a|b)(?=$|[._ -])")
EPISODE_RE = re.compile(r"(?i)(^|[._ -])s\d{1,2}e\d{1,2}(?=$|[._ -])")
SKIP_DIR_NAMES = {"花絮", "Featurettes", "featurettes", "extras", "Extras", "Supplements", "supplements"}
CATEGORY_DIR_NAMES = {"默片", "有声片", "短片", "花絮", "字幕", "字幕及备份", "资料", "合集", "电视剧"}
DIRECTOR_SINGLE_IGNORE_DIRECTORS = {"巴斯特·基顿", "乔治·梅里爱"}
REVIEW_EXTRA_RE = re.compile(
    r"(?i)(花絮|访谈|采访|专访|评论|comment|commentary|making|behind|"
    r"featurette|trailer|剧照|修复|纪录|documentary|portrait|boxes|"
    r"visions|梦魇人生|美国梦|资料|影人|Pasolini|Tarkovsky|Kubrick|"
    r"Lucky\.Malcolm|盒子|视角|岛\.Andrei\.Tarkovsky|导评|简介|侧拍|"
    r"预言|馈赠|善与恶|回归|遗忘的风景|导演自述|科林·麦凯布|"
    r"贝尔纳多·贝托鲁奇|Scorsese|斯科塞斯|讨论自己的艺术|"
    r"The\.Last\.Movie|性、爱、欲|Private\.Collections|Sample|"
    r"吟游\.帕拉杰诺夫|吟游\.莱蒙托夫|I\.Wish\.You\.Love|Haze|"
    r"Kaori\.Fuji|原一男)"
)
REVIEW_COLLECTION_RE = re.compile(
    r"(?i)(合集|作品集|短片集|电影史|三部曲|六个道德故事|坚忍的航程|"
    r"里约之声|音乐现场|动画作品集|Collected\.Shorts|Histoire|"
    r"特伦斯·戴维斯三部曲|Terayama-Shuji\.Experimental-Image-World|"
    r"燃火的时刻|十诫|巴斯特·基顿|乔治·梅里爱)"
)
REVIEW_FOREIGN_OK_RE = re.compile(
    r"(?i)(322\.1969|Thanksgiving\.Prayer\.1991|Mannen\.fra|"
    r"The\.Prowler\.1951|Junior\.Bonner\.1972|Komedie\.om\.Geld|"
    r"Nuts\.In\.May|Le\.Roman|Le\.Capitaine|Dedictvi|Slameny|Stin|"
    r"Egor\.i\.Nastya|Isabelle\.aux\.Dombes)"
)
DIRECTOR_SINGLE_SKIP_RE = re.compile(
    r"(?i)(bonus|featurette|featurettes|supplement|supplements|extra|extras|"
    r"making[._ -]?of|behind[._ -]?the[._ -]?scenes|interview|trailer|teaser|"
    r"mini[._ -]?biography|family[._ -]?films|chronological[._ -]?table|"
    r"radio[._ -]?audio|memento|scoring[._ -]?for[._ -]?comedy|remembering|"
    r"from[._ -]?the[._ -]?safe|greenacres|kepp.?em[._ -]?rollin|"
    r"花絮|访谈|采访|预告|制作特辑|纪录片|documentary|人物|关于|眼中的|介绍|纪念)"
)


# Matches already researched during this cleanup pass.
# confidence:
#   高: executed safely in the last run when selected.
#   中: candidate exists, but should be reviewed before execution.
MATCHES = [
    ("WHAT.DOES.THAT.NATURE.SAY.TO.YOU", "大自然对你说了什么", "What.Does.That.Nature.Say.To.You", "2025", "高", "https://movie.douban.com/subject/36961962/", "豆瓣匹配"),
    ("中邪", "中邪", "The.Possessed", "2016", "高", "https://movie.douban.com/subject/26820833/", "豆瓣又名含 The Possessed / Exorcism"),
    ("宝岛.2025", "宝岛", "Heros.Island", "2025", "高", "https://movie.douban.com/subject/36883109/", "豆瓣又名 Hero's Island"),
    ("弗兰茨", "弗兰兹", "Frantz", "2016", "高", "https://movie.douban.com/subject/26616719/", "豆瓣匹配；建议中文名用豆瓣“弗兰兹”"),
    ("时间戳", "时间戳", "Timestamp", "2025", "高", "https://movie.douban.com/subject/36779042/", "豆瓣又名 Timestamp"),
    ("母亲的宝贝", "母亲的宝贝", "Mothers.Baby", "2025", "高", "https://movie.douban.com/subject/36159758/", "豆瓣匹配"),
    ("孤儿", "孤儿", "The.Orphan", "2025", "高", "https://movie.douban.com/subject/36243544/", "用户确认豆瓣条目"),
    ("母鸡", "母鸡", "Hen", "2025", "高", "https://movie.douban.com/subject/35182657/", "用户确认豆瓣条目"),
    ("破石之刃", "破石之刃", "Cutting.Through.Rocks", "2025", "高", "https://movie.douban.com/subject/36921211/", "用户确认豆瓣条目"),
    ("东京出租车", "东京出租车", "Tokyo.Taxi", "2025", "高", "https://movie.douban.com/subject/37213104/", "用户确认 2025 版"),
    ("父影之下", "父影之下", "My.Fathers.Shadow", "2025", "高", "https://movie.douban.com/subject/37231952/", "用户确认豆瓣条目"),
    ("The.Nothing.Factory", "破败工厂", "The.Nothing.Factory", "2017", "高", "https://movie.douban.com/awards/cannes/70/nominees", "豆瓣戛纳片单含破败工厂 A Fabrica de Nada；英文按文件名"),
    ("卢丹的恶魔", "卢丹的恶魔", "The.Devils", "1971", "高", "https://movie.douban.com/subject/1823255/", "豆瓣匹配"),
    ("After.Hours", "下班后", "After.Hours", "1985", "高", "https://movie.douban.com/subject/1303531/", "豆瓣匹配；BONUS 作为剩余部分保留"),
    ("Beyond.the.Hills", "山之外", "Beyond.the.Hills", "2012", "高", "https://movie.douban.com/subject/10521893/", "豆瓣匹配"),
    ("拥挤的房间", "拥挤的房间", "The.Crowded.Room", "2023", "高", "https://movie.douban.com/subject/35426974/", "豆瓣匹配"),
    ("Amintiri.Din.Epoca.De.Aur", "黄金时代的故事", "Amintiri.Din.Epoca.De.Aur", "2009", "高", "https://movie.douban.com/subject/3692290/", "豆瓣/戛纳片单匹配"),
    ("木星之卫", "木星之卫", "Jupiters.Moon", "2017", "高", "https://movie.douban.com/awards/cannes/70/nominees?k=a", "豆瓣戛纳片单匹配"),
    ("利莫诺夫", "利莫诺夫.埃迪的歌谣", "Limonov.The.Ballad", "2024", "高", "https://movie.douban.com/subject/24888580/", "豆瓣匹配"),
    ("门徒", "门徒", "The.Student", "2016", "高", "https://movie.douban.com/subject/26693233/", "豆瓣匹配"),
    ("燃烧", "燃烧", "Burning", "2018", "高", "https://movie.douban.com/subject/26842702/", "豆瓣匹配"),
    ("Tom.at.the.Farm", "汤姆的农场旅行", "Tom.at.the.Farm", "2013", "高", "https://movie.douban.com/subject/20276230/", "豆瓣匹配"),
    ("A.Gentle.Creature.2017", "温柔女子", "A.Gentle.Creature", "2017", "高", "https://movie.douban.com/subject/26683283/", "豆瓣匹配"),
    ("快乐结局", "快乐结局", "Happy.End", "2017", "高", "https://movie.douban.com/subject/26698601/", "豆瓣匹配"),
    ("Lemminge", "旅鼠", "Lemminge", "1979", "高", "https://movie.douban.com/subject/3131244/", "豆瓣匹配"),
    ("Amour.2012", "爱", "Amour", "2012", "高", "https://movie.douban.com/subject/4798707/", "豆瓣匹配"),
    ("Love.2012", "爱", "Amour", "2012", "高", "https://movie.douban.com/subject/4798707/", "豆瓣又名 Love，规范为 Amour"),
    ("Le.meraviglie", "奇迹", "Le.meraviglie", "2014", "高", "https://movie.douban.com/subject/25733490/", "豆瓣匹配"),
    ("浮士德", "浮士德", "Faust", "2011", "高", "https://movie.douban.com/subject/3731625/", "用户确认豆瓣条目"),
    ("The.Strange.Case.of.Angelica", "安吉里卡奇遇", "The.Strange.Case.of.Angelica", "2010", "高", "https://movie.douban.com/subject/3287715/", "豆瓣匹配"),
    ("流浪的迪潘", "流浪的迪潘", "Dheepan", "2015", "高", "https://movie.douban.com/subject/26295860/", "豆瓣匹配"),
    ("Court.2014", "法庭", "Court", "2014", "高", "https://movie.douban.com/subject/25934374/", "豆瓣匹配"),
    ("狐步舞", "狐步舞", "Foxtrot", "2017", "高", "https://movie.douban.com/subject/26756258/", "豆瓣匹配"),
    ("离开的女人.Ang.Babaeng.Humayo", "离开的女人", "Ang.Babaeng.Humayo", "2016", "高", "https://movie.douban.com/subject/26844993/", "豆瓣匹配"),
    ("顿巴斯", "顿巴斯", "Donbass", "2018", "高", "https://movie.douban.com/subject/search?search_text=%E9%A1%BF%E5%B7%B4%E6%96%AF%202018", "用户确认 2018 剧情片"),
    ("4等", "4等", "4th.Place", "2015", "高", "https://movie.douban.com/subject/26303204/", "豆瓣匹配"),
    ("我们的世界", "我们的世界", "The.World.of.Us", "2016", "高", "https://movie.douban.com/subject/26616436/", "豆瓣匹配"),
    ("对不起宝贝", "对不起宝贝", "Sorry.Baby", "2025", "高", "https://movie.douban.com/subject/36809707/", "豆瓣匹配"),
    ("摇尾狗", "摇尾狗", "Wag.the.Dog", "1997", "高", "https://movie.douban.com/subject/1293985/", "豆瓣匹配"),
    ("牡丹花下", "牡丹花下", "The.Beguiled", "2017", "高", "https://movie.douban.com/subject/26761325/", "用户确认 2017 版"),
    ("痴男怨女", "痴男怨女", "The.Man.Who.Loved.Women", "1977", "高", "https://movie.douban.com/subject/1292964/", "用户确认豆瓣条目"),
    ("黎明的一切", "黎明的一切", "All.the.Long.Nights", "2024", "高", "https://movie.douban.com/subject/36135198/", "豆瓣匹配"),
    ("Divine.Intervention", "神的介入", "Divine.Intervention", "2002", "中", "https://movie.douban.com/subject/search?search_text=Divine%20Intervention", "需复核豆瓣条目"),
    ("中英街1号", "中英街1号", "No.1.Chung.Ying.Street", "2018", "中", "https://movie.douban.com/subject/search?search_text=No.1%20Chung%20Ying%20Street", "需复核豆瓣条目"),
    ("幸福在西方", "幸福在西方", "Occident", "2002", "中", "https://movie.douban.com/subject/search?search_text=Occident", "需复核豆瓣条目"),
    ("末路狂奔2", "末路狂奔2", "Pusher.II", "2004", "中", "https://embed.letterboxd.com/film/pusher-ii/", "未找到豆瓣直达结果；外部资料匹配"),
    ("老无所惧", "老无所惧", "Too.Old.to.Die.Young", "2019", "中", "https://www.meijuq.com/tv/5862", "未找到豆瓣直达结果；外部资料匹配"),
    ("血流不止", "血流不止", "Bleeder", "1999", "中", "https://movie.douban.com/subject/search?search_text=Bleeder", "需复核豆瓣条目"),
    ("马蒂亚斯与马克西姆", "马蒂亚斯与马克西姆", "Matthias.and.Maxime", "2019", "中", "https://movie.douban.com/subject/search?search_text=Matthias%20and%20Maxime", "需复核豆瓣条目"),
    ("Майдан.Maidan", "中央广场", "Maidan", "2014", "中", "https://movie.douban.com/subject/search?search_text=Maidan", "需复核豆瓣条目"),
    ("毁灭的自然史", "毁灭的自然史", "The.Natural.History.of.Destruction", "2022", "中", "https://www.6huo.com/movie/56142", "外部资料匹配"),
    ("Les.Ponts.de.Sarajevo", "萨拉热窝的桥", "Les.Ponts.de.Sarajevo", "2014", "中", "https://movie.douban.com/subject/search?search_text=Les%20Ponts%20de%20Sarajevo", "需复核豆瓣条目"),
    ("Die.Rebellion", "反叛", "Die.Rebellion", "1993", "中", "https://movie.douban.com/subject/search?search_text=Die%20Rebellion%201993", "需复核豆瓣条目"),
    ("The.Castle.1997", "城堡", "The.Castle", "1997", "中", "https://movie.douban.com/subject/search?search_text=The%20Castle%201997%20Haneke", "需复核豆瓣条目"),
    ("Crazy.Horse.2011", "疯马歌舞秀", "Crazy.Horse", "2011", "中", "https://www.xb1.com/content/1822356", "外部资料匹配；豆瓣搜索结果有同名 1999，需复核"),
    ("两扇门", "两扇门", "Two.Doors", "2011", "中", "https://movie.douban.com/subject/search?search_text=%E4%B8%A4%E6%89%87%E9%97%A8%20Two%20Doors", "需复核豆瓣条目"),
    ("花葬", "花葬", "Revivre", "2014", "中", "https://movie.douban.com/subject/search?search_text=%E8%8A%B1%E8%91%AC%20Revivre", "需复核豆瓣条目"),
    ("Dooman.River", "豆满江", "Dooman.River", "2010", "中", "https://movie.douban.com/subject/search?search_text=Dooman%20River", "需复核豆瓣条目"),
    ("酒神小姐", "酒神小姐", "The.Bacchus.Lady", "2016", "中", "https://dianying.fm/movie/the-bacchus-lady", "外部资料匹配"),
    ("Arirang.2011", "阿里郎", "Arirang", "2011", "中", "https://movie.douban.com/subject/search?search_text=Arirang%202011", "需复核豆瓣条目"),
]

AMBIGUOUS = {
    "一夜无眠": "用户已指定删除",
    "父影之下": "搜索结果不可靠，未找到唯一豆瓣条目",
    "S01E04": "文件名本身只有集数，没有片名信息，不能只按文件本身匹配",
    "[zmk.pw][baidu-en-zh].123": "文件名本身没有片名信息，不能只按文件本身匹配",
    "#3：视频论文": "这是花絮/视频论文，不是正片条目，暂不按电影格式改",
}


def iter_supported_files(root: Path, excludes: set[str]):
    excluded_paths = {root / name for name in excludes if name}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(excluded in path.parents or path == excluded for excluded in excluded_paths):
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.suffix.lower() in SUPPORTED_EXTS:
            yield path


def has_chinese(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def has_latin(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]", text))


def check_status(path: Path) -> str:
    stem = path.stem
    missing = []
    if not has_chinese(stem):
        missing.append("文件名缺中文名")
    if not has_latin(stem):
        missing.append("文件名缺英文名")
    if not re.search(r"(?:19|20)\d{2}", stem):
        missing.append("文件名缺年份")
    return "；".join(missing) if missing else "文件名已有中文/英文/年份"


def match_name(name: str) -> dict:
    stem = Path(name).stem
    for needle, cn, en, year, confidence, source, note in MATCHES:
        if re.match(r"^\[?" + re.escape(needle) + r"($|[._\]-])", stem, flags=re.I):
            return {
                "匹配中文名": cn,
                "匹配英文名": en,
                "匹配年份": year,
                "置信度": confidence,
                "来源": source,
                "备注": note,
                "状态": "可生成改名预览",
            }
    for needle, note in AMBIGUOUS.items():
        if needle in name:
            return {
                "匹配中文名": "",
                "匹配英文名": "",
                "匹配年份": "",
                "置信度": "不建议自动改",
                "来源": "",
                "备注": note,
                "状态": "暂不建议改名",
            }
    return {
        "匹配中文名": "",
        "匹配英文名": "",
        "匹配年份": "",
        "置信度": "未匹配",
        "来源": "",
        "备注": "本轮搜索未找到可靠结果",
        "状态": "暂不建议改名",
    }


def cleanup_rest(rest: str, year: str) -> str:
    rest = rest.strip("._- ")
    rest = re.sub(r"^" + re.escape(year) + r"($|[._-])", "", rest, count=1)
    rest = re.sub(r"(^|[._-])" + re.escape(year) + r"($|[._-])", ".", rest, count=1)
    rest = rest.strip("._- ")
    rest = rest.replace("_婚姻与健美字幕组", ".婚姻与健美字幕组")
    return re.sub(r"\.{2,}", ".", rest).strip("._- ")


def cn_variants(cn: str) -> list[str]:
    variants = {cn, cn.replace("兹", "茨")}
    return sorted(variants, key=len, reverse=True)


def suggested_name(old_name: str, cn: str, en: str, year: str) -> str:
    if not cn or not en or not year:
        return ""
    stem, ext = os.path.splitext(old_name)
    rest = ""

    match = re.search(re.escape(en), stem, flags=re.I)
    if match:
        rest = stem[match.end():]
    else:
        known_english_variants = [
            "WHAT.DOES.THAT.NATURE.SAY.TO.YOU",
            "The.Crowded.Room",
            "Too.Old.to.Die.Young",
            "Ang.Babaeng.Humayo",
            "Tom.at.the.Farm",
            "Le.meraviglie",
            "The.Strange.Case.of.Angelica",
            "Beyond.the.Hills",
            "After.Hours",
            "A.Gentle.Creature",
            "Les.Ponts.de.Sarajevo",
            "Die.Rebellion",
            "The.Castle",
            "Lemminge",
            "Amour",
            "Love",
            "Court",
            "Crazy.Horse",
            "Dooman.River",
            "Arirang",
        ]
        for variant in known_english_variants:
            found = re.search(re.escape(variant), stem, flags=re.I)
            if found:
                rest = stem[found.end():]
                break
        else:
            for variant in cn_variants(cn):
                if stem == variant:
                    rest = ""
                    break
                if stem.startswith(variant + ".") or stem.startswith(variant + "_") or stem.startswith(variant + "-"):
                    rest = stem[len(variant):]
                    break
            else:
                if not has_latin(stem):
                    year_match = re.search(re.escape(year), stem)
                    rest = stem[year_match.end():] if year_match else ""
                else:
                    rest = stem

    rest = cleanup_rest(rest, year)
    parts = [cn, en, year]
    if rest:
        parts.append(rest)
    return re.sub(r"\.{2,}", ".", ".".join(parts) + ext)


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def out_path(name: str) -> Path:
    return DEFAULT_OUTPUT_DIR / name


def cmd_scan(args) -> None:
    files = [str(p) for p in iter_supported_files(args.root, args.exclude)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(files) + ("\n" if files else ""), encoding="utf-8")
    print(f"wrote={args.output}")
    print(f"count={len(files)}")


def cmd_check(args) -> None:
    rows = []
    counts = Counter()
    for path in iter_supported_files(args.root, args.exclude):
        status = check_status(path)
        counts[status] += 1
        rows.append({"路径": str(path), "文件名": path.name, "检查结果": status})
    write_csv(args.output, rows, ["路径", "文件名", "检查结果"])
    print(f"wrote={args.output}")
    for key, value in counts.most_common():
        print(value, key)


def cmd_preview(args) -> None:
    rows = []
    for path in iter_supported_files(args.root, args.exclude):
        status = check_status(path)
        if status == "文件名已有中文/英文/年份":
            continue
        item = match_name(path.name)
        item["路径"] = str(path)
        item["当前文件名"] = path.name
        item["检查结果"] = status
        item["建议新文件名"] = suggested_name(path.name, item["匹配中文名"], item["匹配英文名"], item["匹配年份"])
        rows.append(item)
    fields = [
        "路径", "当前文件名", "检查结果", "匹配中文名", "匹配英文名", "匹配年份",
        "建议新文件名", "置信度", "状态", "来源", "备注",
    ]
    write_csv(args.output, rows, fields)
    print(f"wrote={args.output}")
    print(Counter(row["状态"] for row in rows))
    print(Counter(row["置信度"] for row in rows))


def cmd_make_script(args) -> None:
    rows = list(csv.DictReader(args.preview.open(encoding="utf-8")))
    selected = []
    conflicts = []
    seen = {}
    for row in rows:
        if row["置信度"] != args.confidence:
            continue
        if row["状态"] != "可生成改名预览" or not row["建议新文件名"]:
            continue
        src = Path(row["路径"])
        dst = src.with_name(row["建议新文件名"])
        if src == dst:
            continue
        if dst.exists():
            conflicts.append((str(src), str(dst), "目标已存在"))
        if str(dst) in seen:
            conflicts.append((str(src), str(dst), "多个源指向同一目标"))
        seen[str(dst)] = str(src)
        selected.append((src, dst))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        handle.write("#!/bin/sh\nset -eu\n\n")
        for src, dst in selected:
            handle.write("mv -n -- ")
            handle.write(shlex.quote(str(src)))
            handle.write(" ")
            handle.write(shlex.quote(str(dst)))
            handle.write("\n")
    os.chmod(args.output, 0o755)
    print(f"wrote={args.output}")
    print(f"selected={len(selected)}")
    print(f"conflicts={len(conflicts)}")
    for conflict in conflicts[:20]:
        print(conflict)


def cmd_summary(args) -> None:
    preview_rows = list(csv.DictReader(args.preview.open(encoding="utf-8")))
    by_path = {row["路径"]: row for row in preview_rows}
    rows = []
    for path in iter_supported_files(args.root, args.exclude):
        status = check_status(path)
        if status == "文件名已有中文/英文/年份":
            continue
        source = by_path.get(str(path), {})
        group = "其他"
        if source.get("置信度") == "中" and source.get("状态") == "可生成改名预览":
            group = "中置信度待复核"
        elif source.get("状态") == "暂不建议改名":
            group = "不建议自动改"
        rows.append({
            "分组": group,
            "路径": str(path),
            "文件名": path.name,
            "检查结果": status,
            "匹配中文名": source.get("匹配中文名", ""),
            "匹配英文名": source.get("匹配英文名", ""),
            "匹配年份": source.get("匹配年份", ""),
            "建议新文件名": source.get("建议新文件名", ""),
            "置信度": source.get("置信度", ""),
            "来源": source.get("来源", ""),
            "备注": source.get("备注", ""),
        })
    fields = [
        "分组", "路径", "文件名", "检查结果", "匹配中文名", "匹配英文名",
        "匹配年份", "建议新文件名", "置信度", "来源", "备注",
    ]
    write_csv(args.output, rows, fields)
    print(f"wrote={args.output}")
    print(Counter(row["分组"] for row in rows))


def iter_director_single_video_files(root: Path):
    """Yield video files directly under /Volumes/导演们/<导演名>."""
    for director in sorted((p for p in root.iterdir() if p.is_dir()), key=lambda p: p.name):
        if director.name in SKIP_DIR_NAMES:
            continue
        for path in sorted(director.iterdir(), key=lambda p: p.name):
            if path.is_file() and path.suffix.lower() in VIDEO_EXTS:
                yield director, path


def cmd_director_single_check(args) -> None:
    rows = []
    skipped = []
    ignored = []
    for director, path in iter_director_single_video_files(args.root):
        if director.name in set(args.ignore_director or []):
            ignored.append({
                "导演": director.name,
                "路径": str(path),
                "文件名": path.name,
                "原因": "用户指定忽略",
            })
            continue
        if DIRECTOR_SINGLE_SKIP_RE.search(path.name):
            skipped.append({
                "导演": director.name,
                "路径": str(path),
                "文件名": path.name,
                "原因": "花絮/附加内容/纪录介绍类关键词",
            })
            continue
        rows.append({
            "导演": director.name,
            "路径": str(path),
            "文件名": path.name,
            "检查结果": check_status(path).replace("文件名", "").replace("；", "、") or "合格",
        })

    bad = [row for row in rows if row["检查结果"] != "已有中文/英文/年份"]
    for row in rows:
        if row["检查结果"] == "已有中文/英文/年份":
            row["检查结果"] = "合格"
    bad = [row for row in rows if row["检查结果"] != "合格"]

    write_csv(args.output, rows, ["导演", "路径", "文件名", "检查结果"])
    write_csv(args.bad_output, bad, ["导演", "路径", "文件名", "检查结果"])
    write_csv(args.skip_output, skipped, ["导演", "路径", "文件名", "原因"])
    write_csv(args.ignore_output, ignored, ["导演", "路径", "文件名", "原因"])
    print(f"wrote={args.output}")
    print(f"counted={len(rows)} skipped={len(skipped)} ignored={len(ignored)} bad={len(bad)}")
    print(Counter(row["检查结果"] for row in rows))


def cmd_harold_strip_d_prefix(args) -> None:
    root = args.root / "哈罗德·劳埃德"
    selected = []
    conflicts = []
    for path in sorted(root.iterdir(), key=lambda p: p.name):
        if not path.is_file():
            continue
        match = re.match(r"^(D\d+)\.(.+)$", path.name, flags=re.I)
        if not match:
            continue
        dst = path.with_name(match.group(2))
        if dst.exists():
            conflicts.append({"当前路径": str(path), "建议路径": str(dst), "冲突": "目标已存在"})
            continue
        selected.append((path, dst, match.group(1)))

    rows = [
        {
            "当前路径": str(src),
            "建议路径": str(dst),
            "当前文件名": src.name,
            "建议文件名": dst.name,
            "移除前缀": prefix,
        }
        for src, dst, prefix in selected
    ]
    write_csv(args.output, rows, ["当前路径", "建议路径", "当前文件名", "建议文件名", "移除前缀"])
    if conflicts:
        write_csv(args.conflicts_output, conflicts, ["当前路径", "建议路径", "冲突"])

    args.script.parent.mkdir(parents=True, exist_ok=True)
    with args.script.open("w", encoding="utf-8") as handle:
        handle.write("#!/bin/zsh\nset -euo pipefail\n")
        for src, dst, _prefix in selected:
            handle.write("mv -- ")
            handle.write(shlex.quote(str(src)))
            handle.write(" ")
            handle.write(shlex.quote(str(dst)))
            handle.write("\n")
    os.chmod(args.script, 0o755)
    print(f"wrote={args.output}")
    print(f"script={args.script}")
    print(f"selected={len(selected)} conflicts={len(conflicts)}")


def cmd_director_folder_structure(args) -> None:
    episode_re = re.compile(r"(?i)(s\d{1,2}e\d{1,2}|第\d+[集话]|ep\.?\d{1,3}|episode)")
    part_re = re.compile(r"(?i)(cd\s*\d+|disc\s*\d+|part\s*\d+|\b[ab]\b|上|下)")

    def direct_counts(folder: Path):
        videos, subs, others, extras = [], [], [], []
        for path in sorted(folder.iterdir(), key=lambda p: p.name):
            if not path.is_file():
                continue
            if path.suffix.lower() in VIDEO_EXTS:
                (extras if DIRECTOR_SINGLE_SKIP_RE.search(path.name) else videos).append(path)
            elif path.suffix.lower() in SUBTITLE_EXTS:
                subs.append(path)
            else:
                others.append(path)
        return videos, subs, others, extras

    def folder_kind(videos, subs, extras):
        names = " ".join(path.name for path in videos + subs + extras)
        if episode_re.search(names):
            return "疑似电视剧/分集"
        if len(videos) == 0 and len(extras) > 0:
            return "只有花絮/资料视频"
        if len(videos) == 0:
            return "无正片视频"
        if len(videos) == 1 and len(subs) == 0:
            return "单视频文件夹"
        if len(videos) == 1 and len(subs) == 1:
            return "单视频+单字幕文件夹"
        if len(videos) == 1 and len(subs) > 1:
            return "单视频+多字幕文件夹"
        if len(videos) > 1 and part_re.search(names):
            return "多段电影文件夹"
        if len(videos) > 1:
            return "多视频文件夹"
        return "其他"

    rows = []
    for director in sorted((p for p in args.root.iterdir() if p.is_dir()), key=lambda p: p.name):
        if director.name == "#recycle":
            continue
        for folder in sorted((p for p in director.iterdir() if p.is_dir()), key=lambda p: p.name):
            if folder.name == "#recycle":
                continue
            videos, subs, others, extras = direct_counts(folder)
            rows.append({
                "分类": folder_kind(videos, subs, extras),
                "导演": director.name,
                "电影文件夹": str(folder),
                "文件夹名": folder.name,
                "正片视频数": len(videos),
                "字幕数": len(subs),
                "花絮视频数": len(extras),
                "其他文件数": len(others),
                "视频示例": " | ".join(path.name for path in videos[:6]),
                "字幕示例": " | ".join(path.name for path in subs[:4]),
                "花絮示例": " | ".join(path.name for path in extras[:4]),
            })

    fields = [
        "分类", "导演", "电影文件夹", "文件夹名", "正片视频数", "字幕数",
        "花絮视频数", "其他文件数", "视频示例", "字幕示例", "花絮示例",
    ]
    write_csv(args.output, rows, fields)
    print(f"wrote={args.output}")
    print(Counter(row["分类"] for row in rows))


def normalize_movie_part(text: str) -> str:
    text = text.strip()
    text = re.sub(r"[\[\]【】（）()]+", ".", text)
    text = re.sub(r"[ _+\-–—/]+", ".", text)
    text = re.sub(r"\.{2,}", ".", text)
    return text.strip(".")


def normalize_single_video_folder_target(video: Path, folder: Path) -> str | None:
    """Return a normalized filename for a one-video movie folder, if parseable."""
    stem = video.stem
    ext = video.suffix
    year_match = re.search(r"(19|20)\d{2}", stem)
    if not year_match:
        year_match = re.search(r"(19|20)\d{2}", folder.name)
    if not year_match:
        return None
    year = year_match.group(0)

    # Prefer already present Chinese title in the file; otherwise use the folder
    # name before the foreign title/year as the Chinese title.
    cn_match = re.match(r"^([\u4e00-\u9fff][\u4e00-\u9fff·：:、，,。！？!?《》\s._-]*?)(?:[A-Za-zÀ-ÿ]|\d{4}|$)", stem)
    if cn_match and has_chinese(cn_match.group(1)):
        cn = normalize_movie_part(cn_match.group(1))
        rest_start = len(cn_match.group(1))
        base = stem[rest_start:]
    else:
        folder_year_match = re.match(r"^\(?((?:19|20)\d{2})\)?[.\s_-]*(.+)$", folder.name)
        folder_base = folder_year_match.group(2) if folder_year_match else folder.name
        folder_cn_match = re.match(r"^([\u4e00-\u9fff][\u4e00-\u9fff·：:、，,。！？!?《》\s._-]*?)(?:[A-Za-zÀ-ÿ]|$)", folder_base)
        if not folder_cn_match:
            return None
        cn = normalize_movie_part(folder_cn_match.group(1))
        base = stem

    if not cn:
        return None

    base = re.sub(r"^\(?((?:19|20)\d{2})\)?[.\s_-]*", "", base)
    base = re.sub(r"\(?"+re.escape(year)+r"\)?", ".", base, count=1)
    base = normalize_movie_part(base)
    if base.startswith(cn + "."):
        base = base[len(cn) + 1:]
    elif base == cn:
        base = ""

    parts = [cn]
    if base:
        parts.append(base)
    parts.append(year)

    # If the year was embedded before tail metadata, put remaining metadata after
    # the year: 中文名.外语名.年份.剩余.ext
    joined = ".".join(part for part in parts if part)
    joined = re.sub(r"\."+re.escape(year)+r"\.([^.]*)$", r".\1."+year, joined)
    joined = re.sub(r"\.{2,}", ".", joined).strip(".")
    return joined + ext


def iter_one_file_movie_folders(root: Path):
    for director in sorted((p for p in root.iterdir() if p.is_dir()), key=lambda p: p.name):
        if director.name == "#recycle":
            continue
        for folder in sorted((p for p in director.iterdir() if p.is_dir()), key=lambda p: p.name):
            entries = [p for p in folder.iterdir() if p.name != ".DS_Store"]
            if len(entries) != 1 or not entries[0].is_file():
                continue
            video = entries[0]
            if video.suffix.lower() not in VIDEO_EXTS:
                continue
            if DIRECTOR_SINGLE_SKIP_RE.search(video.name) or DIRECTOR_SINGLE_SKIP_RE.search(folder.name):
                continue
            yield director, folder, video


def cmd_director_single_video_folder_plan(args) -> None:
    rows = []
    skipped = []
    conflicts = []
    selected: list[tuple[Path, Path, Path, str]] = []
    seen: dict[str, str] = {}

    for director, folder, video in iter_one_file_movie_folders(args.root):
        new_name = normalize_single_video_folder_target(video, folder)
        if not new_name:
            skipped.append({
                "导演": director.name,
                "电影文件夹": str(folder),
                "视频": str(video),
                "原因": "缺中文名或年份，未能按当前规则解析",
            })
            continue
        dst = director / new_name
        if dst.exists() and dst != video:
            conflicts.append({"当前路径": str(video), "目标路径": str(dst), "原因": "目标已存在"})
            continue
        if str(dst) in seen:
            conflicts.append({"当前路径": str(video), "目标路径": str(dst), "原因": "多个源指向同一目标"})
            continue
        seen[str(dst)] = str(video)
        selected.append((video, dst, folder, "单视频文件夹：规范命名、移到导演文件夹第一层、删除空文件夹"))
        rows.append({
            "动作": "改名并移出单视频文件夹",
            "当前路径": str(video),
            "目标路径": str(dst),
            "当前名称": video.name,
            "目标名称": dst.name,
            "依据": "由单视频文件夹规则生成",
        })
        rows.append({
            "动作": "删除移出后空文件夹",
            "当前路径": str(folder),
            "目标路径": "",
            "当前名称": folder.name,
            "目标名称": "",
            "依据": "移出唯一视频后删除空文件夹",
        })

    write_csv(args.output, rows, ["动作", "当前路径", "目标路径", "当前名称", "目标名称", "依据"])
    write_csv(args.skip_output, skipped, ["导演", "电影文件夹", "视频", "原因"])
    write_csv(args.conflicts_output, conflicts, ["当前路径", "目标路径", "原因"])

    args.script.parent.mkdir(parents=True, exist_ok=True)
    with args.script.open("w", encoding="utf-8") as handle:
        handle.write("#!/bin/zsh\nset -euo pipefail\n\n")
        for src, dst, folder, _note in selected:
            handle.write("mv -- ")
            handle.write(shlex.quote(str(src)))
            handle.write(" ")
            handle.write(shlex.quote(str(dst)))
            handle.write("\n")
            handle.write("rmdir -- ")
            handle.write(shlex.quote(str(folder)))
            handle.write("\n")
    os.chmod(args.script, 0o755)

    print(f"wrote={args.output}")
    print(f"script={args.script}")
    print(f"selected_actions={len(rows)} move_actions={len(selected)} rmdir_actions={len(selected)}")
    print(f"skipped={len(skipped)} conflicts={len(conflicts)}")


def iter_archive_files(root: Path):
    for path in sorted(root.rglob("*"), key=lambda p: str(p)):
        if not path.is_file() or path.name == ".DS_Store" or "#recycle" in path.parts:
            continue
        if path.suffix.lower() in ARCHIVE_EXTS or ARCHIVE_PART_RE.search(path.name):
            yield path


def archive_name_category(path: Path) -> str:
    lower = path.name.lower()
    if path.suffix.lower() == ".iso":
        return "光盘镜像"
    if ARCHIVE_PART_RE.search(path.name):
        return "分卷压缩包"
    if any(key in lower for key in ["sub", "subtitle", "srt", "ass", "字幕", "chs", "cht", "eng"]):
        return "疑似字幕压缩包"
    if any(key in lower for key in ["sample", "trailer", "extra", "bonus", "featurette", "花絮", "访谈", "采访"]):
        return "疑似花絮/附加资料压缩包"
    return "普通压缩包"


def cmd_director_archive_scan(args) -> None:
    inspectable = []
    rows = []
    for path in iter_archive_files(args.root):
        try:
            size_mb = path.stat().st_size / 1024 / 1024
        except OSError:
            size_mb = -1
        name_category = archive_name_category(path)
        content_category = ""
        content_count = ""
        content_example = ""
        result = ""
        if name_category in {"分卷压缩包", "光盘镜像"} or size_mb > args.max_inspect_mb:
            content_category = "未检查：分卷/镜像/大文件"
        else:
            try:
                cp = subprocess.run(
                    ["bsdtar", "-tf", str(path)],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=args.timeout,
                )
            except Exception as exc:
                cp = None
                content_category = "无法读取"
                result = str(exc)
            if cp is not None:
                if cp.returncode != 0:
                    content_category = "无法读取"
                    result = cp.stderr.strip()[:300]
                else:
                    names = [line.strip() for line in cp.stdout.splitlines() if line.strip() and not line.endswith("/")]
                    exts = [Path(name).suffix.lower() for name in names]
                    content_count = str(len(names))
                    content_example = " | ".join(names[:8])
                    result = "ok"
                    if names and all(ext in SUBTITLE_ARCHIVE_EXTS for ext in exts):
                        content_category = "纯字幕压缩包"
                    elif names and all(ext in SUBTITLE_ARCHIVE_EXTS | {".txt", ".nfo"} for ext in exts):
                        content_category = "字幕+说明压缩包"
                    elif any(ext in VIDEO_EXTS for ext in exts):
                        content_category = "含视频压缩包"
                    else:
                        content_category = "其他/不明内容压缩包"

        row = {
            "分类": name_category,
            "内容分类": content_category,
            "扩展名": path.suffix.lower() or "分卷",
            "路径": str(path),
            "文件名": path.name,
            "所在目录": str(path.parent),
            "大小MB": "" if size_mb < 0 else f"{size_mb:.2f}",
            "内容数量": content_count,
            "内容示例": content_example,
            "检查结果": result,
        }
        rows.append(row)
        if content_category in {"纯字幕压缩包", "字幕+说明压缩包"}:
            inspectable.append(row)

    fields = ["分类", "内容分类", "扩展名", "路径", "文件名", "所在目录", "大小MB", "内容数量", "内容示例", "检查结果"]
    write_csv(args.output, rows, fields)
    write_csv(args.subtitle_output, inspectable, fields)
    print(f"wrote={args.output}")
    print(f"subtitle_archives={len(inspectable)} total_archives={len(rows)}")
    print(Counter(row["内容分类"] for row in rows))


def director_video_naming_issues(path: Path) -> tuple[list[str], list[str]]:
    stem = path.stem
    issues = []
    notes = []
    if DIRECTOR_SINGLE_SKIP_RE.search(stem) or any(DIRECTOR_SINGLE_SKIP_RE.search(part) for part in path.parts):
        issues.append("疑似花絮/资料片/访谈/预告，可跳过")
    if not has_chinese(stem):
        issues.append("缺中文名")
    if not FOREIGN_CHAR_RE.search(stem):
        issues.append("缺外语名")
    if not YEAR_TOKEN_RE.search(stem):
        issues.append("缺年份")
    elif not DOT_YEAR_RE.search(stem):
        issues.append("年份不是点分隔")
    if has_chinese(stem) and FOREIGN_CHAR_RE.search(stem) and not re.search(r"[\u4e00-\u9fff].*\.[A-Za-z\u3040-\u30ff\u0400-\u04ff]", stem):
        issues.append("中文/外语名疑似未用点分隔或顺序异常")
    if re.search(r"[\[\]【】]", stem):
        issues.append("含方括号")
    if re.search(r"[ _]+", stem):
        issues.append("含空格或下划线")
    sibling_videos = []
    try:
        sibling_videos = [item for item in path.parent.iterdir() if item.is_file() and item.suffix.lower() in VIDEO_EXTS]
    except OSError:
        sibling_videos = []
    has_ab_group = len(sibling_videos) > 1 and any(AB_PART_RE.search(item.stem) for item in sibling_videos)
    if CD_PART_RE.search(stem) or EPISODE_RE.search(stem) or has_ab_group:
        notes.append("疑似多段/CD/Part")
    return issues, notes


def json_default_path(name: str) -> Path:
    return DEFAULT_OUTPUT_DIR / name


def file_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in VIDEO_EXTS:
        return "video"
    if suffix in SUBTITLE_ARCHIVE_EXTS:
        return "subtitle"
    if suffix in ARCHIVE_EXTS or ARCHIVE_PART_RE.search(path.name):
        return "archive"
    return "other"


def relative_parts(path: Path, root: Path) -> list[str]:
    try:
        return list(path.relative_to(root).parts)
    except ValueError:
        return list(path.parts)


def snapshot_item(path: Path, root: Path) -> dict:
    parts = relative_parts(path, root)
    try:
        stat = path.stat()
        size = stat.st_size
        mtime = stat.st_mtime
    except OSError:
        size = None
        mtime = None
    return {
        "path": str(path),
        "relative_path": "/".join(parts),
        "parent": str(path.parent),
        "name": path.name,
        "stem": path.stem,
        "suffix": path.suffix.lower(),
        "kind": file_kind(path),
        "director": parts[0] if parts else "",
        "depth": len(parts),
        "size": size,
        "mtime": mtime,
        "status": "unknown",
        "category": "unreviewed",
        "issues": [],
        "notes": [],
        "proposed_path": None,
        "source": "snapshot",
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def movie_folder_title_from_parts(parts: list[str]) -> str:
    if len(parts) != 3:
        return ""
    folder = Path(parts[-2]).name.strip()
    if folder in CATEGORY_DIR_NAMES or not has_chinese(folder):
        return ""
    title = re.sub(r"^[（(]?\s*(?:18|19|20)\d{2}\s*[）)]?[._ -]*", "", folder)
    match = re.match(r"^(.+?)(?:\s+-\s+[A-Za-z]|[._ ]+[A-Za-z]|[（(]\s*(?:18|19|20)\d{2})", title)
    if match and has_chinese(match.group(1)):
        title = match.group(1)
    title = re.sub(r"[\[\]【】]", "", title)
    title = re.sub(r"[\s_]+", ".", title).strip(". -_")
    return title


def has_multisegment_sibling(item: dict, items_by_parent: dict[str, list[dict]]) -> bool:
    siblings = [entry for entry in items_by_parent.get(item["parent"], []) if entry.get("kind") == "video"]
    if len(siblings) <= 1:
        return False
    return any(
        CD_PART_RE.search(entry.get("stem", ""))
        or AB_PART_RE.search(entry.get("stem", ""))
        or EPISODE_RE.search(entry.get("stem", ""))
        for entry in siblings
    )


def analyze_video_item(item: dict, items_by_parent: dict[str, list[dict]]) -> dict:
    stem = item.get("stem", "")
    issues: list[str] = []
    notes: list[str] = []
    status = "review"
    category = "needs_review"
    proposed_path = item.get("proposed_path")

    if DIRECTOR_SINGLE_SKIP_RE.search(stem) or any(DIRECTOR_SINGLE_SKIP_RE.search(part) for part in item.get("relative_path", "").split("/")):
        issues.append("疑似花絮/资料片/访谈/预告")
        category = "skip_extra"
        status = "skip"
    if has_multisegment_sibling(item, items_by_parent):
        notes.append("同目录疑似多段/CD/Part/剧集，先整组跳过")
        category = "skip_multisegment"
        status = "skip"

    if not has_chinese(stem):
        folder_title = movie_folder_title_from_parts(item.get("relative_path", "").split("/"))
        if folder_title:
            issues.append("文件缺中文名，可用电影文件夹中文名")
            proposed_name = f"{folder_title}.{item['name']}"
            proposed_path = str(Path(item["parent"]) / proposed_name)
            category = "can_use_movie_folder_title"
        else:
            issues.append("缺中文名")
    if not FOREIGN_CHAR_RE.search(stem):
        issues.append("缺外语名")
    if not YEAR_TOKEN_RE.search(stem):
        issues.append("缺年份")
    elif not DOT_YEAR_RE.search(stem):
        issues.append("年份不是点分隔")
        normalized = re.sub(r"[（(]\s*((?:18|19|20)\d{2})\s*[）)]", r".\1.", stem)
        normalized = re.sub(r"(?<!\d)-((?:18|19|20)\d{2})(?!\d)-?", r".\1.", normalized)
        normalized = re.sub(r"\.{2,}", ".", normalized).strip(". _-")
        if normalized != stem and has_chinese(normalized):
            proposed_path = str(Path(item["parent"]) / f"{normalized}{item['suffix']}")
            if category == "needs_review":
                category = "can_normalize_punctuation"
    if has_chinese(stem) and FOREIGN_CHAR_RE.search(stem) and not re.search(r"[\u4e00-\u9fff].*\.[A-Za-z\u3040-\u30ff\u0400-\u04ff]", stem):
        issues.append("中文/外语名疑似未用点分隔或顺序异常")
    if re.search(r"[\[\]【】]", stem):
        issues.append("含方括号")
    if re.search(r"[ _]+", stem):
        issues.append("含空格或下划线")

    if not issues:
        status = "done"
        category = "done"
        proposed_path = None
    elif status != "skip":
        status = "review"

    item["status"] = status
    item["category"] = category
    item["issues"] = issues
    item["notes"] = notes
    item["proposed_path"] = proposed_path
    item["source"] = "analyze-json"
    return item


def cmd_snapshot_json(args) -> None:
    if not args.root.exists():
        raise SystemExit(f"root not found: {args.root}")
    if not args.root.is_dir():
        raise SystemExit(f"root is not a directory: {args.root}")
    items = []
    for path in sorted(args.root.rglob("*"), key=lambda entry: str(entry)):
        if not path.is_file():
            continue
        if not args.include_recycle and "#recycle" in path.parts:
            continue
        items.append(snapshot_item(path, args.root))
    data = {
        "schema_version": 1,
        "root": str(args.root),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "workflow": "snapshot-json -> analyze-json -> review/edit JSON -> apply-json --execute",
        "items": items,
    }
    write_json(args.output, data)
    counts = Counter(item["kind"] for item in items)
    print(f"wrote={args.output}")
    print(f"total={len(items)}")
    print(counts)


def cmd_analyze_json(args) -> None:
    data = read_json(args.input)
    items = data.get("items", [])
    items_by_parent: dict[str, list[dict]] = {}
    for item in items:
        items_by_parent.setdefault(item.get("parent", ""), []).append(item)

    for item in items:
        if item.get("kind") == "video":
            analyze_video_item(item, items_by_parent)
        elif item.get("kind") in {"subtitle", "archive"}:
            item.setdefault("issues", [])
            item.setdefault("notes", [])
            item["status"] = item.get("status") if item.get("status") in {"review", "planned"} else "related"
            item["category"] = item.get("kind")
        else:
            item.setdefault("issues", [])
            item.setdefault("notes", [])
            item["status"] = "ignore"
            item["category"] = "other"

    data["analyzed_at"] = datetime.now().isoformat(timespec="seconds")
    data["summary"] = {
        "status": dict(Counter(item.get("status", "") for item in items)),
        "category": dict(Counter(item.get("category", "") for item in items)),
        "video_issues": dict(Counter(issue for item in items if item.get("kind") == "video" for issue in item.get("issues", []))),
    }
    write_json(args.output, data)
    print(f"wrote={args.output}")
    print(f"items={len(items)}")
    print(data["summary"])


def cmd_apply_json(args) -> None:
    data = read_json(args.input)
    planned = []
    skipped = []
    for item in data.get("items", []):
        proposed = item.get("proposed_path")
        original = item.get("original_path") or item.get("path")
        if item.get("operation", "rename") != "rename":
            continue
        if item.get("status") not in {"planned", "approved"} or not proposed or not original:
            continue
        src = Path(original)
        dst = Path(proposed)
        if not src.exists():
            skipped.append({"path": str(src), "reason": "source_missing"})
            continue
        if dst.exists():
            skipped.append({"path": str(src), "reason": "target_exists", "target": str(dst)})
            continue
        planned.append((src, dst))

    print(f"planned={len(planned)} skipped={len(skipped)} execute={args.execute}")
    for src, dst in planned[: args.preview_limit]:
        print(f"{src} -> {dst}")
    if skipped:
        print("skipped:")
        for row in skipped[: args.preview_limit]:
            print(row)
    if not args.execute:
        print("dry-run only; add --execute to rename files")
        return
    for src, dst in planned:
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
    print(f"renamed={len(planned)}")


def cmd_validate_plan(args) -> None:
    snapshot = read_json(args.snapshot)
    plan = read_json(args.plan)
    snapshot_paths = {item.get("path") for item in snapshot.get("items", [])}
    planned_originals = []
    planned_targets = []
    problems = []

    for item in plan.get("items", []):
        if item.get("operation", "rename") != "rename" or item.get("status") not in {"planned", "approved"}:
            continue
        original = item.get("original_path") or item.get("path")
        target = item.get("proposed_path")
        planned_originals.append(original)
        planned_targets.append(target)
        if not original:
            problems.append({"id": item.get("id"), "problem": "missing original_path"})
        elif original not in snapshot_paths:
            problems.append({"id": item.get("id"), "path": original, "problem": "original_path not in source snapshot"})
        if not target:
            problems.append({"id": item.get("id"), "path": original, "problem": "missing proposed_path"})
        elif target in snapshot_paths and target != original:
            problems.append({"id": item.get("id"), "path": original, "target": target, "problem": "target already existed in source snapshot"})

    for value, count in Counter(planned_originals).items():
        if value and count > 1:
            problems.append({"path": value, "problem": "duplicate original_path", "count": count})
    for value, count in Counter(planned_targets).items():
        if value and count > 1:
            problems.append({"target": value, "problem": "duplicate proposed_path", "count": count})

    result = {
        "plan": str(args.plan),
        "snapshot": str(args.snapshot),
        "planned_count": len(planned_originals),
        "problem_count": len(problems),
        "problems": problems,
    }
    if args.output:
        write_json(args.output, result)
        print(f"wrote={args.output}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def iter_plan_items(plan: dict) -> list[dict]:
    return plan.get("items", []) if isinstance(plan, dict) else []


def plan_paths_by_status(plan: dict, statuses: set[str] | None = None) -> set[str]:
    paths = set()
    for item in iter_plan_items(plan):
        if statuses is not None and item.get("status") not in statuses:
            continue
        for key in ("original_path", "path", "legacy_original_path"):
            value = item.get(key)
            if value:
                paths.add(value)
    return paths


def multipart_paths(multipart: dict) -> set[str]:
    paths = set()
    for group in multipart.get("groups", []):
        for part in group.get("parts", []):
            if part.get("path"):
                paths.add(part["path"])
    return paths


def classify_remaining_review(path: str) -> str:
    if REVIEW_EXTRA_RE.search(path):
        return "花絮资料/影人相关"
    if REVIEW_COLLECTION_RE.search(path):
        return "合集/系列/短片集保留"
    if REVIEW_FOREIGN_OK_RE.search(path):
        return "外文名年份已可接受"
    return "仍需人工看"


def cmd_plan_status(args) -> None:
    plan = read_json(args.plan)
    statuses = Counter(item.get("status", "") for item in iter_plan_items(plan))
    operations = Counter(item.get("operation", "rename") for item in iter_plan_items(plan))
    result = {
        "plan": str(args.plan),
        "item_count": len(iter_plan_items(plan)),
        "status": dict(statuses),
        "operation": dict(operations),
        "last_sync": plan.get("review", {}).get("last_sync"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_remaining_review(args) -> None:
    analyzed = read_json(args.analyzed)
    plan = read_json(args.plan)
    multipart = read_json(args.multipart) if args.multipart.exists() else {"groups": []}
    excluded_paths = plan_paths_by_status(plan) | multipart_paths(multipart)

    classes: dict[str, list[dict]] = {
        "花絮资料/影人相关": [],
        "合集/系列/短片集保留": [],
        "外文名年份已可接受": [],
        "仍需人工看": [],
    }
    for item in analyzed.get("items", []):
        if item.get("kind") != "video":
            continue
        if item.get("path") in excluded_paths:
            continue
        if item.get("status") in {"done", "skip"}:
            continue
        category = classify_remaining_review(item.get("path", ""))
        classes[category].append({
            "path": item.get("path"),
            "issues": item.get("issues", []),
            "category": item.get("category"),
            "status": item.get("status"),
        })

    result = {
        "analyzed": str(args.analyzed),
        "plan": str(args.plan),
        "multipart": str(args.multipart),
        "remaining_total": sum(len(items) for items in classes.values()),
        "summary": {key: len(value) for key, value in classes.items()},
        "examples": {key: value[: args.limit] for key, value in classes.items() if value},
    }
    if args.output:
        write_json(args.output, result)
        print(f"wrote={args.output}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_director_all_video_naming_check(args) -> None:
    rows = []
    total = 0
    good = 0
    for path in sorted(args.root.rglob("*"), key=lambda item: str(item)):
        if not path.is_file() or path.suffix.lower() not in VIDEO_EXTS:
            continue
        if any(part in DEFAULT_EXCLUDES for part in path.parts):
            continue
        total += 1
        issues, notes = director_video_naming_issues(path)
        if issues:
            relative = path.relative_to(args.root)
            rows.append({
                "路径": str(path),
                "文件名": path.name,
                "导演": relative.parts[0] if len(relative.parts) > 1 else "",
                "所在目录": str(path.parent),
                "问题": "；".join(issues),
                "备注": "；".join(notes),
            })
        else:
            good += 1

    write_csv(args.output, rows, ["路径", "文件名", "导演", "所在目录", "问题", "备注"])

    counts = Counter()
    for row in rows:
        for issue in row["问题"].split("；"):
            counts[issue] += 1
    summary_rows = [
        {"项目": "视频总数", "数量": total},
        {"项目": "格式合格", "数量": good},
        {"项目": "不合格/需看", "数量": len(rows)},
    ]
    summary_rows.extend({"项目": issue, "数量": count} for issue, count in counts.most_common())
    write_csv(args.summary_output, summary_rows, ["项目", "数量"])

    print(f"total={total} good={good} bad={len(rows)}")
    print(f"wrote={args.output}")
    print(f"summary={args.summary_output}")
    print(counts)


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def infer_subtitle_language(name: str) -> str:
    text = Path(name).stem.lower()
    normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", ".", text)
    tokens = [token for token in normalized.split(".") if token]
    token_set = set(tokens)
    if any(token in token_set for token in ["cht", "tc", "big5", "traditional"]):
        return "cht"
    if any(token in token_set for token in ["chs", "sc", "gb", "gbk", "simplified", "cn", "zh", "chi", "chseng"]):
        return "chs"
    if any(token in token_set for token in ["eng", "en", "english"]):
        return "eng"
    if re.search(r"(?:^|[^a-z])cht(?:$|[^a-z])", text) or "繁" in text:
        return "cht"
    if re.search(r"(?:^|[^a-z])chs(?:$|[^a-z])", text) or "简" in text or "中字" in text:
        return "chs"
    if re.search(r"(?:^|[^a-z])eng(?:$|[^a-z])", text) or "英字" in text:
        return "eng"
    return "未识别"


def planned_subtitle_name(video: Path, subtitle_name: str, used: set[Path]) -> Path:
    lang = infer_subtitle_language(subtitle_name)
    suffix = Path(subtitle_name).suffix.lower()
    stem = video.stem if lang == "未识别" else f"{video.stem}.{lang}"
    candidate = video.with_name(f"{stem}{suffix}")
    counter = 2
    while candidate in used or (candidate.exists() and candidate.name != Path(subtitle_name).name):
        candidate = video.with_name(f"{stem}.{counter}{suffix}")
        counter += 1
    used.add(candidate)
    return candidate


def archive_member_names(path: Path, timeout: int) -> tuple[list[str], str]:
    cp = subprocess.run(
        ["bsdtar", "-tf", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    if cp.returncode != 0:
        return [], cp.stderr.strip()[:300]
    names = [line.strip() for line in cp.stdout.splitlines() if line.strip() and not line.endswith("/")]
    return names, "ok"


def cmd_director_subtitle_archive_cleanup_plan(args) -> None:
    rows = []
    skipped = []
    deletes = []
    used_destinations: set[Path] = set()
    archive_rows = read_csv_rows(args.subtitle_archives)

    for row in archive_rows:
        archive = Path(row.get("路径", ""))
        if not archive.exists():
            skipped.append({"路径": str(archive), "原因": "压缩包不存在", "详情": ""})
            continue

        names, result = archive_member_names(archive, args.timeout)
        if result != "ok":
            skipped.append({"路径": str(archive), "原因": "无法读取压缩包", "详情": result})
            continue

        subtitle_names = [name for name in names if Path(name).suffix.lower() in SUBTITLE_ARCHIVE_EXTS]
        if not subtitle_names:
            skipped.append({"路径": str(archive), "原因": "压缩包内无字幕文件", "详情": " | ".join(names[:8])})
            continue

        videos = [path for path in archive.parent.iterdir() if path.is_file() and path.suffix.lower() in VIDEO_EXTS]
        if len(videos) != 1:
            reason = "无视频文件" if not videos else "多视频目录无法确定匹配哪一个视频"
            skipped.append({"路径": str(archive), "原因": reason, "详情": " | ".join(str(path) for path in videos[:8])})
            continue

        video = videos[0]
        archive_actions = []
        missing = []
        for name in subtitle_names:
            extracted = archive.parent / Path(name).name
            if not extracted.exists():
                missing.append(str(extracted))
                continue
            target = planned_subtitle_name(video, extracted.name, used_destinations)
            archive_actions.append({
                "动作": "字幕改名匹配电影文件",
                "当前路径": str(extracted),
                "目标路径": str(target),
                "电影文件": str(video),
                "语言": infer_subtitle_language(extracted.name),
                "来源压缩包": str(archive),
            })

        if missing:
            skipped.append({"路径": str(archive), "原因": "已解压字幕未找到", "详情": " | ".join(missing[:8])})
            continue

        rows.extend(archive_actions)
        deletes.append({
            "动作": "删除已解压字幕压缩包",
            "当前路径": str(archive),
            "目标路径": "",
            "电影文件": str(video),
            "语言": "",
            "来源压缩包": str(archive),
        })

    rows.extend(deletes)
    fields = ["动作", "当前路径", "目标路径", "电影文件", "语言", "来源压缩包"]
    write_csv(args.output, rows, fields)
    write_csv(args.skip_output, skipped, ["路径", "原因", "详情"])

    args.script.parent.mkdir(parents=True, exist_ok=True)
    with args.script.open("w", encoding="utf-8") as handle:
        handle.write("#!/bin/zsh\nset -euo pipefail\n\n")
        for row in rows:
            if row["动作"] == "字幕改名匹配电影文件":
                handle.write("mv -n -- ")
                handle.write(shlex.quote(row["当前路径"]))
                handle.write(" ")
                handle.write(shlex.quote(row["目标路径"]))
                handle.write("\n")
            elif row["动作"] == "删除已解压字幕压缩包":
                handle.write("rm -- ")
                handle.write(shlex.quote(row["当前路径"]))
                handle.write("\n")
    os.chmod(args.script, 0o755)

    print(f"wrote={args.output}")
    print(f"script={args.script}")
    print(f"subtitle_renames={sum(1 for row in rows if row['动作'] == '字幕改名匹配电影文件')}")
    print(f"archive_deletes={len(deletes)} skipped={len(skipped)}")


def available_archive_tools() -> dict[str, str | None]:
    local_7zz = Path(__file__).resolve().parents[2] / "Documents" / "电影整理计划" / "bin" / "7zz"
    if not local_7zz.exists():
        local_7zz = Path.cwd() / "bin" / "7zz"
    tools = {
        "unar": shutil.which("unar"),
        "lsar": shutil.which("lsar"),
        "7zz": shutil.which("7zz") or (str(local_7zz) if local_7zz.exists() else None),
        "7z": shutil.which("7z"),
        "unrar": shutil.which("unrar"),
    }
    keka_paths = {
        "keka7zz": "/Applications/Keka.app/Contents/MacOS/keka7zz",
        "kekaunrar": "/Applications/Keka.app/Contents/MacOS/kekaunrar",
        "kekaunar": "/Applications/Keka.app/Contents/MacOS/kekaunar",
    }
    for name, path in keka_paths.items():
        tools[name] = path if Path(path).exists() else None
    return tools


def archive_shape_from_name(name: str) -> str:
    lower = name.lower()
    if re.search(r"\.part\d+\.rar$", lower):
        return "part-rar"
    if re.search(r"\.\d{3}$", lower):
        return "numeric-split"
    return "other"


def cmd_multipart_archive_status(args) -> None:
    data = read_json(args.input)
    items = data.get("items", [])
    by_status = Counter(item.get("local_extract_status", item.get("status", "unknown")) for item in items)
    by_shape = Counter(archive_shape_from_name(item.get("name", Path(item.get("path", "")).name)) for item in items)
    tools = available_archive_tools()
    usable = [name for name in ("unar", "7zz", "7z", "unrar") if tools.get(name)]

    print(f"input={args.input}")
    print(f"items={len(items)}")
    print("status=" + json.dumps(dict(by_status), ensure_ascii=False, sort_keys=True))
    print("shape=" + json.dumps(dict(by_shape), ensure_ascii=False, sort_keys=True))
    print("usable_cli_tools=" + (", ".join(usable) if usable else "none"))
    keka_found = [name for name in ("keka7zz", "kekaunrar", "kekaunar") if tools.get(name)]
    print("keka_internal_tools=" + (", ".join(keka_found) if keka_found else "none"))
    if not usable:
        print("decision=RAR 分卷暂不自动处理：需要安装或提供可直接命令行调用的 unar/7zz/7z/unrar。")
        print("note=Keka.app 内置工具存在时也只作为线索；本轮实测这些内部二进制不能直接作为 CLI 后端。")
    else:
        print("decision=可以继续走本地临时解压 -> 校验 -> 回写 NAS -> 删除原分卷流程。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="整理 NAS 电影文件名的最新版工具")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--exclude",
        action="append",
        default=sorted(DEFAULT_EXCLUDES),
        help="可重复传入；默认排除 剧 和 #recycle",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    snapshot_json = sub.add_parser("snapshot-json", help="只扫描一次 NAS，把 /Volumes/导演们 的全部文件路径保存成 JSON 快照")
    snapshot_json.add_argument("--root", type=Path, default=DIRECTORS_ROOT)
    snapshot_json.add_argument("--output", type=Path, default=json_default_path("导演们文件快照.json"))
    snapshot_json.add_argument("--include-recycle", action="store_true", help="默认排除 #recycle；需要时可包含")
    snapshot_json.set_defaults(func=cmd_snapshot_json)

    analyze_json = sub.add_parser("analyze-json", help="只分析本地 JSON 快照，按当前规则标记 done/review/skip 并写回新 JSON")
    analyze_json.add_argument("--input", type=Path, default=json_default_path("导演们文件快照.json"))
    analyze_json.add_argument("--output", type=Path, default=json_default_path("导演们文件快照_已分析.json"))
    analyze_json.set_defaults(func=cmd_analyze_json)

    apply_json = sub.add_parser("apply-json", help="从小型改名计划 JSON 中读取 status=planned/approved 的项目并执行改名")
    apply_json.add_argument("--input", type=Path, default=json_default_path("导演们_改名计划.json"))
    apply_json.add_argument("--preview-limit", type=int, default=50)
    apply_json.add_argument("--execute", action="store_true", help="默认 dry-run；加这个参数才真正改 NAS 文件名")
    apply_json.set_defaults(func=cmd_apply_json)

    validate_plan = sub.add_parser("validate-plan", help="用原始快照校验小型改名计划：原路径、目标冲突、重复项")
    validate_plan.add_argument("--snapshot", type=Path, default=json_default_path("导演们文件快照.json"))
    validate_plan.add_argument("--plan", type=Path, default=json_default_path("导演们_改名计划.json"))
    validate_plan.add_argument("--output", type=Path, default=json_default_path("导演们_改名计划_校验结果.json"))
    validate_plan.set_defaults(func=cmd_validate_plan)

    plan_status = sub.add_parser("plan-status", help="汇总小型改名计划的状态，确认是否还有 planned/approved 待执行")
    plan_status.add_argument("--plan", type=Path, default=json_default_path("导演们_改名计划.json"))
    plan_status.set_defaults(func=cmd_plan_status)

    remaining_review = sub.add_parser(
        "remaining-review",
        help="基于已分析快照，排除改名计划和多段清单后，汇总剩余待看视频",
    )
    remaining_review.add_argument("--analyzed", type=Path, default=Path("/tmp/导演们文件快照_已分析.json"))
    remaining_review.add_argument("--plan", type=Path, default=json_default_path("导演们_改名计划.json"))
    remaining_review.add_argument("--multipart", type=Path, default=json_default_path("导演们_多段资源清单.json"))
    remaining_review.add_argument("--output", type=Path, default=Path("/tmp/导演们_剩余待看摘要.json"))
    remaining_review.add_argument("--limit", type=int, default=12)
    remaining_review.set_defaults(func=cmd_remaining_review)

    scan = sub.add_parser("scan", help="列出非剧目录视频/字幕文件")
    scan.add_argument("--output", type=Path, default=out_path("非剧目录文件名单.txt"))
    scan.set_defaults(func=cmd_scan)

    check = sub.add_parser("check", help="检查文件名是否已有中文/英文/年份")
    check.add_argument("--output", type=Path, default=out_path("非剧目录_仅按文件名检查.csv"))
    check.set_defaults(func=cmd_check)

    preview = sub.add_parser("preview", help="按已查匹配表生成重命名预览")
    preview.add_argument("--output", type=Path, default=out_path("非剧目录_豆瓣匹配预览.csv"))
    preview.set_defaults(func=cmd_preview)

    script = sub.add_parser("make-script", help="从预览表生成指定置信度的 mv 脚本")
    script.add_argument("--preview", type=Path, default=out_path("非剧目录_豆瓣匹配预览.csv"))
    script.add_argument("--confidence", default="高", choices=["高", "中"])
    script.add_argument("--output", type=Path, default=out_path("执行非剧目录_高置信度重命名.sh"))
    script.set_defaults(func=cmd_make_script)

    summary = sub.add_parser("summary", help="执行后生成剩余待处理摘要")
    summary.add_argument("--preview", type=Path, default=out_path("非剧目录_豆瓣匹配预览.csv"))
    summary.add_argument("--output", type=Path, default=out_path("非剧目录_剩余待处理摘要.csv"))
    summary.set_defaults(func=cmd_summary)

    director = sub.add_parser("director-single-check", help="只检查 /Volumes/导演们/<导演名>/ 这一层的单一电影文件")
    director.add_argument("--root", type=Path, default=DIRECTORS_ROOT)
    director.add_argument(
        "--ignore-director",
        action="append",
        default=sorted(DIRECTOR_SINGLE_IGNORE_DIRECTORS),
        help="可重复传入；默认忽略用户指定的巴斯特·基顿短片集",
    )
    director.add_argument("--output", type=Path, default=out_path("导演们_单一电影文件_检查清单.csv"))
    director.add_argument("--bad-output", type=Path, default=out_path("导演们_单一电影文件_待处理.csv"))
    director.add_argument("--skip-output", type=Path, default=out_path("导演们_单一电影文件_花絮类跳过.csv"))
    director.add_argument("--ignore-output", type=Path, default=out_path("导演们_单一电影文件_用户指定忽略.csv"))
    director.set_defaults(func=cmd_director_single_check)

    harold = sub.add_parser("harold-strip-d-prefix", help="为哈罗德·劳埃德文件生成去 D1./D2. 前缀脚本")
    harold.add_argument("--root", type=Path, default=DIRECTORS_ROOT)
    harold.add_argument("--output", type=Path, default=out_path("导演们_哈罗德劳埃德_去D前缀计划.csv"))
    harold.add_argument("--conflicts-output", type=Path, default=out_path("导演们_哈罗德劳埃德_去D前缀冲突.csv"))
    harold.add_argument("--script", type=Path, default=out_path("执行哈罗德劳埃德_去D前缀.sh"))
    harold.set_defaults(func=cmd_harold_strip_d_prefix)

    folders = sub.add_parser("director-folder-structure", help="统计 /Volumes/导演们/<导演名>/<电影文件夹> 的结构分类")
    folders.add_argument("--root", type=Path, default=DIRECTORS_ROOT)
    folders.add_argument("--output", type=Path, default=out_path("导演们_单一电影文件夹_结构分类.csv"))
    folders.set_defaults(func=cmd_director_folder_structure)

    one_video_folders = sub.add_parser(
        "director-single-video-folder-plan",
        help="为只有一个视频文件的电影文件夹生成移出到导演文件夹并删除空文件夹的计划",
    )
    one_video_folders.add_argument("--root", type=Path, default=DIRECTORS_ROOT)
    one_video_folders.add_argument("--output", type=Path, default=out_path("导演们_单视频文件夹_全局移出计划.csv"))
    one_video_folders.add_argument("--skip-output", type=Path, default=out_path("导演们_单视频文件夹_全局移出跳过.csv"))
    one_video_folders.add_argument("--conflicts-output", type=Path, default=out_path("导演们_单视频文件夹_全局移出冲突.csv"))
    one_video_folders.add_argument("--script", type=Path, default=out_path("执行导演们_单视频文件夹_全局移出.sh"))
    one_video_folders.set_defaults(func=cmd_director_single_video_folder_plan)

    archives = sub.add_parser("director-archive-scan", help="扫描 /Volumes/导演们 中的压缩包、分卷、镜像，并识别字幕压缩包")
    archives.add_argument("--root", type=Path, default=DIRECTORS_ROOT)
    archives.add_argument("--max-inspect-mb", type=float, default=20.0)
    archives.add_argument("--timeout", type=int, default=20)
    archives.add_argument("--output", type=Path, default=out_path("导演们_压缩文件内容分类.csv"))
    archives.add_argument("--subtitle-output", type=Path, default=out_path("导演们_字幕压缩包_解压计划.csv"))
    archives.set_defaults(func=cmd_director_archive_scan)

    all_video_check = sub.add_parser(
        "director-all-video-naming-check",
        help="扫描 /Volumes/导演们 下所有视频文件，找出不符合 中文名.外语名.年份.ext 规则的项目",
    )
    all_video_check.add_argument("--root", type=Path, default=DIRECTORS_ROOT)
    all_video_check.add_argument("--output", type=Path, default=out_path("导演们_全视频_命名规则复查_不合格.csv"))
    all_video_check.add_argument("--summary-output", type=Path, default=out_path("导演们_全视频_命名规则复查_摘要.csv"))
    all_video_check.set_defaults(func=cmd_director_all_video_naming_check)

    subtitle_cleanup = sub.add_parser(
        "director-subtitle-archive-cleanup-plan",
        help="为已解压字幕包生成字幕跟随电影名的改名计划，并为成功匹配的原压缩包生成删除脚本",
    )
    subtitle_cleanup.add_argument("--subtitle-archives", type=Path, default=out_path("导演们_字幕压缩包_解压计划.csv"))
    subtitle_cleanup.add_argument("--timeout", type=int, default=20)
    subtitle_cleanup.add_argument("--output", type=Path, default=out_path("导演们_字幕文件改名并删除已解压压缩包计划.csv"))
    subtitle_cleanup.add_argument("--skip-output", type=Path, default=out_path("导演们_字幕文件改名并删除已解压压缩包跳过.csv"))
    subtitle_cleanup.add_argument("--script", type=Path, default=out_path("执行导演们_字幕改名并删除已解压压缩包.sh"))
    subtitle_cleanup.set_defaults(func=cmd_director_subtitle_archive_cleanup_plan)

    multipart_status = sub.add_parser(
        "multipart-archive-status",
        help="汇总分卷压缩包 JSON 状态，并检查本机是否有可用的 unar/7zz/7z/unrar",
    )
    multipart_status.add_argument("--input", type=Path, default=json_default_path("分类_分卷压缩包清单.json"))
    multipart_status.set_defaults(func=cmd_multipart_archive_status)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
