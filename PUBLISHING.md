# Публикация digitarium.cc

Замена старого Jekyll-сайта на новый статический сайт из этого репозитория.

**Раскладка после миграции:**

| Папка | Что это | Репозиторий на GitHub |
|---|---|---|
| `~/Sites/digitarium_builder` | исходники сайта + `parser.py` | (пока локальный) |
| `~/Sites/digitarium` | собранный сайт | `pyotr777/digitarium` → GitHub Pages |
| `~/Sites/digitarium_jekyll` | старый Jekyll-сайт | `pyotr777/digitarium_jekyll` |

---

## Шаг 0. Локальная уборка

```bash
cd ~/Sites/digitarium_builder
rmdir rawsite/pages          # осталась пустой после переноса страниц в корень
rm -rf site                  # сборка теперь уходит в ~/Sites/digitarium
```

## Шаг 1. Зафиксировать исходники

`.gitignore` переписан: теперь отслеживаются картинки, PDF, CSV и `parser.py`,
а собранный сайт (`site/`) исключён.

```bash
cd ~/Sites/digitarium_builder
git add -A
git commit -m "Restructure URLs to match the old Jekyll site"
```

## Шаг 2. Собрать сайт

```bash
mkdir -p ~/Sites/digitarium
cd ~/Sites/digitarium_builder
python3 parser.py rawsite -o ~/Sites/digitarium
```

`CNAME` лежит в `rawsite/`, поэтому копируется в сборку автоматически.

Проверить локально:

```bash
cd ~/Sites/digitarium && python3 -m http.server 8000
# открыть http://localhost:8000/
```

## Шаг 3. Освободить домен у старого репозитория

**Это обязательно до шага 5** — GitHub не даёт привязать один домен к двум репозиториям.

1. `https://github.com/pyotr777/digitarium` → Settings → General → Repository name → переименовать в **`digitarium_jekyll`** → Rename.
   GitHub оставит редиректы со старого адреса, локальный клон продолжит работать.
2. Там же → Settings → Pages → Custom domain → очистить поле → Save.
3. Удалить файл `CNAME` из репозитория:

```bash
cd ~/Sites/digitarium_jekyll
git remote set-url origin https://github.com/pyotr777/digitarium_jekyll.git
git rm CNAME && git commit -m "Move digitarium.cc to the new site" && git push
```

## Шаг 4. Создать новый репозиторий и залить сайт

1. На GitHub: New repository → имя **`digitarium`**, публичный, **без** README, .gitignore и лицензии.
2. Локально:

```bash
cd ~/Sites/digitarium
touch .nojekyll              # отключает обработку Jekyll на стороне GitHub
git init
git branch -M main
git add -A
git commit -m "New Digitarium site"
git remote add origin https://github.com/pyotr777/digitarium.git
git push -u origin main
```

Проверить, что `CNAME` и `.nojekyll` попали в коммит:

```bash
git ls-files | grep -E 'CNAME|nojekyll'
```

## Шаг 5. Включить GitHub Pages

`https://github.com/pyotr777/digitarium` → Settings → Pages:

1. Source: **Deploy from a branch**, ветка `main`, папка `/ (root)` → Save.
2. Custom domain: `digitarium.cc` → Save. Дождаться зелёной галочки DNS check.
3. Поставить галочку **Enforce HTTPS** (появится через несколько минут, после выпуска сертификата).

## Шаг 6. Сбросить кэш Cloudflare

Домен проксируется через Cloudflare — старые страницы могут отдаваться из кэша.
Cloudflare → домен `digitarium.cc` → Caching → Configuration → **Purge Everything**.

## Шаг 7. Проверить адреса

Все старые URL должны работать:

```
https://digitarium.cc/
https://digitarium.cc/tags/
https://digitarium.cc/blog/
https://digitarium.cc/page2/                      → редирект на /
https://digitarium.cc/docker-network-performance/
https://digitarium.cc/connect-virtualbox-vms/
https://digitarium.cc/docker-ecosystem/
https://digitarium.cc/bash-expanding-variables-in-text/
https://digitarium.cc/cloud-gpu-providers-comparison/
https://digitarium.cc/cloud-gpu-providers-more-graphs/
https://digitarium.cc/horovod-on-nvidia-jetson/
https://digitarium.cc/pandemic-travel-ru/
https://digitarium.cc/pandemic-travel-jp/
```

Новые адреса, которых не было раньше: `/blog/ru/`, `/blog/jp/`.

## Обновление сайта в дальнейшем

```bash
cd ~/Sites/digitarium_builder
# правки в rawsite/...
python3 parser.py rawsite -o ~/Sites/digitarium
git add -A && git commit -m "..." && git push          # исходники

cd ~/Sites/digitarium
git add -A && git commit -m "Rebuild" && git push      # сайт
```

---

## Откат

Если что-то пошло не так, вернуть старый сайт:

1. `pyotr777/digitarium_jekyll` → вернуть файл `CNAME` с содержимым `digitarium.cc`, запушить.
2. Settings → Pages → Custom domain → `digitarium.cc` → Save.
3. В новом репозитории `digitarium` — убрать custom domain.
4. Purge cache в Cloudflare.

## Осталось решить

- **`/feed.xml`** — в `<head>` каждой страницы есть ссылка на RSS, но файла нет.
  Либо генерировать фид в `parser.py`, либо убрать ссылку.
- **`/sitemap.xml`** — был у Jekyll (плагин `jekyll-sitemap`), сейчас отсутствует.
- **`/404.html`** — GitHub Pages отдаёт свою стандартную страницу.
- **Старые адреса картинок** — в старом сайте картинки лежали по
  `/wp-content/uploads/2014/06/*.png`, теперь по `/<слаг>/images/*.png`.
  Внешние ссылки на картинки и выдача Google Images перестанут работать.
