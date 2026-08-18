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
        self._seed_scenarios()
        self._seed_lab_details()
        self._seed_projects()
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

        # One-time cleanup: these categories were restructured into the backend-focused
        # set below — their skills are preserved under the new category names.
        SkillCategory.objects.filter(name__in=['Backend Development', 'Data & Search', 'Version Control']).delete()
        # Kafka moved from Cloud & DevOps to its own Distributed Systems category.
        Skill.objects.filter(category__name='Cloud & DevOps', name='Kafka').delete()

        # (name, icon, order, is_core, skills) — is_core=True surfaces in the featured
        # "Core Expertise" row; the rest render as a compact secondary row.
        skill_data = [
            ('Backend & APIs', '🐍', 0, True, ['Python', 'Django', 'FastAPI', 'DRF', 'REST APIs', 'JWT Auth', 'Swagger/OpenAPI', 'Pandas']),
            ('Databases', '🗄️', 1, True, ['PostgreSQL', 'MongoDB', 'Elasticsearch', 'SQL', 'NoSQL']),
            ('Distributed Systems', '🔗', 2, True, ['Kafka', 'Celery', 'Event-Driven Architecture', 'Background Jobs']),
            ('Cloud & DevOps', '☁️', 3, True, ['AWS', 'EC2', 'S3', 'Docker', 'Kubernetes', 'GitLab CI/CD']),
            ('System Design', '🏗️', 4, True, ['HLD/LLD', 'Scalability', 'API Design', 'Data Modeling']),
            ('AI / ML Integration', '🧠', 5, False, ['NLP', 'sci-spaCy', 'Predictive Analytics', 'Risk Scoring', '21 CFR Part 11', 'R/Shiny']),
            ('Frontend', '🎨', 6, False, ['React', 'JavaScript', 'HTML5', 'CSS3', 'Chart.js', 'Go.js']),
            ('Tools & Practices', '🔀', 7, False, ['Git', 'GitLab', 'Bitbucket', 'JIRA']),
        ]
        for cat_name, icon, order, is_core, skills in skill_data:
            cat, _ = SkillCategory.objects.update_or_create(
                name=cat_name, defaults={'icon': icon, 'order': order, 'is_core': is_core},
            )
            for i, skill in enumerate(skills):
                Skill.objects.get_or_create(category=cat, name=skill, defaults={'order': i})
        self.stdout.write('  ✓ Skills created/updated')

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
                'Implemented JWT authentication, API versioning, and clear endpoint documentation.',
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
                'excerpt': 'A deep dive into API versioning strategies, JWT authentication patterns, and documentation practices that keep APIs maintainable as they grow.',
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

## API Documentation

Keep endpoint contracts, examples, and error responses close to the APIs they describe so that clients can integrate confidently.

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

    def _seed_scenarios(self):
        from apps.portfolio.models import Scenario
        scenario_data = [
            ('notification', '01', 'SENIOR / SYSTEM DESIGN', 'Notification System',
             'Process 10 million events per day with low latency and reliable multi-channel delivery.',
             ['10M events/day', 'Retries + dedupe', 'Email · SMS · Push'],
             'Notification delivery, from first principles.', 0),
            ('payments', '02', 'SENIOR / RELIABILITY', 'Payments Ledger',
             'Build a payment workflow that keeps financial state correct while integrating unreliable external gateways.',
             ['Strong consistency', 'Audit trail', 'Idempotency'],
             'Payment correctness, from first principles.', 1),
            ('media', '03', 'SENIOR / PLATFORM', 'Media Processing Pipeline',
             'Accept large uploads, process them asynchronously, and deliver globally without blocking users.',
             ['Large uploads', 'Async jobs', 'Global delivery'],
             'Media processing, from first principles.', 2),
        ]
        for key, number, difficulty, title, description, chips, journey_title, order in scenario_data:
            Scenario.objects.update_or_create(
                key=key,
                defaults={
                    'number': number, 'difficulty': difficulty, 'title': title,
                    'description': description, 'requirement_chips': chips,
                    'journey_title': journey_title, 'order': order,
                },
            )
        self.stdout.write('  ✓ Scenarios created/updated')

    def _seed_lab_details(self):
        from apps.portfolio.models import (
            Scenario, Stage, StagePoint, StageNode, Component, Decision, FailureMode,
            ArchitectureDecisionRecord, TrafficMetric, SimulatorPlan, SimulatorBottleneck,
        )

        stages_by_scenario = {
            'notification': [
                ('requirements', 'FOUNDATION', '01 — Frame the constraints',
                 'Before selecting technology, make the shape of the problem explicit.',
                 ['10M events/day ≈ 116 events/sec average; bursts matter more than averages.',
                  'P95 delivery latency under 500 ms; delivery is eventually consistent.',
                  '99.9% availability, durable delivery intent, and bounded operational spend.'],
                 ['CLIENT', 'API', 'DATABASE', 'PROVIDER']),
                ('initial', 'SIMPLE PATH', '02 — Start with one deployable',
                 'A synchronous service is the right first architecture when volume and failure modes are manageable.',
                 ['Easy to build and deploy.', 'Low operational complexity.',
                  'The API is coupled to provider latency and availability.'],
                 ['CLIENT', 'API', 'APPLICATION', 'POSTGRESQL', 'PROVIDER']),
                ('bottleneck', 'LOAD TEST', '03 — Find the limit',
                 'At sustained volume, the request path becomes the queue. Slow providers hold connections, retries amplify load, and the database becomes hot.',
                 ['API latency climbs with provider latency.', 'Connection pools exhaust during retry storms.',
                  'Synchronous processing cannot absorb bursts safely.'],
                 ['CLIENT', 'LOAD BALANCER', 'API', 'APPLICATION', 'POSTGRESQL', 'PROVIDER']),
                ('evolved', 'DURABLE PIPELINE', '04 — Decouple the critical path',
                 'Keep accepting requests quickly, then let independent channel workers deliver from a durable stream.',
                 ['Kafka buffers bursts and enables independent scaling.', 'Idempotency keys make at-least-once delivery safe.',
                  'Retry queues and a DLQ prevent poisoned events from blocking healthy work.'],
                 ['CLIENT', 'LOAD BALANCER', 'API', 'KAFKA', 'EMAIL WORKER', 'SMS WORKER', 'PUSH WORKER',
                  'REDIS', 'POSTGRESQL', 'DLQ', 'PROVIDERS']),
            ],
            'payments': [
                ('requirements', 'MONEY MOVEMENT', '01 — Protect correctness first',
                 'A payment system is defined by durable state, idempotency, and a full audit trail — not request throughput alone.',
                 ['Never charge twice for the same client intent.', 'Record every state transition durably.',
                  'External gateway success can arrive late or be ambiguous.'],
                 ['CLIENT', 'PAYMENTS API', 'POSTGRESQL', 'GATEWAY']),
                ('initial', 'SIMPLE LEDGER', '02 — Start with a transactional core',
                 'One payment service and PostgreSQL give a clear source of truth before integrations become complex.',
                 ['A transaction records payment intent and ledger state.', 'The gateway call is isolated behind one service.',
                  'A timeout must not be interpreted as a failed charge.'],
                 ['CLIENT', 'PAYMENTS API', 'PAYMENT SERVICE', 'POSTGRESQL', 'GATEWAY']),
                ('bottleneck', 'RECONCILIATION', '03 — Make uncertainty explicit',
                 'Gateway retries, webhooks, and slow responses create ambiguous outcomes. Correctness needs a state machine, not blind retries.',
                 ['Idempotency keys bind client intent to one payment.', 'Webhook events are verified and reconciled.',
                  'The ledger remains the audit source of truth.'],
                 ['CLIENT', 'LOAD BALANCER', 'PAYMENTS API', 'POSTGRESQL', 'GATEWAY', 'WEBHOOKS']),
                ('evolved', 'RELIABLE LEDGER', '04 — Separate the ledger from side effects',
                 'Persist the intent, emit an outbox event, and let workers handle receipts, reconciliation, and retries safely.',
                 ['PostgreSQL transaction + outbox prevents lost events.', 'Workers process gateway callbacks idempotently.',
                  'Monitoring watches reconciliation lag and payment state drift.'],
                 ['CLIENT', 'LOAD BALANCER', 'PAYMENTS API', 'POSTGRESQL', 'OUTBOX', 'KAFKA', 'RECONCILER',
                  'GATEWAY', 'AUDIT LOG']),
            ],
            'media': [
                ('requirements', 'UPLOAD PIPELINE', '01 — Keep uploads off the request server',
                 'Large files and slow encoding should never occupy web workers or block a user request.',
                 ['Uploads can be gigabytes and resumable.', 'Processing is CPU intensive and asynchronous.',
                  'Published media needs low-latency global delivery.'],
                 ['CLIENT', 'UPLOAD API', 'OBJECT STORAGE', 'CDN']),
                ('initial', 'DIRECT UPLOAD', '02 — Start with direct-to-storage uploads',
                 'The API issues signed upload URLs. The browser transfers directly to object storage.',
                 ['Application servers avoid large file transfer.', 'Storage is durable and cost-effective.',
                  'A simple worker can generate one derivative.'],
                 ['CLIENT', 'UPLOAD API', 'OBJECT STORAGE', 'WORKER', 'CDN']),
                ('bottleneck', 'PROCESSING QUEUE', '03 — Isolate expensive work',
                 'Concurrent uploads and video encoding can overwhelm a single worker. Queue jobs and control concurrency.',
                 ['Queue depth expresses demand safely.', 'Workers scale independently from the API.',
                  'Failures must preserve the original upload for replay.'],
                 ['CLIENT', 'LOAD BALANCER', 'UPLOAD API', 'OBJECT STORAGE', 'QUEUE', 'TRANSCODER', 'CDN']),
                ('evolved', 'GLOBAL MEDIA PLATFORM', '04 — Scale delivery and processing independently',
                 'Object storage is the source; events trigger specialized workers; a CDN serves finished assets close to users.',
                 ['Separate image, video, and metadata workers.', 'Use lifecycle policies for originals and derivatives.',
                  'Observe processing latency, failed jobs, and CDN cache hit rate.'],
                 ['CLIENT', 'LOAD BALANCER', 'UPLOAD API', 'OBJECT STORAGE', 'KAFKA', 'IMAGE WORKER',
                  'TRANSCODER', 'POSTGRESQL', 'CDN', 'DLQ']),
            ],
        }

        for scenario_key, stage_rows in stages_by_scenario.items():
            scenario = Scenario.objects.get(key=scenario_key)
            for order, (key, mode, title, text, points, nodes) in enumerate(stage_rows):
                stage, _ = Stage.objects.update_or_create(
                    scenario=scenario, key=key,
                    defaults={'mode': mode, 'title': title, 'text': text, 'order': order},
                )
                stage.points.all().delete()
                for i, point_text in enumerate(points):
                    StagePoint.objects.create(stage=stage, text=point_text, order=i)
                stage.nodes.all().delete()
                for i, node_name in enumerate(nodes):
                    StageNode.objects.create(stage=stage, name=node_name, order=i)

        component_data = [
            ('KAFKA', 'Kafka', 'Decouples API acceptance from external delivery.', 'Adds durable buffering and horizontal consumer scale.', 'Requires partitions, consumer operations, and idempotency.', 'RabbitMQ or a task queue for a simpler operating model.'),
            ('REDIS', 'Redis', 'Protects Postgres from repeat reads and coordinates rate limits.', 'Low-latency cache and ephemeral counters.', 'Cache invalidation and a failure fallback are required.', 'In-process cache for smaller, single-instance workloads.'),
            ('POSTGRESQL', 'PostgreSQL', 'Stores durable notification intent and delivery state.', 'Transactions and flexible relational queries fit auditability.', 'Write-heavy scaling requires careful indexes and partitioning.', 'NoSQL when access patterns and global scale clearly justify it.'),
            ('DLQ', 'Dead-letter queue', 'Contains messages that repeatedly fail.', 'Prevents a poison event from blocking progress.', 'Needs monitoring and an explicit replay process.', 'Dropping messages — fast, but usually unacceptable.'),
            ('CLIENT', 'Client', 'Initiates a user action or event.', 'Sends an idempotency key so retries do not create duplicate work.', 'Clients can retry unexpectedly and have unreliable networks.', 'Server-generated request identifiers alone.'),
            ('API', 'API service', 'Accepts notification requests quickly.', 'Validates input and records durable intent before asynchronous delivery.', 'Must remain stateless and protected from traffic bursts.', 'Direct provider calls from the client.'),
            ('LOAD BALANCER', 'Load balancer', 'One server cannot safely absorb all traffic.', 'Distributes requests across healthy, stateless API instances.', 'Adds health-check and routing configuration.', 'A single vertically scaled API server at low volume.'),
            ('APPLICATION', 'Application server', 'Contains the first version of business logic.', 'Keeps deployment simple while the problem is small.', 'Couples request time to database and provider work.', 'Separate services only after a measured boundary appears.'),
            ('DATABASE', 'Database', 'The early design needs durable state.', 'Stores accepted requests and delivery state.', 'Synchronous reads and writes become a scaling limit under bursts.', 'An in-memory store, which is not durable enough here.'),
            ('PROVIDER', 'Notification provider', 'Actually sends email, SMS, or push messages.', 'Provides channel delivery capability outside the core system.', 'Latency, rate limits, and failures are outside your control.', 'Operating a channel delivery network directly.'),
            ('PROVIDERS', 'Notification providers', 'Different channels need independent failure boundaries.', 'Workers route work to email, SMS, or push providers.', 'Each provider needs throttling, retries, and delivery observability.', 'One provider for every channel.'),
            ('PAYMENTS API', 'Payments API', 'Clients need a stable, authenticated payment boundary.', 'Validates the request and persists one payment intent per idempotency key.', 'It must never infer success from a gateway timeout.', 'Letting clients call gateways directly.'),
            ('PAYMENT SERVICE', 'Payment service', 'Gateway-specific logic should not leak through the API.', 'Owns the payment state machine and gateway adapter.', 'Adds another logical boundary to operate and test.', 'Placing gateway code directly in controllers.'),
            ('GATEWAY', 'Payment gateway', 'Processes an external financial transaction.', 'Authorizes or captures funds and returns provider references.', 'Responses can be delayed, duplicated, or ambiguous.', 'Building card processing infrastructure.'),
            ('WEBHOOKS', 'Gateway webhooks', 'Some payment outcomes arrive asynchronously.', 'Reconciles the ledger with signed provider events.', 'Events can be delivered more than once or out of order.', 'Polling only, which increases latency and cost.'),
            ('OUTBOX', 'Transactional outbox', 'A database write and emitted event must not diverge.', 'Records an event in the same transaction as the payment state.', 'Requires a publisher and cleanup policy.', 'Publishing directly after commit, which can lose events on a crash.'),
            ('RECONCILER', 'Reconciliation worker', 'Provider and internal state can temporarily disagree.', 'Matches gateway records, webhooks, and the ledger.', 'Needs clear remediation paths for exceptions.', 'Assuming every gateway response is final.'),
            ('AUDIT LOG', 'Audit log', 'Financial changes need a traceable history.', 'Preserves who changed what and when for investigation.', 'Retention and access control add operational obligations.', 'Overwriting mutable records without history.'),
            ('UPLOAD API', 'Upload API', 'Users need authorization without streaming files through app servers.', 'Issues signed upload URLs and records media intent.', 'Signed URL expiry and upload validation need careful design.', 'Proxying every large upload through the web application.'),
            ('OBJECT STORAGE', 'Object storage', 'Original media must be durable and inexpensive to store.', 'Stores uploads and processed derivatives independently of compute.', 'Lifecycle, permissions, and event consistency must be managed.', 'Database blobs for large media.'),
            ('QUEUE', 'Processing queue', 'Encoding work must not block an upload request.', 'Buffers jobs and controls worker concurrency.', 'Requires retry policy and backlog monitoring.', 'Running transformations inline in the API.'),
            ('TRANSCODER', 'Transcoder', 'Video and image conversion are CPU-intensive.', 'Creates delivery-ready formats asynchronously.', 'Workers are expensive and need resource limits.', 'Serving original files only.'),
            ('CDN', 'Content delivery network', 'Global users should not fetch every asset from origin storage.', 'Caches finished assets near users and reduces origin load.', 'Invalidation and cache-key design require discipline.', 'Serving all media directly from the application.'),
            ('IMAGE WORKER', 'Image worker', 'Image transformations differ from video workloads.', 'Scales image resizing and metadata extraction independently.', 'More worker types increase deployment surface area.', 'One generic worker when workloads remain small.'),
        ]
        for name, display_name, problem, decision, tradeoff, alternatives in component_data:
            Component.objects.update_or_create(
                name=name,
                defaults={'display_name': display_name, 'problem': problem, 'decision': decision,
                          'tradeoff': tradeoff, 'alternatives': alternatives},
            )

        decision_data = [
            ('Why Kafka?', 'The API should not wait for external notification providers.', 'Decouple acceptance from delivery with a durable event stream.', 'Benefits: burst absorption, horizontal consumers, replayability. Trade-offs: operations, ordering, duplicate processing.', 'Alternatives: RabbitMQ, Celery, direct synchronous processing.'),
            ('PostgreSQL vs NoSQL', 'Delivery intent needs transactional, queryable state.', 'Use PostgreSQL as the source of truth.', 'Transactions and relationships fit audit trails; scaling is vertical plus targeted horizontal strategies.', 'NoSQL is a valid choice for different access patterns or global distribution requirements.'),
            ('Retries + idempotency', 'Providers fail and at-least-once queues can redeliver.', 'Retry with backoff; dedupe by idempotency key.', 'Reliable delivery without duplicate user notifications. Trade-off: state and retry policy complexity.', 'Alternatives: best-effort delivery or provider-only retries.'),
        ]
        for order, (title, problem, decision, detail, alternatives) in enumerate(decision_data):
            Decision.objects.update_or_create(
                title=title,
                defaults={'problem': problem, 'decision': decision, 'detail': detail,
                          'alternatives': alternatives, 'order': order},
            )

        failure_data = [
            ('Kafka goes down', 'Event stream unavailable', 'New events are durably held at the API boundary or rejected with a retryable response; workers drain the backlog after recovery.', 'Use multi-broker replication, health checks, and a bounded fallback queue.'),
            ('Redis goes down', 'Increased database traffic', 'Requests bypass cache and fall back to PostgreSQL. The core system remains operational with higher latency.', 'Circuit-break the cache client and protect Postgres with rate limits.'),
            ('Database becomes slow', 'Delivery state reads and writes slow down', 'Consumers reduce concurrency; queue lag rises instead of exhausting the database.', 'Alert on latency, use indexes/replicas where appropriate, and preserve headroom.'),
            ('Notification provider fails', 'One channel is delayed', 'Workers back off, retry on a separate schedule, and route exhausted events to the DLQ.', 'Provider-level circuit breakers and secondary providers limit blast radius.'),
            ('Consumer crashes', 'One partition pauses', 'Another consumer claims work after rebalance; idempotency protects redelivery.', 'Autoscaling, liveness checks, and graceful shutdown limit interruption.'),
            ('Traffic suddenly increases 10×', 'Backlog grows', 'Kafka absorbs the burst while autoscaling workers increases delivery throughput.', 'Rate limiting and provider throttling prevent downstream collapse.'),
        ]
        for order, (name, impact, response, recovery) in enumerate(failure_data):
            FailureMode.objects.update_or_create(
                name=name,
                defaults={'impact': impact, 'response': response, 'recovery': recovery, 'order': order},
            )

        adr_data = [
            ('ADR-001', 'Use asynchronous processing for notification delivery.', 'Decision: Kafka-based event processing. Reason: decouple API requests from external providers. Rejected: synchronous delivery. Trade-off: increased infrastructure complexity.'),
            ('ADR-002', 'Treat delivery as at-least-once.', 'Decision: idempotency keys and durable delivery state. Reason: provider and worker failures make exactly-once delivery impractical end-to-end.'),
            ('ADR-003', 'Use Redis selectively.', 'Decision: cache templates, preferences, and counters — not the durable delivery record. Reason: failure must degrade safely.'),
        ]
        for order, (identifier, title, detail) in enumerate(adr_data):
            ArchitectureDecisionRecord.objects.update_or_create(
                identifier=identifier,
                defaults={'title': title, 'detail': detail, 'order': order},
            )

        metric_data = [
            (0, '10K events/day', '10,000', '0.1 events/sec', '82 ms', '0.01%', '—', '12%'),
            (1, '100K events/day', '100,000', '1.2 events/sec', '110 ms', '0.03%', '—', '24%'),
            (2, '1M events/day', '1,000,000', '11.6 events/sec', '148 ms', '0.05%', '43', '41%'),
            (3, '10M events/day', '10,000,000', '116 events/sec', '182 ms', '0.08%', '213', '64%'),
        ]
        for level, traffic_label, events, throughput, latency, error_rate, queue_lag, db_load in metric_data:
            TrafficMetric.objects.update_or_create(
                level=level,
                defaults={'traffic_label': traffic_label, 'events': events, 'throughput': throughput,
                          'latency': latency, 'error_rate': error_rate, 'queue_lag': queue_lag, 'db_load': db_load},
            )

        plan_data = {
            'notification': [
                (0, 'Simple notification service', 'API → PostgreSQL → Worker → Provider'),
                (1, 'Queued delivery service', 'API → Queue → Workers → Provider + PostgreSQL'),
                (2, 'Durable event pipeline', 'Load Balancer → API → Kafka → Workers → Providers + Redis + PostgreSQL'),
                (3, 'Highly available delivery platform', 'Multi-AZ API → Kafka → autoscaled workers → multi-provider routing + DLQ'),
            ],
            'payments': [
                (0, 'Transactional payment core', 'Payments API → PostgreSQL → Gateway'),
                (1, 'Idempotent payment service', 'Payments API → Payment Service → PostgreSQL → Gateway'),
                (2, 'Outbox-backed payment workflow', 'Payments API → PostgreSQL + Outbox → Kafka → Reconciler → Gateway'),
                (3, 'Highly reliable payments platform', 'Multi-AZ API → Ledger + Outbox → reconciliation workers → gateway failover'),
            ],
            'media': [
                (0, 'Direct upload service', 'Upload API → Object Storage → CDN'),
                (1, 'Async media worker', 'Upload API → Object Storage → Queue → Worker → CDN'),
                (2, 'Scalable processing pipeline', 'Load Balancer → Upload API → Storage → Kafka → workers → CDN'),
                (3, 'Global media platform', 'Multi-region upload → storage → specialist workers → CDN + DLQ'),
            ],
        }
        for scenario_key, tiers in plan_data.items():
            scenario = Scenario.objects.get(key=scenario_key)
            for tier, name, diagram in tiers:
                SimulatorPlan.objects.update_or_create(
                    scenario=scenario, tier=tier,
                    defaults={'name': name, 'diagram': diagram},
                )

        bottleneck_data = [
            (0, 'Single service capacity'),
            (1, 'Queue backlog and downstream limits'),
            (2, 'Worker concurrency and third-party quotas'),
            (3, 'Cross-region operations and cost'),
        ]
        for tier, text in bottleneck_data:
            SimulatorBottleneck.objects.update_or_create(tier=tier, defaults={'text': text})

        self.stdout.write('  ✓ Lab details (stages, components, decisions, failures, ADRs, metrics, simulator) created/updated')

    def _seed_projects(self):
        from apps.portfolio.models import Project
        # Keyed by slug so this both fills in missing projects and fixes up
        # placeholder content on ones already created (e.g. via admin).
        project_data = [
            {
                'slug': 'patient-registry',
                'title': 'Patient Registry System',
                'description': '21 CFR Part 11-compliant patient registry for capturing and auditing patient records across a healthcare organization.',
                'problem': 'Manual, spreadsheet-driven patient tracking led to data silos and compliance risk.',
                'outcome': 'Replaced manual tracking with a centralized, audit-ready system.',
                'tech_stack': ['Django', 'DRF', 'PostgreSQL', 'sci-spaCy', 'Celery'],
                'is_featured': True, 'order': 0,
            },
            {
                'slug': 'etl-tool',
                'title': 'ETL Tool',
                'description': 'Configurable ETL pipeline for ingesting, transforming, and loading large third-party datasets on a schedule.',
                'problem': 'Manual data imports were slow and error-prone for large datasets.',
                'outcome': 'Replaced slow manual imports with scheduled, automated processing.',
                'tech_stack': ['Python', 'Pandas', 'Celery', 'PostgreSQL'],
                'is_featured': True, 'order': 1,
            },
            {
                'slug': 'real-time-analytics-dashboard',
                'title': 'Real-Time Analytics Dashboard',
                'description': 'Kafka-backed streaming pipeline feeding live Chart.js/Go.js dashboards for operational visibility.',
                'outcome': 'Enabled real-time operational visibility without manual polling.',
                'tech_stack': ['Django', 'Kafka', 'Chart.js', 'Go.js', 'PostgreSQL'],
                'is_featured': True, 'order': 2,
            },
        ]
        for p in project_data:
            slug = p.pop('slug')
            Project.objects.update_or_create(slug=slug, defaults=p)
        self.stdout.write('  ✓ Projects created/updated')
