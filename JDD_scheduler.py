import pandas as pd
from datetime import timedelta, datetime

def generate_jdd_latex(schedule, time_col_width="12mm", speaker_col_width="48mm", filename=None):
   """
   Generate LaTeX document for the 'Journée des Doctorants' schedule.

   Args:
      schedule (list[dict]): List of talks or events with keys:
         - 'Start': datetime
         - 'End': datetime
         - 'Speaker': str
         - 'Title': str
         - 'Online': [0/1]
         - 'ID': integer ID
      time_col_width (str): Width of the time column (e.g. '12mm')
      speaker_col_width (str): Width of the speaker column (e.g. '48mm')
      filename (str, optional): If provided, saves LaTeX content to this file.

   Returns:
      str: The generated LaTeX content.
   """

   # --- Static document header ---
   header = r"""% JDD Generator
% 11/2025: v0.0: Erwan ZAMORA MEDINA 
% 11/2025: v0.1: Simon KERN
%
\documentclass[11pt,a4paper]{article}
% --- Encoding & language ---
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[french]{babel}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage[a4paper,margin=20mm]{geometry}
\usepackage{xcolor}
% RED HESAM/CNAM FOR M2N
\definecolor{redHESAM}{RGB}{210,0,37}
\definecolor{brand}{HTML}{0B7BD0} 
\definecolor{brandlight}{HTML}{EAF4FC}
\definecolor{accent}{HTML}{FF7A59} 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%--- Typography & rules ---
\usepackage{titlesec}
\titleformat{\section}
  {\Large\bfseries\color{brand}}
  {\thesection}{1em}{}
\titleformat{\subsection}
  {\large\bfseries\color{brand}}
  {\thesubsection}{1em}{}
\usepackage{enumitem}
\setlist[itemize]{label=\textbullet, leftmargin=1.2em}
%% Beautiful color box :)
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{array}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% --- Logos & header ---
\usepackage{graphicx}
\usepackage{fancyhdr}
\graphicspath{{./} {../} {./logos/}} %Repertoire des images
\newlength\logoh
\setlength{\logoh}{12mm} % logo height (adjust as needed)
\newcommand{\LeftLogo}{}
\newcommand{\RightLogo}{}
\newcommand{\setlogos}[2]{\renewcommand{\LeftLogo}{#1}\renewcommand{\RightLogo}{#2}}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\setlength{\headheight}{18mm} % must be >= logo height
\setlength{\headsep}{1mm}
\lhead{\ifx\LeftLogo\empty\relax\else\includegraphics[height=\logoh]{\LeftLogo}\fi}
\rhead{\ifx\RightLogo\empty\relax\else\includegraphics[height=\logoh]{\RightLogo}\fi}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Define template boxes s...
\newtcolorbox{eventheader}[1][]{enhanced, colback=brandlight, colframe=brand, boxrule=0.7pt, arc=2mm, left=3mm, right=3mm, top=3mm, bottom=3mm, before skip=6pt, after skip=10pt, breakable, #1}
\newtcolorbox{separatorbox}[1][]{enhanced, colback=brand!6, colframe=brand!40, boxrule=0.5pt, arc=1.6mm, fontupper=\bfseries, left=4mm,right=4mm,top=2.5mm,bottom=2.5mm, before skip=6pt, after skip=6pt, before upper=\centering, #1}
\renewcommand{\titleline}{\par\vspace{2mm}\noindent\color{brand}\rule{\linewidth}{0.9pt}\par\vspace{1mm}}
\newcolumntype{L}{>{\raggedright\arraybackslash}X}
\newcommand{\talk}[4]{\textbf{#1:#2} & \textbf{#3} & \emph{\og #4 \fg}\\}
\newcommand{\onlinetalk}[4]{\textbf{#1:#2} & \textbf{#3} & \emph{\og #4 \fg} \textbf{(online)}\\}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\EventTitle}{Journée des doctorants \the\year\, \textendash\, Planning}
\newcommand{\EventDate}{Lundi 17~novembre~2025} % change as needed
\newcommand{\EventOrg}{DynFluid}                % change as needed
\newcommand{\EventPlace}{Amphi Pinel}           % change as needed
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\begin{document}
\setlogos{logos/dynfluid_980.png}{logos/m2n_1.png}
\sffamily

% Title
{\huge\bfseries\color{redHESAM} \EventTitle\par}
\vspace*{-3mm}
\titleline
{\large \EventDate \quad\textcolor{brand}{\textbullet}\quad \EventPlace\par}

% Header info
\begin{eventheader}
\begin{itemize}[nosep]
  \item \textbf{Accueil \EventOrg :} Café — à partir de \textbf{9\,h\,00}
  \item \textbf{Démarrage Teams :} \EventPlace{} — \textbf{9\,h\,25}
\end{itemize}
\end{eventheader}
\renewcommand{\arraystretch}{1.2}
"""

   # --- Schedule block generation ---
   latex = []
   latex.append("%Schedule block")
   latex.append("\\begin{tcolorbox}[enhanced, breakable, colback=white, colframe=brand!50, boxrule=0.6pt, arc=2mm, left=3mm, right=3mm, top=2mm, bottom=2mm]\\vspace{1mm}")
   latex.append("\\noindent\\textbf{Matinée}\\par\\smallskip")
   latex.append(f"\\begin{{tabularx}}{{\\linewidth}}{{@{{}}>{{\\bfseries}}p{{{time_col_width}}} >{{\\raggedright\\arraybackslash}}p{{{speaker_col_width}}} X@{{}}}}")
   latex.append("\\toprule")

   for s in schedule:
      if "Lunch" in s["Speaker"]:
         latex.append("\\bottomrule\\\[-6mm]")
         latex.append("\\end{tabularx}\n")
         latex.append("\\begin{separatorbox}[colback=accent!10,colframe=accent!50]")
         latex.append(f" {s['Start'].strftime('%H')}\\,h\\,{s['Start'].strftime('%M')} — {s['End'].strftime('%H')}\\,h\\,{s['End'].strftime('%M')} \\quad Pause déjeuner")
         latex.append("\\end{separatorbox}\n")
         latex.append("\\noindent\\textbf{Après-midi}\\par\\smallskip")
         latex.append(f"\\begin{{tabularx}}{{\\linewidth}}{{@{{}}>{{\\bfseries}}p{{{time_col_width}}} >{{\\raggedright\\arraybackslash}}p{{{speaker_col_width}}} X@{{}}}}")
         latex.append("\\toprule")
      elif "Coffee" in s["Speaker"]:
         latex.append("\\multicolumn{3}{@{}l@{}}{\\begin{separatorbox}[colback=brand!6,colframe=brand!30]")
         latex.append(f" {s['Start'].strftime('%H')}\\,h\\,{s['Start'].strftime('%M')} — {s['End'].strftime('%H')}\\,h\\,{s['End'].strftime('%M')} \\quad Pause café")
         latex.append("\\end{separatorbox}}\\\\[2mm]")
      else:
         if s['Online'] == 1:
             ttype = 'onlinetalk'
         else:
             ttype = 'talk'
         latex.append(f"\\{ttype}{{{s['Start'].strftime('%H')}}}{{{s['Start'].strftime('%M')}}}{{{s['Speaker']}}}{{{s['Title']}}}")

   latex.append("\\bottomrule\n\\end{tabularx}\n\\vspace{1mm}\n\\end{tcolorbox}")

   # --- Footer ---
   footer = r"""
\begin{flushright}
\small \textcolor{redHESAM!70}{Content coordinator: J. S. KERN. Artistic director: E. ZAMORA-MEDINA. \today}
\end{flushright}
\end{document}
"""

   full_tex = "\n".join([header] + latex + [footer])

   if filename:
      with open(filename, "w", encoding="utf-8") as f:
         f.write(full_tex)

   return full_tex

# --- Read CSV and label rows ---
df = pd.read_csv("JDD_2025.csv")
df.insert(0, "ID", range(len(df)))  # add row numbers for reference

# --- Define constants ---
START_TIME = datetime.strptime("09:25", "%H:%M")
LUNCH_START = datetime.strptime("12:00", "%H:%M")
LUNCH_END = datetime.strptime("14:00", "%H:%M")
COFFEE_START = datetime.strptime("15:40", "%H:%M")
COFFEE_END = datetime.strptime("16:00", "%H:%M")

# Example speaking order (all talks in order)
order = [3, 2, 6, 10, 11, 4, 0, 1, 5, 9, 8, 7]

# --- Build schedule ---
schedule = []
current_time = START_TIME

for idx in order:
    row = df.iloc[idx]
    duration = int(row["TIME"]) + 10
    end_time = current_time + timedelta(minutes=duration)

    # Handle lunch break
    if current_time <= LUNCH_START and end_time > LUNCH_START:
        schedule.append({
            "Speaker": "--- Lunch Break ---",
            "Title": "",
            "Start": LUNCH_START,
            "End": LUNCH_END,
            "ID": -1,
            "Online": -1
        })
        current_time = LUNCH_END
        end_time = current_time + timedelta(minutes=duration)

    # Handle coffee break
    if current_time <= COFFEE_START and end_time > COFFEE_START:
        schedule.append({
            "Speaker": "--- Coffee Break ---",
            "Title": "",
            "Start": COFFEE_START,
            "End": COFFEE_END,
            "ID": -1,
            "Online": -1
        })
        current_time = COFFEE_END
        end_time = current_time + timedelta(minutes=duration)

    schedule.append({
        "Speaker": f"{row['FIRSTNAME']} {row['LASTNAME']}",
        "Title": row["TITLE"],
        "Start": current_time,
        "End": end_time,
        "ID": idx,
        "Online": row["ONLINE"]
    })
    current_time = end_time

# --- Display schedule summary ---
print("\nGenerated Schedule:")
for s in schedule:
    if "Lunch" in s["Speaker"]:
        print(f"\n{s['Start'].strftime('%H:%M')}–{s['End'].strftime('%H:%M')}   Lunch Break\n")
    elif "Coffee" in s["Speaker"]:
        print(f"\n{s['Start'].strftime('%H:%M')}–{s['End'].strftime('%H:%M')}   Coffee Break\n")
    else:
        print(f"{s['Start'].strftime('%H:%M')}–{s['End'].strftime('%H:%M')} {s['ID']:3d} {s['Speaker']:20s} {s['Title']}")

# --- Ask user for confirmation ---
resp = input("\nCreate Latex output for this schedule? (yes/NO): ").strip().lower()

if resp == "yes":
   latex = generate_jdd_latex(schedule, time_col_width="12mm", speaker_col_width="48mm", filename="jdd_schedule.tex")
   print("\n\n===== LaTeX Schedule Block =====\n")
   print(latex)
   print("\n================================")
else:
    print("\nExit.")