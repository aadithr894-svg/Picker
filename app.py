from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# Admin controlled numbers
BASE_ALLOWED_NUMBERS = [2,3,5,22, 11, 44]

# Track used numbers per range
USED_NUMBERS = set()

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
    h1{margin:0 0 10px;font-size:1.6rem;color:#333}
    .range-inputs{display:flex;gap:10px;margin-bottom:14px}
    input{
        width:100%;padding:12px;border-radius:10px;
        border:1px solid #ccc;font-size:1rem
    }
    button{
        width:100%;padding:14px 0;border:none;border-radius:30px;
        font-size:1.1rem;color:#fff;cursor:pointer;
        background:linear-gradient(135deg,#667eea,#764ba2);
    }
    .roller{
        margin-top:20px;height:70px;display:flex;
        align-items:center;justify-content:center;
        font-size:3rem;font-weight:700;color:#4a4aff
    }
    .rolling{animation:shake .12s infinite}
    @keyframes shake{
        0%{transform:translateY(0)}
        50%{transform:translateY(-4px)}
        100%{transform:translateY(0)}
    }
</style>
</head>
<body>
<div class="card">
    <h1>🎯 Number Picker</h1>

    <form method="post" onsubmit="startRoll()">
        <div class="range-inputs">
            <input type="number" name="start" required placeholder="Start">
            <input type="number" name="end" required placeholder="End">
        </div>
        <button type="submit">Pick Number</button>
    </form>

    <div id="roller" class="roller {% if rolling %}rolling{% endif %}">
        {% if number is not none %}{{ number }}{% else %}—{% endif %}
    </div>
</div>

<script>
function startRoll(){
    const r = document.getElementById('roller');
    const start = parseInt(document.querySelector('[name="start"]').value);
    const end = parseInt(document.querySelector('[name="end"]').value);

    if(isNaN(start) || isNaN(end) || start >= end) return;

    r.classList.add('rolling');
    let n = start;

    const t = setInterval(()=>{
        r.textContent = n;
        n++;
        if(n > end) n = start;
    }, 35);

    setTimeout(()=>{ clearInterval(t); }, 900);
}
</script>
</body>
</html>
"""

@app.route('/', methods=['GET','POST'])
def index():
    global USED_NUMBERS
    number = None
    rolling = False

    if request.method == 'POST':
        rolling = True
        start = int(request.form['start'])
        end = int(request.form['end'])

        # Allowed numbers inside typed range
        allowed = [n for n in BASE_ALLOWED_NUMBERS if start <= n <= end]

        if not allowed:
            number = "—"
        else:
            # Reset when exhausted
            if USED_NUMBERS.issuperset(allowed):
                USED_NUMBERS.clear()

            remaining = list(set(allowed) - USED_NUMBERS)
            number = random.choice(remaining)
            USED_NUMBERS.add(number)

    return render_template_string(
        HTML,
        number=number,
        rolling=rolling
    )

if __name__ == '__main__':
    app.run()
