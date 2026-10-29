/* One local setup panel, shared by stage guides and the checkpoint catalogue. */
(() => {
  const base=new URL('../',document.currentScript.src);
  const node=(tag,text)=>{const n=document.createElement(tag);if(text)n.textContent=text;return n;};
  const link=(text,path)=>{const a=node('a',text);a.href=new URL(path,base).href;return a;};
  const command=(parent,text,label='Copy command')=>{
    const pre=node('pre',text),copy=node('button',label);copy.type='button';
    copy.onclick=async()=>{try{await navigator.clipboard.writeText(text);copy.textContent='Copied';}catch(_){copy.textContent='Select and copy the command above';}};
    parent.append(pre,copy);
  };
  function render(panel,c){
    panel.replaceChildren();
    const heading=node('h3',c.kind==='aggregator'?'Run '+c.stage+' locally':'Run r/'+c.entity+' locally');
    heading.id=panel.id+'-title';panel.setAttribute('aria-labelledby',heading.id);panel.append(heading);
    panel.append(node('p','Checkpoint '+c.milestone+': '+c.title+'.'));
    if(c.availability!=='ready'||!c.bundle?.url||!c.bundle?.sha256){panel.append(node('p',c.reason||'This checkpoint is not yet available for local interviews.'));return;}
    if(!/^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(c.id)||!['codex','claude'].includes(c.backend))throw Error('This checkpoint needs a manually checked launch command.');
    panel.append(node('p','Paste this command into Terminal on your Mac or Linux computer. It downloads and verifies the launcher and checkpoint, asks you to sign in if needed, and opens the selected interview.'));
    const downloads=new URL('downloads',base),quote=value=>"'"+value.replaceAll("'","'\\''")+"'";
    if(downloads.protocol==='https:'||(downloads.protocol==='http:'&&['localhost','127.0.0.1','[::1]'].includes(downloads.hostname))){
      const run='set -e; script=$(curl -fsSL "$1/start-interview.sh"); exec bash -c "$script" -- "$2" "$1"';
      command(panel,'bash -c '+quote(run)+' _ '+quote(downloads.href)+' '+quote(c.id));
    }else panel.append(node('p','Open this guide through its HTTPS website or a localhost preview to copy the setup command. The steps below are also available.'));
    panel.append(node('p','Use Python 3.11 or newer, Git, GitHub CLI and the supported '+(c.backend==='claude'?'Claude Code':'Codex')+' version. Missing tools or access are reported before an interview starts.'));
    panel.append(node('p','No model turn begins until you ask a question. Questions use your own account.'));
    panel.append(node('h4','Or follow these steps'));
    const steps=node('ol');steps.className='local-setup-steps';
    const download=node('li');download.append(link('Download the interview launcher','downloads/rplace-interviews.zip'),node('p','Extract the ZIP and open Terminal in its rplace-interviews folder. Follow the full setup instructions for dependencies and repository access.'));
    const login=node('li');login.append(node('p','Sign in with your account.'));command(login,'python3 -m website.interview login '+c.backend,'Copy sign-in command');
    const launch=node('li');launch.append(node('p','Open checkpoint '+c.milestone+'.'));command(launch,'python3 -m website.interview launch '+c.id,'Copy launch command');
    steps.append(download,login,launch);panel.append(steps);
    const offline=node('details');offline.append(node('summary','Already downloaded the checkpoint?'),link('Verified checkpoint bundle',c.bundle.url));command(offline,'python3 -m website.interview launch '+c.id+' --bundle /path/to/bundle.tar.gz','Copy offline command');panel.append(offline);
    panel.append(link('Full setup instructions','guides/interviews.html#open-an-interview-on-your-computer'));
  }
  let catalogue;
  const entry=id=>{
    if(!catalogue)catalogue=fetch(new URL('catalog.json',base)).then(r=>{if(!r.ok)throw Error('The checkpoint catalogue could not be loaded.');return r.json();}).catch(e=>{catalogue=null;throw e;});
    return catalogue.then(cat=>{const c=cat.checkpoints.find(c=>c.id===id);if(!c)throw Error('This checkpoint is not in the catalogue.');return c;});
  };
  function mount(button,panel,checkpoint){
    panel.hidden=true;panel.classList.add('local-setup');panel.setAttribute('role','region');
    button.type='button';button.setAttribute('aria-controls',panel.id);button.setAttribute('aria-expanded','false');
    let loaded=false;
    async function toggle(){
      const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));panel.hidden=!open;
      if(!open||loaded)return;
      panel.replaceChildren(node('p','Loading local setup…'));panel.setAttribute('aria-busy','true');
      try{render(panel,typeof checkpoint==='string'?await entry(checkpoint):checkpoint);loaded=true;}
      catch(e){const message=node('p',e.message+' Close and reopen Chat Locally to retry.');message.setAttribute('role','status');panel.replaceChildren(message);}
      finally{panel.removeAttribute('aria-busy');}
    }
    button.addEventListener('click',toggle);return {open:()=>button.getAttribute('aria-expanded')==='true'?Promise.resolve():toggle()};
  }
  window.RplaceLocalSetup={mount};
  document.querySelectorAll('button[data-local-checkpoint]').forEach(button=>{
    const panel=document.getElementById(button.getAttribute('aria-controls'));
    if(panel)mount(button,panel,button.dataset.localCheckpoint);
  });
})();
