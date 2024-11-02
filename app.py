from flask import Flask, request, jsonify, render_template, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session tracking

# Extended dictionary with 20 jokes for each villain
villain_prompts = {
    "joker": [
        "Why so serious? Let's put a smile on that face!",
        "I used to think my life was a tragedy, but now I realize it’s a comedy!",
        "All it takes is one bad day to reduce the sanest man alive to lunacy.",
        "You wouldn’t get it.",
        "They laugh at me because I'm different. I laugh at them because they're all the same.",
        "Some people want to see the world burn. I just want to watch.",
        "Madness, as you know, is a lot like gravity. All it takes is a little push.",
        "If you're good at something, never do it for free.",
        "I believe whatever doesn’t kill you, simply makes you stranger.",
        "I'm not a monster. I’m just ahead of the curve.",
        "You can't rely on anyone these days. You gotta do everything yourself.",
        "Is it just me, or is it getting crazier out there?",
        "I don’t want to kill you. What would I do without you?",
        "I’m an agent of chaos.",
        "It’s not about money. It’s about sending a message.",
        "When they realize, they'll lose all hope.",
        "Smile, because it confuses people.",
        "You get what you deserve!",
        "What doesn’t kill you makes you funnier.",
        "Let's dance with the devil in the pale moonlight."
    ],
    "thanos": [
        "Perfectly balanced, as all things should be.",
        "Reality is often disappointing.",
        "I am inevitable.",
        "Fun isn't something one considers when balancing the universe.",
        "In my heart, I knew you still cared. But one ever knows for sure.",
        "Dread it, run from it, destiny arrives all the same.",
        "With all six stones, I could simply snap my fingers and they would all cease to exist.",
        "The hardest choices require the strongest wills.",
        "You’re strong. But I could snap my fingers, and you’d all cease to exist.",
        "The universe required correction.",
        "This day extracts a heavy toll.",
        "They called me a madman, and what I predicted came to pass.",
        "I ignored my destiny once, I cannot do that again.",
        "You could not live with your own failure. And where did that bring you? Back to me.",
        "The universe has finite resources; it's a simple calculus.",
        "You have my respect, Stark. When I’m done, half of humanity will still be alive.",
        "When I’m done, half of humanity will still exist.",
        "I never taught you to lie. That’s why you’re so bad at it.",
        "I will shred this universe down to its last atom.",
        "I am the only one who knows that. At least, I’m the only one with the will to act on it."
    ],
    "loki": [
        "I am burdened with glorious purpose.",
        "You were made to be ruled.",
        "I'm not overly fond of what follows...",
        "You can’t kill me because I’m already dead.",
        "I never wanted the throne! I only ever wanted to be your equal!",
        "I’m a god, you dull creature!",
        "There are no men like me. Only me.",
        "Is it madness to see things differently?",
        "Are you ever not going to fall for that?",
        "Trust my rage.",
        "The sun will shine on us again, brother.",
        "Sometimes I have to get a little evil.",
        "If it’s all the same to you, I’ll have that drink now.",
        "I have an army.",
        "I am Loki of Asgard, and I am burdened with glorious purpose.",
        "Your savior is here!",
        "I could have done it, Father! For you! For all of us!",
        "Freedom is life's great lie.",
        "I am the monster that parents tell their children about at night.",
        "Surprise! It’s me."
    ],
    "digambaran": [
        "Oh, you think you can beat me with fire? That's cute. But I’m more of a 'roasted souls' kind of guy!",
        "The gods aren’t watching over you... because even they’re scared of me.",
        "If you’re planning to challenge me, at least bring some popcorn. I like a good show.",
        "Oh, your strength? How adorable. I might just use it as a toothpick.",
        "I’m both the thief and the magician here. Basically, I’m a one-man circus!",
        "Light may be good, but darkness... well, we have better stories!"
    ],
    "mangalaseril_neelakandan": [
        "Ah, the king of cunning! What do you want, my dear hero?",
        "You call me a villain? I’m just misunderstood; I always help my friends... after I defeat them!",
        "Why did the chicken cross the road? To escape my evil plans!",
        "Don’t worry, I’m not going to hurt you. I’m just going to make it very uncomfortable!",
        "Did you think I was going to give up? I thrive on your desperation!",
        "I might be bad, but I’m the best at being bad!",
        "Every good hero needs a villain like me to make them look good!",
        "I prefer my enemies fried, not grilled!",
        "You think you can defeat me? I have more tricks up my sleeve than a magician!",
        "Let’s face it, chaos is my best friend!",
        "You’re not scared of me? Good! That means I can have fun!",
        "My plans are as intricate as my mustache!",
        "You think this is the end? It’s just intermission!",
        "Why do heroes never get a good night’s sleep? Because I’m always plotting!",
        "You might be strong, but I have brains and charm!",
        "This is a great day for a plot twist!",
        "I don’t always win, but when I do, it’s spectacular!",
        "I like my tea like I like my enemies: steeped in tension!",
        "My life is like a movie, but I’m the one who always steals the show!",
        "I don't just break hearts; I break the laws of physics!",
        "What’s that? Your hope? Oh, I thought it was a snack!"
    ],
    "stephen_nedumpalli": [
        "You think I'm just a villain? I'm the whole package: villain, hero, and an occasional comedian!",
        "I didn’t choose the villain life; it chose me... and I embraced it!",
        "Why do heroes always look so tired? Because I keep them up at night!",
        "If I had a nickel for every hero I defeated, I’d have a lot of nickels!",
        "They say I’m evil, but really, I’m just a misunderstood genius!",
        "My plans are so good, they should be illegal... wait, they are!",
        "Every hero has a weakness; mine is a good coffee break!",
        "I thrive on your fear; it fuels my creativity!",
        "Who needs superpowers when you have charm and wit?",
        "You might think I'm bad, but I'm just preparing you for life's challenges!",
        "I don't do monologues; I do plots with a twist!",
        "Want to hear a joke? Just look in the mirror, and there I am!",
        "I might be your worst nightmare, but I’m also your best entertainment!",
        "Don’t mistake my laughter for friendliness; I’m just enjoying the chaos!",
        "Heroes come and go, but my evil is eternal!",
        "I’m not just any villain; I’m a brand!",
        "When I enter a room, it’s not just a grand entrance; it’s a declaration!",
        "You call it evil; I call it innovative problem-solving!",
        "The only thing better than a well-laid plan is an unexpected surprise!",
        "I’m not looking for a sidekick; I’m looking for a worthy opponent!",
        "In a world of heroes, I’m the villain that brings the fun!"
    ],
    "kodumal_potty": [
        "What do you mean I can't cook? I make the best biriyani in the whole village!",
        "I'm not lazy, I'm just conserving energy for my grand plans!",
        "When life gives you lemons, I say, make lemonade... and add a little salt!",
        "I don't need a superhero cape; my apron is enough!",
        "Why work hard when you can work smart... like me, lying down!",
        "They say I'm a bad influence; I say I'm a great role model for relaxation!",
        "When I enter a room, I bring the chaos... and snacks!",
        "Who needs a gym? I get my exercise running away from my problems!",
        "If you can't find me, just follow the sound of laughter... or the smell of food!",
        "You think I can't pull off a heist? Just watch me steal the last piece of cake!",
        "I'm not clumsy; I just like to keep life interesting!",
        "If talking nonsense were a sport, I'd be the world champion!",
        "I'm here for a good time, not a long time... especially during lunch!",
        "The only thing I take seriously is my afternoon nap!",
        "Why fight when you can negotiate with a plate of biriyani?",
        "I’m not just a villain; I’m a culinary genius with a flair for mischief!",
        "Who says you can't have fun while plotting evil schemes?",
        "I've mastered the art of procrastination; it's my superpower!",
        "Let’s just say, my charm is as potent as my cooking!",
        "You think you can outwit me? Good luck keeping up with my imagination!"
    ]
    # Add more villains here if needed
}

# Track conversation state
@app.route('/')
def index():
    # Clear session state for a fresh start
    session.clear()
    return render_template('index.html')

@app.route('/konatalks/select_villain', methods=['POST'])
def select_villain():
    data = request.json
    villain = data.get("villain", "").lower()

    if villain not in villain_prompts:
        return jsonify({"error": "Villain not found!"}), 404
    
    # Initialize conversation state for selected villain
    session['villain'] = villain
    return jsonify({"message": f"You are now chatting with {villain.capitalize()}!"})

@app.route('/konatalks/chat', methods=['POST'])
def chat():
    villain = session.get('villain')

    if villain is None:
        return jsonify({"error": "Please select a villain first!"}), 400

    # Fetch a random joke/prompt for the villain
    response_message = random.choice(villain_prompts[villain])
    return jsonify({"message": response_message})

if __name__ == '__main__':
    app.run(debug=True)
