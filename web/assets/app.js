/* Utility Shelf v3: dependency-free, same-origin application interface. */
"use strict";

const S = {
  tools: [], categories: [], current: null, filter: "All tools", query: "",
  theme: localStorage.getItem("shelf_theme_v3") === "dark" ? "dark" : "light",
  favs: readStore("shelf_favourites_v3", []),
  recent: readStore("shelf_recent_v3", []),
  results: {}, inputs: {}, sources: {}, tab: "run",
  modal: false, modalQuery: "", menu: false, busy: false,
  ready: false, error: "",
};
const GH = "https://github.com/AdityaSreevatsaK/Useful-Code-Snippets";
const icons = {
  grid:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  spark:'<path d="m12 3 1.6 6.4L20 11l-6.4 1.6L12 19l-1.6-6.4L4 11l6.4-1.6L12 3Z"/><path d="m20 18 .6 1.4L22 20l-1.4.6L20 22l-.6-1.4L18 20l1.4-.6L20 18Z"/>',
  search:'<circle cx="10.8" cy="10.8" r="7.2"/><path d="m16.1 16.1 5.1 5.1"/>',
  file:'<path d="M13 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V10z"/><path d="M13 3v7h7"/><path d="M8 15h8M8 18h5"/>',
  image:'<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 16-5-5L5 21"/>',
  code:'<path d="m8 8-4 4 4 4m8-8 4 4-4 4m-3-14-2 20"/>',
  terminal:'<rect x="2.5" y="4" width="19" height="16" rx="2"/><path d="m7 9 3 3-3 3m5 0h5"/>',
  audio:'<path d="M9 5 5 9H2v6h3l4 4zM13 9a4 4 0 0 1 0 6M16 6a8 8 0 0 1 0 12"/>',
  boxes:'<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/>',
  layers:'<path d="m12 3 9 5-9 5-9-5 9-5Zm-9 9 9 5 9-5M3 16l9 5 9-5"/>',
  github:'<path d="M9 19c-4 1-4-2-6-2m12 4v-4a4 4 0 0 0-1-3c3-.4 6-1.5 6-6a5 5 0 0 0-1.4-3.5A5 5 0 0 0 18.5 1L15 3a13 13 0 0 0-6 0L5.5 1a5 5 0 0 0-.1 3.5A5 5 0 0 0 4 8c0 4.5 3 5.6 6 6a4 4 0 0 0-1 3v4"/>',
  shield:'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
  book:'<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/>',
  star:'<path d="m12 2 3.1 6.4 7.1 1-5.1 5 1.2 7.1L12 18.1l-6.3 3.4 1.2-7.1-5.1-5 7.1-1L12 2Z"/>',
  clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  arrow:'<path d="M5 12h14m-6-6 6 6-6 6"/>',
  back:'<path d="M19 12H5m6-6-6 6 6 6"/>',
  chevron:'<path d="m9 18 6-6-6-6"/>',
  sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"/>',
  moon:'<path d="M20 15.7A8.5 8.5 0 0 1 8.3 4 8.5 8.5 0 1 0 20 15.7Z"/>',
  upload:'<path d="M12 16V4m-5 5 5-5 5 5M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
  download:'<path d="M12 3v12m-5-5 5 5 5-5M4 17v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3"/>',
  copy:'<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>',
  check:'<path d="m4 12 5 5 11-11"/>',
  close:'<path d="M5 5 19 19M19 5 5 19"/>',
  menu:'<path d="M4 6h16M4 12h16M4 18h16"/>',
  info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7h.01"/>',
  lock:'<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
  bolt:'<path d="m13 2-9 12h7l-1 8 10-12h-7z"/>',
  folder:'<path d="M3 6a2 2 0 0 1 2-2h5l2 3h7a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
  refresh:'<path d="M20 11a8 8 0 0 0-14-5L3 9m0-5v5h5m-4 4a8 8 0 0 0 14 5l3-3m0 5v-5h-5"/>',
  play:'<path d="m8 5 11 7-11 7z"/>',
};
const CATEGORY_ICONS = {
  "Audio & Speech Processing":"audio",
  "Automation & Productivity":"bolt",
  "File Handling":"file",
  "Git Utilities":"terminal",
  "Hugging Face Utilities":"shield",
  "Image Processing":"image",
  "Jupyter Notebook Utilities":"book",
  "Regex Cheatsheet":"code"
};
const FILE_TYPES = {
  "pdf-to-word":".pdf", "pdf-to-images":".pdf", "word-to-pdf":".docx",
  "merge-pdfs":".pdf", "split-pdf":".pdf", "create-zip":"",
  "extract-zip":".zip", "recursive-unzip":".zip",
  "grayscale-image":".png,.jpg,.jpeg,.gif,.webp",
  "compress-image":".png,.jpg,.jpeg,.gif,.webp",
  "convert-image":".png,.jpg,.jpeg,.gif,.webp",
  "resize-images":".png,.jpg,.jpeg,.gif,.webp",
  "pitch-analysis":".mp3,.wav,.ogg,.flac",
  "notebook-to-python":".ipynb"
};
const MULTI = new Set(["merge-pdfs","create-zip","resize-images"]);
const TEXT = new Set([
  "text-to-speech","embed-youtube","upper-case","lower-case","sentence-case",
  "extract-dates","extract-hashtags","extract-urls","find-phone-numbers",
  "validate-email","remove-spaces"
]);
const FEATURED = ["pdf-to-word","convert-image","extract-urls"];

function readStore(name, fallback) {
  try { const value = JSON.parse(localStorage.getItem(name)); return Array.isArray(value) ? value : fallback; }
  catch { return fallback; }
}
function store(name, value) {
  try { localStorage.setItem(name, JSON.stringify(value)); } catch {}
}
function esc(value) {
  return String(value == null ? "" : value).replace(/[&<>"']/g, function(ch) {
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch];
  });
}
function svg(name, size) {
  return '<svg xmlns="http://www.w3.org/2000/svg" width="' + (size||18) + '" height="' +
    (size||18) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    (icons[name]||icons.boxes) + '</svg>';
}
function toolIcon(tool) {
  return CATEGORY_ICONS[tool.category] || "boxes";
}
function slugFromPath() {
  const match = location.pathname.match(/^\/tools\/([a-z0-9-]+)\/?$/);
  return match ? match[1] : null;
}
function count(category) { return S.tools.filter(t => t.category === category).length; }
function bySlug(slug) { return S.tools.find(t => t.slug === slug); }
function matching(query, cat) {
  const terms = (query||"").trim().toLowerCase().split(/\s+/).filter(Boolean);
  return S.tools.filter(t => (cat === "All tools" || t.category === cat) &&
    terms.every(q => (t.title+" "+t.description+" "+t.category+" "+t.tags.join(" ")).toLowerCase().includes(q)));
}
function fav(slug) { return S.favs.includes(slug); }
function button(action, title, cls, iconName, extra) {
  return '<button type="button" data-action="' + action + '" class="' + cls + '" ' + (extra||"") + '>' +
    (iconName?svg(iconName,16):"") + esc(title) + '</button>';
}
function categoryNav(cat) {
  return '<button type="button" class="nav-item ' +
    ((S.current && bySlug(S.current) && bySlug(S.current).category === cat) ||
      (!S.current && S.filter === cat) ? 'active':'') +
    '" data-action="category" data-category="' + esc(cat) + '">' +
    '<span class="icon">' + svg(CATEGORY_ICONS[cat],17) + '</span>' +
    '<span>' + esc(cat.replace(" & Speech Processing"," & Speech").replace(" & Productivity"," & Productivity").replace("Jupyter Notebook Utilities","Notebooks").replace("Hugging Face Utilities","Hugging Face").replace("Regex Cheatsheet","Text & Regex")) +
    '</span><span class="count">' + count(cat) + '</span></button>';
}
function sidebar() {
  return '<aside class="sidebar" aria-label="Main navigation">' +
    '<a href="/" class="brand" data-action="home">' +
    '<span class="brand-symbol">' + svg("grid",21) + '</span>' +
    '<span class="brand-copy"><span class="brand-name">Utility Shelf</span><span class="brand-sub">DEVELOPER TOOLKIT</span></span></a>' +
    '<div class="nav-group"><div class="nav-label">WORKSPACE</div>' +
    '<button class="nav-item ' + (!S.current && S.filter === "All tools" ? "active":"") +
    '" data-action="home"><span class="icon">' + svg("grid",18) + '</span>Overview</button>' +
    '<button class="nav-item" data-action="search"><span class="icon">' + svg("search",18) + '</span>Find a tool</button></div>' +
    '<div class="nav-group"><div class="nav-label">COLLECTIONS</div>' + S.categories.map(categoryNav).join("") + '</div>' +
    '<div class="sidebar-bottom"><div class="sidebar-note">' + svg("shield",17) +
    '<div><strong>Privacy by design</strong><br>Uploads are processed temporarily. No account or permanent file storage.</div></div>' +
    '<div class="sidebar-footer"><span>Utility Shelf v3</span><span>Open-source tools</span></div></div>' +
    '</aside>';
}
function topbar() {
  const tool = S.current && bySlug(S.current);
  return '<header class="topbar"><div style="display:flex;align-items:center;gap:13px">' +
    '<button class="icon-button mobile-menu" aria-label="Open menu" data-action="menu">' + svg("menu") + '</button>' +
    '<div class="crumb"><span>Workspace</span>' + svg("chevron",13) +
    (tool ? '<strong>' + esc(tool.title) + '</strong>' :
      '<strong>' + (S.filter === "All tools" ? "Overview" : esc(S.filter)) + '</strong>') +
    '</div></div><div class="top-actions">' +
    '<button class="header-search" data-action="search" aria-label="Search tools">' +
    svg("search",17) + '<span>Search anything...</span><kbd>Ctrl K</kbd></button>' +
    '<a class="icon-button" href="' + GH + '" target="_blank" rel="noopener noreferrer" aria-label="GitHub repository">' + svg("github",18) + '</a>' +
    '<button class="icon-button" data-action="theme" aria-label="Toggle colour theme" title="Toggle colour theme">' +
    svg(S.theme === "dark" ? "sun":"moon",18) + '</button>' +
    '<span class="version">V3.0</span></div></header>';
}
function card(tool) {
  return '<article class="tool-card">' +
    '<div class="card-head"><span class="card-icon">' + svg(toolIcon(tool),21) + '</span>' +
    '<button type="button" data-action="fav" data-slug="' + tool.slug + '" class="card-fav ' + (fav(tool.slug)?"saved":"") +
    '" aria-label="' + (fav(tool.slug)?"Remove favourite":"Add favourite") + '">' + svg("star",17) + '</button></div>' +
    '<div class="card-category">' + esc(tool.category) + '</div>' +
    '<a href="/tools/' + tool.slug + '" data-action="open" data-slug="' + tool.slug + '" class="card-title">' + esc(tool.title) + '</a>' +
    '<p class="card-description">' + esc(tool.description) + '</p><div class="card-foot">' +
    '<span class="card-badge ' + (tool.local_only?"local":"") + '">' +
    svg(tool.local_only?"lock":"check",13) + (tool.local_only?"Local-only":"Browser-ready") +
    '</span><a href="/tools/' + tool.slug + '" data-action="open" data-slug="' + tool.slug +
    '" class="card-arrow" aria-label="Open ' + esc(tool.title) + '">' + svg("arrow",18) + '</a></div></article>';
}
function grid(tools) {
  return tools.length ? '<div class="cards">' + tools.map(card).join("") + '</div>' :
    '<div class="empty-card">' + svg("search",26) +
    '<h3>No matching tools</h3><p>Try a different search or select another category.</p></div>';
}
function section(title, desc, action) {
  return '<div class="section-heading"><div><h2>' + esc(title) + '</h2>' +
    (desc?'<p>'+esc(desc)+'</p>':"")+'</div>'+(action||"")+'</div>';
}
function filters() {
  return '<div class="filter-row">' + ['All tools'].concat(S.categories).map(cat =>
    '<button class="filter ' + (S.filter===cat?'active':'') + '" data-action="category" data-category="' + esc(cat) +
    '">' + esc(cat==="All tools"?"All tools":cat.replace(" & Speech Processing","").replace(" & Productivity","").replace(" Utilities","").replace(" Cheatsheet","")) +
    '</button>').join("") + '</div>';
}
function home() {
  const starred = S.favs.map(bySlug).filter(Boolean).slice(0,3);
  const recent = S.recent.map(bySlug).filter(Boolean).slice(0,3);
  const selected = matching(S.query,S.filter);
  return '<section class="hero"><div class="hero-content">' +
    '<div class="hero-label"><span class="dot"></span> PURPOSE-BUILT FOR PRACTICAL WORK</div>' +
    '<h1>Good tools.<br>Better workflows.</h1>' +
    '<p>A refined workspace for documents, images, text and developer utilities. Find the right tool, run it and take your result with you.</p>' +
    '<div class="hero-actions">' +
    button("scroll-tools","Explore the toolkit","btn btn-light","arrow") +
    '<a href="' + GH + '" class="btn btn-outline-light" target="_blank" rel="noopener noreferrer">' + svg("github",16) + ' View on GitHub</a>' +
    '</div></div></section>' +
    '<div class="stat-row"><div class="stat-card"><span class="stat-icon">' + svg("boxes",21) + '</span><div><div class="stat-value">' +
    S.tools.length + '</div><div class="stat-label">Curated utilities</div></div></div>' +
    '<div class="stat-card"><span class="stat-icon">' + svg("layers",21) +
    '</span><div><div class="stat-value">' + S.categories.length +
    '</div><div class="stat-label">Organised collections</div></div></div>' +
    '<div class="stat-card"><span class="stat-icon">' + svg("check",21) + '</span><div><div class="stat-value">' +
    S.tools.filter(t=>!t.local_only).length + '</div><div class="stat-label">Ready in the browser</div></div></div></div>' +
    (!S.query && S.filter === "All tools" ? section("Start with these","Useful picks for everyday tasks",
      '<button class="text-link" data-action="scroll-tools">Browse all ' + svg("arrow",15) + '</button>') +
      grid(FEATURED.map(bySlug).filter(Boolean)) : "") +
    (starred.length && !S.query && S.filter==="All tools" ? section("Your favourites","Quick access to saved utilities") + grid(starred) : "") +
    (recent.length && !S.query && S.filter==="All tools" ? section("Recently used","Pick up where you left off") + grid(recent) : "") +
    '<div id="all-tools">' +
    section(S.filter==="All tools"?"Explore the toolkit":S.filter,"Find the utility for your next task") +
    '<div class="toolbar"><div class="search-field">' + svg("search",18) +
    '<input id="catalog-search" type="search" placeholder="Search by tool, format or task..." value="' + esc(S.query) +
    '" autocomplete="off" aria-label="Search catalogue"></div>' +
    '<span class="result-count" id="match-count">' + selected.length + ' tools</span></div>' +
    '<div id="filters">' + filters() + '</div><div id="catalogue-grid">' + grid(selected) + '</div></div>';
}
function optionsFor(slug) {
  if (slug === "text-to-speech")
    return '<div class="field"><label for="option-voice">Voice</label><select id="option-voice" data-option="voice">' +
      '<option value="male">Voice 1</option><option value="female">Voice 2</option></select>' +
      '<p class="field-hint">Voices depend on the installed speech engine.</p></div>' +
      '<div class="field"><label for="option-rate">Speech speed (words/min)</label>' +
      '<input class="control" id="option-rate" type="number" data-option="rate" min="70" max="260" value="160"></div>';
  if (slug === "pdf-to-images")
    return '<div class="field"><label for="option-dpi">Output quality</label>' +
      '<select id="option-dpi" data-option="dpi"><option value="120">Standard · 120 DPI</option>' +
      '<option value="160">High · 160 DPI</option><option value="200">Very high · 200 DPI</option></select></div>';
  if (slug === "convert-image")
    return '<div class="field"><label for="option-format">Output format</label>' +
      '<select id="option-format" data-option="format"><option value="PNG">PNG</option>' +
      '<option value="JPEG">JPEG</option><option value="GIF">GIF</option></select></div>';
  if (slug === "compress-image" || slug === "resize-images")
    return '<div class="field"><label for="option-percentage">Resize amount (%)</label>' +
      '<input class="control" id="option-percentage" type="number" data-option="percentage" min="1" max="' +
      (slug==="compress-image"?"95":"100") + '" value="' + (slug==="compress-image"?"35":"50") + '">' +
      '<p class="field-hint">Reduces image dimensions by the chosen percentage.</p></div>';
  return "";
}
function runForm(tool) {
  const slug = tool.slug;
  if (tool.local_only)
    return '<div class="warning"><strong>' + svg("lock",15) +
      ' Protected operation</strong><p>This utility touches local resources or privileged services. ' +
      'It is deliberately not available on the public website. Inspect its Python source to run it in a trusted environment.</p></div>' +
      button("tab","View Python source","btn btn-ghost","code",'data-tab="code"');
  const saved = S.inputs[slug] || {};
  let control = "";
  if (Object.prototype.hasOwnProperty.call(FILE_TYPES,slug)) {
    const accept=FILE_TYPES[slug];
    const multiple=MULTI.has(slug);
    const items=saved.files||[];
    control='<div class="field"><label>Input files</label><div class="dropzone" id="dropzone" role="button" tabindex="0" aria-label="Choose files">' +
      '<div class="drop-icon">' + svg("upload",22) + '</div>' +
      '<strong>Drop files here, or click to browse</strong>' +
      '<span>Up to 20 MiB per file · ' + (accept?esc(accept.replaceAll(","," · ")):"Any file type") +
      '</span><input type="file" id="file-upload" ' +
      (accept?'accept="'+esc(accept)+'" ':"")+(multiple?"multiple ":"")+
      'hidden></div><div id="files-list" class="files-list">' + fileRows(items) + '</div></div>';
  } else if (TEXT.has(slug)) {
    const youtube = slug === "embed-youtube";
    control='<div class="field"><label for="tool-text">' +
      (youtube?"YouTube video ID":slug==="text-to-speech"?"Text to speak":"Input text") +
      '</label>' +
      (youtube ? '<input class="control" id="tool-text" type="text" maxlength="11" placeholder="11-character YouTube ID" value="' +
        esc(saved.text||"") + '">'
        : '<textarea id="tool-text" placeholder="' +
          (slug==="text-to-speech"?"Enter a message to convert into speech...":"Paste or type your text here...") +
          '">' + esc(saved.text||"") + '</textarea>') +
      '<p class="field-hint">No account needed. Text is processed for this request only.</p></div>';
  } else if (slug==="git-commands") {
    control='<div class="tip">' + svg("book",17) +
      '<span>Open the Git commands reference in the results panel, or browse its source.</span></div>';
  }
  return control + optionsFor(slug) +
    '<div class="run-row">' + button("run",slug==="git-commands"?"Load reference":"Run utility","btn btn-primary","play",
      S.busy?'disabled':'') +
    '<span class="note">Processed on a temporary server workspace. Files are not retained.</span></div>' +
    '<div id="form-error"></div>';
}
function fileRows(files) {
  if(!files||!files.length) return "";
  return files.map((f,i)=>'<div class="file-chip">' + svg("file",14) +
    '<span title="' + esc(f.name) + '">' + esc(f.name) + '</span><small>' +
    formatSize(f.size) + '</small><button type="button" class="file-clear" data-action="remove-file" data-index="' +
    i + '" aria-label="Remove file">' + svg("close",14) + '</button></div>').join("");
}
function formatSize(size) {
  if(size>=1024*1024)return (size/1024/1024).toFixed(1)+" MiB";
  if(size>=1024)return Math.round(size/1024)+" KiB";
  return size+" B";
}
function resultPane(tool) {
  const result = S.results[tool.slug];
  if(S.busy) return '<div class="result-placeholder">' +
    '<div class="result-icon">' + svg("refresh",27) + '</div>' +
    '<h3>Processing your request</h3><p>Preparing your result. This runs on the server.</p></div><div class="progress"></div>';
  if(!result) return '<div class="result-placeholder"><div class="result-icon">' +
    svg("spark",25)+'</div><h3>Ready when you are</h3><p>Your output will appear here after running the tool. Downloads remain available while this tab stays open.</p></div>';
  if(result.kind==="file") {
    const preview=result.mime.startsWith("image/")?'<img class="preview-image" src="' + result.url +
      '" alt="Generated file preview">':result.mime.startsWith("audio/")?
      '<audio controls preload="metadata" src="' + result.url + '" style="width:100%"></audio>':"";
    return '<div class="result-content"><div class="result-state">' + svg("check",17) +
      ' Output generated successfully</div>' + preview +
      '<div class="result-file"><div class="fileicon">' + svg("file",20) +
      '</div><div class="details"><strong>' + esc(result.filename) + '</strong>' +
      '<span>' + formatSize(result.blob.size) + ' · Ready to download</span></div></div>' +
      button("download","Download result","btn btn-primary","download") +
      '<div class="result-meta">Stored only in this browser tab. Reloading clears the result.</div></div>';
  }
  if(result.kind==="video")
    return '<div class="result-content"><div class="result-state">' + svg("check",16) + ' Video ready</div>' +
      '<iframe title="YouTube video" src="https://www.youtube-nocookie.com/embed/' + esc(result.value) +
      '" allow="encrypted-media; picture-in-picture" allowfullscreen style="width:100%;aspect-ratio:16/9;border:0;border-radius:12px"></iframe></div>';
  let displayed=typeof result.value==="string"?result.value:JSON.stringify(result.value,null,2);
  if(result.value===true)displayed="Valid email syntax";
  if(result.value===false)displayed="Invalid email syntax";
  return '<div class="result-content"><div class="result-state">' + svg("check",16) +
    ' Completed successfully</div><pre class="result-data">' + esc(displayed) + '</pre>' +
    button("copy-result","Copy result","btn btn-ghost","copy") +
    '<div class="result-meta">Output is available in this browser tab.</div></div>';
}
function workspace() {
  const tool=bySlug(S.current);
  if(!tool)return home();
  const selectedTab=S.tab;
  const code=S.sources[tool.slug];
  return '<button class="workspace-back" data-action="home">' + svg("back",15) + ' All tools</button>' +
    '<div class="workspace-heading"><div><span class="eyebrow">' + esc(tool.category) + '</span>' +
    '<h1>' + esc(tool.title) + '</h1><p class="lead">' + esc(tool.description) + '</p></div>' +
    '<div class="workspace-heading-actions">' +
    button("fav",fav(tool.slug)?"Saved":"Save tool","btn btn-ghost","star",'data-slug="'+tool.slug+'"') +
    '<a href="' + GH + '/blob/main/' + encodeURI(tool.source) +
    '" target="_blank" rel="noopener noreferrer" class="btn btn-ghost">' + svg("github",16) + ' Source</a>' +
    '</div></div><div class="workspace-grid">' +
    '<section class="panel"><div class="panel-head"><div><h2>Configure &amp; run</h2><p>' +
    (tool.local_only?"Local execution required":"Choose inputs and run the utility") +
    '</p></div><span class="card-badge '+(tool.local_only?'local':'')+'">' +
    svg(tool.local_only?"lock":"check",15) + (tool.local_only?"Local only":"Available online") +
    '</span></div><div class="panel-body">' + runForm(tool) + '</div></section>' +
    '<section class="panel" id="output-panel"><div class="panel-tabs" role="tablist" aria-label="Tool information">' +
    tabButton("run","Output",selectedTab)+tabButton("code","Source code",selectedTab)+
    tabButton("about","Details",selectedTab)+'</div><div class="panel-body" id="result-container">' +
    (selectedTab==="run"?resultPane(tool):selectedTab==="code"?codePane(tool,code):aboutPane(tool)) +
    '</div></section></div><div class="footer"><span>Purpose-built Python tools · Utility Shelf v3</span>' +
    '<a href="' + GH + '" target="_blank" rel="noopener noreferrer">Open source on GitHub</a></div>';
}
function tabButton(tab,label,active) {
  return '<button role="tab" aria-selected="'+(active===tab)+'" class="panel-tab '+(active===tab?'active':'')+
    '" data-action="tab" data-tab="'+tab+'">'+label+'</button>';
}
function codePane(tool, code) {
  return '<div class="code-toolbar"><span>'+esc(tool.source)+'</span>'+
    button("copy-code","Copy","btn btn-ghost btn-small","copy")+'</div>'+
    (code==null?'<div class="result-placeholder"><p>Loading source file...</p></div>':
      '<pre class="code-block"><code>'+esc(code)+'</code></pre>')+
    '<p class="field-hint">View the complete implementation in the GitHub repository.</p>';
}
function aboutPane(tool) {
  return '<div class="tip">' + svg("info",18) +
    '<span>'+esc(tool.description)+'</span></div>' +
    '<h3 style="font-size:13px;margin:24px 0 8px">How it works</h3>' +
    '<ol class="note-list"><li>Provide the required input in the left panel.</li>'+
    '<li>Run the tool and review its result here.</li>'+
    '<li>Download or copy your result, or inspect the standalone Python code.</li></ol>'+
    (tool.local_only?'<div class="warning">This operation is not exposed through the public API.</div>':
      '<div class="warning"><strong>Privacy note:</strong> Uploaded content is processed temporarily on the server and is not deliberately retained.</div>');
}
function modal() {
  const tools=matching(S.modalQuery,"All tools").slice(0,12);
  return '<div class="modal-backdrop" data-action="dismiss-modal"><section class="search-modal" role="dialog" aria-modal="true" aria-label="Search tools">' +
    '<div class="modal-search-row">'+svg("search",20)+
    '<input id="modal-input" type="search" placeholder="Search tools and commands..." value="'+esc(S.modalQuery)+
    '" autocomplete="off" aria-label="Search tools"><kbd>ESC</kbd></div>'+
    '<div class="modal-results" id="modal-results">'+modalResults(tools)+'</div>'+
    '<div class="modal-foot">Search by tool name, category or file type · Enter to open first result</div></section></div>';
}
function modalResults(tools) {
  return tools.length?tools.map(t=>'<button data-action="open" data-slug="'+t.slug+'" class="modal-item">'+
    svg(toolIcon(t),19)+'<span><strong>'+esc(t.title)+'</strong><small>'+esc(t.category)+'</small></span>'+
    '<span class="arrow">'+svg("arrow",16)+'</span></button>').join(""):
    '<div class="empty-card" style="padding:25px">No tools found</div>';
}
function render() {
  document.documentElement.dataset.theme=S.theme;
  document.body.classList.toggle("menu-open",S.menu);
  const root=document.getElementById("app");
  if(!S.ready) {
    root.innerHTML='<div style="min-height:100vh;display:grid;place-items:center;padding:30px;color:var(--muted)">'+
      '<div style="text-align:center">'+svg("boxes",35)+'<p>'+esc(S.error||"Loading Utility Shelf...")+'</p>'+
      (S.error?button("retry","Try again","btn btn-primary","refresh"):"")+'</div></div>';
    return;
  }
  root.innerHTML='<div class="app-shell">'+sidebar()+'<div class="scrim" data-action="menu"></div>'+
    '<div class="main">'+topbar()+'<main class="content" id="main-content">'+
    (S.current?workspace():home())+'</main></div></div>'+(S.modal?modal():"");
  if(S.modal) {
    const search=document.getElementById("modal-input");
    if(search)search.focus();
  }
  if(S.current && S.tab==="code" && S.sources[S.current]===undefined)loadSource(S.current);
  if(S.current) restoreOptions();
}
function restoreOptions() {
  const form=S.inputs[S.current] || {};
  for(const [key,value] of Object.entries(form.options||{})) {
    const field=document.getElementById("option-"+key);
    if(field)field.value=String(value);
  }
}
function navigate(slug, filter) {
  S.menu=false;S.modal=false;S.current=slug||null;S.tab="run";S.query="";
  if(slug) {
    const t=bySlug(slug);
    if(!t){S.current=null;return navigate(null,"All tools");}
    S.recent=[slug].concat(S.recent.filter(x=>x!==slug)).slice(0,8);
    store("shelf_recent_v3",S.recent);
    history.pushState({}, "", "/tools/"+encodeURIComponent(slug));
  } else {
    S.filter=filter||"All tools";
    history.pushState({}, "", "/");
  }
  render();
  window.scrollTo({top:0,behavior:"instant"});
}
function toggleFav(slug) {
  S.favs=fav(slug)?S.favs.filter(x=>x!==slug):S.favs.concat([slug]);
  store("shelf_favourites_v3",S.favs);
  render();
}
function toast(message) {
  const root=document.getElementById("toast-root");
  const node=document.createElement("div");
  node.className="toast";node.textContent=message;
  root.appendChild(node);
  setTimeout(()=>node.remove(),3000);
}
async function copy(value) {
  try { await navigator.clipboard.writeText(value); toast("Copied to clipboard"); }
  catch { toast("Clipboard unavailable in this browser"); }
}
function updateCatalog() {
  const matches=matching(S.query,S.filter);
  const countEl=document.getElementById("match-count");
  if(countEl)countEl.textContent=matches.length+" tools";
  const gridEl=document.getElementById("catalogue-grid");
  if(gridEl)gridEl.innerHTML=grid(matches);
}
function setFiles(fileList) {
  const slug=S.current;if(!slug)return;
  const items=Array.from(fileList).slice(0,30);
  S.inputs[slug]=Object.assign({},S.inputs[slug],{files:MULTI.has(slug)?items:items.slice(0,1)});
  const target=document.getElementById("files-list");
  if(target)target.innerHTML=fileRows(S.inputs[slug].files);
}
async function loadSource(slug) {
  S.sources[slug]=null;
  try {
    const response=await fetch("/api/tools/"+encodeURIComponent(slug)+"/source");
    if(!response.ok)throw Error("Source not available");
    const content=await response.text();
    S.sources[slug]=content;
    if(S.current===slug && S.tab==="code") {
      const target=document.getElementById("result-container");
      if(target)target.innerHTML=codePane(bySlug(slug),content);
    }
  }catch {
    S.sources[slug]="Source could not be loaded.";
    if(S.current===slug && S.tab==="code") {
      const target=document.getElementById("result-container");
      if(target)target.innerHTML=codePane(bySlug(slug),S.sources[slug]);
    }
  }
}
function setFormError(message) {
  const root=document.getElementById("form-error");
  if(root)root.innerHTML=message?'<div class="error-message" role="alert">'+esc(message)+'</div>':"";
}
function storeResult(slug,result) {
  const existing=S.results[slug];
  if(existing && existing.url)URL.revokeObjectURL(existing.url);
  S.results[slug]=result;
  const files=Object.keys(S.results).filter(key=>S.results[key].kind==="file");
  let total=files.reduce((size,key)=>size+S.results[key].blob.size,0);
  for(const key of files) {
    if(total<=40*1024*1024)break;
    if(key===slug)continue;
    total-=S.results[key].blob.size;
    URL.revokeObjectURL(S.results[key].url);
    delete S.results[key];
  }
}
async function run() {
  const slug=S.current, tool=bySlug(slug);
  if(!tool || tool.local_only || S.busy)return;
  const state=S.inputs[slug]||{};
  const uploads=state.files||[];
  if(Object.prototype.hasOwnProperty.call(FILE_TYPES,slug) && !uploads.length) {
    setFormError("Select the file you want to process.");return;
  }
  if(MULTI.has(slug) && slug==="merge-pdfs" && uploads.length<2){
    setFormError("Select at least two PDF files.");return;
  }
  const content=TEXT.has(slug)?(state.text||""):"";
  if(TEXT.has(slug) && slug!=="git-commands" && !content.trim()){
    setFormError("Enter some text to continue.");return;
  }
  const form=new FormData();
  form.append("text",content);
  const options={};
  document.querySelectorAll("[data-option]").forEach(el=>{
    const v=el.value;
    options[el.dataset.option]=el.type==="number" ? Number(v) : v;
  });
  form.append("options",JSON.stringify(options));
  for(const file of uploads)form.append("files",file,file.name);
  S.busy=true;setFormError("");
  const buttonEl=document.querySelector('[data-action="run"]');
  if(buttonEl)buttonEl.disabled=true;
  const panel=document.getElementById("result-container");
  if(panel)panel.innerHTML=resultPane(tool);
  try {
    const response=await fetch("/api/tools/"+encodeURIComponent(slug)+"/run",{method:"POST",body:form});
    if(!response.ok){
      const body=await response.json().catch(()=>({}));
      throw Error(typeof body.detail==="string"?body.detail:"The operation could not be completed.");
    }
    const mime=response.headers.get("content-type")||"application/octet-stream";
    if(mime.includes("application/json")) {
      const payload=await response.json();
      storeResult(slug,{kind:payload.kind==="video"?"video":"text",value:payload.result});
    }else {
      const blob=await response.blob();
      const filename=response.headers.get("x-utility-filename")||"result.bin";
      storeResult(slug,{kind:"file",blob,filename,mime,url:URL.createObjectURL(blob)});
    }
    S.tab="run";
    toast("Your result is ready");
  }catch(error){
    setFormError(error instanceof Error?error.message:"Processing failed");
    toast("Could not complete this operation");
  }finally{
    S.busy=false;
    if(buttonEl)buttonEl.disabled=false;
    if(panel&&S.current===slug)panel.innerHTML=resultPane(tool);
  }
}
async function handleClick(event) {
  const target=event.target.closest("[data-action]");
  if(!target)return;
  const action=target.dataset.action;
  if(target.tagName==="A" || action==="dismiss-modal")event.preventDefault();
  if(action==="dismiss-modal" && event.target!==target)return;
  switch(action){
    case "home":navigate(null,"All tools");break;
    case "category":navigate(null,target.dataset.category||"All tools");break;
    case "open":navigate(target.dataset.slug);break;
    case "fav":toggleFav(target.dataset.slug||S.current);break;
    case "search":S.modal=true;S.modalQuery="";render();break;
    case "close-modal":case "dismiss-modal":S.modal=false;render();break;
    case "theme":S.theme=S.theme==="dark"?"light":"dark";localStorage.setItem("shelf_theme_v3",S.theme);render();break;
    case "menu":S.menu=!S.menu;render();break;
    case "scroll-tools":{
      const t=document.getElementById("all-tools");
      if(t)t.scrollIntoView({behavior:"smooth"});break;
    }
    case "tab":
      S.tab=target.dataset.tab;
      render();break;
    case "run":await run();break;
    case "remove-file":{
      const input=S.inputs[S.current]||{};
      input.files=(input.files||[]).filter((_,i)=>i!==Number(target.dataset.index));
      S.inputs[S.current]=input;
      const filelist=document.getElementById("files-list");
      if(filelist)filelist.innerHTML=fileRows(input.files);break;
    }
    case "download":{
      const result=S.results[S.current];
      if(!result || !result.url)return;
      const link=document.createElement("a");
      link.href=result.url;link.download=result.filename;
      document.body.appendChild(link);link.click();link.remove();break;
    }
    case "copy-result":{
      const result=S.results[S.current];
      if(result)await copy(typeof result.value==="string"?result.value:JSON.stringify(result.value,null,2));
      break;
    }
    case "copy-code":await copy(S.sources[S.current]||"");break;
    case "retry":await init();break;
  }
}
function handleInput(event) {
  const el=event.target;
  if(el.id==="catalog-search") {
    S.query=el.value;
    updateCatalog();
  }
  if(el.id==="modal-input") {
    S.modalQuery=el.value;
    const target=document.getElementById("modal-results");
    if(target)target.innerHTML=modalResults(matching(S.modalQuery,"All tools").slice(0,12));
  }
  if(el.id==="tool-text" && S.current){
    S.inputs[S.current]=Object.assign({},S.inputs[S.current],{text:el.value});
  }
}
function handleChange(event) {
  const el=event.target;
  if(el.id==="file-upload")setFiles(el.files);
  if(el.dataset.option && S.current){
    const old=S.inputs[S.current]||{};
    old.options=Object.assign({},old.options,{[el.dataset.option]:el.value});
    S.inputs[S.current]=old;
  }
}
async function init() {
  S.ready=false;S.error="";render();
  try {
    const response=await fetch("/api/tools");
    if(!response.ok)throw Error("Could not load the tool catalogue");
    const data=await response.json();
    if(!Array.isArray(data.tools)||!Array.isArray(data.categories))throw Error("Invalid catalogue response");
    S.tools=data.tools;S.categories=data.categories;
    const slug=slugFromPath();
    S.current=slug&&bySlug(slug)?slug:null;
    if(S.current) {
      S.recent=[S.current].concat(S.recent.filter(v=>v!==S.current)).slice(0,8);
      store("shelf_recent_v3",S.recent);
    }
    S.ready=true;render();
  }catch(error) {
    S.error=error instanceof Error?error.message:"Could not load Utility Shelf";
    render();
  }
}
document.addEventListener("click",handleClick);
document.addEventListener("input",handleInput);
document.addEventListener("change",handleChange);
document.addEventListener("keydown",function(event){
  if((event.ctrlKey||event.metaKey) && event.key.toLowerCase()==="k") {
    event.preventDefault();S.modal=true;S.modalQuery="";render();
  } else if(event.key==="Escape" && S.modal){
    S.modal=false;render();
  } else if(event.key==="Enter" && S.modal && document.activeElement?.id==="modal-input"){
    const first=matching(S.modalQuery,"All tools")[0];
    if(first){event.preventDefault();navigate(first.slug);}
  } else if((event.key==="Enter"||event.key===" ") && document.activeElement?.id==="dropzone"){
    event.preventDefault();document.getElementById("file-upload")?.click();
  }
});
document.addEventListener("click",function(event){
  if(event.target.closest("#dropzone") && !event.target.closest("input")) {
    document.getElementById("file-upload")?.click();
  }
});
document.addEventListener("dragover",function(event){
  if(event.target.closest("#dropzone")){event.preventDefault();event.target.closest("#dropzone").classList.add("dragging");}
});
document.addEventListener("dragleave",function(event){
  if(event.target.closest("#dropzone"))event.target.closest("#dropzone").classList.remove("dragging");
});
document.addEventListener("drop",function(event){
  const target=event.target.closest("#dropzone");
  if(target){event.preventDefault();target.classList.remove("dragging");if(event.dataTransfer?.files)setFiles(event.dataTransfer.files);}
});
window.addEventListener("popstate",function(){
  S.current=slugFromPath()&&bySlug(slugFromPath())?slugFromPath():null;
  S.tab="run";S.modal=false;S.menu=false;render();
});
init();
