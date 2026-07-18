# Film Subtitle Plan

本项目是一套在 Mac 上运行的本地脚本，用来整理 NAS 里的电影文件夹，把外挂字幕软封进 MKV，并在验证通过后清理原始散文件。

目标目录主要是：

- `/Volumes/导演们`
- `/Volumes/分类`

处理原则：

- 不重新编码视频。
- 使用 `mkvmerge` remux / mux 字幕。
- 文本字幕会先做编码判断并转成 UTF-8。
- 新 MKV 生成后会抽取刚添加的文本字幕做乱码检查。
- `.idx` + 同名 `.sub` 会作为 VobSub 图片软字幕处理。
- `.sup`、`.vtt`、`.smi`、单独 `.sub` 不自动处理。

## 当前文件

- `14_run_mux_clean_queue.sh`: 执行队列，生成 MKV、验证字幕、清理已验证源文件。
- `15_rescan_remaining_subtitles.py`: 重新扫描剩余字幕，生成审计报告。
- `16_prepare_remaining_mux_queue.py`: 移动纯字幕子文件夹里的字幕，并生成剩余处理队列。
- `remaining_mux_clean_queue.tsv`: 当前剩余处理队列。
- `rescan-plan/`: 最新扫描结果。
- `docs/`: 阶段性说明和历史状态。
- `archive/`: 旧脚本、旧队列、旧报告，仅作留档。
- `logs/`: 本地运行日志，不提交到 GitHub。
- `tools/`: 本地工具，不提交到 GitHub。

## 快速使用

进入项目目录：

```bash
cd /Users/milou/Movies/FilmSubTitlePlan
```

重新扫描，先只生成报告，不改 NAS：

```bash
DRY_RUN=1 ./15_rescan_remaining_subtitles.py
```

预览字幕移动和队列生成：

```bash
DRY_RUN=1 ./16_prepare_remaining_mux_queue.py
```

确认后真实移动纯字幕子文件夹里的字幕，并重建队列：

```bash
DRY_RUN=0 ./16_prepare_remaining_mux_queue.py
```

先 dry-run 第一条队列：

```bash
QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv RUN_LIMIT=1 ./14_run_mux_clean_queue.sh
```

真实跑小批量：

```bash
DRY_RUN=0 QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv RUN_LIMIT=5 PROGRESS_INTERVAL=60 ./14_run_mux_clean_queue.sh
```

继续跑更大批量：

```bash
DRY_RUN=0 QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv RUN_LIMIT=20 PROGRESS_INTERVAL=60 ./14_run_mux_clean_queue.sh
```

查看队列状态：

```bash
awk -F '\t' 'NR>1{c[$1]++} END{for(k in c) print k, c[k]}' remaining_mux_clean_queue.tsv
```

## 安全边界

脚本只会在验证通过后清理源文件。遇到字幕乱码、工具警告、音画同步风险、无法判断的 `.sub`/`.sup` 等情况，会标记为 `FAILED` 或 `DONE_REVIEW`，不会强行删除源文件。
