# 🖥️ CodeShifter Backend (Flask)

This is the **Flask backend** for CodeShifter.  
It provides a REST API for reorganizing project structures: moving files, updating imports, cleaning empty directories, and adding `__init__.py` files.  

---

## ▶️ Usage

Run the server:

```bash
cd server
docker build -it <code-shifter-server> .
docker run docker run -it -p 5000:5000 -v ${pwd}/:/app/ <code-shifter-server>
cd app
```
