import argparse
import contextlib
import io
import os
import re
import shutil
import sys
import textwrap

from bs4 import BeautifulSoup

version = "0.3.1"
description = f"Build a static site from a directory of HTML files with Python inserts. {sys.argv[0]} version {version}"

# Directory whose files are only for include(), never copied to the output
INCLUDES_DIR = "_include"

script_re = re.compile(
    r'<script\s+type=["\']text/python["\']\s*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)

# Files currently being rendered, to detect include() cycles
_render_stack: list[str] = []

# Names always present in an insert's namespace; include() parameters cannot shadow them
RESERVED_NAMES = {"soup", "include", "params", "__file__", "page_file"}


def render_file(filepath, params=None):
    """Execute python inserts in an html file and return the rendered html text.

    params are made available to the inserts of this file: both as
    individual variables and as the `params` dict (for defaults via .get()).
    """
    filepath = os.path.abspath(filepath)
    if filepath in _render_stack:
        chain = " -> ".join(_render_stack + [filepath])
        raise RecursionError(f"Circular include: {chain}")
    params = dict(params or {})
    reserved = RESERVED_NAMES & params.keys()
    if reserved:
        raise ValueError(f"Parameter names {sorted(reserved)} are reserved (in include of {filepath})")
    _render_stack.append(filepath)
    try:
        with open(filepath, encoding="utf-8") as f:
            source = f.read()

        # Read-only view of the source document for the inserts;
        # changes made to it do not affect the output file
        soup = BeautifulSoup(source, "html.parser")
        basedir = os.path.dirname(filepath)

        def include(filename, **inc_params):
            # Paths are relative to the file that calls include()
            included = os.path.normpath(os.path.join(basedir, filename))
            html = render_file(included, inc_params)
            return html, BeautifulSoup(html, "html.parser")

        # Shared namespace for all inserts of this file;
        # included files get their own namespace (fresh call to render_file)
        # page_file is the top-level page being rendered (the same in all
        # includes), so an included template can compute paths relative to it
        namespace = {"soup": soup, "include": include, "__file__": filepath, "params": params, "page_file": _render_stack[0]}
        namespace.update(params)

        chunk_no = 0

        def run_chunk(match):
            nonlocal chunk_no
            chunk_no += 1
            code = textwrap.dedent(match.group(1))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(compile(code, f"{filepath} (insert #{chunk_no})", "exec"), namespace)
            return buf.getvalue()

        # Replacement happens in the source text, not through soup,
        # so everything outside the inserts stays byte-for-byte intact
        return script_re.sub(run_chunk, source)
    finally:
        _render_stack.pop()


def build_site(srcdir, outdir):
    """Render every html file and copy everything else from srcdir to outdir."""
    srcdir = os.path.abspath(srcdir)
    outdir = os.path.abspath(outdir)
    if srcdir == outdir:
        raise ValueError("Source and output directories must differ")
    this_script = os.path.abspath(__file__)
    os.makedirs(outdir, exist_ok=True)

    for root, dirs, files in os.walk(srcdir):
        # Skip _includes, hidden dirs and the output dir itself
        dirs[:] = [d for d in dirs if d != INCLUDES_DIR and not d.startswith('.') and os.path.join(root, d) != outdir]
        target_root = os.path.join(outdir, os.path.relpath(root, srcdir))
        os.makedirs(target_root, exist_ok=True)
        for name in files:
            src = os.path.join(root, name)
            if name.startswith('.') or src == this_script:
                continue
            dst = os.path.join(target_root, name)
            if name.lower().endswith(('.html', '.htm')):
                print(f"Rendering {os.path.relpath(src, srcdir)}...", end=' ')
                html = render_file(src)
                with open(dst, "w", encoding="utf-8") as f:
                    f.write(html)
                print("done")
            else:
                shutil.copy2(src, dst)
    print(f"Site written to {outdir}")


def main(args_main):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('dir', nargs='?', default='.', help='Site source directory')
    parser.add_argument('--output', '-o', type=str, default="tmp", help='Output directory')
    args = parser.parse_args(args_main)

    build_site(args.dir, args.output)


if __name__ == '__main__':
    main(sys.argv[1:])
