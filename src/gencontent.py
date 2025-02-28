import os
from blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, base_path):
    lst = os.listdir(dir_path_content)
    for i in lst:
        current = os.path.join(dir_path_content, i)
        if os.path.isfile(current):
            # Read the markdown content
            with open(current, "r") as from_file:
                markdown_content = from_file.read()

            # Read the template content
            with open(template_path, "r") as template_file:
                template = template_file.read()

            node = markdown_to_html_node(markdown_content)
            html = node.to_html()
            
            title = extract_title(markdown_content)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)
            template = template.replace(f'href="/', f'href="{base_path}')
            template = template.replace(f'src="/', f'src="{base_path}')

            filename = os.path.basename(current)  # Get the filename (e.g., "file.md")
            filename_without_ext = os.path.splitext(filename)[0]  # Remove the ".md" extension
            dest_file_path = os.path.join(dest_dir_path, f"{filename_without_ext}.html")
            
            os.makedirs(dest_dir_path, exist_ok=True)
            with open(dest_file_path, "w") as to_file:
                to_file.write(template)
            print(f"Generated: {dest_file_path}")
        else:
            sub_dest_dir = os.path.join(dest_dir_path, i)
            generate_pages_recursively(current, template_path, sub_dest_dir, base_path)



def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")