from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import User_profile, Question, Answer, Tag, QuestionTag, QuestionLike, AnswerLike
from faker import Faker
import random
from django.db import transaction
import time


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Multiplication ratio for entities')

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']
        start_time = time.time()
        
        self.stdout.write(f'Starting database fill with ratio={ratio}...')
        
        t = time.time()
        self.stdout.write('Creating users and profiles...')
        profiles = self.create_users(ratio)
        self.stdout.write(self.style.SUCCESS(f'Created {len(profiles)} users and profiles ({time.time()-t:.1f}s)'))
        
        t = time.time()
        self.stdout.write('Creating tags...')
        tags = self.create_tags(ratio)
        self.stdout.write(self.style.SUCCESS(f'Created {len(tags)} tags ({time.time()-t:.1f}s)'))
        
        t = time.time()
        self.stdout.write('Creating questions...')
        questions = self.create_questions(ratio * 10, profiles)
        self.stdout.write(self.style.SUCCESS(f'Created {len(questions)} questions ({time.time()-t:.1f}s)'))
        
        t = time.time()
        self.stdout.write('Linking questions and tags...')
        self.create_question_tags(questions, tags)
        self.stdout.write(self.style.SUCCESS(f'Linked questions and tags ({time.time()-t:.1f}s)'))
        
        t = time.time()
        self.stdout.write('Creating answers...')
        answers = self.create_answers(ratio * 100, profiles, questions)
        self.stdout.write(self.style.SUCCESS(f'Created {len(answers)} answers ({time.time()-t:.1f}s)'))
        
        t = time.time()
        self.stdout.write('Creating likes...')
        self.create_likes(ratio * 200, profiles, questions, answers)
        self.stdout.write(self.style.SUCCESS(f'Created likes ({time.time()-t:.1f}s)'))
        
        total_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'\nDatabase successfully filled in {total_time:.1f}s ({total_time/60:.1f} min)!'))
        self.stdout.write(f'Total statistics:')
        self.stdout.write(f'  Users: {ratio}')
        self.stdout.write(f'  Questions: {ratio * 10}')
        self.stdout.write(f'  Answers: {ratio * 100}')
        self.stdout.write(f'  Tags: {ratio}')
        self.stdout.write(f'  Likes: {ratio * 200}')

    def create_users(self, count):
        fake = Faker()
        
        users_to_create = []
        for i in range(count):
            user = User(
                username=f"user_{i}",
                email=f"user_{i}@example.com",
                first_name=f"First{i}",
                last_name=f"Last{i}"
            )
            user.set_password('password123')
            users_to_create.append(user)
        
        User.objects.bulk_create(users_to_create, batch_size=5000)
        
        created_users = list(User.objects.all().order_by('-id')[:count])
        
        profiles_to_create = []
        for i, user in enumerate(created_users):
            about = fake.text(max_nb_chars=200) if i % 2 == 0 else ''
            profile = User_profile(
                user_id=user,
                nickname=f"nick_{i}",
                image='',
                about=about
            )
            profiles_to_create.append(profile)
        
        User_profile.objects.bulk_create(profiles_to_create, batch_size=5000)
        
        return list(User_profile.objects.all().order_by('-id')[:count])

    def create_tags(self, count):
        tags_to_create = []
        for i in range(count):
            tag = Tag(name=f"tag_{i}")
            tags_to_create.append(tag)
        
        Tag.objects.bulk_create(tags_to_create, batch_size=5000)
        
        return list(Tag.objects.all().order_by('-id')[:count])

    def create_questions(self, count, profiles):
        fake = Faker()
        profile_ids = [p.id for p in profiles]
        
        questions_to_create = []
        for i in range(count):
            title = f"Question {i}: {fake.sentence()[:50]}"[:256]
            text = fake.text(max_nb_chars=500)
            
            question = Question(
                title=title,
                text=text,
                rating=0,
                profile_id_id=random.choice(profile_ids)
            )
            questions_to_create.append(question)
        
        Question.objects.bulk_create(questions_to_create, batch_size=5000)
        
        return list(Question.objects.all().order_by('-id')[:count])

    def create_question_tags(self, questions, tags):
        question_ids = [q.id for q in questions]
        tag_ids = [t.id for t in tags]
        
        question_tags_to_create = []
        
        for q_id in question_ids:
            num_tags = random.randint(1, min(5, len(tag_ids)))
            selected_tag_ids = random.sample(tag_ids, num_tags)
            
            for t_id in selected_tag_ids:
                qt = QuestionTag(
                    question_id_id=q_id,
                    tag_id_id=t_id
                )
                question_tags_to_create.append(qt)
        
        QuestionTag.objects.bulk_create(question_tags_to_create, batch_size=5000)

    def create_answers(self, count, profiles, questions):
        fake = Faker()
        profile_ids = [p.id for p in profiles]
        question_ids = [q.id for q in questions]
        
        answers_to_create = []
        for i in range(count):
            text = fake.text(max_nb_chars=300)
            is_correct = i % 10 == 0  # Каждый 10-й ответ правильный
            
            answer = Answer(
                text=text,
                is_correct=is_correct,
                rating=0,
                profile_id_id=random.choice(profile_ids),
                question_id_id=random.choice(question_ids)
            )
            answers_to_create.append(answer)
        
        Answer.objects.bulk_create(answers_to_create, batch_size=5000)
        
        return list(Answer.objects.all().order_by('-id')[:count])

    def create_likes(self, count, profiles, questions, answers):
        question_likes_count = count // 2
        answer_likes_count = count - question_likes_count
        
        profile_ids = [p.id for p in profiles]
        question_ids = [q.id for q in questions]
        answer_ids = [a.id for a in answers]
        
        self.stdout.write(f'  Creating {question_likes_count} question likes...')
        batch_size = 10000
        for batch_start in range(0, question_likes_count, batch_size):
            batch_end = min(batch_start + batch_size, question_likes_count)
            batch_count = batch_end - batch_start
            
            question_likes_batch = []
            for _ in range(batch_count):
                value = 1 if random.random() < 0.7 else -1
                ql = QuestionLike(
                    profile_id_id=random.choice(profile_ids),
                    question_id_id=random.choice(question_ids),
                    value=value
                )
                question_likes_batch.append(ql)
            
            QuestionLike.objects.bulk_create(question_likes_batch, ignore_conflicts=True)
        
        self.stdout.write(f'  Creating {answer_likes_count} answer likes...')
        for batch_start in range(0, answer_likes_count, batch_size):
            batch_end = min(batch_start + batch_size, answer_likes_count)
            batch_count = batch_end - batch_start
            
            answer_likes_batch = []
            for _ in range(batch_count):
                value = 1 if random.random() < 0.7 else -1
                al = AnswerLike(
                    profile_id_id=random.choice(profile_ids),
                    answer_id_id=random.choice(answer_ids),
                    value=value
                )
                answer_likes_batch.append(al)
            
            AnswerLike.objects.bulk_create(answer_likes_batch, ignore_conflicts=True)

