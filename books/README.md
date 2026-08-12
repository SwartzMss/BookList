# Books

这个目录按“能拿到实体文件就优先拿实体文件”的原则管理电子书。

## 目录约定

- `public-domain/`：已确认属于公版或可公开再分发的版本。可以加入 Git 仓库。
- `local-only/`：来源官方允许下载，但没有确认允许再分发的版本。只下载到你自己的本地仓库，**不要提交到公开 GitHub 仓库**。
- 借阅、Preview Only、购买类电子书不下载文件，只在根目录 `ebook-sources.md` 中保存入口。

## 一键同步到本地仓库

在仓库根目录执行：

```bash
python3 scripts/sync_books.py
```

目前会下载：

| 原书单序号 | 书 | 版本 | 本地位置 |
|---:|---|---|---|
| 18 | 《金融的本质》 | Bernanke 2012 四场官方讲座 PDF（对应原书讲座来源，**不是中文译本电子书**） | `books/local-only/18-Federal-Reserve-and-Financial-Crisis/` |
| 40 | 《股票作手回忆录》 | *Reminiscences of a Stock Operator*，英文公版 EPUB | `books/public-domain/` |
| 47 | 《世界经济简史》 | Max Weber *Wirtschaftsgeschichte*，1923 德文原版 PDF | `books/public-domain/` |
| 54 | 《乌合之众》 | *The Crowd*，英文公版 EPUB | `books/public-domain/` |
| 62 | 《美国大萧条》 | *America's Great Depression*，Mises Institute 官方 EPUB + PDF | `books/local-only/` |
| 80 | 《地理与世界霸权》 | *Geography and World Power*，1915 英文公版 PDF | `books/public-domain/` |
| 81 | 《逻辑学入门》 | 原书 *How Logic Works* 作者公开的 LaTeX 源码 ZIP；可在本地尝试编译 PDF | `books/local-only/81-How-Logic-Works-Hans-Halvorson/` |

> 第 47 本还定位到了 Max Weber *General Economic History* 的 1927 年 Frank H. Knight 英译扫描线索。The Online Books Page / HathiTrust 有页面图像入口，但目前没有确认一个适合 GitHub Actions 稳定直拉、且无需登录/交互的 PDF URL，所以暂不替换仓库里的 1923 德文版。
>
> 现代中文译本不因为原著或旧版进入公版而自动成为公版，因此暂不把现代中文译本放入公开仓库。
>
> 第 18 本暂时没有找到可合法保存的中文完整电子书，所以先保存 Federal Reserve Board 官方发布的四场讲座 PDF。它们是该书内容的直接来源材料，但不是出版后的中文电子书。
>
> 第 81 本的作者 Hans Halvorson 在个人课程/图书页面直接提供了 `logic-works` 的 LaTeX 源码入口，但该 GitHub 仓库目前没有 `LICENSE` 文件。因此这里按保守策略只下载到 `local-only`，不把源码或本地编译出的 PDF 提交到公开仓库。

### 第 81 本：本地编译 PDF

先同步：

```bash
python3 scripts/sync_books.py --scope local-only
```

如果本机有完整 TeX Live、`latexmk` 和 `unzip`，可以尝试：

```bash
bash scripts/build_how_logic_works.sh
```

成功后会生成：

```text
books/local-only/81-How-Logic-Works-Hans-Halvorson/81-How-Logic-Works-Hans-Halvorson.pdf
```

这个 PDF 仍然只放本地，不进入公开 Git 仓库。

只下载可以公开提交的公版文件：

```bash
python3 scripts/sync_books.py --scope public-domain
```

只下载本地使用、不应提交 Git 的官方免费版本/官方配套材料：

```bash
python3 scripts/sync_books.py --scope local-only
```

## 为什么不把所有 PDF / EPUB 都直接提交？

这个仓库是公开仓库。“网站允许免费阅读或免费下载”与“允许你把文件重新发布到自己的 GitHub 仓库”不是一回事。

因此这里区分：

1. **确认可再分发** → 文件可以进入仓库。
2. **官方可下载，但版权或其中部分素材的再分发权限未确认** → 脚本下载到 `local-only/`，Git 忽略。
3. **只能借阅/预览/购买** → 仅保留在线入口。

后续找到新的合法来源时，继续往 `scripts/sync_books.py` 中增加即可。
