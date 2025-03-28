#!/usr/bin/env python3
import os

def list_project_py_files(startpath, include_dirs=None, exclude_dirs=None):
    """Liste les fichiers .py du projet en excluant les dossiers indésirables."""
    if include_dirs is None:
        include_dirs = ["MidiTools", "MusicUtils", "TrainerUI"]  # Dossiers de ton code
    if exclude_dirs is None:
        exclude_dirs = ["__pycache__", ".git", "venv", "lib", "site-packages"]

    output = []
    for root, dirs, files in os.walk(startpath):
        # Vérifie si le chemin contient un dossier exclu
        if any(excluded in root for excluded in exclude_dirs):
            continue
        # Vérifie si le chemin est dans un dossier inclus ou à la racine
        root_relative = os.path.relpath(root, startpath)
        is_root = root_relative == "."
        is_included_dir = any(included in root for included in include_dirs)

        if not (is_root or is_included_dir):
            continue

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                output.append(f"\n=== {file_path} ===")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        output.append(content)
                except Exception as e:
                    output.append(f"Erreur : {e}")
    return output

def save_to_file(filename, content_lines):
    """Enregistre dans un fichier."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines))

if __name__ == "__main__":
    project_root = "."  # Répertoire courant
    output_lines = list_project_py_files(project_root)

    if not output_lines:
        output_lines.append("Aucun fichier .py trouvé dans les dossiers spécifiés.")
    
    save_to_file("projet.txt", output_lines)
    print("Le code de ton projet a été enregistré dans 'projet.txt'.")