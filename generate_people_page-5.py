import yaml

# Read the people.yml file
with open('_data/people.yml', 'r', encoding='utf-8') as f:
    people_data = yaml.safe_load(f)

# Filter out any template rows
for category in ['students', 'academics', 'researchers', 'fellows', 'postdocs', 'alumni']:
    if category in people_data and people_data[category]:
        people_data[category] = [p for p in people_data[category] if p.get('name') != 'Full name']

# Sort academics by rank (Professors first, then Lecturers/Assistant Professors)
if people_data.get('academics'):
    def academic_rank(person):
        role = person.get('role', '').lower()
        # Check for full professor (but not assistant professor)
        if 'professor' in role and 'assistant' not in role and 'associate' not in role:
            return 0
        # Lecturers and Assistant/Associate Professors
        elif 'lecturer' in role or 'assistant professor' in role or 'associate professor' in role:
            return 1
        else:
            return 2
    
    people_data['academics'] = sorted(people_data['academics'], key=academic_rank)

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>People - Environmental Modelling, Data & AI Systems Group</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --electric: #ffa726;
            --deep-blue: #1a1a2e;
            --slate: #16213e;
            --ice: #eef1f5;
            --accent: #ff6b9d;
            --warm: #ffcc80;
            --grid-size: 40px;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            scroll-behavior: smooth;
            scroll-padding-top: 100px;
        }
        
        body {
            font-family: 'Outfit', sans-serif;
            background: var(--deep-blue);
            color: var(--ice);
            line-height: 1.6;
            overflow-x: hidden;
            position: relative;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(90deg, rgba(255, 167, 38, 0.03) 1px, transparent 1px),
                linear-gradient(rgba(255, 167, 38, 0.03) 1px, transparent 1px);
            background-size: var(--grid-size) var(--grid-size);
            pointer-events: none;
            z-index: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 100px 50px;
            position: relative;
            z-index: 1;
        }
        
        header {
            margin-bottom: 50px;
        }
        
        h1 {
            font-size: 3.5rem;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 20px;
            background: linear-gradient(135deg, var(--ice) 0%, var(--warm) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .back-link {
            display: inline-block;
            color: var(--electric);
            text-decoration: none;
            margin-bottom: 30px;
            font-size: 0.95rem;
            transition: color 0.3s ease;
        }
        
        .back-link:hover {
            color: var(--warm);
        }
        
        /* People page navigation */
        .people-nav {
            background: rgba(22, 33, 62, 0.6);
            padding: 20px 30px;
            border-radius: 8px;
            border-left: 4px solid var(--electric);
            margin-bottom: 50px;
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .people-nav span {
            color: var(--electric);
            font-weight: 600;
            font-size: 1rem;
        }
        
        .people-nav a {
            color: rgba(238, 241, 245, 0.8);
            text-decoration: none;
            font-size: 0.95rem;
            transition: color 0.3s ease;
            padding: 5px 10px;
            border-radius: 4px;
        }
        
        .people-nav a:hover {
            color: var(--electric);
            background: rgba(255, 167, 38, 0.1);
        }
        
        .section-title {
            font-size: 2rem;
            font-weight: 700;
            margin: 60px 0 30px 0;
            color: var(--electric);
        }
        
        .person-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }
        
        .person-card {
            background: rgba(22, 33, 62, 0.6);
            padding: 30px;
            border-left: 3px solid var(--slate);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .person-card:hover {
            border-left-color: var(--electric);
            background: rgba(22, 33, 62, 0.8);
            transform: translateY(-5px);
        }
        
        .person-photo {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 20px;
            border: 3px solid var(--electric);
        }
        
        .person-name {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--electric);
            margin-bottom: 8px;
        }
        
        .person-role {
            font-size: 1rem;
            color: var(--warm);
            margin-bottom: 15px;
            font-weight: 500;
        }
        
        .person-bio, .person-interests {
            font-size: 0.95rem;
            color: rgba(238, 241, 245, 0.9);
            margin-bottom: 12px;
            line-height: 1.6;
        }
        
        .person-hobby {
            font-size: 0.9rem;
            color: var(--accent);
            font-style: italic;
            margin-top: 15px;
        }
        
        .person-tools {
            font-size: 0.85rem;
            color: rgba(238, 241, 245, 0.7);
            font-family: 'JetBrains Mono', monospace;
            margin-top: 10px;
        }
        
        .person-contact {
            font-size: 0.9rem;
            margin-top: 15px;
            word-break: break-word;
        }
        
        .person-contact a {
            color: var(--electric);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .person-contact a:hover {
            color: var(--warm);
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 60px 25px;
            }
            
            h1 {
                font-size: 2.5rem;
            }
            
            .person-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← Back to home</a>
        <header>
            <h1>Our People</h1>
        </header>
        
        <nav class="people-nav">
            <span>Jump to:</span>
            <a href="#faculty">Faculty</a>
            <a href="#phd-students">PhD Students</a>
            <a href="#researchers">Researchers & Fellows</a>
            <a href="#alumni">Alumni</a>
        </nav>
'''

def generate_person_card(person):
    card = '            <div class="person-card">\n'
    # Use placeholder if no photo provided
    photo_url = person.get('photo', 'placeholder_profile.png')
    card += f'                <img src="{photo_url}" alt="{person["name"]}" class="person-photo">\n'
    card += f'                <div class="person-name">{person["name"]}</div>\n'
    card += f'                <div class="person-role">{person["role"]}</div>\n'
    if person.get('bio'):
        card += f'                <div class="person-bio">{person["bio"]}</div>\n'
    if person.get('interests'):
        card += f'                <div class="person-interests"><strong>Research:</strong> {person["interests"]}</div>\n'
    if person.get('hobby'):
        card += f'                <div class="person-hobby"><strong>Hobby:</strong> {person["hobby"]}</div>\n'
    if person.get('tools'):
        card += f'                <div class="person-tools">Tools: {person["tools"]}</div>\n'
    if person.get('contact'):
        card += f'                <div class="person-contact">{person["contact"]}</div>\n'
    card += '            </div>\n'
    return card

def generate_alumni_card(person):
    card = '            <div class="person-card">\n'
    # Use placeholder if no photo provided
    photo_url = person.get('photo', 'placeholder_profile.png')
    card += f'                <img src="{photo_url}" alt="{person["name"]}" class="person-photo">\n'
    card += f'                <div class="person-name">{person["name"]}</div>\n'
    if person.get('former_role'):
        card += f'                <div class="person-role">{person["former_role"]}</div>\n'
    if person.get('bio'):
        card += f'                <div class="person-bio">{person["bio"]}</div>\n'
    if person.get('interests'):
        card += f'                <div class="person-interests"><strong>Research:</strong> {person["interests"]}</div>\n'
    if person.get('hobby'):
        card += f'                <div class="person-hobby"><strong>Hobby:</strong> {person["hobby"]}</div>\n'
    if person.get('tools'):
        card += f'                <div class="person-tools">Tools: {person["tools"]}</div>\n'
    if person.get('contact'):
        card += f'                <div class="person-contact">{person["contact"]}</div>\n'
    card += '            </div>\n'
    return card

# Academics section
if people_data.get('academics'):
    html_template += '        <h2 class="section-title" id="faculty">Faculty</h2>\n'
    html_template += '        <div class="person-grid">\n'
    for person in people_data['academics']:
        html_template += generate_person_card(person)
    html_template += '        </div>\n'

# Fellows section
if people_data.get('fellows'):
    html_template += '        <h2 class="section-title" id="fellows">Research Fellows</h2>\n'
    html_template += '        <div class="person-grid">\n'
    for person in people_data['fellows']:
        html_template += generate_person_card(person)
    html_template += '        </div>\n'

# Postdocs section
if people_data.get('postdocs'):
    html_template += '        <h2 class="section-title" id="postdocs">Postdoctoral Researchers</h2>\n'
    html_template += '        <div class="person-grid">\n'
    for person in people_data['postdocs']:
        html_template += generate_person_card(person)
    html_template += '        </div>\n'

# Students section
if people_data.get('students'):
    html_template += '        <h2 class="section-title" id="phd-students">PhD Students</h2>\n'
    html_template += '        <div class="person-grid">\n'
    for person in people_data['students']:
        html_template += generate_person_card(person)
    html_template += '        </div>\n'

# Researchers section  
if people_data.get('researchers'):
    html_template += '        <h2 class="section-title" id="researchers">Researchers & Fellows</h2>\n'
    html_template += '        <div class="person-grid">\n'
    for person in people_data['researchers']:
        html_template += generate_person_card(person)
    html_template += '        </div>\n'

# Alumni section
if people_data.get('alumni'):
    html_template += '        <h2 class="section-title" id="alumni">Alumni</h2>\n'
    html_template += '        <div class="person-grid">\n'
    for person in people_data['alumni']:
        html_template += generate_alumni_card(person)
    html_template += '        </div>\n'

html_template += '''    </div>
</body>
</html>'''

with open('people.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Generated people.html successfully")
