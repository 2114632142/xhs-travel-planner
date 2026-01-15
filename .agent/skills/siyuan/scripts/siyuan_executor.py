import os
import sys
import json
import requests
import argparse

class SiYuanClient:
    def __init__(self, host="127.0.0.1", port="6806", token=None):
        self.base_url = f"http://{host}:{port}/api"
        self.headers = {
            "Authorization": f"Token {token}" if token else ""
        }

    def _post(self, path, data=None):
        url = f"{self.base_url}{path}"
        try:
            response = requests.post(url, json=data or {}, headers=self.headers)
            response.raise_for_status()
            res_json = response.json()
            if res_json.get("code") != 0:
                return {"status": "error", "message": res_json.get("msg", "Unknown error"), "code": res_json.get("code")}
            return {"status": "success", "data": res_json.get("data")}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_notebooks(self):
        return self._post("/notebook/lsNotebooks")

    def create_doc(self, notebook, path, markdown):
        return self._post("/filetree/createDocWithMd", {
            "notebook": notebook,
            "path": path,
            "markdown": markdown
        })

    def sql_query(self, sql):
        return self._post("/query/sql", {"stmt": sql})

    def get_block_kramdown(self, id):
        return self._post("/block/getBlockKramdown", {"id": id})

    def insert_block(self, data, dataType, parentID, previousID=None):
        payload = {
            "data": data,
            "dataType": dataType,
            "parentID": parentID
        }
        if previousID:
            payload["previousID"] = previousID
        return self._post("/block/insertBlock", payload)

def main():
    parser = argparse.ArgumentParser(description="SiYuan Note API Executor")
    parser.add_argument("command", help="Command to execute (list_notebooks, create_doc, sql, etc.)")
    parser.add_argument("--notebook", help="Notebook ID")
    parser.add_argument("--path", help="Document path")
    parser.add_argument("--markdown", help="Markdown content")
    parser.add_argument("--sql", help="SQL statement")
    parser.add_argument("--id", help="Block/Doc ID")
    parser.add_argument("--data", help="Block data")
    parser.add_argument("--parent", help="Parent ID")
    
    args = parser.parse_args()

    # Load config from env or fallback
    host = os.environ.get("SIYUAN_HOST", "127.0.0.1")
    port = os.environ.get("SIYUAN_PORT", "6806")
    token = os.environ.get("SIYUAN_TOKEN")

    if not token:
        print(json.dumps({"status": "error", "message": "SIYUAN_TOKEN environment variable is not set."}))
        sys.exit(1)

    client = SiYuanClient(host, port, token)

    if args.command == "list_notebooks":
        result = client.list_notebooks()
    elif args.command == "create_doc":
        result = client.create_doc(args.notebook, args.path, args.markdown)
    elif args.command == "sql":
        result = client.sql_query(args.sql)
    elif args.command == "get_block":
        result = client.get_block_kramdown(args.id)
    elif args.command == "insert_block":
        result = client.insert_block(args.data, "markdown", args.parent)
    else:
        result = {"status": "error", "message": f"Unknown command: {args.command}"}

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
