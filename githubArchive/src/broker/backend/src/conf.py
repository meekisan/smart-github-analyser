conf ={
    "broker": {"host": "rabbitmq", "port":"","exchange": "github_archive", "routing_key": "*.*", "queue": "archives"},
    "backend": {"host": "datastorage-primary", "port":"27017","db": "github","collection":"archives"},
    "githubarchive": {"url": "http://data.githubarchive.org/"}
}
