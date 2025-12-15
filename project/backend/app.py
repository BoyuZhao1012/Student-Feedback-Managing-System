from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from same_or_not import same_or_not

load_dotenv()

app = Flask(__name__)
CORS(app)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:123456@localhost/campus_feedback')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-123'

db = SQLAlchemy(app)

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, admin, supervisor, specialist
    avatar = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 反馈模型
class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    specialist_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin_comment = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)  # 添加公开状态字段
    
    # 关系
    student = db.relationship('User', foreign_keys=[student_id], backref='submitted_feedbacks')
    specialist = db.relationship('User', foreign_keys=[specialist_id], backref='assigned_feedbacks')
    progress_records = db.relationship('Progress', backref='feedback', lazy=True)

# 进度记录模型
class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'), nullable=False)
    progress_status = db.Column(db.String(20), nullable=False)  # 进度状态
    comment = db.Column(db.Text, nullable=False)  # 进度说明
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 创建者ID
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', foreign_keys=[created_by], backref='created_progress')

# 用户相关路由
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'avatar': user.avatar
    } for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        role=data['role'],
        avatar=data.get('avatar', 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'avatar': user.avatar
    })

# 反馈相关路由
@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    user_id = request.args.get('student_id', type=int)
    assigned_to = request.args.get('specialist_id', type=int)
    is_public = request.args.get('is_public', type=bool)

    query = Feedback.query
    if user_id:
        query = query.filter_by(student_id=user_id)
    if assigned_to:
        query = query.filter_by(specialist_id=assigned_to)
    if is_public is not None:
        query = query.filter_by(is_public=is_public)

    feedbacks = query.all()
    return jsonify([{
        'id': feedback.id,
        'title': feedback.title,
        'content': feedback.content,
        'category': feedback.category,
        'status': feedback.status,
        'created_at': feedback.created_at.isoformat(),
        'updated_at': feedback.updated_at.isoformat(),
        'student': {
            'id': feedback.student.id,
            'username': feedback.student.username,
            'avatar': feedback.student.avatar
        } if feedback.student else None,
        'specialist': {
            'id': feedback.specialist.id,
            'username': feedback.specialist.username,
            'avatar': feedback.specialist.avatar
        } if feedback.specialist else None,
        'is_public': feedback.is_public,
        'progress': [{
            'id': p.id,
            'content': p.content,
            'created_at': p.created_at.isoformat(),
            'user_id': p.created_by
        } for p in feedback.progress_records]
    } for feedback in feedbacks])

@app.route('/api/feedbacks', methods=['POST'])
def create_feedback():
    data = request.json
    feedback = Feedback(
        title=data['title'],
        content=data['content'],
        category=data['category'],
        student_id=data['student_id'],
        is_public=data.get('is_public', True)
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({
        'id': feedback.id,
        'title': feedback.title,
        'content': feedback.content,
        'category': feedback.category,
        'status': feedback.status,
        'created_at': feedback.created_at.isoformat(),
        'updated_at': feedback.updated_at.isoformat(),
        'student': {
            'id': feedback.student.id,
            'username': feedback.student.username,
            'avatar': feedback.student.avatar
        },
        'specialist': {
            'id': feedback.specialist.id,
            'username': feedback.specialist.username,
            'avatar': feedback.specialist.avatar
        } if feedback.specialist else None,
        'is_public': feedback.is_public,
        'progress': []
    })

@app.route('/api/feedbacks/<int:feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    data = request.json
    
    if 'status' in data:
        feedback.status = data['status']
    if 'specialist_id' in data:
        feedback.specialist_id = data['specialist_id']
    
    db.session.commit()
    return jsonify({
        'id': feedback.id,
        'title': feedback.title,
        'content': feedback.content,
        'category': feedback.category,
        'status': feedback.status,
        'created_at': feedback.created_at.isoformat(),
        'updated_at': feedback.updated_at.isoformat(),
        'student': {
            'id': feedback.student.id,
            'username': feedback.student.username,
            'avatar': feedback.student.avatar
        },
        'specialist': {
            'id': feedback.specialist.id,
            'username': feedback.specialist.username,
            'avatar': feedback.specialist.avatar
        } if feedback.specialist else None,
        'is_public': feedback.is_public,
        'progress': [{
            'id': p.id,
            'content': p.content,
            'created_at': p.created_at.isoformat(),
            'user_id': p.created_by
        } for p in feedback.progress_records]
    })

# 进度相关路由
@app.route('/api/feedbacks/<int:feedback_id>/progress', methods=['POST'])
def add_progress(feedback_id):
    data = request.json
    feedback = Feedback.query.get_or_404(feedback_id)
    
    progress = Progress(
        content=data['content'],
        created_by=data['created_by'],
        feedback_id=feedback_id
    )
    db.session.add(progress)
    
    if feedback.status == 'pending':
        feedback.status = 'processing'
    
    db.session.commit()
    return jsonify({
        'id': progress.id,
        'content': progress.content,
        'created_at': progress.created_at.isoformat(),
        'created_by': progress.created_by
    })

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'avatar': user.avatar
        })
    return jsonify({'error': '用户名或密码错误'}), 401

# 注册接口
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'student')  # 默认注册为学生角色
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    # 创建新用户
    new_user = User(
        username=username,
        password=generate_password_hash(password),
        role=role,
        avatar=f'https://api.dicebear.com/7.x/avataaars/svg?seed={username}'
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'id': new_user.id,
            'username': new_user.username,
            'role': new_user.role,
            'avatar': new_user.avatar
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '注册失败，请重试'}), 500

# 获取学生反馈列表
@app.route('/api/student/feedbacks', methods=['GET'])
def get_student_feedbacks():
    student_id = request.args.get('student_id')
    if not student_id:
        return jsonify({'error': '缺少学生ID'}), 400
    
    feedbacks = Feedback.query.filter_by(student_id=student_id).order_by(Feedback.created_at.desc()).all()
    return jsonify([{
        'id': f.id,
        'title': f.title,
        'content': f.content,
        'category': f.category,
        'status': f.status,
        'created_at': f.created_at.isoformat(),
        'updated_at': f.updated_at.isoformat(),
        'admin_comment': f.admin_comment,
        'is_public': f.is_public,
        'specialist': {
            'id': f.specialist.id,
            'username': f.specialist.username,
            'avatar': f.specialist.avatar
        } if f.specialist else None,
        'progress_records': [{
            'id': p.id,
            'progress_status': p.progress_status,
            'comment': p.comment,
            'created_at': p.created_at.isoformat(),
            'created_by': {
                'id': p.user.id,
                'username': p.user.username,
                'avatar': p.user.avatar
            } if p.user else None
        } for p in f.progress_records]
    } for f in feedbacks])

# 提交新反馈
@app.route('/api/student/feedbacks', methods=['POST'])
def submit_feedback():
    data = request.json
    
    new_feedback = Feedback(
        title=data['title'],
        content=data['content'],
        category=data['category'],
        student_id=data['student_id']
    )
    
    try:
        db.session.add(new_feedback)
        db.session.commit()
        return jsonify({
            'id': new_feedback.id,
            'title': new_feedback.title,
            'content': new_feedback.content,
            'category': new_feedback.category,
            'status': new_feedback.status,
            'created_at': new_feedback.created_at.isoformat(),
            'updated_at': new_feedback.updated_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '提交反馈失败'}), 500

# 获取所有用户（管理员专用）
@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'avatar': user.avatar,
        'created_at': user.created_at.isoformat()
    } for user in users])

# 获取所有反馈（管理员专用）
@app.route('/api/admin/feedbacks', methods=['GET'])
def get_all_feedbacks():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return jsonify([{
        'id': f.id,
        'title': f.title,
        'content': f.content,
        'category': f.category,
        'status': f.status,
        'created_at': f.created_at.isoformat(),
        'updated_at': f.updated_at.isoformat(),
        'admin_comment': f.admin_comment,
        'is_public': f.is_public,
        'student': {
            'id': f.student.id,
            'username': f.student.username,
            'avatar': f.student.avatar,
            'role': f.student.role
        } if f.student else None,
        'specialist': {
            'id': f.specialist.id,
            'username': f.specialist.username,
            'avatar': f.specialist.avatar
        } if f.specialist else None,
        'progress_records': [{
            'id': p.id,
            'progress_status': p.progress_status,
            'comment': p.comment,
            'created_at': p.created_at.isoformat(),
            'created_by': {
                'id': p.user.id,
                'username': p.user.username,
                'avatar': p.user.avatar
            } if p.user else None
        } for p in f.progress_records]
    } for f in feedbacks])

# 管理员审核反馈
@app.route('/api/admin/feedbacks/<int:feedback_id>/review', methods=['POST'])
def review_feedback(feedback_id):
    data = request.get_json()
    feedback = Feedback.query.get_or_404(feedback_id)
    
    # 更新反馈状态和管理员意见
    feedback.status = data['status']  # 'rejected' 或 'processing'
    feedback.admin_comment = data.get('comment', '')
    
    try:
        db.session.commit()
        return jsonify({
            'id': feedback.id,
            'status': feedback.status,
            'admin_comment': feedback.admin_comment
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '审核失败'}), 500

# 总负责人获取反馈列表
@app.route('/api/supervisor/feedbacks', methods=['GET'])
def get_supervisor_feedbacks():
    try:
        # 只获取未分配专项负责人的反馈
        feedbacks = Feedback.query.filter(
            Feedback.status == 'processing',
            Feedback.specialist_id == None
        ).order_by(Feedback.created_at.desc()).all()
        return jsonify([{
            'id': f.id,
            'title': f.title,
            'content': f.content,
            'category': f.category,
            'status': f.status,
            'created_at': f.created_at.isoformat(),
            'updated_at': f.updated_at.isoformat(),
            'student': {
                'id': f.student.id,
                'username': f.student.username,
                'avatar': f.student.avatar
            },
            'specialist': {
                'id': f.specialist.id,
                'username': f.specialist.username,
                'avatar': f.specialist.avatar
            } if f.specialist else None,
            'admin_comment': f.admin_comment
        } for f in feedbacks])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 总负责人分配反馈
@app.route('/api/supervisor/feedbacks/<int:feedback_id>/assign', methods=['POST'])
def assign_feedback(feedback_id):
    try:
        data = request.get_json()
        specialist_id = data.get('specialist_id')
        
        if not specialist_id:
            return jsonify({'error': '专项负责人ID不能为空'}), 400
            
        feedback = Feedback.query.get_or_404(feedback_id)
        
        # 检查专项负责人是否存在且角色正确
        specialist = User.query.filter_by(id=specialist_id, role='specialist').first()
        if not specialist:
            return jsonify({'error': '无效的专项负责人'}), 400
            
        # 更新反馈的专项负责人和状态
        feedback.specialist_id = specialist_id
        feedback.status = 'processing'  # 更新状态为处理中
        
        # 创建进度记录
        progress = Progress(
            feedback_id=feedback_id,
            progress_status='processing',
            comment=f'已分配给专项负责人 {specialist.username}',
            created_by=feedback.student_id
        )
        db.session.add(progress)
        
        db.session.commit()
        
        return jsonify({
            'id': feedback.id,
            'title': feedback.title,
            'content': feedback.content,
            'category': feedback.category,
            'status': feedback.status,  # 返回更新后的状态
            'created_at': feedback.created_at.isoformat(),
            'updated_at': feedback.updated_at.isoformat(),
            'student': {
                'id': feedback.student.id,
                'username': feedback.student.username,
                'avatar': feedback.student.avatar
            },
            'specialist': {
                'id': specialist.id,
                'username': specialist.username,
                'avatar': specialist.avatar
            },
            'admin_comment': feedback.admin_comment
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 专项负责人获取反馈列表
@app.route('/api/specialist/feedbacks', methods=['GET'])
def get_specialist_feedbacks():
    try:
        specialist_id = request.args.get('specialist_id')
        if not specialist_id:
            return jsonify({'error': '专项负责人ID不能为空'}), 400
            
        # 获取分配给该专项负责人的所有反馈
        feedbacks = Feedback.query.filter_by(specialist_id=specialist_id).order_by(Feedback.created_at.desc()).all()
        
        return jsonify([{
            'id': f.id,
            'title': f.title,
            'content': f.content,
            'category': f.category,
            'status': f.status,
            'created_at': f.created_at.isoformat(),
            'updated_at': f.updated_at.isoformat(),
            'student': {
                'id': f.student.id,
                'username': f.student.username,
                'avatar': f.student.avatar
            },
            'admin_comment': f.admin_comment,
            'progress_records': [{
                'id': p.id,
                'progress_status': p.progress_status,
                'comment': p.comment,
                'created_at': p.created_at.isoformat(),
                'created_by': {
                    'id': p.user.id,
                    'username': p.user.username,
                    'avatar': p.user.avatar
                }
            } for p in f.progress_records]
        } for f in feedbacks])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 专项负责人更新反馈进度
@app.route('/api/specialist/feedbacks/<int:feedback_id>/progress', methods=['POST'])
def update_feedback_progress(feedback_id):
    try:
        data = request.get_json()
        progress_status = data.get('progress_status')
        comment = data.get('comment')
        specialist_id = data.get('specialist_id')
        
        if not all([progress_status, comment, specialist_id]):
            return jsonify({'error': '进度状态、说明和专项负责人ID不能为空'}), 400
            
        feedback = Feedback.query.get_or_404(feedback_id)
        
        # 检查是否是分配给该专项负责人的反馈
        if feedback.specialist_id != int(specialist_id):
            return jsonify({'error': '无权操作此反馈'}), 403
            
        # 创建进度记录
        progress = Progress(
            feedback_id=feedback_id,
            progress_status=progress_status,
            comment=comment,
            created_by=specialist_id
        )
        db.session.add(progress)
        
        # 如果进度状态是completed，更新反馈状态
        if progress_status == 'completed':
            feedback.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'id': feedback.id,
            'title': feedback.title,
            'content': feedback.content,
            'category': feedback.category,
            'status': feedback.status,
            'created_at': feedback.created_at.isoformat(),
            'updated_at': feedback.updated_at.isoformat(),
            'student': {
                'id': feedback.student.id,
                'username': feedback.student.username,
                'avatar': feedback.student.avatar
            },
            'admin_comment': feedback.admin_comment,
            'progress_records': [{
                'id': p.id,
                'progress_status': p.progress_status,
                'comment': p.comment,
                'created_at': p.created_at.isoformat(),
                'created_by': {
                    'id': p.user.id,
                    'username': p.user.username,
                    'avatar': p.user.avatar
                }
            } for p in feedback.progress_records]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 获取公开反馈列表
@app.route('/api/public/feedbacks', methods=['GET'])
def get_public_feedbacks():
    try:
        print("Fetching public feedbacks...")
        # 获取所有公开的反馈
        public_feedbacks = Feedback.query.filter_by(is_public=True).all()
        print(f"Found {len(public_feedbacks)} public feedbacks")
        
        feedbacks_list = []
        for feedback in public_feedbacks:
            try:
                feedback_data = {
                    'id': feedback.id,
                    'title': feedback.title,
                    'content': feedback.content,
                    'category': feedback.category,
                    'status': feedback.status,
                    'is_public': feedback.is_public,
                    'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S') if feedback.created_at else None,
                    'student': {
                        'id': feedback.student.id,
                        'username': feedback.student.username
                    } if feedback.student else None,
                    'progress_records': [{
                        'id': record.id,
                        'status': record.progress_status,
                        'comment': record.comment,
                        'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S') if record.created_at else None
                    } for record in feedback.progress_records]
                }
                feedbacks_list.append(feedback_data)
                print(f"Added feedback {feedback.id} to public list")
            except Exception as e:
                print(f"Error processing feedback {feedback.id}: {str(e)}")
                continue
        
        print(f"Returning {len(feedbacks_list)} public feedbacks")
        return jsonify(feedbacks_list)
    except Exception as e:
        print(f"Error in get_public_feedbacks: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

# 切换反馈公开状态
@app.route('/api/student/feedbacks/<int:feedback_id>/public', methods=['POST'])
def toggle_feedback_public(feedback_id):
    try:
        data = request.get_json()
        print(f"Received data for feedback {feedback_id}:", data)
        
        if not data or 'is_public' not in data:
            print("Missing required parameters")
            return jsonify({'error': '缺少必要参数'}), 400

        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            print(f"Feedback {feedback_id} not found")
            return jsonify({'error': '反馈不存在'}), 404

        print(f"Current feedback status: {feedback.status}, is_public: {feedback.is_public}")
        print(f"Requested is_public value: {data['is_public']}")

        # 检查是否是反馈的提交者
        if feedback.student_id != data.get('student_id'):
            print(f"Permission denied: student_id {data.get('student_id')} != feedback.student_id {feedback.student_id}")
            return jsonify({'error': '无权操作此反馈'}), 403

        # 更新公开状态
        old_status = feedback.is_public
        feedback.is_public = data['is_public']
        db.session.commit()
        print(f"Updated feedback {feedback_id} public status from {old_status} to {feedback.is_public}")

        return jsonify({
            'message': '更新成功',
            'feedback': {
                'id': feedback.id,
                'title': feedback.title,
                'is_public': feedback.is_public
            }
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error in toggle_feedback_public: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

# 检查相似反馈
@app.route('/api/student/feedbacks/check-similar', methods=['POST'])
def check_similar_feedback():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['title', 'content', 'category']):
            return jsonify({'error': '缺少必要参数'}), 400

        # 获取所有已存在的反馈
        existing_feedbacks = Feedback.query.all()
        
        # 检查每个已存在的反馈
        for feedback in existing_feedbacks:
            # 调用相似度检查函数
            is_similar = same_or_not(
                data['title'],
                feedback.title,
                data['content'],
                feedback.content,
                data['category'],
                feedback.category
            )
            
            if is_similar:
                # 如果找到相似反馈，返回该反馈的信息
                return jsonify({
                    'similar': True,
                    'similar_feedback': {
                        'id': feedback.id,
                        'title': feedback.title,
                        'content': feedback.content,
                        'category': feedback.category,
                        'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S') if feedback.created_at else None,
                        'student': {
                            'id': feedback.student.id,
                            'username': feedback.student.username
                        } if feedback.student else None
                    }
                })
        
        # 如果没有找到相似反馈
        return jsonify({
            'similar': False
        })
        
    except Exception as e:
        print(f"Error in check_similar_feedback: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

# 初始化数据库
def init_db():
    with app.app_context():
        db.create_all()
        # 添加一些初始数据
        if not User.query.first():
            users = [
                User(
                    username='张三',
                    password=generate_password_hash('123456'),
                    role='student',
                    avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=张三'
                ),
                User(
                    username='李四',
                    password=generate_password_hash('123456'),
                    role='admin',
                    avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=李四'
                ),
                User(
                    username='王五',
                    password=generate_password_hash('123456'),
                    role='supervisor',
                    avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=王五'
                ),
                User(
                    username='赵六',
                    password=generate_password_hash('123456'),
                    role='specialist',
                    avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=赵六'
                )
            ]
            db.session.add_all(users)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 