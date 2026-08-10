import os, re, shutil

root_dir = "/root/cv/online-cv"
includes_dir = os.path.join(root_dir, "_includes")
layouts_dir = os.path.join(root_dir, "_layouts")
site_dir = os.path.join(root_dir, "_site")

def get_include(name):
    path = os.path.join(includes_dir, name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def process_includes(text):
    def replace_inc(match):
        inc_file = match.group(1).strip()
        content = get_include(inc_file)
        return process_includes(content)
    pattern = r"\{%\s*include\s+([^\s%]+)\s*%\}"
    return re.sub(pattern, replace_inc, text)

def process_liquid(text, page_url=""):
    text = process_includes(text)
    # site variables
    text = text.replace("{{site.baseurl}}", "/online-cv")
    text = text.replace("{{ site.baseurl }}", "/online-cv")
    text = text.replace("{{site.name}}", "Kristof Stroobants")
    text = text.replace("{{ site.name }}", "Kristof Stroobants")
    text = text.replace("{{site.title}}", "Curriculum Vitae")
    text = text.replace("{{site.email}}", "kristofstroobants@gmail.com")
    text = text.replace("{{site.website}}", "kristofstroobants.github.io")
    text = text.replace("{{site.linkedin}}", "kristof-stroobants-1220106")
    text = text.replace("{{site.github}}", "kristofstroobants")
    text = text.replace("{% if site.pic %}{{ site.pic }}{% else %}profile.png{% endif %}", "profile-ghibli.png")

    # conditionals for page url
    if "projects" in page_url:
        text = text.replace("{% if page.url contains 'projects' %}active{% endif %}", "active")
        text = text.replace("{% if page.url contains 'projects' %}display: block; min-height: auto;{% endif %}", "display: block; min-height: auto;")
        text = re.sub(r"\{%\s*if page\.url contains 'projects'\s*%\}.*?\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}", "", text, flags=re.DOTALL)
    else:
        text = text.replace("{% if page.url contains 'projects' %}active{% endif %}", "")
        text = text.replace("{% if page.url contains 'projects' %}display: block; min-height: auto;{% endif %}", "")
        text = re.sub(r"\{%\s*if page\.url contains 'projects'\s*%\}.*?\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}", r"\1", text, flags=re.DOTALL)

    return text

# Build index.html
with open(os.path.join(root_dir, "index.html"), "r", encoding="utf-8") as f:
    idx_content = f.read()

idx_body = re.sub(r"^---.*?---", "", idx_content, flags=re.DOTALL)
idx_rendered = process_liquid(idx_body, page_url="/")

with open(os.path.join(layouts_dir, "default.html"), "r", encoding="utf-8") as f:
    layout_content = f.read()

layout_body = re.sub(r"^---.*?---", "", layout_content, flags=re.DOTALL)
full_index = layout_body.replace("{{content}}", idx_rendered)
full_index = process_liquid(full_index, page_url="/")

os.makedirs(site_dir, exist_ok=True)
with open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(full_index)

# Build projects.html
with open(os.path.join(root_dir, "projects.html"), "r", encoding="utf-8") as f:
    proj_content = f.read()

proj_body = re.sub(r"^---.*?---", "", proj_content, flags=re.DOTALL)
proj_rendered = process_liquid(proj_body, page_url="/projects.html")

full_projects = layout_body.replace("{{content}}", proj_rendered)
full_projects = process_liquid(full_projects, page_url="/projects.html")

with open(os.path.join(site_dir, "projects.html"), "w", encoding="utf-8") as f:
    f.write(full_projects)

# Copy assets and create online-cv subfolder for path compatibility
shutil.copytree(os.path.join(root_dir, "assets"), os.path.join(site_dir, "assets"), dirs_exist_ok=True)
os.makedirs(os.path.join(site_dir, "online-cv"), exist_ok=True)
shutil.copytree(os.path.join(root_dir, "assets"), os.path.join(site_dir, "online-cv", "assets"), dirs_exist_ok=True)
shutil.copyfile(os.path.join(site_dir, "index.html"), os.path.join(site_dir, "online-cv", "index.html"))
shutil.copyfile(os.path.join(site_dir, "projects.html"), os.path.join(site_dir, "online-cv", "projects.html"))
print("Build complete!")
