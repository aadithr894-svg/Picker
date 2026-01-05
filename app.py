from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

DEFAULT_START = 1
DEFAULT_END = 10

# Manipulated numbers (admin controlled)
BASE_ALLOWED_NUMBERS = [2,11,44]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Number Picker</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
    body{
        margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
        font-family:'Segoe UI',Arial,sans-serif;
        background:linear-gradient(135deg,#667eea,#764ba2);
    }
    .card{
        background:#fff;width:92%;max-width:420px;padding:26px 22px;border-radius:18px;
        box-shadow:0 20px 40px rgba(0,0,0,.25);text-align:center;
    }
    h1{margin:0 0 8px;font-size:1.6rem;color:#333}
    .sub{font-size:.9rem;color:#666;margin-bottom:16px}
    .range-inputs{display:flex;gap:10px;margin-bottom:16px}
    input[type=number]{
        width:100%;padding:12px;border-radius:10px;border:1px solid #ccc;font-size:1rem
    }
    button{
        width:100%;padding:14px 0;border:none;border-radius:30px;font-size:1.1rem;
        color:#fff;cursor:pointer;background:linear-gradient(135deg,#667eea,#764ba2);
        transition:transform .15s,box-shadow .15s
    }
    button:active{transform:scale(.97)}
    .roller{
        margin-top:20px;height:70px;display:flex;align-items:center;justify-content:center;
        font-size:3rem;font-weight:700;color:#4a4aff
    }
    .rolling{animation:shake .15s infinite}
    @keyframes shake{0%{transform:translateY(0)}50%{transform:translateY(-4px)}100%{transform:translateY(0)}}
    footer{margin-top:14px;font-size:.75rem;color:#aaa}
    @media(max-width:480px){h1{font-size:1.4rem}.roller{font-size:2.6rem}}
</style>
</head>
<body>
<div class="card">
    <h1>🎯 Number Picker</h1>
    <div class="sub">Select range & tap to roll</div>

    <form method="post" onsubmit="startRoll()">
        <div class="range-inputs">
            <input type="number" name="start" value="{{ range_start }}" required>
            <input type="number" name="end" value="{{ range_end }}" required>
        </div>
        <button type="submit">Pick</button>
    </form>

    <div id="roller" class="roller {% if rolling %}rolling{% endif %}">
        {% if number is not none %}{{ number }}{% else %}—{% endif %}
    </div>

    <footer>Mobile-friendly • Animated • Controlled</footer>
</div>

<script>
    function startRoll(){
        const r=document.getElementById('roller');
        r.classList.add('rolling');
        let fake=1;
        const t=setInterval(()=>{r.textContent=fake;fake=(fake%9)+1},60);
        setTimeout(()=>{clearInterval(t)},800);
    }
</script>
</body>
</html>
"""

@app.route('/', methods=['GET','POST'])
def index():
    range_start = DEFAULT_START
    range_end = DEFAULT_END
    number = None
    rolling = False

    if request.method == 'POST':
        rolling = True
        range_start = int(request.form.get('start', DEFAULT_START))
        range_end = int(request.form.get('end', DEFAULT_END))

        allowed = [n for n in BASE_ALLOWED_NUMBERS if range_start <= n <= range_end]
        if not allowed:
            allowed = BASE_ALLOWED_NUMBERS

        number = random.choice(allowed)

    return render_template_string(
        HTML,
        number=number,
        range_start=range_start,
        range_end=range_end,
        rolling=rolling
    )

if __name__ == '__main__':
    app.run()
