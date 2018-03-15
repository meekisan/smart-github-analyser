conf ={
    "mogoBackend": {"host": "datastorage", "port":"27017","db": "github","collection":"archives"},
    "elasticBackend": { "url" : "http://search:9200/github/archives"},
    "githubarchive": {"url": "http://data.githubarchive.org/"},
    "broker":{"archives":{"host": "rabbitmq", "port":"", "exchange": "github_archive", "routing_key": "*.*", "queue": "archives"},
    "search": {"host": "rabbitmq", "port":"", "exchange": "github_archive", "routing_key": "*.*", "queue": "search"},
    "simulator": {"host": "rabbitmq", "port":"", "exchange": "simulator", "routing_key": "*.*", "queue": "commits"}
    }
}
