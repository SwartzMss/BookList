# 全书单覆盖审计（2026-08-13）

## 结论

原始截图编号范围为 `1..101`，但没有 #10，因此共有 **100 个编号记录**。其中 #24 与 #57 都是《股市真规则》，所以共有 **99 个不同书目**。

把初始扫描与 Round 2～Round 10 的研究记录合并后，唯一此前没有被系统覆盖的编号是 **#8《大国大城》**。本次补查 #8 后，当前覆盖率为：

- 编号记录：**100 / 100**
- 不同书目：**99 / 99**
- 未核对编号：**0**

## #8 《大国大城》补查

确认信息：

- 作者：陆铭
- 书名：《大国大城：当代中国的统一、发展与平衡》
- ISBN：`9787208138636`
- 2016 年出版
- 正版数字版已确认存在，但属于商业/平台授权，不是自由下载文件。

可用正版入口：

- Google Play Books：<https://play.google.com/store/books/details/%E9%99%86%E9%93%AD_%E5%A4%A7%E5%9B%BD%E5%A4%A7%E5%9F%8E?id=TdMsEQAAQBAJ>
- 豆瓣阅读：<https://read.douban.com/ebook/29567579/>
- 得到：<https://www.dedao.cn/ebook/detail?id=bODoM61kAj9Rql84gzG5nVNZopXKY3DqOKwJLrBmEDv2QPMOyx7a6e1dbPQj2Zdm>
- 华艺电子书：<https://www.airitibooks.com/Publication/Details?publicationID=P20240902270>

华艺页面明确标注阅读格式为 EPUB，但仍属于授权数字阅读，因此不把平台文件导出到 `books/local-only/`，更不会重新上传到公开仓库。

## 当前实体文件状态

### 已进入公开仓库

已实际核验 `books/public-domain/`，当前存在 4 个公版实体文件：

1. #40 `40-Reminiscences-of-a-Stock-Operator.epub`
2. #47 `47-Wirtschaftsgeschichte-Max-Weber-1923-de.pdf`
3. #54 `54-The-Crowd.epub`
4. #80 `80-Geography-and-World-Power.pdf`

### 可同步到 local-only

当前 `scripts/sync_books.py` 还支持以下不公开提交的内容：

- #18：Bernanke 2012 四场官方讲座 PDF。它们是《金融的本质》的直接来源材料，但**不是中文译本整书**。
- #62：Mises Institute 官方提供的 *America's Great Depression* EPUB + PDF。
- #81：Hans Halvorson 作者公开的 *How Logic Works* LaTeX 源码 ZIP；仓库未看到明确 LICENSE，因此保守放入 `local-only`，可在本地尝试编译 PDF。

## 需要长期保留的元数据说明

以下条目不应直接按原截图文字当作最终标准书目：

| # | 问题 | 当前结论 |
|---:|---|---|
| 19 | 《国力大循环》未找到可靠正式出版记录 | 高度疑似对应贾根良《国内大循环：经济发展新战略与政策选择》；暂不静默改原始 README |
| 21 | 作者不完整 | *Virtual Competition* 作者为 Ariel Ezrachi 与 Maurice E. Stucke |
| 24 / 57 | 重复 | 两个编号都是《股市真规则》 |
| 25 | 英文原书曾映射错 | 正确为 John Steele Gordon 的 *The Great Game*，不是 *An Empire of Wealth* |
| 34 | 作者字段错误 | 《一往无前》正式作者为范海涛；雷军为亲述者 |
| 35 | 版本/作者需区分 | 2019 中信《大历史》为 David Christian + DK，不能与《时间地图》等其他“大历史”作品混同 |
| 40 | 原截图作者归属有误 | *Reminiscences of a Stock Operator* 原作者为 Edwin Lefèvre，不是 Jesse Livermore |
| 47 | 中文译名/人名 | Max Weber 常译“马克斯·韦伯”；仓库保存的是 1923 德文 *Wirtschaftsgeschichte* |
| 51 | 英文映射曾经错误 | 《真相》对应 *Blur*，不是 *The Elements of Journalism* |
| 56 | 作者不完整 | *Money Capital* 作者为 Patrick Bolton 与 Haizhou Huang |
| 59 | 原书映射曾经错误 | 《投资的护城河》对应 *Why Moats Matter*，作者 Heather Brilliant 与 Elizabeth Collins |
| 63 | 单本/丛书不明 | “国防军”常指 Robert M. Citino 的三部曲，不能直接强行对应第一册 |
| 67 | 丛书作者关系 | 《哈佛中国史》是 Timothy Brook 主编的六卷系列，不是卜正民单独著作 |
| 69 | 中文题名映射不足 | 候选是 Robert D. Kaplan 的 *The Revenge of Geography*，但仍保留待确认标记 |
| 72 | 作者拼写与合著者 | 应为 Daron Acemoglu 与 James A. Robinson |
| 86 | 题名高度疑似有误 | 可靠书目指向《全球化逆潮》 / *Globalization and Its Discontents Revisited* |
| 90 | 作者字段不完整 | 正式责任者还包括刘健芝、黄钰书、薛翠 |

## 覆盖来源

研究记录：

- [`scan-2026-08-12.md`](scan-2026-08-12.md)
- [`scan-2026-08-12-round2.md`](scan-2026-08-12-round2.md)
- [`scan-2026-08-12-round3.md`](scan-2026-08-12-round3.md)
- [`scan-2026-08-12-round4.md`](scan-2026-08-12-round4.md)
- [`scan-2026-08-13-round5.md`](scan-2026-08-13-round5.md)
- [`scan-2026-08-13-round6.md`](scan-2026-08-13-round6.md)
- [`scan-2026-08-13-round7.md`](scan-2026-08-13-round7.md)
- [`scan-2026-08-13-round8.md`](scan-2026-08-13-round8.md)
- [`scan-2026-08-13-round9.md`](scan-2026-08-13-round9.md)
- [`scan-2026-08-13-round10.md`](scan-2026-08-13-round10.md)

统一结果见仓库根目录 [`catalog.md`](../catalog.md)。

## 后续维护方式

后续不再需要按“Round 11、12……”无限增加零散文件。建议以 `catalog.md` 为主索引：

1. 找到新的合法实体文件时，先核实版权/再分发条件。
2. 可公开再分发的加入 `books/public-domain/`。
3. 官方允许个人下载、但再分发许可不明确的加入 `scripts/sync_books.py` 的 `local-only`。
4. Borrow / DRM / Preview / 平台阅读只更新 `catalog.md` 和来源入口。
5. 元数据纠正保留原截图与标准书目两套信息，避免把历史输入静默覆盖。
