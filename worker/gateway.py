from http.server import BaseHTTPRequestHandler,HTTPServer
import urllib.request
import sqlite3


DB="/home/jeet/nono/backend/nono.db"


class Gateway(BaseHTTPRequestHandler):

    def do_GET(self):

        project_id=self.path.strip("/")


        try:

            conn=sqlite3.connect(DB)

            cur=conn.cursor()

            cur.execute(
                "SELECT port FROM projects WHERE id=?",
                (project_id,)
            )

            row=cur.fetchone()

            conn.close()


            if not row or not row[0]:

                self.send_response(404)
                self.end_headers()
                self.wfile.write(
                    b"PROJECT NOT FOUND"
                )
                return


            port=row[0]


            url=f"http://127.0.0.1:{port}"


            data=urllib.request.urlopen(
                url,
                timeout=5
            ).read()


            self.send_response(200)
            self.end_headers()
            self.wfile.write(data)


        except Exception as e:

            self.send_response(503)
            self.end_headers()

            self.wfile.write(
                str(e).encode()
            )



def start_gateway():

    print(
        "NONO Gateway Started :9000"
    )

    HTTPServer(
        ("0.0.0.0",9000),
        Gateway
    ).serve_forever()


if __name__=="__main__":
    start_gateway()
