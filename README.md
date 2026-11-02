# github-trends-MCP MCP server that gives AI assistants live access to trending
and searchable GitHub repositories. No API key needed.

## Tools
- `trending(language, days, limit)`: new repos ranked by stars
- `search(query, limit)`: keyword search
- `repo_info(owner, name)`: stars, forks, issues, license

## Run
```
pip install -r requirements.txt
python server.py
```

## Test
```
mcp dev server.py
```