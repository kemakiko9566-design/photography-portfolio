# KEMA · 摄影作品集

纯静态摄影展示站（HTML + Tailwind + Fancybox 灯箱），部署在 GitHub Pages。
线上地址：<https://kemakiko9566-design.github.io/photography-portfolio/>

## 目录结构

```
photography-portfolio/
├── index.html            ← 首页（由脚本生成，不要手改！）
├── photos.json           ← 照片清单（加照片改这里）
├── build_gallery.py      ← 生成脚本（读 photos.json → 产出 index.html）
├── dist/
│   ├── about_me.html     ← 关于页（手写页面）
│   ├── contact.html      ← 联系页（手写页面）
│   ├── tailwindcdn.js    ← Tailwind 自托管脚本
│   ├── output.css        ← 模板预编译样式
│   └── assets/photos/    ← 全部照片
└── src/input.css         ← Tailwind 源文件（改样式才需要动）
```

## 如何加一张照片（3 步）

1. 把图片放进 `dist/assets/photos/`，命名建议 `系列缩写-描述.jpg`（如 `temple-sunset.jpg`）。
2. 打开 `photos.json`，在对应系列的 `photos` 数组里加一行：
   ```json
   { "file": "temple-sunset.jpg", "title": "夕照", "alt": "香积寺夕照" }
   ```
   - 想新建一个系列：复制现有某个 series 块，改 `id`/`title`/`description` 即可，顶部导航自动生成。
   - 数组内的顺序 = 页面显示顺序，调换位置即可排序。
3. 运行生成脚本，然后推送：
   ```
   python build_gallery.py
   git add -A && git commit -m "add photo" && git push
   ```

脚本会自动校验：photos.json 里引用了但目录里不存在的文件会打警告。

## 如何改样式

- 布局/内容：改 `build_gallery.py` 里的模板常量（PAGE_HEAD / SECTION / FIGURE），重新运行生成。
- 颜色/间距微调：改 `src/input.css` 后需要重新编译 Tailwind（进阶，不常用）；或直接改 `dist/output.css`。
- 关于页/联系页是手写页面，直接编辑 `dist/about_me.html`、`dist/contact.html`。

## 技术说明

- Tailwind 已自托管（`dist/tailwindcdn.js`），不依赖 cdn.tailwindcss.com；字体走系统栈，无 Google Fonts 依赖 → 国内访问无墙外资源。
- Fancybox（灯箱）与 Alpine.js（移动端菜单）来自 jsdelivr CDN，如需完全离线可再自托管。
- 模板基于 [JoaoFranco03/photography-portfolio](https://github.com/JoaoFranco03/photography-portfolio)（GPL-3.0）修改。
