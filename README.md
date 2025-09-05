# Video Sharing System

## Usage

### Local run
1. The main backend app:
```bash
python backend/app.py
```
2. The client's submission form
```bach
streamlit run client_page/client_webform.py
```
3. The manager's page, which can see all videos in queue, and manege  it.
```bash
streamlit run manager_page/manager_page.py

```


### Docker
which does not support Google Credential for manager page
```bash
 docker compose up --build
```