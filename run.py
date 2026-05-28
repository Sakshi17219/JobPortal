from app import create_app
from app.extensions import db, login_manager
from app.socket_events import socketio

login_manager.login_view = 'auth.login'
app = create_app()

with app.app_context():
    db.create_all()
    from app.models import User, Job
    from werkzeug.security import generate_password_hash
    import json

    if not User.query.first():
        admin = User(email='admin@jobportal.com', username='Admin',
                     password_hash=generate_password_hash('admin123'), role='admin', skills=json.dumps([]))
        seeker = User(email='user@jobportal.com', username='Alex',
                      password_hash=generate_password_hash('user123'), role='seeker',
                      skills=json.dumps(['Python', 'Flask', 'React', 'SQL', 'Docker', 'TypeScript']))
        db.session.add_all([admin, seeker])
        db.session.flush()

        jobs_data = [
            dict(title='Senior Backend Engineer', company='Stripe', location='Remote', job_type='Remote',
                 salary_min=130000, salary_max=170000,
                 description='Build and scale payment APIs used by millions of businesses. Work with Python, Go, and distributed systems.',
                 tags=['Python', 'Go', 'API', 'PostgreSQL', 'Kafka', 'Microservices'],
                 requirements=['5+ years backend experience', 'Python or Go proficiency', 'Strong SQL skills']),
            dict(title='Full-Stack Developer', company='Vercel', location='New York, NY', job_type='Hybrid',
                 salary_min=105000, salary_max=145000,
                 description='Build developer tools and frontend infrastructure. Own features end-to-end from React UI to Node.js API.',
                 tags=['React', 'Next.js', 'TypeScript', 'Node.js', 'CSS', 'GraphQL'],
                 requirements=['Strong React + TypeScript skills', '3+ years full-stack experience']),
            dict(title='ML Engineer', company='OpenAI', location='San Francisco, CA', job_type='Full-time',
                 salary_min=190000, salary_max=260000,
                 description='Train and deploy large-scale ML models. Work with PyTorch on cutting-edge language and vision systems.',
                 tags=['Python', 'PyTorch', 'ML', 'CUDA', 'Docker', 'Kubernetes'],
                 requirements=['PhD or MS in CS/ML preferred', 'Deep learning experience', 'Python mastery']),
            dict(title='DevOps Engineer', company='HashiCorp', location='Remote', job_type='Remote',
                 salary_min=115000, salary_max=155000,
                 description='Build and maintain CI/CD pipelines, cloud infrastructure, and internal tooling.',
                 tags=['Docker', 'Kubernetes', 'Terraform', 'AWS', 'Python', 'CI/CD'],
                 requirements=['Kubernetes experience', 'AWS or GCP knowledge', 'Terraform experience']),
            dict(title='Data Engineer', company='Databricks', location='Seattle, WA', job_type='Hybrid',
                 salary_min=135000, salary_max=175000,
                 description='Design and build scalable data pipelines. Work with Spark, Airflow, and SQL at petabyte scale.',
                 tags=['Python', 'SQL', 'Spark', 'Airflow', 'Kafka', 'dbt'],
                 requirements=['4+ years data engineering', 'Python and SQL expertise', 'Spark experience']),
            dict(title='Frontend Engineer', company='Linear', location='Remote', job_type='Remote',
                 salary_min=100000, salary_max=135000,
                 description='Craft pixel-perfect UI. You care deeply about performance, accessibility, and design.',
                 tags=['React', 'TypeScript', 'CSS', 'GraphQL', 'Figma', 'WebGL'],
                 requirements=['Expert CSS + React skills', 'Eye for design details']),
            dict(title='iOS Engineer', company='Airbnb', location='San Francisco, CA', job_type='Full-time',
                 salary_min=140000, salary_max=185000,
                 description='Build the Airbnb iOS app used by 100M+ users. Work in Swift and contribute to our design system.',
                 tags=['Swift', 'iOS', 'UIKit', 'SwiftUI', 'Objective-C'],
                 requirements=['4+ years iOS development', 'Strong Swift skills']),
            dict(title='Android Engineer', company='Spotify', location='Remote', job_type='Remote',
                 salary_min=120000, salary_max=160000,
                 description='Shape the Spotify Android experience for 500M+ users.',
                 tags=['Kotlin', 'Android', 'Jetpack Compose', 'Coroutines', 'Room'],
                 requirements=['3+ years Android development', 'Kotlin proficiency']),
            dict(title='Cloud Architect', company='AWS', location='Seattle, WA', job_type='Full-time',
                 salary_min=165000, salary_max=220000,
                 description='Design enterprise-grade cloud architectures for Fortune 500 customers.',
                 tags=['AWS', 'Architecture', 'Terraform', 'Python', 'Security', 'Networking'],
                 requirements=['8+ years cloud experience', 'AWS Solutions Architect certification preferred']),
            dict(title='Security Engineer', company='Cloudflare', location='Remote', job_type='Remote',
                 salary_min=130000, salary_max=170000,
                 description='Protect Cloudflare and its customers. Work on threat detection and incident response.',
                 tags=['Security', 'Python', 'Go', 'Cryptography', 'Linux', 'Networking'],
                 requirements=['4+ years security engineering', 'Network security fundamentals']),
            dict(title='Data Scientist', company='Netflix', location='Los Gatos, CA', job_type='Hybrid',
                 salary_min=145000, salary_max=195000,
                 description='Drive content recommendations and subscriber growth insights using ML and statistics.',
                 tags=['Python', 'R', 'SQL', 'ML', 'Statistics', 'Spark'],
                 requirements=['MS or PhD in quantitative field', 'Strong Python + SQL']),
            dict(title='AI Research Engineer', company='Anthropic', location='San Francisco, CA', job_type='Full-time',
                 salary_min=200000, salary_max=300000,
                 description='Build safe and steerable AI systems at the frontier of AI research.',
                 tags=['Python', 'PyTorch', 'ML', 'NLP', 'Research', 'CUDA'],
                 requirements=['Strong ML research background', 'Publications preferred']),
            dict(title='Analytics Engineer', company='dbt Labs', location='Remote', job_type='Remote',
                 salary_min=110000, salary_max=145000,
                 description='Bridge data engineering and analysis. Build trusted data models used by the entire company.',
                 tags=['SQL', 'dbt', 'Python', 'Snowflake', 'BigQuery', 'Looker'],
                 requirements=['3+ years analytics engineering', 'Expert SQL']),
            dict(title='Product Manager', company='Figma', location='San Francisco, CA', job_type='Full-time',
                 salary_min=150000, salary_max=200000,
                 description='Define the roadmap for Figma developer tools. Work closely with engineers and designers.',
                 tags=['Product', 'Strategy', 'Analytics', 'Figma', 'B2B', 'SaaS'],
                 requirements=['4+ years PM experience', 'Technical background preferred']),
            dict(title='UX Designer', company='Notion', location='Remote', job_type='Remote',
                 salary_min=110000, salary_max=150000,
                 description='Design intuitive experiences for Notion 30M+ users. Drive design from concept to launch.',
                 tags=['Figma', 'UX', 'Design Systems', 'Prototyping', 'User Research'],
                 requirements=['Portfolio showing shipped product work', '3+ years UX experience']),
            dict(title='Site Reliability Engineer', company='Google', location='Mountain View, CA', job_type='Full-time',
                 salary_min=160000, salary_max=210000,
                 description='Keep Google services running reliably at global scale.',
                 tags=['Go', 'Python', 'Kubernetes', 'Linux', 'Monitoring', 'SLO'],
                 requirements=['Software engineering background', 'Linux systems expertise']),
            dict(title='Platform Engineer', company='Shopify', location='Remote', job_type='Remote',
                 salary_min=120000, salary_max=160000,
                 description='Build the internal developer platform powering 1.7M+ merchants.',
                 tags=['Ruby', 'Go', 'Kubernetes', 'Docker', 'CI/CD', 'AWS'],
                 requirements=['3+ years platform / infra engineering', 'Container orchestration experience']),
            dict(title='Blockchain Engineer', company='Coinbase', location='Remote', job_type='Remote',
                 salary_min=140000, salary_max=185000,
                 description='Build integrations with blockchain protocols and own crypto trading infrastructure reliability.',
                 tags=['Go', 'Python', 'Blockchain', 'Ethereum', 'PostgreSQL', 'gRPC'],
                 requirements=['3+ years backend engineering', 'Blockchain / Web3 knowledge']),
            dict(title='API Platform Engineer', company='Twilio', location='Remote', job_type='Remote',
                 salary_min=115000, salary_max=155000,
                 description='Build the APIs powering communications for 290k+ companies worldwide.',
                 tags=['Python', 'Java', 'REST', 'gRPC', 'PostgreSQL', 'Redis'],
                 requirements=['4+ years backend experience', 'REST API design expertise']),
            dict(title='Embedded Systems Engineer', company='Tesla', location='Austin, TX', job_type='Full-time',
                 salary_min=130000, salary_max=175000,
                 description='Develop firmware and embedded software for Tesla vehicle systems.',
                 tags=['C', 'C++', 'Embedded', 'RTOS', 'Linux', 'CAN Bus'],
                 requirements=['5+ years embedded development', 'C/C++ mastery']),
            dict(title='Backend Engineer (Payments)', company='Brex', location='Remote', job_type='Remote',
                 salary_min=125000, salary_max=165000,
                 description='Build financial infrastructure for the next generation of businesses.',
                 tags=['Elixir', 'Python', 'PostgreSQL', 'Kafka', 'Fintech', 'API'],
                 requirements=['3+ years backend experience', 'Strong system design skills']),
            dict(title='Game Backend Engineer', company='Epic Games', location='Cary, NC', job_type='Full-time',
                 salary_min=120000, salary_max=160000,
                 description='Build scalable multiplayer backend services for Fortnite and Unreal Engine ecosystems.',
                 tags=['C++', 'Go', 'AWS', 'PostgreSQL', 'Redis', 'Game Dev'],
                 requirements=['3+ years backend engineering', 'Experience with real-time systems']),
        ]

        for jd in jobs_data:
            job = Job(
                title=jd['title'], company=jd['company'],
                location=jd['location'], job_type=jd['job_type'],
                salary_min=jd['salary_min'], salary_max=jd['salary_max'],
                description=jd['description'],
                tags=json.dumps(jd['tags']),
                requirements=json.dumps(jd['requirements']),
                posted_by=1
            )
            db.session.add(job)

        db.session.commit()
        print(f"✅ Demo data seeded — {len(jobs_data)} jobs added.")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=False)