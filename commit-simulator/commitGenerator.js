function CommitGenerator(){
  this.commit = '';
  this.repositories = [
    {repo_id:'0',repo_name: "fake/test",  repo_url:'https://github.com/fake/test', repo_owner:'Jchabbam', repo_owner_email:'Jchabbam@best.com'},
    {repo_id:'1',repo_name: "fake/test1", repo_url:'https://github.com/fake/test1', repo_owner:'Mfranc', repo_owner_email:'Mfranc@best.com'},
    {repo_id:'2',repo_name: "fake/test2", repo_url:'https://github.com/fake/test2', repo_owner:'Balex', repo_owner_email:'Balex@best.com'},
    {repo_id:'3',repo_name: "fake/test3", repo_url:'https://github.com/fake/test3', repo_owner:'Gcecile', repo_owner_email:'Gcecile@best.com'},
    {repo_id:'4',repo_name: "fake/test4", repo_url:'https://github.com/fake/test4', repo_owner:'Papy', repo_owner_email:'Papy@best.com'}
  ];

  this.users = [
    {user_id: 0,user_name:"a", user_email:"a@a.com", user_username:"aa", user_full_name:"aa aa", user_login:'aa'},
    {user_id: 1,user_name:"z", user_email:"z@z.com", user_username:"zz", user_full_name:"zz zz", user_login:'zz'},
    {user_id: 2,user_name:"e", user_email:"e@e.com", user_username:"ee", user_full_name:"ee ee", user_login:'ee'},
    {user_id: 3,user_name:"r", user_email:"r@r.com", user_username:"rr", user_full_name:"rr rr", user_login:'rr'},
    {user_id: 4,user_name:"t", user_email:"t@t.com", user_username:"tt", user_full_name:"tt tt", user_login:'tt'},
    {user_id: 5,user_name:"y", user_email:"y@y.com", user_username:"yy", user_full_name:"yy yy", user_login:'yy'},
  ];
}

CommitGenerator.prototype.randomIntBetween1And = (stop) => Math.floor(Math.random() * stop);
CommitGenerator.prototype.generator= function () {
    var repo = this.repositories[this.randomIntBetween1And(5)];
    var user = this.users[this.randomIntBetween1And(6)];
    var date = new Date();
    console.log("generator");
    var template = require('./commitTemplate.js');
    // actor
    template['actor']['id'] = user['user_id'];
    template['actor']['login'] = user['user_login'];
    template['actor']['display_login'] = user['user_login'];
    //repo
    template['repo']['id'] = repo['repo_id'];
    template['repo']['name'] = repo['repo_name'];
    template['repo']['url'] = repo['repo_url'];
    //payload
    template['payload']['commits'][0]['author']['name'] = user['user_name'];
    template['payload']['commits'][0]['author']['email'] = user['user_email'];
    //created_at
    template['created_at'] = date.toISOString();
    this.commit = template;
}


module.exports = CommitGenerator;
