from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Job, Application, User
from ..ai_matcher import compute_match_score, get_recommended_jobs
import json
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    return redirect(url_for('main.seeker_dashboard'))

# ── SEEKER ─────────────────────────────────────────────────────────────────────
@main_bp.route('/dashboard')
@login_required
def seeker_dashboard():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    user_skills = current_user.get_skills()
    recommended = get_recommended_jobs(user_skills, jobs, top_n=6)
    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('seeker/dashboard.html',
                           recommended=recommended,
                           applications=applications,
                           user_skills=user_skills)

@main_bp.route('/jobs')
@login_required
def job_list():
    q = request.args.get('q', '')
    job_type = request.args.get('type', '')
    location = request.args.get('location', '')
    query = Job.query.filter_by(is_active=True)
    if q:
        query = query.filter(Job.title.ilike(f'%{q}%') | Job.company.ilike(f'%{q}%'))
    if job_type:
        query = query.filter_by(job_type=job_type)
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    jobs = query.order_by(Job.created_at.desc()).all()
    user_skills = current_user.get_skills()
    jobs_with_scores = [(job, compute_match_score(user_skills, job.get_tags(), job.description)) for job in jobs]
    return render_template('jobs/list.html', jobs_with_scores=jobs_with_scores, q=q, job_type=job_type, location=location)

@main_bp.route('/jobs/<int:job_id>')
@login_required
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    user_skills = current_user.get_skills()
    score = compute_match_score(user_skills, job.get_tags(), job.description)
    existing = Application.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    return render_template('jobs/detail.html', job=job, score=score, existing=existing)

@main_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
@login_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    existing = Application.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'Already applied'})
    user_skills = current_user.get_skills()
    score = compute_match_score(user_skills, job.get_tags(), job.description)
    app_obj = Application(
        user_id=current_user.id,
        job_id=job_id,
        match_score=score,
        cover_letter=request.form.get('cover_letter', '')
    )
    db.session.add(app_obj)
    db.session.commit()
    return jsonify({'success': True, 'score': score})

@main_bp.route('/applications')
@login_required
def my_applications():
    apps = Application.query.filter_by(user_id=current_user.id).order_by(Application.applied_at.desc()).all()
    return render_template('seeker/applications.html', applications=apps)

# ── ADMIN ──────────────────────────────────────────────────────────────────────
@main_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('main.seeker_dashboard'))
    total_jobs = Job.query.count()
    total_users = User.query.filter_by(role='seeker').count()
    total_apps = Application.query.count()
    recent_apps = Application.query.order_by(Application.applied_at.desc()).limit(10).all()
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('dashboard/admin.html',
                           total_jobs=total_jobs,
                           total_users=total_users,
                           total_apps=total_apps,
                           recent_apps=recent_apps,
                           jobs=jobs)

@main_bp.route('/admin/jobs/new', methods=['GET', 'POST'])
@login_required
def new_job():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
        reqs = [r.strip() for r in request.form.get('requirements', '').split('\n') if r.strip()]
        job = Job(
            title=request.form.get('title'),
            company=request.form.get('company'),
            location=request.form.get('location'),
            job_type=request.form.get('job_type', 'Full-time'),
            salary_min=int(request.form.get('salary_min') or 0),
            salary_max=int(request.form.get('salary_max') or 0),
            description=request.form.get('description'),
            requirements=json.dumps(reqs),
            tags=json.dumps(tags),
            posted_by=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('dashboard/new_job.html')

@main_bp.route('/admin/applications/<int:app_id>/status', methods=['POST'])
@login_required
def update_status(app_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    app_obj = Application.query.get_or_404(app_id)
    new_status = request.json.get('status')
    if new_status in ['applied', 'interview', 'hired', 'rejected']:
        app_obj.status = new_status
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid status'}), 400

# ── API ────────────────────────────────────────────────────────────────────────
@main_bp.route('/api/jobs')
@login_required
def api_jobs():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(20).all()
    user_skills = current_user.get_skills()
    result = []
    for job in jobs:
        score = compute_match_score(user_skills, job.get_tags(), job.description)
        result.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'job_type': job.job_type,
            'tags': job.get_tags(),
            'match_score': score,
            'created_at': job.created_at.isoformat()
        })
    return jsonify(result)
