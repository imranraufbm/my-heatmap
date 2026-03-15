# GitHub Heatmap Designer 🚀

A specialized tool for designing and automating GitHub contribution heatmaps with natural-looking activity patterns.

## 🌟 Features
- **Custom Date Ranges**: Precisely define your activity period (Jan 2025 - July 2025).
- **Natural Distribution**: Logic-driven commit density favoring nights and weekends.
- **Realistic History**: Uses a variety of commit messages (Fixes, Features, Docs, Refactors).
- **Secure Configuration**: Keeps sensitive tokens safe via `.gitignore` and local `config.py`.

## 🛠️ Setup & Usage
1. **Configure**: Update `config.py` with your GitHub PAT and email.
2. **Generate**: Run the designer to create local history.
   ```bash
   python heatmap_app.py
   ```
3. **Sync**: Push the generated history to your GitHub profile.

## 🔒 Security
Sensitive information like Personal Access Tokens (PAT) are stored in `config.py`, which is explicitly ignored by Git to prevent accidental exposure.

---
*Created with ❤️ for imranraufbm*
