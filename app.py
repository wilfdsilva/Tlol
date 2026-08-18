import streamlit as st
import streamlit.components.v1 as components
import pathlib
import base64
import json
import re

# Configure the Streamlit page for maximum width and updated tab name
st.set_page_config(
    page_title="TCOE League of Legends",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------------
# PATHLIB METHOD: Safely load local images regardless of Streamlit Cloud working directory
# -------------------------------------------------------------------
current_dir = pathlib.Path(__file__).parent.resolve()
images_dir = current_dir / "images"

# List of all players to map
ALL_PARTICIPANTS = [
    "Adnan Shaikh","Amit Singh","Amitabh Singh","Ankit Yadav","Arijit Ghosh",
    "Arvind Arumuga Nainar","Asif Khan","Ashna Kumar","Avinash Chorage","Avinash Gowda",
    "Bhagyashree Dhotre","Bhaskar Patil","Bijal Gala","Bishal Pandit","Blessen Thomas",
    "Darshil Vekaria","Dhananjay Kulkarni","Esakki Shummugavel","Gayatri Zuting",
    "Gurpreet Kaur","Hitesh Ghadigaonkar","Irshad Darji","Jay Jagad","Jincy Geevarghese",
    "John Yesudasan","Johnson Thomas","Kartik Nair","Kiran Padwal","Kishansingh Devda",
    "Komal Panjwani","Kshitij Wadankar","Lalit Chavan","Mahesh Pale","Mayur Pawar",
    "N Pratap Kumar","Nilesh Mulik","Nilesh Sansare","Nisha Saini","Pooja Nandoskar",
    "Prachi Dalvi","Pramod Patel","Pritam Paparkar","Pritesh Menon","Rachita Harit",
    "Rahul Arjun","Rahul Pokharkar","Ravi Chavan","Ravi Khanra","Samiksha Prabhu",
    "Sanjay Tumma","Sanket Patil","Sanskar Bagwe","Saurabh Mahadik","Shreejith Menon",
    "Shweta Vichare","Somansh Datta","Suraj Kamerkar","Umesh Gawde","Umesh Tank",
    "Vibhuti Dabholkar","Vijay Chinkate","Vijay Sangale","Vishal Dubey","Vishal Shinde",
    "Wilfred Dsilva", "Esha Patel", "Parth Passi", "Kaumod Bagale", "Jagruti Chaudhari", 
    "Darshan Walwatkar", "Pritam Purohit", "Akhilesh Rai", "Soujanya Siripuram", 
    "Yogesh Karande", "Chandrajit Yadav", "Nitin Nakadi"
]

def normalize_name(name):
    """Strips all spaces, quotes, underscores, and lowers the text for foolproof matching"""
    return re.sub(r'[^a-z0-9]', '', name.lower())

image_b64_map = {}

if images_dir.exists() and images_dir.is_dir():
    local_files = {normalize_name(p.stem): p for p in images_dir.glob("*") if p.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']}
    
    for player in ALL_PARTICIPANTS:
        norm_player = normalize_name(player)
        if norm_player in local_files:
            try:
                with open(local_files[norm_player], "rb") as f:
                    b64_str = base64.b64encode(f.read()).decode("utf-8")
                    suffix = local_files[norm_player].suffix.lower()
                    if suffix == '.png':
                        mime_type = "image/png"
                    elif suffix == '.webp':
                        mime_type = "image/webp"
                    else:
                        mime_type = "image/jpeg"
                    image_b64_map[player] = f"data:{mime_type};base64,{b64_str}"
            except Exception as e:
                pass

# Serialize dictionary to JSON so JavaScript can use it safely
images_json_str = json.dumps(image_b64_map)


# Inject CSS into Streamlit to remove extra scrollbars, padding, and make the iframe fullscreen
st.markdown("""
    <style>
        .block-container { padding: 0rem !important; max-width: 100% !important; }
        header[data-testid="stHeader"] { display: none !important; }
        iframe { height: 100vh !important; width: 100vw !important; border: none !important; display: block; }
        body, html, [data-testid="stAppViewContainer"] { overflow: hidden !important; margin: 0 !important; padding: 0 !important; }
    </style>
""", unsafe_allow_html=True)

# The HTML, CSS, and JS code
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TCOE League of Legends</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0a0c12;
    --panel:#161b28;
    --panel-2:#1d2333;
    --gold:#d8b26b;
    --gold-bright:#f3d18e;
    --maroon:#7c2438;
    --maroon-bright:#a3324b;
    --cream:#f3ead8;
    --muted:#9098ac;
    --line:rgba(120,160,255,0.16);
    --hextech:#0ac8b9;
    --t-challenger:#f3d18e;
    --t-diamond:#79d3f0;
    --t-gold:#e0b64f;
    --t-bronze:#b5793f;
    --t-rookie:#8a93a6;
  }
  *{box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{
    margin:0;
    background:
      radial-gradient(1200px 600px at 15% -10%, rgba(10,200,185,0.12), transparent 60%),
      radial-gradient(1000px 500px at 90% 0%, rgba(216,178,107,0.10), transparent 55%),
      var(--bg);
    color:var(--cream);
    font-family:'Inter',sans-serif;
    -webkit-font-smoothing:antialiased;
    overflow-x: hidden;
  }
  ::selection{background:var(--gold); color:#1a1200;}
  a{color:inherit;}

  #spotlight{
    position:fixed; inset:0; pointer-events:none; z-index:5;
    background:radial-gradient(320px 320px at var(--mx,50%) var(--my,50%), rgba(10,200,185,0.07), transparent 70%);
    transition:background 0.05s linear;
  }

  /* Global Header */
  .main-header {
    position:relative; padding:70px 4vw 0; text-align:center;
  }
  .eyebrow{
    display:inline-flex; align-items:center; gap:10px;
    font-weight:700; letter-spacing:0.35em; text-transform:uppercase; font-size:11px;
    color:var(--hextech); margin-bottom:22px;
  }
  .eyebrow::before, .eyebrow::after{content:"";width:28px;height:1px;background:var(--gold);}
  .subhead{
    font-family:'Fraunces', serif; font-style:italic; font-weight:500;
    font-size:clamp(16px,2.4vw,22px); color:var(--muted); max-width:640px; margin:0 auto;
  }

  /* Custom Tab Navigation */
  .tab-nav {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 40px;
    border-bottom: 1px solid var(--line);
    padding: 0 4vw;
    flex-wrap: wrap;
  }
  .tab-btn {
    background: transparent;
    border: none;
    color: var(--muted);
    font-family: 'Bebas Neue', sans-serif;
    font-size: 24px;
    letter-spacing: 0.1em;
    padding: 12px 20px;
    cursor: pointer;
    position: relative;
    transition: color 0.3s;
  }
  .tab-btn:hover { color: var(--cream); }
  .tab-btn.active { color: var(--gold-bright); }
  .tab-btn.active::after {
    content: "";
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gold-bright);
    box-shadow: 0 -2px 10px rgba(243, 209, 142, 0.5);
  }

  .tab-content {
    display: none;
    animation: fadeIn 0.4s ease forwards;
  }
  .tab-content.active {
    display: block;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .placeholder-tab {
    text-align: center;
    padding: 100px 20px;
  }
  .placeholder-tab h2 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 48px;
    color: var(--gold-bright);
    margin: 0 0 10px;
    letter-spacing: 0.05em;
  }
  .placeholder-tab p {
    color: var(--muted);
    font-size: 16px;
  }

  .stat-strip{
    display:flex; flex-wrap:wrap; justify-content:center; margin:30px auto 44px; max-width:820px;
    border:1px solid var(--line); border-radius:14px; overflow:hidden; background:rgba(255,255,255,0.02);
  }
  .stat{flex:1 1 150px; padding:22px 18px; text-align:center; border-right:1px solid var(--line);}
  .stat:last-child{border-right:none;}
  .stat b{display:block; font-family:'Bebas Neue',sans-serif; font-size:34px; color:var(--gold-bright); letter-spacing:0.03em;}
  .stat span{font-size:11px; text-transform:uppercase; letter-spacing:0.14em; color:var(--muted);}

  /* Widened block boundaries */
  section.block{padding:60px 4vw 80px; max-width:1800px; margin:0 auto;}
  .block-head{margin-bottom:44px; text-align:center;}
  .block-head .kicker{font-size:11px; letter-spacing:0.3em; text-transform:uppercase; color:var(--maroon-bright); font-weight:700; margin-bottom:10px;}
  .block-head h2{font-family:'Bebas Neue',sans-serif; font-size:clamp(34px,5vw,54px); letter-spacing:0.03em; margin:0 0 12px;}
  .block-head p{color:var(--muted); max-width:620px; margin:0 auto; font-size:15px; line-height:1.6;}

  /* ---------- New Tabs: Schedule, Format, Teams ---------- */
  .table-responsive { overflow-x: auto; max-width: 1000px; margin: 0 auto; border-radius: 12px; border: 1px solid var(--line); background: var(--panel); }
  .styled-table { width: 100%; border-collapse: collapse; text-align: center; font-size: 15px; }
  .styled-table th, .styled-table td { padding: 16px; border-bottom: 1px solid var(--line); border-right: 1px solid var(--line); }
  .styled-table th:last-child, .styled-table td:last-child { border-right: none; }
  .styled-table th { color: var(--gold-bright); font-family: 'Bebas Neue', sans-serif; font-size: 22px; letter-spacing: 0.1em; font-weight: normal; background: rgba(0,0,0,0.2); }
  .styled-table tr:last-child td { border-bottom: none; }
  .styled-table tr:nth-child(even) { background: rgba(255,255,255,0.02); }
  .styled-table tr:hover { background: rgba(10,200,185,0.05); }

  .format-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; max-width: 1000px; margin: 0 auto; text-align: left; }
  .format-card { background: linear-gradient(180deg, var(--panel), var(--panel-2)); border: 1px solid var(--line); border-radius: 16px; padding: 36px 30px; }
  .format-card h3 { font-family: 'Bebas Neue', sans-serif; color: var(--gold-bright); font-size: 32px; margin: 0 0 20px; letter-spacing: 0.05em; text-align: center; }
  .format-card ul { padding-left: 20px; color: var(--cream); line-height: 1.8; font-size: 15px; margin: 0; }
  .points-list { list-style: none; padding: 0 !important; }
  .points-list li { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--line); }
  .points-list li:last-child { border-bottom: none; padding-bottom: 0; }
  .points-list li:first-child { padding-top: 0; }
  .points-list span.pts { color: var(--gold-bright); font-weight: 700; font-family: 'Bebas Neue', sans-serif; font-size: 20px; letter-spacing: 0.05em; }

  /* Modified Team Grid styling */
  .team-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px; max-width: 1200px; margin: 0 auto; }
  .team-card { background: linear-gradient(180deg, var(--panel), var(--panel-2)); border: 1px solid var(--line); border-radius: 16px; padding: 20px; text-align: center; transition: transform 0.3s ease, border-color 0.3s ease; }
  .team-card:hover { transform: translateY(-8px); border-color: var(--hextech); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
  .team-poster { width: 100%; aspect-ratio: 16/9; object-fit: cover; border-radius: 8px; border: 1px solid var(--line); margin-bottom: 20px; }
  .team-card h3 { font-family: 'Bebas Neue', sans-serif; color: var(--gold-bright); font-size: 26px; margin: 0 0 16px; letter-spacing: 0.05em; line-height: 1.1; }
  .team-role { color: var(--muted); margin: 0 0 12px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; }
  .team-role b { color: var(--cream); font-size: 14px; display: block; margin-top: 4px; text-transform: none; letter-spacing: normal; font-weight: 500; }
  .team-role:last-child { margin-bottom: 0; }

  /* ---------- Chapter 1: Story Slider ---------- */
  .story-slider-wrapper {
    position: relative; width: 100%; max-width: 1000px; margin: 0 auto; overflow: hidden;
    border-radius: 16px; border: 1px solid var(--line); box-shadow: 0 20px 50px rgba(0,0,0,0.5); background: var(--panel);
  }
  .story-track { display: flex; transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1); }
  .story-slide {
    min-width: 100%; position: relative; background-size: cover; background-position: center;
    aspect-ratio: 16/9; display: flex; align-items: flex-end;
  }
  .story-slide::before {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(10,12,18,0.95) 0%, rgba(10,12,18,0.7) 40%, rgba(10,12,18,0.2) 100%);
  }
  .story-content { position: relative; z-index: 2; padding: 40px 60px; width: 100%; text-align: center; }
  .story-sentence {
    opacity: 0; transform: translateY(20px); transition: opacity 0.8s ease, transform 0.8s ease;
    font-size: clamp(15px, 2vw, 18px); line-height: 1.6; color: var(--cream); margin: 0 auto 12px; max-width: 800px;
  }
  .story-sentence.visible { opacity: 1; transform: translateY(0); }
  .story-quote { font-family: 'Fraunces', serif; font-style: italic; color: var(--gold-bright); font-size: clamp(18px, 2.5vw, 24px); margin: 20px auto; }

  /* Slider Navigation */
  .slider-nav { position: absolute; top: 50%; transform: translateY(-50%); width: 100%; display: flex; justify-content: space-between; padding: 0 20px; z-index: 5; pointer-events: none; }
  .nav-btn { pointer-events: auto; background: rgba(255,255,255,0.1); border: 1px solid var(--line); color: var(--cream); width: 44px; height: 44px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 20px; backdrop-filter: blur(4px); transition: all 0.2s; }
  .nav-btn:hover:not(:disabled) { background: var(--hextech); color: #0a0c12; border-color: var(--hextech); }
  .nav-btn:disabled { opacity: 0.3; cursor: not-allowed; }
  .slider-indicators { display: flex; justify-content: center; gap: 8px; margin-top: 20px; }
  .indicator { width: 10px; height: 10px; border-radius: 50%; background: rgba(255,255,255,0.2); cursor: pointer; transition: background 0.3s; }
  .indicator.active { background: var(--gold-bright); }
  @media (max-width:760px) { .story-slide { aspect-ratio: 4/3; } .story-content { padding: 30px 40px; } }

  /* ---------- Trophy Cabinet ---------- */
  .cabinet-row{display:grid; grid-template-columns:repeat(auto-fit, minmax(320px,1fr)); gap:28px;}
  .case{position:relative; background:linear-gradient(180deg, var(--panel), var(--panel-2)); border:1px solid var(--line); border-radius:18px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.35);}
  .case-top{padding:26px 26px 20px; background:linear-gradient(160deg, rgba(124,36,56,0.5), rgba(124,36,56,0) 60%), radial-gradient(circle at 85% 0%, rgba(10,200,185,0.14), transparent 55%); border-bottom:1px dashed var(--line); position:relative;}
  .case-year{font-family:'Bebas Neue',sans-serif; font-size:15px; letter-spacing:0.25em; color:var(--gold-bright); text-transform:uppercase;}
  .case-title{font-family:'Bebas Neue',sans-serif; font-size:32px; letter-spacing:0.02em; margin:4px 0 2px;}
  .case-edition{font-family:'Fraunces',serif; font-style:italic; color:var(--muted); font-size:15px;}
  .trophy-mark{position:absolute; top:22px; right:22px; font-size:34px; display:flex; align-items:center; justify-content:center; filter:drop-shadow(0 6px 10px rgba(0,0,0,0.5));}
  .champion-line, .mvp-highlight{margin-top:14px; padding:12px 14px; border-radius:10px; font-size:13.5px; display:flex; gap:10px; align-items:flex-start; border:1px solid var(--line);}
  .champion-line{background:rgba(124,36,56,0.2); border-color:rgba(163,50,75,0.4);}
  .mvp-highlight{background:rgba(10,200,185,0.08); border-color:rgba(10,200,185,0.3);}
  .champion-line b, .mvp-highlight b{font-weight:700; display:block; font-size:12px; letter-spacing:0.06em; text-transform:uppercase;}
  .champion-line b{color:var(--maroon-bright);}
  .mvp-highlight b{color:var(--hextech);}
  .champion-line .team-name{font-family:'Fraunces',serif; font-style:italic; font-size:16px; color:var(--cream); display:block; margin-top:1px;}
  .mvp-highlight .mvp-names{font-size:15px; color:var(--cream); font-weight:600; display:block; margin-top:1px;}
  .mvp-highlight .mvp-count{font-size:11.5px; color:var(--muted);}

  .case-body{padding:18px 26px 8px;}
  .mvp-label{font-size:10.5px; letter-spacing:0.22em; text-transform:uppercase; color:var(--maroon-bright); font-weight:700; margin-bottom:10px;}
  .mvp-list{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:8px;}
  .mvp-list li{display:flex; justify-content:space-between; gap:10px; font-size:13.5px; padding:8px 10px; border-radius:8px; background:rgba(255,255,255,0.02); border:1px solid transparent;}
  .mvp-list li:hover{border-color:var(--line); background:rgba(10,200,185,0.05);}
  .mvp-list .ev{color:var(--muted); font-weight:600;}
  .mvp-list .who{color:var(--cream); text-align:right; font-weight:500;}
  .mvp-list .who.team{color:var(--gold-bright); font-style:italic;}

  .case-toggle{width:100%; margin-top:14px; padding:14px 26px; background:rgba(124,36,56,0.15); border:none; border-top:1px solid var(--line); color:var(--gold-bright); font-weight:700; font-size:12px; letter-spacing:0.15em; text-transform:uppercase; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px;}
  .case-toggle:hover{background:rgba(124,36,56,0.28);}
  .case-toggle .chev{transition:transform .25s ease;}
  .case.open .case-toggle .chev{transform:rotate(180deg);}
  .roster{max-height:0; overflow:hidden; transition:max-height .35s ease; padding:0 26px;}
  .case.open .roster{max-height:500px; padding:16px 26px 22px;}
  .roster-label{font-size:10.5px; letter-spacing:0.22em; text-transform:uppercase; color:var(--muted); margin-bottom:10px;}
  .roster-grid{display:flex; flex-wrap:wrap; gap:8px;}
  .roster-grid span{background:rgba(255,255,255,0.04); border:1px solid var(--line); padding:6px 11px; border-radius:20px; font-size:12.5px;}

  /* ---------- Round avatar frame ---------- */
  .avatar-frame{position:relative; width:100%; aspect-ratio:1; border-radius:50%; flex-shrink:0;}
  .avatar-inner{position:absolute; inset:4px; border-radius:50%; background:transparent; overflow:hidden;}
  .avatar-inner img{transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); filter: drop-shadow(0 4px 6px rgba(0,0,0,0.4)); object-fit: cover; object-position: center;}
  .rank-badge{
    position:absolute; bottom:0px; right:0px; width:26px; height:26px; border-radius:50%;
    display:flex; align-items:center; justify-content:center; font-size:13px;
    border:2px solid #0a0c12; box-shadow:0 4px 10px rgba(0,0,0,0.6); z-index:2;
  }

  /* ---------- Walk of Fame ---------- */
  .wof-controls{display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:center; margin-bottom:36px;}
  .wof-search{flex:1 1 240px; max-width:320px; background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:11px 16px; color:var(--cream); font-size:14px;}
  .wof-search::placeholder{color:var(--muted);}
  .wof-search:focus{outline:none; border-color:var(--hextech);}
  .chip-group{display:flex; gap:8px; flex-wrap:wrap;}
  .chip{padding:9px 16px; border-radius:20px; border:1px solid var(--line); background:transparent; color:var(--muted); font-size:12.5px; font-weight:600; letter-spacing:0.04em; cursor:pointer;}
  .chip:hover{color:var(--cream); border-color:var(--hextech);}
  .chip.active{background:var(--hextech); color:#04211d; border-color:var(--hextech);}

  .wof-grid{display:grid; grid-template-columns:repeat(auto-fill, minmax(230px,1fr)); gap:20px;}
  .pcard{background:linear-gradient(180deg, var(--panel), var(--panel-2)); border:1px solid var(--line); border-radius:16px; padding:26px 18px 18px; text-align:center; cursor:pointer; position:relative; overflow:hidden; transition:transform .3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow .3s ease, border-color .3s ease;}
  .pcard::before{content:""; position:absolute; inset:0; background:radial-gradient(160px 100px at 50% -10%, rgba(10,200,185,0.16), transparent 60%); opacity:0; transition:opacity .25s ease;}
  .pcard:hover{transform:translateY(-8px) scale(1.03); border-color:var(--hextech); box-shadow:0 22px 45px rgba(0,0,0,0.5);}
  .pcard:hover::before{opacity:1;}
  .pcard:hover .avatar-inner img{transform: scale(1.15);}
  .pcard .avatar-frame{width:104px; margin:0 auto 14px;}
  .tier-chip{display:inline-flex; align-items:center; gap:4px; font-size:9.5px; font-weight:800; letter-spacing:0.1em; text-transform:uppercase; padding:3px 10px; border-radius:20px; margin-bottom:8px;}
  .pcard-name{font-weight:700; font-size:15.5px; margin-bottom:4px;}
  .pcard-tag{font-size:11.5px; color:var(--muted); margin-bottom:12px;}

  .pcard-stats, .modal-stats, .tt-stats{display:flex; justify-content:center; gap:10px; font-size:10.5px; color:var(--muted);}
  .pcard-stats div, .modal-stats div, .tt-stats div {
    flex: 1; aspect-ratio: 1 / 1; display: flex; flex-direction: column; justify-content: center;
    align-items: center; background: rgba(255,255,255,0.03); border: 1px solid var(--line);
    border-radius: 8px; padding: 6px;
  }
  .pcard-stats b, .modal-stats b, .tt-stats b {display:block; color:var(--gold-bright); font-family:'Bebas Neue',sans-serif; font-size:22px; letter-spacing:0.02em; line-height:1;}

  .champ-ribbon{position:absolute; top:12px; right:-32px; transform:rotate(40deg); background:var(--maroon); color:var(--gold-bright); font-size:9.5px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; padding:4px 38px; box-shadow:0 4px 10px rgba(0,0,0,0.3); z-index:3;}
  .no-results{text-align:center; color:var(--muted); padding:40px 0; font-size:14px; display:none;}

  /* Fixed Click Animation for Cards */
  @keyframes cardPress { 0% { transform: translateY(-8px) scale(1.03); } 50% { transform: translateY(0px) scale(0.96); border-color: var(--hextech); } 100% { transform: translateY(-8px) scale(1.03); border-color: var(--hextech); } }
  .pcard.slotting { animation: cardPress 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; pointer-events: none; }

  /* ---------- Chapter 4: Full roster grid ---------- */
  .lineup-grid{ display:grid; grid-template-columns:repeat(auto-fill, minmax(130px, 1fr)); gap:26px 14px; justify-content: center; }
  .roster-card{position:relative; text-align:center; cursor:pointer;}
  .roster-card .avatar-frame{transition:transform .3s cubic-bezier(0.175, 0.885, 0.32, 1.275); margin: 0 auto; width: 90px;}
  .roster-card:hover .avatar-frame{transform:translateY(-6px) scale(1.08);}
  .roster-name{ font-size: 11.5px; font-weight: 600; color: var(--cream); margin-top: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding: 0 4px; }
  .roster-trophies{display:flex; justify-content:center; gap:4px; margin-top:4px; min-height:16px; font-size:13px;}
  .roster-tooltip{
    position:absolute; bottom:100%; left:50%; transform:translate(-50%, 12px) scale(0.9);
    width:210px; background:linear-gradient(180deg, var(--panel), var(--panel-2)); border:1px solid var(--hextech);
    border-radius:12px; padding:13px 13px 11px; opacity:0; pointer-events:none;
    transition:opacity .2s ease, transform .2s cubic-bezier(0.175, 0.885, 0.32, 1.275); z-index:20; box-shadow:0 16px 40px rgba(0,0,0,0.55);
  }
  .roster-card:hover .roster-tooltip{opacity:1; transform:translate(-50%, -4px) scale(1);}
  .roster-tooltip::after{content:""; position:absolute; top:100%; left:50%; transform:translateX(-50%); border:7px solid transparent; border-top-color:var(--hextech);}
  .roster-tooltip .tt-name{font-weight:800; font-size:14px; margin-bottom:6px;}
  .roster-tooltip .tt-tier{font-size:10px; font-weight:800; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px; display:inline-flex; align-items:center; gap:4px;}
  .roster-tooltip .tt-stats b{font-size:18px;}
  .lineup-legend{display:flex; flex-wrap:wrap; gap:16px; justify-content:center; margin-top:50px; font-size:11.5px; color:var(--muted);}
  .lineup-legend span{display:inline-flex; align-items:center; gap:6px;}

  @media (max-width:760px){ .lineup-grid{grid-template-columns:repeat(auto-fill, minmax(100px, 1fr)); gap:20px 8px;} }

  /* ---------- Modal ---------- */
  .overlay{position:fixed; inset:0; background:rgba(6,7,11,0.78); backdrop-filter:blur(6px); display:none; align-items:center; justify-content:center; z-index:50; padding:24px;}
  .overlay.show{display:flex;}
  .modal{width:100%; max-width:480px; max-height:88vh; overflow-y:auto; background:linear-gradient(180deg, var(--panel), var(--panel-2)); border:1px solid var(--line); border-radius:20px; position:relative; box-shadow:0 30px 80px rgba(0,0,0,0.6); animation:popBounce .4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;}

  @keyframes popBounce{ 0% { transform: translateY(80px) scale(0.95); opacity: 0; } 100% { transform: translateY(0) scale(1); opacity: 1; } }

  .modal-close{position:absolute; top:16px; right:16px; width:32px; height:32px; border-radius:50%; background:rgba(255,255,255,0.06); border:1px solid var(--line); color:var(--cream); font-size:16px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition: transform 0.2s, background 0.2s;}
  .modal-close:hover{background:var(--maroon); border-color:var(--maroon); transform:rotate(90deg);}
  .modal-top{padding:34px 28px 22px; text-align:center; background:radial-gradient(220px 140px at 50% 0%, rgba(10,200,185,0.12), transparent 65%); border-bottom:1px dashed var(--line);}
  .modal-top .avatar-frame{width:140px; margin:0 auto 16px;}
  .modal-name{font-family:'Bebas Neue',sans-serif; font-size:32px; letter-spacing:0.02em; margin-top:8px;}
  .modal-quote{font-family:'Fraunces',serif; font-style:italic; color:var(--gold-bright); font-size:14.5px; margin-top:10px; line-height:1.5;}
  .modal-body{padding:22px 28px 30px;}
  .modal-section{margin-bottom:20px;}
  .modal-section h4{font-size:10.5px; letter-spacing:0.22em; text-transform:uppercase; color:var(--muted); margin:0 0 10px; font-weight:700;}
  .badge-row{display:flex; flex-wrap:wrap; gap:8px;}
  .badge{padding:6px 12px; border-radius:20px; font-size:12px; font-weight:600; border:1px solid var(--line); background:rgba(255,255,255,0.03); color:var(--cream);}
  .badge.gold{background:rgba(216,178,107,0.14); border-color:var(--gold); color:var(--gold-bright);}
  .award-row{display:flex; justify-content:space-between; gap:10px; font-size:13px; padding:9px 0; border-bottom:1px solid var(--line);}
  .award-row:last-child{border-bottom:none;}
  .award-row .ev{color:var(--muted);}
  .award-row .yr{color:var(--gold-bright); font-weight:700; font-family:'Bebas Neue',sans-serif; letter-spacing:0.03em;}
  .modal-stats span{font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:var(--muted);}

  footer{text-align:center; padding:50px 6vw 60px; color:var(--muted); font-size:12.5px; border-top:1px solid var(--line);}
  footer b{color:var(--gold-bright);}
</style>
</head>
<body>

<div id="spotlight"></div>

<!-- Global Header with Tabs -->
<header class="main-header">
  <div class="eyebrow">Est. 2023 &middot; TCOE League of Legends</div>
  <p class="subhead">Three editions. One rivalry that never sat down. This is where every champion, every MVP, and every ridiculous team name earns a permanent plaque.</p>

  <div class="tab-nav">
    <button class="tab-btn active" data-target="tab-history">History</button>
    <button class="tab-btn" data-target="tab-hof">Hall of Fame</button>
    <button class="tab-btn" data-target="tab-schedule">Schedule</button>
    <button class="tab-btn" data-target="tab-format">Format</button>
    <button class="tab-btn" data-target="tab-teams">Teams</button>
    <button class="tab-btn" data-target="tab-fixtures">Fixtures</button>
    <button class="tab-btn" data-target="tab-dashboard">Dashboard</button>
  </div>
</header>

<!-- TAB: HISTORY -->
<div id="tab-history" class="tab-content active">
  <section class="block" id="story">
    <div class="block-head">
      <div class="kicker">Chapter One</div>
      <h2>The Legend of TCOE League of Legends</h2>
    </div>

    <div class="story-slider-wrapper">
      <div class="story-track" id="storyTrack">
        <!-- Slide 1 -->
        <div class="story-slide" style="background-image: url('https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/Story/1.webp');">
          <div class="story-content">
            <p class="story-sentence">Long ago, hidden behind glowing screens and endless lines of code, stood a kingdom called the Technical Center of Excellence.</p>
            <p class="story-sentence">Its people were brilliant builders, solving impossible problems every day—but many heroes knew each other only through meetings and emails.</p>
          </div>
        </div>
        <!-- Slide 2 -->
        <div class="story-slide" style="background-image: url('https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/Story/2.webp');">
          <div class="story-content">
            <p class="story-sentence">One evening, a small fellowship of dreamers gathered and asked a simple question:</p>
            <p class="story-sentence story-quote">"If we can build extraordinary solutions together, why can't we build extraordinary memories together?"</p>
            <p class="story-sentence">From that question, a magical quest began.</p>
            <p class="story-sentence">The fellowship discovered that the kingdom needed more than work. It needed friendship, teamwork, wellness, leadership, laughter, and a stronger sense of belonging.</p>
            <p class="story-sentence">So they set out to create something that would unite everyone.</p>
          </div>
        </div>
        <!-- Slide 3 -->
        <div class="story-slide" style="background-image: url('https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/Story/3.webp');">
          <div class="story-content">
            <p class="story-sentence">But the journey was not easy.</p>
            <p class="story-sentence">The dragons of Doubt, Chaos, and Logistics stood in their way. Schedules clashed, plans changed, venues vanished, and countless challenges tested their resolve.</p>
            <p class="story-sentence">Yet with every obstacle, more volunteers joined the quest, proving that the greatest strength of the kingdom was its people.</p>
          </div>
        </div>
        <!-- Slide 4 -->
        <div class="story-slide" style="background-image: url('https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/Story/4.webp');">
          <div class="story-content">
            <p class="story-sentence">At last, the fellowship unveiled The TCOE League of Legends.</p>
            <p class="story-sentence">What began as a tournament became a tradition. Colleagues became teammates, departments became one kingdom, and every match created stories that would be remembered far longer than the final score.</p>
          </div>
        </div>
        <!-- Slide 5 -->
        <div class="story-slide" style="background-image: url('https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/Story/5.webp');">
          <div class="story-content">
            <p class="story-sentence">They soon realized the greatest treasure was never the trophy—it was the friendships forged, the leaders discovered, and the culture they built together.</p>
            <p class="story-sentence">And so, every new season begins with the same timeless invitation:</p>
            <p class="story-sentence story-quote">"The next chapter of the legend is waiting... Will you become one of them?"</p>
          </div>
        </div>
      </div>
      <div class="slider-nav">
        <button class="nav-btn" id="prevBtn" disabled>&larr;</button>
        <button class="nav-btn" id="nextBtn">&rarr;</button>
      </div>
    </div>
    <div class="slider-indicators" id="sliderIndicators">
      <div class="indicator active" data-slide="0"></div>
      <div class="indicator" data-slide="1"></div>
      <div class="indicator" data-slide="2"></div>
      <div class="indicator" data-slide="3"></div>
      <div class="indicator" data-slide="4"></div>
    </div>
  </section>
</div>

<!-- TAB: HALL OF FAME -->
<div id="tab-hof" class="tab-content">
  <section class="block" id="cabinet">
    <div class="block-head">
      <div class="kicker">Chapter Two</div>
      <h2>Yearly Trophy Cabinet</h2>
      <p>Every edition, glassed in. The Year MVP is whoever won the most events that year &mdash; tap a case to open the full winning roster.</p>
    </div>
    <div class="stat-strip" id="statStrip"></div>
    <div class="cabinet-row" id="cabinetRow"></div>
  </section>

  <section class="block" id="wof">
    <div class="block-head">
      <div class="kicker">Chapter Three</div>
      <h2>Walk of Fame</h2>
      <p>Every player who ever left the TLOL floor with a trophy, styled as a Rift-ready summoner icon &mdash; rank border generated from their stats. Click a card for the full story.</p>
    </div>
    <div class="wof-controls">
      <input class="wof-search" id="searchInput" type="text" placeholder="Search a legend by name&hellip;">
      <div class="chip-group" id="yearChips"></div>
    </div>
    <div class="wof-grid" id="wofGrid"></div>
    <div class="no-results" id="noResults">No legend matches that search. Try another name or year.</div>
  </section>

  <section class="block" id="lineup">
    <div class="block-head">
      <div class="kicker">Chapter Four</div>
      <h2>The Full Roster Line-Up</h2>
      <p>Every single person who's ever played TLOL, ranked by stats &mdash; strongest record first. Hover anyone to see who they are and what they won.</p>
    </div>
    <div class="lineup-grid" id="lineupGrid"></div>
    <div class="lineup-legend" id="lineupLegend"></div>
  </section>
</div>

<!-- TAB: SCHEDULE -->
<div id="tab-schedule" class="tab-content">
  <section class="block">
    <div class="block-head">
      <h2>Tournament Schedule</h2>
      <p>Dates, venues, and formats for all upcoming events.</p>
    </div>
    <div class="table-responsive">
      <table class="styled-table">
        <thead>
          <tr>
            <th>Event</th>
            <th>Location</th>
            <th>Format</th>
            <th>Match Dates</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Mini Auction</td><td>Webex</td><td>-</td><td>Wednesday, August 12</td></tr>
          <tr><td>Mega Auction</td><td>Webex/Airoli</td><td>All</td><td>Tuesday, August 18</td></tr>
          <tr><td>Old School Game</td><td>Airoli</td><td>All</td><td>Wednesday, August 19</td></tr>
          <tr><td>Bowling</td><td>Thane</td><td>Team</td><td>Wednesday, August 19</td></tr>
          <tr><td>Foosball</td><td>Airoli</td><td>Doubles</td><td>September 2, September 9 and October 7</td></tr>
          <tr><td>Carrom</td><td>Airoli</td><td>Doubles</td><td>September 2, September 9 and October 7</td></tr>
          <tr><td>Table Tennis</td><td>Nesco</td><td>Doubles</td><td>September 3, September 30 and October 6</td></tr>
          <tr><td>Badminton</td><td>Airoli</td><td>Doubles</td><td>Thursday, October 1</td></tr>
          <tr><td>Olympic Games</td><td>Airoli</td><td>Team</td><td>Friday, October 9</td></tr>
          <tr><td>Cricket</td><td>Airoli</td><td>Team</td><td>Friday, October 9</td></tr>
          <tr><td>Prize Distribution</td><td>Airoli</td><td>-</td><td>Friday, October 9</td></tr>
        </tbody>
      </table>
    </div>
  </section>
</div>

<!-- TAB: FORMAT -->
<div id="tab-format" class="tab-content">
  <section class="block">
    <div class="block-head">
      <h2>Tournament Format</h2>
      <p>Rules, points, and mechanics driving the league.</p>
    </div>
    <div class="format-grid">
      <div class="format-card">
        <h3>How It Works</h3>
        <ul>
          <li>Players compete across various sports and challenges.</li>
          <li>Each game awards points based on performance (participation/win/bonus card points).</li>
          <li>Leaderboard will be updated weekly.</li>
          <li>Top scoring teams win prizes + ultimate bragging rights.</li>
        </ul>
      </div>
      <div class="format-card">
        <h3>Points System</h3>
        <ul class="points-list">
          <li><span>Participation</span> <span class="pts">50 Points</span></li>
          <li><span>Quarter Finals</span> <span class="pts">250 Points</span></li>
          <li><span>Semi Finals</span> <span class="pts">500 Points</span></li>
          <li><span>Runners Up</span> <span class="pts">750 Points</span></li>
          <li><span>Champion</span> <span class="pts">1000 Points</span></li>
        </ul>
      </div>
    </div>
  </section>
</div>

<!-- TAB: TEAMS -->
<div id="tab-teams" class="tab-content">
  <section class="block">
    <div class="block-head">
      <h2>The Franchises</h2>
      <p>The four teams competing for glory in the TCOE League of Legends.</p>
    </div>
    <div class="team-grid">
      
      <div class="team-card">
        <img class="team-poster" src="https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/Team%20Poster/Gayatri%20Indians.webp" alt="Gayatri Indians">
        <h3>Gayatri Indians</h3>
        <p class="team-role">Captain <b>Gayatri Zuting</b></p>
        <p class="team-role">Vice Captains <b>Sanket Patil, Johnson Thomas</b></p>
        <p class="team-role">Leads <b>Amitabh Singh</b><b>Akhilesh Rai</b></p>
        <p class="team-role">Grade 1 <b>Adnan Shaikh</b></p>
        <p class="team-role">Grade 2 <b>Somansh Datta</b></p>
        <p class="team-role">Grade 3 <b>Saurabh Mahadik</b></p>
        <p class="team-role">Grade 4 <b>Soujanya Siripuram, Rahul Arjun, Kiran Padwal</b></p>
      </div>
      
      <div class="team-card">
        <img class="team-poster" src="https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/Team%20Poster/Komal%20Knight%20Riders.webp" alt="Komal Knight Riders">
        <h3>Komal Knight Riders</h3>
        <p class="team-role">Captain <b>Komal Panjwani</b></p>
        <p class="team-role">Vice Captains <b>Umesh Gawde & Avinash Gowda</b></p>
        <p class="team-role">Leads <b>Ravi Chavan</b></p>
        <p class="team-role">Grade 1 <b>Pritesh Menon</b></p>
        <p class="team-role">Grade 2 <b>Lalit Chavan</b></p>
        <p class="team-role">Grade 3 <b>Hitesh Ghadigaonkar</b></p>
        <p class="team-role">Grade 4 <b>Bijal Gala, Esakki Shummugavel, Arvind Nainar, Kaumod Bagale, N Pratap Kumar, Mayur Pawar</b></p>
      </div>
      
      <div class="team-card">
        <img class="team-poster" src="https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/Team%20Poster/Pooja%20Super%20Kings.webp" alt="Pooja Super Kings">
        <h3>Pooja Super Kings</h3>
        <p class="team-role">Captain <b>Pooja Nandoskar</b></p>
        <p class="team-role">Vice Captains <b>Vijay Chinkate & Vishal Shinde</b></p>
        <p class="team-role">Leads <b>Nitin Nakadi</b></p>
        <p class="team-role">Grade 1 <b>Dhananjay Kulkarni</b></p>
        <p class="team-role">Grade 2 <b>Blessen Thomas</b></p>
        <p class="team-role">Grade 3 <b>Kishansingh Devda</b></p>
        <p class="team-role">Grade 4 <b>Esha Patel</b></p>
      </div>
      
      <div class="team-card">
        <img class="team-poster" src="https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/Team%20Poster/Royal%20Challengers%20Bhagyashree.webp" alt="Royal Challengers Bhagyashree">
        <h3>Royal Challengers Bhagyashree</h3>
        <p class="team-role">Captain <b>Bhagyashree Dhotre</b></p>
        <p class="team-role">Vice Captains <b>Sanskar Bagwe & Pramod Patel</b></p>
        <p class="team-role">Leads <b>Avinash Chorage, Rachita Harit</b></p>
        <p class="team-role">Grade 1 <b>Wilfred Dsilva</b></p>
        <p class="team-role">Grade 2 <b>Umesh Tank</b></p>
        <p class="team-role">Grade 3 <b>Asif Khan</b></p>
        <p class="team-role">Grade 4 <b>Yogesh Karande, Arijit Ghosh</b></p>
      </div>

    </div>
  </section>
</div>

<!-- TAB: FIXTURES -->
<div id="tab-fixtures" class="tab-content">
  <div class="placeholder-tab">
    <h2>Fixtures</h2>
    <p>The match schedule will be updated here once the teams are drawn.</p>
  </div>
</div>

<!-- TAB: DASHBOARD -->
<div id="tab-dashboard" class="tab-content">
  <div class="placeholder-tab">
    <h2>Dashboard</h2>
    <p>Player stats, historical data analysis, and advanced metrics coming soon.</p>
  </div>
</div>

<footer>
  Built from three years of carrom smack talk, foosball rematches, and one unforgettable cricket final.<br>
  <b>TLOL &mdash; The League of Legends*</b> &middot; *not that one.
</footer>

<div class="overlay" id="overlay">
  <div class="modal" id="modal"></div>
</div>

<script>
/* Inject Local Base64 Images */
const LOCAL_IMAGES = /* __IMAGES_JSON__ */;

/* ============ TAB NAVIGATION ============ */
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    tabBtns.forEach(b => b.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.target).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});

/* ============ STORY SLIDER ANIMATION ============ */
const track = document.getElementById('storyTrack');
const slides = document.querySelectorAll('.story-slide');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const indicators = document.querySelectorAll('.indicator');
let currentSlide = 0;
let storyTimeouts = [];

function updateSlider() {
  track.style.transform = `translateX(-${currentSlide * 100}%)`;
  prevBtn.disabled = currentSlide === 0;
  nextBtn.disabled = currentSlide === slides.length - 1;
  indicators.forEach((ind, i) => ind.classList.toggle('active', i === currentSlide));

  storyTimeouts.forEach(clearTimeout);
  storyTimeouts = [];

  slides.forEach((slide, sIdx) => {
    const sentences = slide.querySelectorAll('.story-sentence');
    if (sIdx === currentSlide) {
      sentences.forEach((sentence, idx) => {
        const t = setTimeout(() => sentence.classList.add('visible'), idx * 1200);
        storyTimeouts.push(t);
      });
    } else {
      sentences.forEach(s => s.classList.remove('visible'));
    }
  });
}

prevBtn.addEventListener('click', () => { if (currentSlide > 0) { currentSlide--; updateSlider(); }});
nextBtn.addEventListener('click', () => { if (currentSlide < slides.length - 1) { currentSlide++; updateSlider(); }});
indicators.forEach(ind => {
  ind.addEventListener('click', (e) => { currentSlide = parseInt(e.target.dataset.slide); updateSlider(); });
});

setTimeout(updateSlider, 300);

/* ============ RAW TOURNAMENT DATA ============ */
const TOURNAMENTS = [
  {
    id:'tlol1', label:'TLOL 1', edition:'The Experiment', year:2023, icon:'🧪',
    champion:{ team:"Tooten Dilon ki Toli", members:["Nisha Saini","Wilfred Dsilva","Dhananjay Kulkarni","Suraj Kamerkar","Saurabh Mahadik","Irshad Darji","Pooja Nandoskar","Vishal Shinde","Mayur Pawar","Mahesh Pale","Sanjay Tumma","Gayatri Zuting"] },
    events:[
      {event:"Carrom &middot; Singles", winners:["Jay Jagad"]},
      {event:"Carrom &middot; Doubles", winners:["Saurabh Mahadik","Sanjay Tumma"]},
      {event:"Foosball &middot; Doubles", winners:["Dhananjay Kulkarni","Gayatri Zuting"]},
      {event:"Table Tennis &middot; Singles", winners:["Dhananjay Kulkarni"]},
      {event:"Table Tennis &middot; Doubles", winners:["Wilfred Dsilva","Dhananjay Kulkarni"]},
      {event:"PS5 &middot; FIFA", winners:["Pritesh Menon"]},
      {event:"PS5 &middot; Racing", winners:["Arijit Ghosh"]},
      {event:"Chess", winners:["Arijit Ghosh"]},
      {event:"Cricket", team:"The MVPs"}
    ]
  },
  {
    id:'tlol2', label:'TLOL 2', edition:'Avengers Edition', year:2024, icon:'🛡️',
    champion:{ team:"Team Captain", members:["Wilfred Dsilva","Rachita Harit","Amitabh Singh","Pooja Nandoskar","Asif Khan","Vishal Shinde","Kartik Nair","Vishal Dubey","Dhananjay Kulkarni","Bishal Pandit","Adnan Shaikh","Amit Singh","Hitesh Ghadigaonkar","Esakki Shummugavel"] },
    events:[
      {event:"Pen Fighting", winners:["Wilfred Dsilva"]},
      {event:"Table Tennis &middot; Doubles", winners:["Adnan Shaikh","Dhananjay Kulkarni"]},
      {event:"PS5 &middot; Volta Doubles", winners:["Adnan Shaikh","Wilfred Dsilva"]},
      {event:"Chess", winners:["Arijit Ghosh"]},
      {event:"Carrom &middot; Doubles", winners:["Jay Jagad","Umesh Tank"]},
      {event:"Foosball &middot; Doubles", winners:["Gayatri Zuting","Blessen Thomas"]},
      {event:"Olympic Games", team:"Team Captain"},
      {event:"Cricket", team:"Team Stark"}
    ]
  },
  {
    id:'tlol3', label:'TLOL 3', edition:'Bollywood Edition', year:2025, icon:'🎬',
    champion:{ team:"Badshah Blasters", members:["Somansh Datta","Pritesh Menon","Samiksha Prabhu","Umesh Gawde","Wilfred Dsilva","Gayatri Zuting","Hitesh Ghadigaonkar","Kiran Padwal","N Pratap Kumar","Pooja Nandoskar","Saurabh Mahadik","Vijay Chinkate","Vishal Shinde"] },
    events:[
      {event:"Table Tennis &middot; Doubles", winners:["Pritesh Menon","Wilfred Dsilva"]},
      {event:"Carrom &middot; Doubles", winners:["Jay Jagad","Umesh Tank"]},
      {event:"Foosball &middot; Doubles", winners:["Blessen Thomas","Asif Khan"]},
      {event:"Chess", winners:["Saurabh Mahadik"]},
      {event:"Badminton &middot; Doubles", winners:["Pritesh Menon","Saurabh Mahadik"]},
      {event:"Olympic Games", team:"Team Gully Gang"},
      {event:"Cricket", team:"Badshah Blasters"}
    ]
  }
];

const NEW_ROOKIES = [
  "Esha Patel", "Parth Passi", "Kaumod Bagale", "Jagruti Chaudhari",
  "Darshan Walwatkar", "Pritam Purohit", "Akhilesh Rai",
  "Soujanya Siripuram", "Yogesh Karande", "Chandrajit Yadav", "Nitin Nakadi"
];

const ALL_PARTICIPANTS = [
  "Adnan Shaikh","Amit Singh","Amitabh Singh","Ankit Yadav","Arijit Ghosh",
  "Arvind Arumuga Nainar","Asif Khan","Ashna Kumar","Avinash Chorage","Avinash Gowda",
  "Bhagyashree Dhotre","Bhaskar Patil","Bijal Gala","Bishal Pandit","Blessen Thomas",
  "Darshil Vekaria","Dhananjay Kulkarni","Esakki Shummugavel","Gayatri Zuting",
  "Gurpreet Kaur","Hitesh Ghadigaonkar","Irshad Darji","Jay Jagad","Jincy Geevarghese",
  "John Yesudasan","Johnson Thomas","Kartik Nair","Kiran Padwal","Kishansingh Devda",
  "Komal Panjwani","Kshitij Wadankar","Lalit Chavan","Mahesh Pale","Mayur Pawar",
  "N Pratap Kumar","Nilesh Mulik","Nilesh Sansare","Nisha Saini","Pooja Nandoskar",
  "Prachi Dalvi","Pramod Patel","Pritam Paparkar","Pritesh Menon","Rachita Harit",
  "Rahul Arjun","Rahul Pokharkar","Ravi Chavan","Ravi Khanra","Samiksha Prabhu",
  "Sanjay Tumma","Sanket Patil","Sanskar Bagwe","Saurabh Mahadik","Shreejith Menon",
  "Shweta Vichare","Somansh Datta","Suraj Kamerkar","Umesh Gawde","Umesh Tank",
  "Vibhuti Dabholkar","Vijay Chinkate","Vijay Sangale","Vishal Dubey","Vishal Shinde",
  "Wilfred Dsilva", ...NEW_ROOKIES
];

function hashStr(s){ let h=0; for(let i=0;i<s.length;i++){ h=(h*31 + s.charCodeAt(i)) >>> 0; } return h; }

function computeYearMVP(t){
  const counts = {};
  t.events.forEach(ev=>{ (ev.winners||[]).forEach(w=>{ counts[w] = (counts[w]||0) + 1; }); });
  const max = Math.max(0, ...Object.values(counts));
  const winners = Object.keys(counts).filter(n=>counts[n]===max && max>0);
  return { winners, count:max };
}

const players = {};
function ensurePlayer(name){
  if(!players[name]) players[name] = { championships:[], events:[], yearMVP:[] };
  return players[name];
}
ALL_PARTICIPANTS.forEach(ensurePlayer);
TOURNAMENTS.forEach(t=>{
  t.champion.members.forEach(m=>{ ensurePlayer(m).championships.push({year:t.year, team:t.champion.team, edition:t.edition}); });
  t.events.forEach(ev=>{ (ev.winners||[]).forEach(w=>{ ensurePlayer(w).events.push({year:t.year, edition:t.edition, event:ev.event}); }); });
  const {winners, count} = computeYearMVP(t);
  winners.forEach(w=>{ ensurePlayer(w).yearMVP.push({year:t.year, edition:t.edition, count}); });
});

function tierFor(p){
  const score = p.championships.length*3 + p.yearMVP.length*2 + p.events.length*1;
  if(score >= 6) return 'challenger';
  if(score >= 3) return 'diamond';
  if(score >= 1) return 'gold';
  if(NEW_ROOKIES.includes(p.name)) return 'rookie';
  return 'bronze';
}

const TIER_META = {
  challenger:{ label:'Challenger', hex:'#f3d18e', badge:'👑' },
  diamond:{ label:'Diamond', hex:'#79d3f0', badge:'💎' },
  gold:{ label:'Gold', hex:'#e0b64f', badge:'🥇' },
  bronze:{ label:'Bronze', hex:'#b5793f', badge:'🥉' },
  rookie:{ label:'Rookie', hex:'#8a93a6', badge:'🌱' }
};

/* Pulls avatar safely utilizing the Pathlib Base64 Injection OR a fallback URL */
function roundAvatar(name, tier, size){
  const meta = TIER_META[tier];
  const exactName = encodeURIComponent(name).replace(/'/g, "%27");
  const fallbackUrl = `https://ui-avatars.com/api/?name=${exactName}&background=transparent&color=0a0c12&bold=true`;
  
  let imgUrl = LOCAL_IMAGES[name];
  if (!imgUrl) {
      imgUrl = `https://raw.githubusercontent.com/wilfdsilva/Tlol/main/images/${exactName}.jpg`;
  }

  return `<div class="avatar-frame" style="background:${meta.hex};${size?`width:${size}px;`:''}">
    <div class="avatar-inner">
      <img src="${imgUrl}" alt="${name}" style="width:100%; height:100%;" onerror="this.onerror=null; this.src='${fallbackUrl}';" />
    </div>
    <div class="rank-badge" style="background:${meta.hex}; color:#0a0c12;">${meta.badge}</div>
  </div>`;
}

const QUOTE_BANK = [
  "Victory isn't an option, it's a habit.",
  "First place is the only place.",
  "I don't play to participate; I play to dominate.",
  "Trophies belong in my cabinet.",
  "They played the game; I mastered it.",
  "Winning is my signature.",
  "Another tournament, another trophy.",
  "I came, I saw, I conquered.",
  "Gold is my favorite color.",
  "Champions aren't made, they are born.",
  "Second place is just the first loser.",
  "I leave no room for doubt, only victory.",
  "The MVP title was made for me.",
  "I don't sweat the competition; I am the competition.",
  "Greatness is a standard, not a goal.",
  "I don't lose. I either win or I learn.",
  "The throne is mine by right.",
  "I am the architect of my own victories.",
  "Losing is a concept I refuse to understand.",
  "Every match is a masterclass.",
  "My legacy is built on gold.",
  "I didn't just break records, I shattered them.",
  "To challenge me is to accept defeat.",
  "I write history with every win.",
  "You can't spell victory without my name.",
  "Excellence is my baseline.",
  "A champion's mindset never rests.",
  "My stat sheet speaks for itself.",
  "I dictate the pace, I determine the outcome.",
  "Undefeated in spirit, unmatched in skill.",
  "Trophies are just souvenirs of my greatness.",
  "I set the bar, then I raised it.",
  "Why be a king when you can be a god of the game?",
  "The pinnacle of competition.",
  "Winning is simply a reflex.",
  "I turn pressure into championships.",
  "Born to win, destined to lead.",
  "I demand perfection and deliver victory.",
  "They hoped for a chance; I gave them a lesson.",
  "I am the benchmark of success."
];
function quoteFor(name){
  if (NEW_ROOKIES.includes(name)) return "A new challenger approaches.";
  return QUOTE_BANK[hashStr(name) % QUOTE_BANK.length];
}

/* Replaced older flatMap with universally compatible set approach */
const allEvents = [];
TOURNAMENTS.forEach(t => t.events.forEach(e => allEvents.push(e.event)));
const uniqueEventsCount = new Set(allEvents).size;

document.getElementById('statStrip').innerHTML = `
  <div class="stat"><b>${TOURNAMENTS.length}</b><span>Editions Played</span></div>
  <div class="stat"><b>${ALL_PARTICIPANTS.length}</b><span>Players Involved</span></div>
  <div class="stat"><b>${uniqueEventsCount}+</b><span>Events Contested</span></div>
  <div class="stat"><b>${TOURNAMENTS.length}</b><span>Championship Titles</span></div>
`;

const cabinetRow = document.getElementById('cabinetRow');
TOURNAMENTS.forEach(t=>{
  const {winners: mvpWinners, count: mvpCount} = computeYearMVP(t);
  const mvpItems = t.events.map(ev=>{
    const who = ev.team ? `<span class="who team">${ev.team}</span>` : `<span class="who">${ev.winners.join(' &amp; ')}</span>`;
    return `<li><span class="ev">${ev.event}</span>${who}</li>`;
  }).join('');
  const el = document.createElement('div');
  el.className = 'case';
  el.innerHTML = `
    <div class="case-top">
      <div class="trophy-mark">${t.icon}</div>
      <div class="case-year">${t.year}</div>
      <div class="case-title">${t.label}</div>
      <div class="case-edition">${t.edition}</div>
      <div class="champion-line"><span style="font-size:20px;line-height:1;">🏆</span><span><b>Champion</b><span class="team-name">${t.champion.team}</span></span></div>
      <div class="mvp-highlight"><span style="font-size:20px;line-height:1;">🥇</span><span><b>Year MVP</b><span class="mvp-names">${mvpWinners.join(' &amp; ')}</span><span class="mvp-count">${mvpCount} event${mvpCount>1?'s':''} won</span></span></div>
    </div>
    <div class="case-body">
      <div class="mvp-label">🎖 Event Champions</div>
      <ul class="mvp-list">${mvpItems}</ul>
    </div>
    <button class="case-toggle" type="button"><span class="txt">View full championship roster</span><span class="chev">▾</span></button>
    <div class="roster">
      <div class="roster-label">${t.champion.team} &middot; ${t.champion.members.length} players</div>
      <div class="roster-grid">${t.champion.members.map(m=>`<span>${m}</span>`).join('')}</div>
    </div>
  `;
  const btn = el.querySelector('.case-toggle');
  btn.addEventListener('click', ()=>{
    el.classList.toggle('open');
    btn.querySelector('.txt').textContent = el.classList.contains('open') ? 'Close case' : 'View full championship roster';
  });
  cabinetRow.appendChild(el);
});

function buildRecord(name){
  const p = players[name];
  const years = new Set([...p.championships.map(c=>c.year), ...p.events.map(m=>m.year)]);
  return { name, ...p, years:[...years].sort(), tier: tierFor(p) };
}

const roster = Object.keys(players).map(buildRecord)
  .filter(p => p.events.length > 0)
  .sort((a,b)=> (b.championships.length*3+b.yearMVP.length*2+b.events.length) - (a.championships.length*3+a.yearMVP.length*2+a.events.length) || a.name.localeCompare(b.name));

let activeYear = 'all';
let activeQuery = '';
const years = [...new Set(TOURNAMENTS.map(t=>t.year))].sort();
yearChips.innerHTML = `<button class="chip active" data-year="all">All Years</button>` + years.map(y=>`<button class="chip" data-year="${y}">${y}</button>`).join('');
yearChips.addEventListener('click', e=>{
  const btn = e.target.closest('.chip'); if(!btn) return;
  yearChips.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
  btn.classList.add('active');
  activeYear = btn.dataset.year;
  renderGrid();
});
searchInput.addEventListener('input', e=>{ activeQuery = e.target.value.trim().toLowerCase(); renderGrid(); });

function renderGrid(){
  const filtered = roster.filter(p=>{
    const matchesYear = activeYear==='all' || p.years.includes(Number(activeYear));
    const matchesQuery = !activeQuery || p.name.toLowerCase().includes(activeQuery);
    return matchesYear && matchesQuery;
  });
  wofGrid.innerHTML = '';
  noResults.style.display = filtered.length ? 'none' : 'block';
  filtered.forEach(p=>{
    const meta = TIER_META[p.tier];
    const tagline = p.championships.length ? `Champion &middot; ${p.championships.map(c=>c.year).join(', ')}` : `${p.events.length} event${p.events.length===1?'':'s'} won`;
    const card = document.createElement('div');
    card.className = 'pcard';
    card.innerHTML = `
      ${p.championships.length ? '<div class="champ-ribbon">Champion</div>' : ''}
      ${roundAvatar(p.name, p.tier)}
      <div class="tier-chip" style="background:${meta.hex}22; color:${meta.hex}; border:1px solid ${meta.hex}66;">${meta.badge} ${meta.label}</div>
      <div class="pcard-name">${p.name}</div>
      <div class="pcard-tag">${tagline}</div>
      <div class="pcard-stats">
        <div><b>${p.championships.length}</b>Champion</div>
        <div><b>${p.yearMVP.length}</b>MVP</div>
        <div><b>${p.events.length}</b>Events</div>
      </div>
    `;
    card.addEventListener('click', function(){
      this.classList.add('slotting');
      setTimeout(() => {
        this.classList.remove('slotting');
        openModal(p);
      }, 250);
    });
    wofGrid.appendChild(card);
  });
}
renderGrid();

const overlay = document.getElementById('overlay');
const modal = document.getElementById('modal');
function openModal(p){
  const meta = TIER_META[p.tier];
  const teamBadges = p.championships.map(c=>`<span class="badge gold">🏆 ${c.team} &middot; ${c.year}</span>`).join('');
  const mvpBadges = p.yearMVP.map(m=>`<span class="badge gold">🥇 ${m.edition} &middot; ${m.year}</span>`).join('');
  const eventRows = p.events.length
    ? p.events.map(m=>`<div class="award-row"><span class="ev">${m.event}</span><span class="yr">${m.year}</span></div>`).join('')
    : `<div class="award-row"><span class="ev">No individual events yet.</span></div>`;

  modal.style.animation = 'none';
  modal.offsetHeight;
  modal.style.animation = null;

  modal.innerHTML = `
    <button class="modal-close" id="closeBtn">&times;</button>
    <div class="modal-top">
      ${roundAvatar(p.name, p.tier)}
      <div class="tier-chip" style="background:${meta.hex}22; color:${meta.hex}; border:1px solid ${meta.hex}66;">${meta.badge} ${meta.label}</div>
      <div class="modal-name">${p.name}</div>
      <div class="modal-quote">&ldquo;${quoteFor(p.name)}&rdquo;</div>
    </div>
    <div class="modal-body">
      <div class="modal-section">
        <div class="modal-stats">
          <div><b>${p.championships.length}</b><span>Champion</span></div>
          <div><b>${p.yearMVP.length}</b><span>MVP</span></div>
          <div><b>${p.events.length}</b><span>Events</span></div>
        </div>
      </div>
      ${p.championships.length ? `<div class="modal-section"><h4>Championship Teams</h4><div class="badge-row">${teamBadges}</div></div>` : ''}
      ${p.yearMVP.length ? `<div class="modal-section"><h4>Year MVP Awards</h4><div class="badge-row">${mvpBadges}</div></div>` : ''}
      <div class="modal-section"><h4>Events Won</h4>${eventRows}</div>
      <div class="modal-section"><h4>Years Active</h4><div class="badge-row">${p.years.length ? p.years.map(y=>`<span class="badge">${y}</span>`).join('') : '<span class="badge">Awaiting First Draft</span>'}</div></div>
    </div>
  `;
  overlay.classList.add('show');
  modal.querySelector('#closeBtn').addEventListener('click', closeModal);
}
function closeModal(){ overlay.classList.remove('show'); }
overlay.addEventListener('click', e=>{ if(e.target===overlay) closeModal(); });
document.addEventListener('keydown', e=>{ if(e.key==='Escape') closeModal(); });

const lineupGrid = document.getElementById('lineupGrid');
const yearIcon = {}; TOURNAMENTS.forEach(t=> yearIcon[t.year] = t.icon);

const fullRoster = ALL_PARTICIPANTS.map(buildRecord)
  .sort((a,b)=> (b.championships.length*3+b.yearMVP.length*2+b.events.length) - (a.championships.length*3+a.yearMVP.length*2+a.events.length) || a.name.localeCompare(b.name));

fullRoster.forEach(p=>{
  const meta = TIER_META[p.tier];
  const trophies = p.championships.map(c=>`<span title="Champion ${c.year}">${yearIcon[c.year]}</span>`).join('');
  const el = document.createElement('div');
  el.className = 'roster-card';

  el.innerHTML = `
    ${roundAvatar(p.name, p.tier)}
    <div class="roster-name" title="${p.name}">${p.name}</div>
    <div class="roster-trophies">${trophies}</div>
    <div class="roster-tooltip">
      <div class="tt-name">${p.name}</div>
      <div class="tt-tier" style="color:${meta.hex};">${meta.badge} ${meta.label}</div>
      <div class="tt-stats">
        <div><b>${p.championships.length}</b>Champ</div>
        <div><b>${p.yearMVP.length}</b>MVP</div>
        <div><b>${p.events.length}</b>Events</div>
      </div>
    </div>
  `;
  el.addEventListener('click', ()=>{ openModal(p); });
  lineupGrid.appendChild(el);
});

const legendEl = document.getElementById('lineupLegend');
legendEl.innerHTML = Object.keys(TIER_META).map(k=>{
  const m = TIER_META[k];
  return `<span><i style="background:${m.hex}; border-radius:50%; display:inline-block; width:10px; height:10px;"></i>${m.label}</span>`;
}).join('');

const spot = document.getElementById('spotlight');
window.addEventListener('pointermove', e=>{
  spot.style.setProperty('--mx', e.clientX+'px');
  spot.style.setProperty('--my', e.clientY+'px');
});
</script>
</body>
</html>
"""

# Dynamically inject the local image Base64 mappings generated by Pathlib
html_code = html_code.replace("/* __IMAGES_JSON__ */", images_json_str)

components.html(html_code, scrolling=True)
