from flask import Flask, render_template, request, jsonify, redirect, url_for
import matplotlib.pyplot as plt
import io, base64, datetime
import mysql.connector

app = Flask(__name__)

# MySQL config
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="k@rthikey123",  # your MySQL password
    database="expression_db"
)
cursor = db.cursor()

# Tree Node
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

def build_tree(postfix):
    stack = []
    for char in postfix:
        node = TreeNode(char)
        if char in "+-*/":
            node.right = stack.pop()
            node.left = stack.pop()
        stack.append(node)
    return stack[-1]

def draw_tree(root):
    def traverse(node, x=0, y=0, dx=1):
        if not node:
            return
        pos[node] = (x, y)
        traverse(node.left, x - dx, y - 1, dx / 2)
        traverse(node.right, x + dx, y - 1, dx / 2)

    def plot_edges(node):
        if not node:
            return
        if node.left:
            x1, y1 = pos[node]
            x2, y2 = pos[node.left]
            ax.plot([x1, x2], [y1, y2], color='black', linewidth=1.2)  # visible black lines
            plot_edges(node.left)
        if node.right:
            x1, y1 = pos[node]
            x2, y2 = pos[node.right]
            ax.plot([x1, x2], [y1, y2], color='black', linewidth=1.2)
            plot_edges(node.right)

    pos = {}
    traverse(root)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_facecolor('#f9f9f9')  # light background
    ax.axis('off')

    # Draw edges first
    plot_edges(root)

    # Draw nodes
    for node, (x, y) in pos.items():
        ax.text(
            x, y, node.val,
            ha='center', va='center', fontsize=12,
            bbox=dict(facecolor='lightblue', boxstyle='circle', edgecolor='black')
        )

    # Save as base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


    def plot_edges(node):
        if not node: return
        if node.left:
            x1, y1 = pos[node]
            x2, y2 = pos[node.left]
            ax.plot([x1, x2], [y1, y2], 'w')
            plot_edges(node.left)
        if node.right:
            x1, y1 = pos[node]
            x2, y2 = pos[node.right]
            ax.plot([x1, x2], [y1, y2], 'w')
            plot_edges(node.right)

    pos = {}
    traverse(root)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    plot_edges(root)
    for node, (x, y) in pos.items():
        ax.text(x, y, node.val, ha='center', va='center', fontsize=12,
                bbox=dict(facecolor='lightblue', boxstyle='circle'))
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack, output = [], []
    for ch in expression:
        if ch.isalnum():
            output.append(ch)
        elif ch in '+-*/':
            while stack and precedence.get(stack[-1], 0) >= precedence[ch]:
                output.append(stack.pop())
            stack.append(ch)
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
    while stack:
        output.append(stack.pop())
    return output

@app.route("/")
def home():
    return render_template("menu.html")

@app.route("/input")
def input():
    return render_template("input.html")
    

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    expression = data.get("expression")

    try:
        # Evaluate result
        result = eval(expression)
        
        # Build tree and generate image
        postfix = to_postfix(expression)
        root = build_tree(postfix)
        tree_img = draw_tree(root)

        # Save to MySQL
        now = datetime.datetime.now()
        cursor.execute(
            "INSERT INTO expressions (expression, result, created_at) VALUES (%s, %s, %s)",
            (expression, str(result), now)
        )
        db.commit()

        return jsonify({
            "result": result,
            "tree_image_url": f"data:image/png;base64,{tree_img}"
        })
    
    except Exception as e:
        return jsonify({"error": "Invalid Expression"}), 400

@app.route('/history')
def history():
    cursor.execute("SELECT * FROM expressions ORDER BY id DESC")
    rows = cursor.fetchall()
    return render_template('history.html', rows=rows)

# ✅ New Clear History Route
@app.route('/clear')
def clear_history():
    try:
        cursor.execute("DELETE FROM expressions")
        db.commit()
    except Exception as e:
        print("Error clearing history:", e)
    return redirect(url_for('history'))

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
