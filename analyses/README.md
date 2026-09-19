# analyses/ 逐库分析目录

规则（对齐 `../ANALYSIS_TEMPLATE.md` 与 PLAN v2）：

- 文件名：`owner__repo.md`（斜杠换双下划线，如 `yibie__awesome-jev.md`）
- 收录条件：批次归位 = B1~B6 且过本批"晋级深读"或"逐库建档"门槛的库；只扫读库**不建单库档**，直接进 FINAL 矩阵行
- 每份文档必须填满模板 7 节，第 6 节（与本地 jev_eval.py 链路映射）不允许写「无」——真无映射就据此降为丢弃
- 状态前缀：`STATUS: 深采|浅采|丢弃`，FINAL 汇总时以 grep STATUS 为准

清单来源：`../eval/inventory.csv`（**259 库**，v7 修订：存在性翻案后删 5 条分类器假阳性，见 `../reports/batch03.md` §五与 `../reports/b0_review.md` I9；历史：v4 winnow B1→B5、v5 foreman→B4、v6 剔 tests/* 垃圾行；存在性已按正确通道重验 256/259，旧“266/266”结论作废）

已建档（11）：B1 深读 kev/decider/openjev；B2 深读 jev-ultrafast/jev-drone；B3 深读 abhixhek__jevcal、zhuyansen__jev-search-rerank-eval；B5 深读 danrwilloughby__snifftest、coldteadotai__abide；B4 深读（晋级）devmortimer__pi-warden；B6 深读（晋级）kyotofin__tax-doc-classifier
