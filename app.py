from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# Final controlled numbers
BASE_ALLOWED_NUMBERS = [2, 11, 44]

# Track used numbers (no repeat)
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
    h1{margin:0 0 8px;font-size:1.6rem;color:#333}
    .sub{font-size:.9rem;color:#666;margin-bottom:16px}
    button{
        width:100%;padding:14px 0;border:none;border-radius:30px;font-size:1.1rem;
        color:#fff;cursor:pointer;background:linear-gradient(135deg,#667eea,#764ba2);
    }
    .roller{
        margin-top:20px;height:70px;display:flex;align-items:center;justify-content:center;
        font-size:3rem;font-weight:700;color:#4a4aff
    }
    .rolling{animation:shake .12s infinite}
    @keyframes shake{0%{transform:translateY(0)}50%{transform:translateY(-4px)}100%{transform:translateY(0)}}
    footer{margin-top:14px;font-size:.75rem;color:#aaa}
</style>
</head>
<body>
<div class="card">
    <h1>🎯 Number Picker</h1>
    <div class="sub">Rolling 1 → 45 • No Repeat</div>

    <form method="post" onsubmit="startRoll()">
        <button type="submit">Pick Number</button>
    </form>

    <div id="roller" class="roller {% if rolling %}rolling{% endif %}">
        {% if number is not none %}{{ number }}{% else %}—{% endif %}
    </div>

    
</div>

<script>
function startRoll(){
    const r = document.getElementById('roller');
    r.classList.add('rolling');
    let n = 1;
    const t = setInterval(()=>{
        r.textContent = n;
        n = (n % 45) + 1;
    }, 40);
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

        # Reset once all numbers used
        if len(USED_NUMBERS) == len(BASE_ALLOWED_NUMBERS):
            USED_NUMBERS.clear()

        remaining = list(set(BASE_ALLOWED_NUMBERS) - USED_NUMBERS)
        number = random.choice(remaining)
        USED_NUMBERS.add(number)

    return render_template_string(
        HTML,
        number=number,
        rolling=rolling
    )

if __name__ == '__main__':
    app.run()
