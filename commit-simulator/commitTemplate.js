var commitTemplate =`{
  "ref": "refs/heads/master",
  "created": false,
  "deleted": false,
  "forced": false,
  "base_ref": null,
  "commits": [
    {
      "id": "0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c",
      "tree_id": "f9d2a07e9488b91af2641b26b9407fe22a451433",
      "distinct": true,
      "message": "Update README.md",
      "timestamp": "update_datetime",
      "url": "user_url_commit",
      "author": {
        "name": "user_name",
        "email": "user_email",
        "username": "user_username"
      },
      "committer": {
        "name": "user_name",
        "email": "user_email",
        "username": "user_username"
      },
      "added": [

      ],
      "removed": [

      ],
      "modified": [
        "README.md"
      ]
    }
  ],
  "head_commit": {
    "id": "0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c",
    "tree_id": "f9d2a07e9488b91af2641b26b9407fe22a451433",
    "distinct": true,
    "message": "Update README.md",
    "timestamp": "update_datetime",
    "url": "user_url_commit",
    "author": {
      "name": "user_name",
      "email": "user_email",
      "username": "user_username"
    },
    "committer": {
      "name": "user_name",
      "email": "user_email",
      "username": "user_username"
    },
    "added": [

    ],
    "removed": [

    ],
    "modified": [
      "README.md"
    ]
  },
  "repository": {
    "id": "repo_id",
    "name": "repo_name",
    "full_name": "repo_name",
    "owner": {
      "name": "repo_owner",
      "email": "repo_owner_mail"
    },
    "private": false,
    "html_url": "repo_url",
    "description": "",
    "fork": false,
    "url": "repo_url",
    "created_at": "created_ts",
    "updated_at": "update_datetime",
    "pushed_at": "push_login",
    "homepage": null,
    "size": 0,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": null,
    "has_issues": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": true,
    "forks_count": 0,
    "mirror_url": null,
    "open_issues_count": 0,
    "forks": 0,
    "open_issues": 0,
    "watchers": 0,
    "default_branch": "master",
    "stargazers": 0,
    "master_branch": "master"
  },
  "pusher": {
    "name": "user_name",
    "email": "user_email"
  },
  "sender": {
    "login": "user_login",
    "id": user_id,
    "type": "User",
    "site_admin": false
  }
}`;

module.exports = commitTemplate;
