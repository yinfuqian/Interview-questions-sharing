from flask import Flask, render_template, request, jsonify
from models import db, Question, Label  # 导入模型

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite 数据库 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # 用于闪现消息的密钥
db.init_app(app)

# 使用一个标志位来确保 `create_tables` 只执行一次
tables_created = False

@app.before_request
def create_tables():
    global tables_created
    if not tables_created:
        with app.app_context():
            db.create_all()
        tables_created = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_text = request.form['question']
        answer_text = request.form['answer']
        existing_labels = request.form.getlist('existing_labels')  # 获取选择的已有标签
        custom_labels_input = request.form['custom_labels']  # 获取自定义标签
        custom_labels = [label.strip() for label in custom_labels_input.split(',') if label.strip()]

        try:
            # 创建新的 Question 实例
            new_question = Question(question=question_text, answer=answer_text)

            # 处理已有标签
            for label_text in existing_labels:
                if new_question.labels:
                    new_question.labels += ',' + label_text
                else:
                    new_question.labels = label_text

            # 处理自定义标签
            for label_text in custom_labels:
                # 检查自定义标签是否已经存在
                existing_label = Label.query.filter_by(label=label_text).first()
                if not existing_label:
                    # 如果标签不存在，则创建一个新的标签
                    new_label = Label(label=label_text)
                    db.session.add(new_label)
                    db.session.commit()
                # 更新 Question 实例以包含标签
                if new_question.labels:
                    new_question.labels += ',' + label_text
                else:
                    new_question.labels = label_text

            # 将数据添加到数据库
            db.session.add(new_question)
            db.session.commit()

            return jsonify({'status': 'success', 'message': '面试题添加成功！'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': f'添加面试题失败: {str(e)}'})

    # 当用户访问添加页面时，获取所有标签并传递给模板
    labels = Label.query.all()
    return render_template('add.html', labels=labels)

@app.route('/get_labels', methods=['GET'])
def get_labels():
    try:
        labels = Label.query.all()
        labels_list = [label.label for label in labels]
        return jsonify(labels_list)
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to retrieve labels: {str(e)}'})


@app.route('/view')
def view_questions():
    questions = Question.query.all()  # 获取所有问题
    return render_template('view.html', questions=questions)


@app.route('/search', methods=['GET'])
def search_questions():
    query = request.args.get('query', '')  # 获取查询参数
    if not query:
        return jsonify([])  # 如果查询为空，返回空列表

    # 执行查询，根据面试题目或标签进行筛选
    search_query = f"%{query}%"
    questions = Question.query.filter(
        (Question.question.ilike(search_query)) | (Question.labels.ilike(search_query))
    ).all()

    # 将结果转换为JSON格式返回
    results = []
    for question in questions:
        results.append({
            'id': question.id,
            'question': question.question,
            'answer': question.answer,
            'labels': question.labels.split(',') if question.labels else []
        })

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
