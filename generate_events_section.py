import yaml
from datetime import datetime

# Read the events.yml file
with open('_data/events.yml', 'r', encoding='utf-8') as f:
    events_data = yaml.safe_load(f)

# Sort events by date
events = sorted(events_data['events'], key=lambda x: x['date'], reverse=False)

# Separate upcoming and past events
today = datetime.now().date()
upcoming_events = []
past_events = []

for event in events:
    # Use end_date if available, otherwise use start date
    event_date = datetime.strptime(event.get('end_date', event['date']), '%Y-%m-%d').date()
    if event_date >= today:
        upcoming_events.append(event)
    else:
        past_events.append(event)

# Generate HTML for events section
html = ''

if upcoming_events:
    html += '<h3 style="font-size: 1.4rem; color: var(--electric); margin-bottom: 20px;">Upcoming Events</h3>\n'
    html += '<div class="events-list">\n'
    for event in upcoming_events:
        start_date = datetime.strptime(event['date'], '%Y-%m-%d')
        
        # Format date - show date range if multi-day
        if event.get('end_date'):
            end_date = datetime.strptime(event['end_date'], '%Y-%m-%d')
            if start_date.month == end_date.month:
                formatted_date = f"{start_date.strftime('%B %d')}-{end_date.strftime('%d, %Y')}"
            else:
                formatted_date = f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
        else:
            formatted_date = start_date.strftime('%B %d, %Y')
        
        html += '    <div class="event-card">\n'
        html += f'        <div class="event-type">{event["type"]}</div>\n'
        
        # Title - make it a link if URL provided
        if event.get('url'):
            html += f'        <h4 class="event-title"><a href="{event["url"]}" target="_blank" style="color: var(--electric); text-decoration: none;">{event["title"]}</a></h4>\n'
        else:
            html += f'        <h4 class="event-title">{event["title"]}</h4>\n'
        
        html += f'        <div class="event-meta">\n'
        html += f'            <span class="event-date">📅 {formatted_date}</span>\n'
        
        # Add time if available
        if event.get('time'):
            html += f'            <span class="event-time">🕒 {event["time"]}</span>\n'
        
        html += f'        </div>\n'
        
        # Speaker info if available
        if event.get('speaker'):
            speaker_text = event['speaker']
            if event.get('affiliation'):
                speaker_text += f" ({event['affiliation']})"
            html += f'        <div class="event-speaker">👤 {speaker_text}</div>\n'
        
        html += f'        <div class="event-location">📍 {event["location"]}</div>\n'
        
        # Description
        if event.get('description'):
            html += f'        <div class="event-description">{event["description"]}</div>\n'
        
        # Link button if URL provided
        if event.get('url'):
            html += f'        <div style="margin-top: 15px;"><a href="{event["url"]}" target="_blank" style="color: var(--electric); text-decoration: none; font-size: 0.9rem;">→ More information</a></div>\n'
        
        html += '    </div>\n'
    html += '</div>\n'

if past_events:
    html += '<h3 style="font-size: 1.4rem; color: var(--electric); margin-top: 50px; margin-bottom: 20px;">Past Events</h3>\n'
    html += '<div class="events-list past-events">\n'
    # Show last 5 past events, most recent first
    for event in reversed(past_events[-5:]):
        start_date = datetime.strptime(event['date'], '%Y-%m-%d')
        
        # Format date
        if event.get('end_date'):
            end_date = datetime.strptime(event['end_date'], '%Y-%m-%d')
            if start_date.month == end_date.month:
                formatted_date = f"{start_date.strftime('%B %d')}-{end_date.strftime('%d, %Y')}"
            else:
                formatted_date = f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
        else:
            formatted_date = start_date.strftime('%B %d, %Y')
        
        html += '    <div class="event-card past">\n'
        html += f'        <div class="event-type">{event["type"]}</div>\n'
        
        if event.get('url'):
            html += f'        <h4 class="event-title"><a href="{event["url"]}" target="_blank" style="color: var(--electric); text-decoration: none;">{event["title"]}</a></h4>\n'
        else:
            html += f'        <h4 class="event-title">{event["title"]}</h4>\n'
        
        html += f'        <div class="event-meta">\n'
        html += f'            <span class="event-date">📅 {formatted_date}</span>\n'
        html += f'        </div>\n'
        
        if event.get('speaker'):
            speaker_text = event['speaker']
            if event.get('affiliation'):
                speaker_text += f" ({event['affiliation']})"
            html += f'        <div class="event-speaker">👤 {speaker_text}</div>\n'
        
        html += f'        <div class="event-location">📍 {event["location"]}</div>\n'
        
        html += '    </div>\n'
    html += '</div>\n'

# Write to file
with open('events_section.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated events section successfully")
