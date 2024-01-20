import csv
import json

from neo4j import GraphDatabase, ManagedTransaction


NEO4J_HOST = "neo4j+s://e5cba486.databases.neo4j.io"
NEO4J_AUTH = ("neo4j", "gNnMFWxLiFN4PK1LZAFlYAYEjPL7Iwifdlxj4FNmGho")


result = []
driver = GraphDatabase.driver(NEO4J_HOST, auth=NEO4J_AUTH)
session = driver.session()


def create_node(
    tx: ManagedTransaction, 
    bentuk: str,
    nomor: str,
    tahun: int,
    source: str,
    ) -> None:
    query = """
        MATCH (b:Bentuk {bpk_name: $bentuk})
        CREATE (b)<-[r:INSTANCE_OF]-(l:Legislation {
            nomor: $nomor,
            tahun: $tahun,
            source: $source,
            created_at: timestamp(),
            last_updated_at: timestamp()
        })
        RETURN l
    """
    tx.run(
        query,
        bentuk=bentuk,
        nomor=nomor,
        tahun=tahun,
        source=source
    )


with open("result_3.json", "r") as f:
    scrape_list = json.load(f)

for bentuk in scrape_list:
    for tahun in scrape_list[bentuk]:
        for url in scrape_list[bentuk][tahun]:
            nomor = url.split("-")[-3]
            legislation = {
                "bentuk": bentuk,
                "nomor": nomor,
                "tahun": int(tahun),
                "source": url
            }
            print(f"Writing {bentuk} Nomor {nomor} Tahun {tahun}...")
            session.execute_write(
                create_node,
                bentuk=bentuk,
                nomor=nomor,
                tahun=int(tahun),
                source=url,
            )
