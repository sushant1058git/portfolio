"""
Management command to seed the database with Sushant's portfolio data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date


class Command(BaseCommand):
    help = 'Seeds the database with initial portfolio data for Sushant Sinha'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Seeding database...'))
        self._seed_profile()
        self._seed_skills()
        self._seed_experience()
        self._seed_education()
        self._seed_certifications()
        self._seed_blog()
        self.stdout.write(self.style.SUCCESS('✅ Database seeded successfully!'))

    def _seed_profile(self):
        from apps.portfolio.models import Profile
        if not Profile.objects.exists():
            Profile.objects.create(
                name='Sushant Sinha',
                role='Senior Application Engineer',
                tagline='Backend Architect & Full-Stack Developer',
                bio='Senior Software Engineer with 5+ years of experience architecting and delivering scalable backend systems. Currently leading a team of 4 developers at Global Value Web Pvt. Ltd., owning end-to-end architecture from HLD/LLD through deployment. Passionate about clean API design, DevOps automation, and integrating AI/ML capabilities into production systems — from NLP pipelines with sci-spaCy to R-based predictive analytics compliant with 21 CFR Part 11.',
                email='sushant1058jan@gmail.com',
                phone='+91-880-015-4942',
                github='https://github.com/sushant1058git',
                location='Bangalore, India',
                years_experience=5,
                deploy_improvement='30%',
                is_available=True,
            )
            self.stdout.write('  ✓ Profile created')

    def _seed_skills(self):
        from apps.portfolio.models import SkillCategory, Skill
        skill_data = [
            ('Backend Development', '⚙️', 0, ['Python', 'Django', 'FastAPI', 'DRF', 'REST APIs', 'JWT Auth', 'Swagger/OpenAPI', 'SQL', 'NoSQL']),
            ('Frontend', '🎨', 1, ['React', 'JavaScript', 'HTML5', 'CSS3', 'Chart.js', 'Go.js']),
            ('Cloud & DevOps', '☁️', 2, ['AWS', 'EC2', 'S3', 'Docker', 'Kubernetes', 'GitLab CI/CD', 'Kafka']),
            ('Data & Search', '🗄️', 3, ['MongoDB', 'Elasticsearch', 'PostgreSQL', 'Pandas', 'Celery', 'R/Shiny', 'sci-spaCy']),
            ('Version Control', '🔀', 4, ['Git', 'GitLab', 'Bitbucket', 'JIRA']),
            ('AI / ML Integration', '🧠', 5, ['NLP', 'sci-spaCy', 'Predictive Analytics', 'Risk Scoring', '21 CFR Part 11']),
        ]
        for cat_name, icon, order, skills in skill_data:
            if not SkillCategory.objects.filter(name=cat_name).exists():
                cat = SkillCategory.objects.create(name=cat_name, icon=icon, order=order)
                for i, skill in enumerate(skills):
                    Skill.objects.create(category=cat, name=skill, order=i)
        self.stdout.write('  ✓ Skills created')

    def _seed_experience(self):
        from apps.portfolio.models import Experience, ExperiencePoint
        if not Experience.objects.exists():
            exp1 = Experience.objects.create(
                role='Senior Application Engineer',
                company='Global Value Web Pvt. Ltd.',
                location='Bangalore, India',
                start_date=date(2023, 1, 1),
                is_current=True,
                order=0,
            )
            exp1_points = [
                'Led a team of 4 developers (including 3 juniors), managing requirements, architecture, and on-time delivery.',
                'Owned end-to-end backend architecture — HLD/LLD, development, and deployment of scalable Django REST APIs.',
                'Implemented JWT authentication, API versioning, and Swagger/OpenAPI documentation.',
                'Automated build, test & deployment pipelines with GitLab CI/CD + Docker — reduced deployment time by 30%.',
                'Integrated Kafka for real-time data streaming to enhance dashboard responsiveness and data accuracy.',
                'Utilized sci-spaCy NLP model to develop advanced text processing and analysis features.',
                'Integrated Chart.js and Go.js for dynamic, interactive data visualizations.',
                'Integrated R-based statistical models in Shiny for predictive analytics, risk scoring, and regulatory reporting (21 CFR Part 11).',
            ]
            for i, pt in enumerate(exp1_points):
                ExperiencePoint.objects.create(experience=exp1, text=pt, order=i)

            exp2 = Experience.objects.create(
                role='Software Engineer',
                company='S & V Software Services (Prometheus Group)',
                location='Bangalore, India',
                start_date=date(2021, 9, 1),
                end_date=date(2023, 1, 1),
                is_current=False,
                order=1,
            )
            exp2_points = [
                'Contributed to both frontend and backend development of the application.',
                'Developed features leveraging Pandas for efficient reading and importing of large datasets.',
                'Implemented background tasks and scheduled cron jobs using Celery for automation.',
                'Collaborated with cross-functional teams for seamless API-frontend integration.',
                'Optimized existing codebases and database schemas to improve performance and scalability.',
            ]
            for i, pt in enumerate(exp2_points):
                ExperiencePoint.objects.create(experience=exp2, text=pt, order=i)

            exp3 = Experience.objects.create(
                role='Associate Software Engineer',
                company='Accenture India',
                location='Bangalore, India',
                start_date=date(2018, 2, 1),
                end_date=date(2018, 6, 1),
                is_current=False,
                order=2,
            )
            exp3_points = [
                'Acted as liaison between teams, managing and prioritizing SAP support tickets for timely resolution.',
                'Ensured timely assignment of tickets to SAP ABAP developers, facilitating smooth workflows.',
            ]
            for i, pt in enumerate(exp3_points):
                ExperiencePoint.objects.create(experience=exp3, text=pt, order=i)
        self.stdout.write('  ✓ Experience created')

    def _seed_education(self):
        from apps.portfolio.models import Education
        if not Education.objects.exists():
            Education.objects.bulk_create([
                Education(degree='B.E. Electrical & Electronics Engineering', institution='BNM Institute of Technology (VTU)', location='Bangalore, Karnataka', start_year=2013, end_year=2017, score='71.3%'),
                Education(degree='12th (PCM)', institution='D.A.V. Public School', location='Patna, Bihar', start_year=2011, end_year=2012, score='81.8%'),
                Education(degree='10th', institution='D.A.V. Public School', location='Patna, Bihar', start_year=2009, end_year=2010, score='9.6 CGPA'),
            ])
        self.stdout.write('  ✓ Education created')

    def _seed_certifications(self):
        from apps.portfolio.models import Certification
        if not Certification.objects.exists():
            Certification.objects.create(
                name='AWS Cloud Practitioner',
                issuer='Udemy / AWS',
                year=2023,
            )
        self.stdout.write('  ✓ Certifications created')

    def _seed_blog(self):
        from apps.blog.models import Category, Post
        if Post.objects.exists():
            return

        cats = {}
        for name, color in [
            ('Backend Engineering', '#00f5d4'),
            ('DevOps', '#7b2fff'),
            ('Data Streaming', '#ff2d6b'),
            ('AI / NLP', '#febc2e'),
            ('Team Leadership', '#28c840'),
            ('Cloud', '#4fc3f7'),
        ]:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'color': color})
            cats[name] = cat

        posts = [
            {
                'title': 'Designing Scalable REST APIs with Django REST Framework',
                'category': cats['Backend Engineering'],
                'excerpt': 'A deep dive into API versioning strategies, JWT authentication patterns, and Swagger documentation practices that keep your APIs maintainable as they grow.',
                'content': '''# Designing Scalable REST APIs with Django REST Framework

Building APIs that scale isn't just about performance — it's about **maintainability, security, and developer experience**.

## API Versioning

Version your APIs from day one. I prefer URL-based versioning (`/api/v1/`) for clarity:

```python
urlpatterns = [
    path('api/v1/', include('apps.v1.urls')),
    path('api/v2/', include('apps.v2.urls')),
]
```

## JWT Authentication

Use `djangorestframework-simplejwt` for stateless auth:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

## Swagger/OpenAPI Docs

Use `drf-spectacular` to auto-generate docs your frontend team will love.

## Key Lessons

1. Always version from day one
2. Use serializer validation — don't trust raw input
3. Document every endpoint, including error responses
4. Rate-limit public endpoints from the start
''',
                'read_time': 8, 'is_featured': True,
            },
            {
                'title': 'CI/CD Pipelines with GitLab & Docker: How I Cut Deploy Time by 30%',
                'category': cats['DevOps'],
                'excerpt': 'How I reduced deployment time by 30% using automated GitLab CI/CD pipelines, containerised environments, and smart staging strategies.',
                'content': '''# CI/CD Pipelines with GitLab & Docker

Before automation, our deploys were manual, error-prone, and slow. Here's how we fixed that.

## The Pipeline Structure

```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python manage.py test

build:
  stage: build
  image: docker:24
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/portfolio app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## Key Wins

- **Parallel test jobs** — unit tests and integration tests run simultaneously
- **Docker layer caching** — dramatically speeds up image builds
- **Environment-specific configs** — staging vs production kept separate

The result: 30% faster deployments and zero manual steps after merge.
''',
                'read_time': 6, 'is_featured': True,
            },
            {
                'title': 'Real-Time Dashboards with Apache Kafka: Beyond the Basics',
                'category': cats['Data Streaming'],
                'excerpt': 'Integrating Kafka into a Django backend for real-time event streaming — architecture decisions, pitfalls, and keeping consumers reliable.',
                'content': '''# Real-Time Dashboards with Apache Kafka

When our healthcare dashboard needed real-time updates without polling, Kafka was the answer.

## Architecture

```
Django App → Kafka Producer → Kafka Topic → Kafka Consumer → WebSocket → Browser
```

## Producer Setup

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def publish_event(topic, data):
    producer.send(topic, value=data)
    producer.flush()
```

## Consumer with Django Channels

We used Django Channels for WebSocket broadcasting, with Kafka consumers running as background workers.

## Lessons Learned

- Always set consumer group IDs explicitly
- Monitor consumer lag — it's your early warning system
- Use dead-letter queues for failed messages
''',
                'read_time': 10, 'is_featured': True,
            },
            {
                'title': 'Integrating sci-spaCy for Healthcare NLP Pipelines',
                'category': cats['AI / NLP'],
                'excerpt': 'Practical lessons from building NLP text processing with sci-spaCy in a healthcare-compliant system — entity recognition, data handling, and compliance.',
                'content': '''# Healthcare NLP with sci-spaCy

Building NLP features in a 21 CFR Part 11-compliant system taught me a lot about the intersection of ML and regulated software.

## Why sci-spaCy?

Standard spaCy lacks biomedical entity models. sci-spaCy provides models trained on medical literature:

```python
import spacy
nlp = spacy.load("en_core_sci_lg")

def extract_medical_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities
```

## Compliance Considerations

In regulated healthcare environments:
- All model outputs must be auditable
- Model versions must be pinned and documented
- Outputs must be reproducible given the same input

## Pipeline Architecture

```
Raw Clinical Text → Preprocessing → sci-spaCy NER → Post-processing → Audit Log → DB
```

Always validate NLP outputs — medical text has high-stakes consequences.
''',
                'read_time': 7, 'is_featured': False,
            },
            {
                'title': 'Leading Junior Developers: What I Learned the Hard Way',
                'category': cats['Team Leadership'],
                'excerpt': 'Reflections on transitioning from individual contributor to tech lead — code reviews, mentorship styles, and feedback that actually makes developers grow.',
                'content': '''# Leading Junior Developers

Moving from IC to tech lead was harder than any technical challenge I'd faced.

## The Biggest Mistakes I Made

**1. Doing instead of teaching**
When a junior was stuck, I'd often just fix the code myself. Faster in the moment, but it robbed them of the learning.

**2. Feedback that felt like attacks**
Early code reviews were too blunt. I learned to use the "question sandwich":
- Ask what they were trying to achieve
- Suggest an alternative approach
- Acknowledge what they did right

## What Actually Works

**Pair programming sessions** — not me coding and them watching, but them driving with me navigating.

**Weekly 1:1s** — even 15 minutes to discuss blockers, career goals, and feedback.

**Public praise, private feedback** — always.

The team ships better code now, and more importantly, they're growing as engineers.
''',
                'read_time': 5, 'is_featured': False,
            },
            {
                'title': 'AWS for Backend Engineers: EC2, S3, and Kubernetes in Production',
                'category': cats['Cloud'],
                'excerpt': 'A practical look at AWS services I use daily — S3 storage patterns, EC2 configurations, and Kubernetes orchestration in production.',
                'content': '''# AWS for Backend Engineers

After earning my AWS Cloud Practitioner cert, here's what actually matters day-to-day.

## S3 Patterns

For media storage in Django:

```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'my-portfolio-media'
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'
```

Use pre-signed URLs for private assets — never expose bucket credentials.

## EC2 Configuration

For a Django app:
- Use t3.small for staging, c5.large for production
- Always put your app behind a load balancer
- Use Auto Scaling Groups — even simple ones

## Kubernetes Basics

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: portfolio-api
```

Start with 3 replicas minimum in production. Rolling updates are your friend.
''',
                'read_time': 9, 'is_featured': False,
            },
        ]

        for p in posts:
            Post.objects.create(
                **p,
                status='published',
                published_at=timezone.now(),
            )
        self.stdout.write('  ✓ Blog posts created')
