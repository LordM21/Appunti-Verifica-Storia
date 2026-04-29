import re

html_path = '/home/lordm21/Desktop/Websites/Materia/Storia.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS to include chapter-questions
css_insert = """
        /* CHAPTER QUESTIONS */
        .chapter-questions {
            background: var(--parchment-mid);
            border-radius: 6px;
            padding: 1.5rem;
            margin-top: 2.5rem;
            border-left: 4px solid var(--teal);
            box-shadow: 0 4px 12px var(--shadow);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .chapter-questions:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px var(--shadow-strong);
        }

        .chapter-questions h4 {
            font-family: 'Playfair Display', serif;
            color: var(--teal);
            margin-bottom: 1rem;
            font-size: 1.15rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .chapter-questions h4::before {
            content: '❓';
            font-size: 1.1rem;
        }

        .question-block {
            margin-bottom: 1rem;
        }

        .question-block:last-child {
            margin-bottom: 0;
        }

        .question-type {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--ink-light);
            display: block;
            margin-bottom: 0.2rem;
        }

        .question-text {
            font-size: 0.95rem;
            color: var(--ink-mid);
            font-weight: 500;
        }
"""
content = content.replace("/* GLOSSARY CARDS */", css_insert + "\n        /* GLOSSARY CARDS */")

# 2. Update Nav
nav_regex = re.compile(r'(<div class="nav-section-label">Parte I — XIII-XV sec\.</div>).*?(<a href="#s4">4\. Guerra dei Cent\'anni</a>)', re.DOTALL)
content = nav_regex.sub(r'\1\n        \2', content)

# 3. Renumber Nav Links
for old_id in range(4, 16):
    new_id = old_id - 3
    # Replace href and number in nav
    content = re.sub(rf'<a href="#s{old_id}">{old_id}\. ', rf'<a href="#s{new_id}">{new_id}. ', content)

# 4. Remove Chapters 1, 2, 3
chaps_regex = re.compile(r'<!-- ======= CHAPTER 1 ======= -->.*?<!-- ======= CHAPTER 4 ======= -->', re.DOTALL)
content = chaps_regex.sub('<!-- ======= CHAPTER 1 ======= -->', content)

# 5. Renumber Chapters and add questions
# First, renumber the Chapter Comments and IDs
for old_id in range(4, 16):
    new_id = old_id - 3
    content = content.replace(f'<!-- ======= CHAPTER {old_id} ======= -->', f'<!-- ======= CHAPTER {new_id} ======= -->')
    content = content.replace(f'<section class="chapter" id="s{old_id}">', f'<section class="chapter" id="s{new_id}">')
    content = content.replace(f'<div class="chapter-number">Capitolo {old_id:02d}</div>', f'<div class="chapter-number">Capitolo {new_id:02d}</div>')

# Define Questions
questions = {
    1: ("Quali furono le principali cause che scatenarono la Guerra dei Cent'anni?", "In quale anno terminò la Guerra dei Cent'anni con la battaglia di Castillon? (A: 1337, B: 1453, C: 1429)"),
    2: ("Perché il conflitto prese il nome di \"Guerra delle Due Rose\"?", "Quale re salì al trono nel 1485 ponendo fine al conflitto? (A: Enrico V, B: Enrico VII Tudor, C: Riccardo III)"),
    3: ("Quali furono le decisioni prese dai Re Cattolici nel 1492 per omogeneizzare il regno dal punto di vista religioso?", "Chi finanziarono i Re Cattolici nel 1492 per il suo viaggio di esplorazione? (A: Amerigo Vespucci, B: Ferdinando Magellano, C: Cristoforo Colombo)"),
    4: ("In che modo Ivan III liberò la Russia dal dominio straniero?", "Da quale parola latina deriva il titolo \"Zar\"? (A: Rex, B: Caesar, C: Imperator)"),
    5: ("Qual era l'obiettivo principale dell'Unione di Kalmar?", "In quale anno si formò l'Unione di Kalmar? (A: 1397, B: 1492, C: 1515)"),
    6: ("Qual è la differenza principale nel modo di pensare tra l'epoca medievale e l'Umanesimo?", "Chi inventò la prospettiva lineare a Firenze? (A: Leonardo da Vinci, B: Filippo Brunelleschi, C: Michelangelo)"),
    7: ("Perché le scoperte astronomiche di Galilei e Copernico crearono conflitti con la Chiesa?", "Chi sostenne per primo che è la Terra a girare intorno al Sole e non viceversa? (A: Galileo Galilei, B: Niccolò Copernico, C: Johannes Kepler)"),
    8: ("Quali furono le conseguenze sociali ed economiche dell'invenzione della stampa?", "Chi è l'inventore della stampa a caratteri mobili in Europa? (A: Johannes Gutenberg, B: Lorenzo il Magnifico, C: Aldo Manuzio)"),
    9: ("Perché Lorenzo de' Medici era chiamato \"l'ago della bilancia\"?", "Quale evento avvenne il 26 aprile 1478 a Firenze? (A: Pace di Lodi, B: Congiura dei Pazzi, C: Discesa di Carlo VIII)"),
    10: ("Quali erano le ragioni economiche e politiche alla base delle grandi esplorazioni marittime del XV secolo?", "Come si chiamavano le tre navi di Cristoforo Colombo? (A: Santa Maria, Niña, Pinta, B: Victoria, Trinidad, San Antonio, C: Mayflower, Speedwell, Discovery)"),
    11: ("Perché si diceva che nel regno di Carlo V \"non tramontasse mai il sole\"?", "Quale dei seguenti territori NON faceva parte dell'impero di Carlo V? (A: Spagna, B: Germania, C: Inghilterra)"),
    12: ("Perché Martin Lutero criticò duramente la pratica delle indulgenze?", "In quale data Martin Lutero pubblicò le sue 95 tesi? (A: 12 ottobre 1492, B: 31 ottobre 1517, C: 26 aprile 1478)"),
}

for chap_id in range(1, 13):
    q_open, q_close = questions[chap_id]
    q_html = f"""
                <div class="chapter-questions">
                    <h4>Domande di Ripasso</h4>
                    <div class="question-block">
                        <span class="question-type">Domanda Aperta</span>
                        <div class="question-text">{q_open}</div>
                    </div>
                    <div class="question-block">
                        <span class="question-type">Domanda Chiusa</span>
                        <div class="question-text">{q_close}</div>
                    </div>
                </div>
            </section>"""
    # Replace the closing tag of the section with the questions + closing tag
    if chap_id < 12:
        content = re.sub(rf'(<section class="chapter" id="s{chap_id}">.*?)(</section>)', rf'\1{q_html}', content, flags=re.DOTALL)
    else:
        # Chapter 12 is the last chapter before Cronologia, need to be careful not to replace all sections
        # Match only up to the first </section> after the start of the chapter
        content = re.sub(rf'(<section class="chapter" id="s12">.*?)(\n            </section>)', rf'\1\n{q_html}', content, flags=re.DOTALL|re.MULTILINE)

# Adjust visual aesthetics (e.g. hero stats if we changed chapters)
content = content.replace('<span class="hero-stat-num">17</span>', '<span class="hero-stat-num">12</span>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
