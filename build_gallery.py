# -*- coding: utf-8 -*-
"""
build_gallery.py — 从 photos.json 生成 index.html

用法:
    python build_gallery.py

加新照片的流程（详见 如何加照片.md）:
    1. 图片放进 dist/assets/photos/
    2. 在 photos.json 对应系列的 photos 数组里加一行
    3. 运行 python build_gallery.py
    4. git add -A && git commit -m "add photo" && git push
"""
import json
import html
from pathlib import Path

ROOT = Path(__file__).parent
PHOTOS_DIR = ROOT / "dist" / "assets" / "photos"
OUTPUT = ROOT / "index.html"

PAGE_HEAD = """<!DOCTYPE html>
<html lang="zh-CN" class="scroll-smooth">

<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>KEMA - 摄影作品集</title>
  <meta name="description"
    content="KEMA 的摄影作品集 —— 古建与寺庙、双重曝光、人文街拍、展览空间与日常光影。用镜头收集安静的瞬间。">
  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="dist/assets/favicon.ico" />
  <link rel="stylesheet" href="dist/output.css" />
  <link rel="stylesheet" href="styles.css" />
  <!-- Alpine.js（移动端菜单） -->
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <!-- Start - Fancybox 灯箱 -->
  <script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.css" />
  <!-- End - Fancybox -->
  <!-- Tailwind（自托管，国内访问快） -->
  <script src="dist/tailwindcdn.js"></script>
  <script>
    tailwind.config = {
      content: ["./dist/*.{html,js}"],
      theme: {
        extend: {
          fontFamily: {
            'signika': ['Signika', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', 'sans-serif'],
            'nothingyoucoulddo': ['Nothing You Could Do', 'Segoe Script', 'Brush Script MT', 'cursive'],
          },
        },
      },
      plugins: [],
    }
  </script>
</head>

<body
  class="dark:bg-black bg-white h-screen text-black dark:text-white px-5 md:px-20 opacity-0 animate-fade-in transition duration-500">
  <!-- Navbar -->
  <header class="flex w-full overflow-hidden pt-10 pb-1">
    <nav id="nav" x-data="{ open: false }" role="navigation" class="w-full">
      <div class="container mx-auto flex flex-wrap items-center md:flex-no-wrap">
        <div class="mr-4 md:mr-8">
          <a href="index.html" class="text-2xl font-signika font-bold">KEMA</a>
        </div>
        <div class="ml-auto md:hidden flex items-center justify-start">
          <button onclick="menuToggle()" @click="open = !open"
            class="tap-highlight-transparent text-black dark:text-white w-5 h-5 relative focus:outline-none"
            @click="open = !open">
            <span class="sr-only">Open main menu</span>
            <div class="block w-5 absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
              <span aria-hidden="true"
                class="block absolute h-0.5 w-5 bg-current transform transition duration-500 ease-in-out"
                :class="{'rotate-45': open,' -translate-y-1.5': !open }"></span>
              <span aria-hidden="true"
                class="block absolute  h-0.5 w-5 bg-current   transform transition duration-500 ease-in-out"
                :class="{'opacity-0': open } "></span>
              <span aria-hidden="true"
                class="block absolute h-0.5 w-5 bg-current transform  transition duration-500 ease-in-out"
                :class="{'-rotate-45': open, ' translate-y-1.5': !open}"></span>
            </div>
          </button>
        </div>
        <div id="menu"
          class="w-full h-0 transition-all ease-out duration-500 md:transition-none md:w-auto md:flex-grow md:flex md:items-center">
          <ul id="ulMenu"
            class="flex flex-col duration-300 ease-out md:space-x-5 sm:transition-none mt-5 md:flex-row md:items-center md:ml-auto md:mt-0 md:pt-0 md:border-0">
            <li class="group transition duration-300">
              <a href="index.html" class="font-signika text-2xl tap-highlight-transparent">作品
                <span class="hidden md:block h-0.5 bg-black dark:bg-white"></span>
              </a>
            </li>
            <li class="group transition duration-300">
              <a href="dist/about_me.html" class="font-signika text-2xl tap-highlight-transparent">关于
                <span
                  class="hidden md:block max-w-0 group-hover:max-w-full transition-all duration-500 h-0.5 bg-black dark:bg-white"></span>
              </a>
            </li>
            <li class="group transition duration-300">
              <a href="dist/contact.html" class="font-signika text-2xl tap-highlight-transparent">联系
                <span
                  class="hidden md:block max-w-0 group-hover:max-w-full transition-all duration-500 h-0.5 bg-black dark:bg-white"></span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
  <!-- Content -->
  <div class="container mx-auto">
    <h1 class="text-4xl pt-10 pb-4 font-bold">摄影作品 <span class="text-2xl text-gray-500 dark:text-gray-400">PHOTOGRAPHY</span></h1>
    <p class="pb-6 text-gray-600 dark:text-gray-300">古建 · 光影 · 双重曝光 · 日常的安静瞬间 —— 点击任意照片查看大图。</p>

    <!-- 系列导航 -->
    <div class="flex flex-wrap gap-2 pb-10">
{NAV_ITEMS}
    </div>

{SECTIONS}
  </div>
  <!-- Footer -->
  <footer>
    <div class="max-w-screen-xl py-16 mx-auto">
      <div class="grid grid-cols-1 gap-8 text-center mx-auto">
        <div>
          <p class="font-signika"><b>KEMA</b></p>
          <p class="mt-4 text-sm text-gray-600 dark:text-gray-300">
            摄影 · 用镜头收集安静的瞬间<br />
            <a href="mailto:kemakiko9566@gmail.com" class="underline">kemakiko9566@gmail.com</a>
          </p>
          <div class="flex mx-auto">
            <div class="mx-auto space-x-6 flex mt-8 text-gray-600 dark:text-gray-300">
              <a class="transition duration-300 hover:opacity-75" href="https://github.com/kemakiko9566-design"
                target="_blank" rel="noreferrer">
                <span class="sr-only">GitHub</span>
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 16 16" aria-hidden="true">
                  <path
                    d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z" />
                </svg>
              </a>
              <a class="transition duration-300 hover:opacity-75" href="mailto:kemakiko9566@gmail.com" rel="noreferrer">
                <span class="sr-only">Email</span>
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 16 16" aria-hidden="true">
                  <path
                    d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697Zm6.761 4.04L.191 12.68A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.317l-6.57-3.943L8 9.586l-1.239-.85ZM16 11.801V4.697l-5.803 3.558L16 11.801Z" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
      <p class="mt-8 text-xs text-gray-600 dark:text-gray-300 text-center">
        © 2026 Photos & built by KEMA · 模板基于
        <a href="https://github.com/JoaoFranco03/photography-portfolio" class="underline">photography-portfolio</a>
        (GPL-3.0) 修改
      </p>
    </div>
  </footer>
  <!-- Script for the LightBox -->
  <script>
    Fancybox.bind("[data-fancybox]", {});
  </script>
  <script src="dist/fade_in.js"></script>
  <script src="dist/menu.js"></script>
</body>

</html>
"""

NAV_ITEM = '''      <a href="#series-{sid}"
        class="text-sm px-4 py-1.5 rounded-full border border-gray-300 dark:border-neutral-700 hover:bg-black hover:text-white dark:hover:bg-white dark:hover:text-black transition duration-300">{title}</a>'''

SECTION = '''    <!-- ============ 系列 · {title} ============ -->
    <section id="series-{sid}" class="pb-16 scroll-mt-8">
      <div class="flex items-baseline gap-3 mb-1">
        <h2 class="text-2xl font-bold">{title}</h2>
        <span class="text-sm text-gray-500 dark:text-gray-400">{subtitle}</span>
      </div>
      <p class="text-gray-600 dark:text-gray-300 mb-6">{description}</p>
      <div class="grid {grid} gap-4">

{FIGURES}
      </div>
    </section>'''

FIGURE = '''        <figure class="group relative overflow-hidden">
          <a href="dist/assets/photos/{file}" data-fancybox="{sid}"
            data-caption="{title}">
            <img alt="{alt}"
              class="block w-full object-cover object-center transition duration-500 transform scale-100 hover:scale-105"
              src="dist/assets/photos/{file}" />
          </a>
          <figcaption
            class="opacity-0 group-hover:opacity-100 transition duration-300 absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-3">
            <span class="text-white text-sm">{title}</span>
          </figcaption>
        </figure>'''


def build():
    data = json.loads((ROOT / "photos.json").read_text(encoding="utf-8"))

    missing = []
    nav_parts, section_parts = [], []
    for series in data["series"]:
        sid = series["id"]
        nav_parts.append(NAV_ITEM.format(sid=sid, title=html.escape(series["title"])))

        figures = []
        for p in series["photos"]:
            if not (PHOTOS_DIR / p["file"]).exists():
                missing.append(p["file"])
            figures.append(FIGURE.format(
                file=html.escape(p["file"]),
                sid=sid,
                title=html.escape(p["title"]),
                alt=html.escape(p.get("alt", p["title"])),
            ))

        section_parts.append(SECTION.format(
            sid=sid,
            title=html.escape(series["title"]),
            subtitle=html.escape(series.get("subtitle", "")),
            description=html.escape(series.get("description", "")),
            grid=series.get("grid", "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"),
            FIGURES="\n\n".join(figures),
        ))

    page = PAGE_HEAD.replace("{NAV_ITEMS}", "\n".join(nav_parts)).replace(
        "{SECTIONS}", "\n\n".join(section_parts))
    OUTPUT.write_text(page, encoding="utf-8")

    total = sum(len(s["photos"]) for s in data["series"])
    print(f"OK: 生成 {OUTPUT.name}（{len(data['series'])} 个系列 / {total} 张照片）")
    if missing:
        print("警告: 以下图片文件不存在，请检查 photos.json 或补图:")
        for m in missing:
            print(f"  - {m}")


if __name__ == "__main__":
    build()
