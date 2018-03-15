const got = require('got');
const commit = require('./commitGenerator.js');

const repeat = () => {
  setTimeout(async () => {
    let url = 'http://git-api/commit';
    let c = new commit();
    c.generator()
    console.log(c.commit);
    try{
			let response = await got.post(url,{body:c.commit});
      console.log("Successfully joined",url);
    }catch(error){
      console.log("Unable to join",url);
    }
    repeat();
  },1000);
};

let multiplierEnv = process.env.multiplier;
let multiplier = multiplierEnv && !isNaN(multiplierEnv) && multiplierEnv > 1 ? parseInt(process.env.multiplier) : 1;
console.log("Multiplier",multiplier);

for(i=0;i <= multiplier;i++){
  setTimeout(() => {
    repeat();
  },100 * i);
}
