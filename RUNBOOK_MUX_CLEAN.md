# 字幕内封与清理流程

这套流程用于 `/Volumes/导演们` 和 `/Volumes/分类` 里的电影文件夹。当前主流程是 14/15/16 三个脚本。

## 当前流程

1. `15_rescan_remaining_subtitles.py` 重新扫描剩余字幕。
2. `16_prepare_remaining_mux_queue.py` 把纯字幕子文件夹里的字幕移动到电影同级目录，并生成 `remaining_mux_clean_queue.tsv`。
3. `14_run_mux_clean_queue.sh` 读取队列，执行字幕内封、验证、清理。

## 支持格式

自动队列只处理已经在执行器里验证过的格式：

- `.srt`
- `.ass`
- `.ssa`
- `.idx` + 同名 `.sub`

暂不自动处理：

- `.sup`
- `.vtt`
- `.smi`
- 没有同名 `.idx` 的 `.sub`
- 多电影、多 CD、花絮混杂、目标文件已存在等复杂情况

## 推荐命令

进入目录：

```bash
cd /Users/milou/Movies/FilmSubTitlePlan
```

只扫描，不改 NAS：

```bash
DRY_RUN=1 ./15_rescan_remaining_subtitles.py
```

预览移动字幕和重建队列：

```bash
DRY_RUN=1 ./16_prepare_remaining_mux_queue.py
```

真实移动纯字幕子文件夹里的字幕，并重建队列：

```bash
DRY_RUN=0 ./16_prepare_remaining_mux_queue.py
```

先 dry-run 第一条：

```bash
QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv RUN_LIMIT=1 ./14_run_mux_clean_queue.sh
```

真实执行前 5 条：

```bash
DRY_RUN=0 QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv RUN_LIMIT=5 PROGRESS_INTERVAL=60 ./14_run_mux_clean_queue.sh
```

继续执行 20 条：

```bash
DRY_RUN=0 QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv RUN_LIMIT=20 PROGRESS_INTERVAL=60 ./14_run_mux_clean_queue.sh
```

## 字幕编码规则

文本字幕会尝试多种编码，包括 `UTF-8`、`GB18030`、`GBK`、`BIG5/CP950`、`UTF-16`、`CP1250`、`CP1251`、`CP1252`、`ISO-8859-1` 等。脚本会按字幕格式、中文字符数量、替换字符、异常控制字符和常见 mojibake 特征打分。

中文字幕必须满足：解码后有足够中文字符，并且没有 `�` 这类替换字符。生成新 MKV 后，脚本还会把刚添加的文本字幕轨抽出来再检查一次。

无法可靠判断语言的字幕会标为 `und`。`und` 可以内封，但不会冒充中文轨；只有正文检测到足够中文字符时，才会升级为中文轨。

VobSub 是图片字幕，脚本只能验证轨道存在，不能 OCR 检查文字内容。

## 清理规则

真实执行时，只有在输出 MKV 验证通过后才会：

- 把新 MKV 移动到父文件夹。
- 删除源电影和已使用的外挂字幕。
- 删除脚本产生的临时文件。
- 尝试删除已经空掉的原电影文件夹。

如果 `mkvmerge` 报 invalid media data / 音画同步风险，脚本会把输出移动出来，但把源电影和字幕保留下来，并将队列标记为 `DONE_REVIEW`。

## 文件位置

- 当前队列：`/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv`
- 最新扫描报告：`/Users/milou/Movies/FilmSubTitlePlan/rescan-plan/`
- 运行日志：`/Users/milou/Movies/FilmSubTitlePlan/logs/run-mux-clean-queue.log`
- 历史文件：`/Users/milou/Movies/FilmSubTitlePlan/archive/`
