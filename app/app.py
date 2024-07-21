from flask import Flask, render_template
import os

app = Flask(__name__)

# Path to your Obsidian vault
OBSIDIAN_VAULT_PATH = '/Users/akbarakbariesfahani/Documents/obsidian_valuts/VulcanMindVault'
PROJECT_PAGE_FILENAME = 'mission_control.md'  # Adjust as needed

# Function to read markdown file from Obsidian vault
def read_obsidian_page():
    try:
        file_path = os.path.join(OBSIDIAN_VAULT_PATH, PROJECT_PAGE_FILENAME)
        with open(file_path, 'r') as file:
            content = file.read()
            # Clean up and parse the content
            html_content = parse_markdown_content(content)
            return html_content
    except Exception as e:
        return f"Failed to read Obsidian page: {e}"

def parse_markdown_content(content):
    # Replace kanban specific tags
    content = content.replace("kanban-plugin: basic", "")
    content = content.replace("%% kanban:settings {\"kanban-plugin\":\"basic\"} %%", "")

    sections = {
        "Backlogged": [],
        "ToDo": [],
        "In Progress": [],
        "Completed": []
    }
    current_section = None

    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('## '):
            section_name = line[3:]
            if section_name in sections:
                current_section = section_name
        elif current_section and line.startswith('- '):
            sections[current_section].append(line)

    section_colors = {
        "Backlogged": "#ffcccc",
        "ToDo": "#ffe0cc",
        "In Progress": "#cce6ff",
        "Completed": "#ccffcc"
    }

    table_html = """
    <table border='1' cellpadding='5' cellspacing='0' style='width: 100%; table-layout: fixed;'>
        <tr>
            <th style='background-color: #ffcccc;'>Backlogged</th>
            <th style='background-color: #ffe0cc;'>ToDo</th>
            <th style='background-color: #cce6ff;'>In Progress</th>
            <th style='background-color: #ccffcc;'>Completed</th>
        </tr>
        <tr>
    """

    for section in ["Backlogged", "ToDo", "In Progress", "Completed"]:
        table_html += f"<td style='vertical-align: top; width: 25%; background-color: {section_colors[section]};'>"
        if sections[section]:
            for task in sections[section]:
                if task.startswith("- [ ]"):
                    task_text = task[5:].strip()
                elif task.startswith("- [x]"):
                    task_text = f"<s>{task[5:].strip()}</s>"  # Strikethrough for completed tasks
                else:
                    task_text = task.strip()

                # Remove double brackets
                task_text = task_text.replace("[[", "").replace("]]", "")

                table_html += f"<div>{task_text}</div>"
        else:
            table_html += "<div>&nbsp;</div>"  # Empty div for empty columns
        table_html += "</td>"

    table_html += "</tr></table>"
    return table_html

@app.route('/')
def daily_report():
    project_content = read_obsidian_page()
    return render_template('index.html', project_content=project_content)

if __name__ == '__main__':
    app.run(debug=True)
